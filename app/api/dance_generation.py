from fastapi import APIRouter, HTTPException, BackgroundTasks
from pydantic import BaseModel
from app.services.youtube_service import get_audio_from_youtube, search_youtube
from app.services.s3_service import upload_to_s3
from app.services.mongodb_service import save_dance_data
from app.services.fbx_service import convert_to_fbx
from app.utils.redis_queue import enqueue_task, pop_queue
from app.core.config import settings
import tempfile
import uuid
import subprocess
import os
import logging  

logger = logging.getLogger(__name__)

router = APIRouter()

class DanceRequest(BaseModel):
    song_name: str

class DanceResponse(BaseModel):
    task_id: str

@router.post("/generate_dance", response_model=DanceResponse)
async def create_dance(request: DanceRequest, background_tasks: BackgroundTasks):
    try:
        task_id = enqueue_task(generate_dance_task, request.song_name)
        return {"task_id": task_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

async def generate_dance_task(song_name: str):
    unique_id = str(uuid.uuid4())
    try:
        with tempfile.TemporaryDirectory() as temp_dir:
            wav_path = os.path.join(temp_dir, f'song_{unique_id}')
            motion_save_dir = os.path.join(temp_dir, 'motions')
            renders_dir = os.path.join(temp_dir, 'renders')
            s3_key_prefix = f'renders/{unique_id}'
        video_url = await search_youtube(song_name)
        audio_file = await get_audio_from_youtube(video_url=video_url, wav_path=wav_path)
        current_dir = os.path.dirname(os.path.abspath(__file__))
        test_script_path = os.path.join(current_dir, '..', '..', 'EDGE', 'test.py')

        subprocess.run([
                'python3', test_script_path,  # 
                '--music_dir', temp_dir,
                '--save_motions',
                '--render_dir', renders_dir,
                '--motion_save_dir', motion_save_dir
            ], check=True)
        
        #mp4 open
        mp4_files = [f for f in os.listdir(renders_dir) if f.endswith('.mp4')]
        if not mp4_files:
            logger.error("No MP4 file generated.")
            raise HTTPException(status_code=500, detail="No MP4 file generated")
        mp4_path = os.path.join(renders_dir, mp4_files[0])
        mp4_s3_key = f'{s3_key_prefix}.mp4'
        upload_to_s3(mp4_path, mp4_s3_key)
        #mp4 close
        
        #pkl open
        pkl_files = [f for f in os.listdir(motion_save_dir) if f.endswith('.pkl')]
        if not pkl_files:
            logger.error("No PKL file generated.")
            raise HTTPException(status_code=500, detail="No PKL file generated")

        pkl_path = os.path.join(motion_save_dir, pkl_files[0])
        pkl_s3_key = f'{s3_key_prefix}.pkl'
        pkl_url = upload_to_s3(pkl_path, pkl_s3_key)

        # Save to MongoDB
        save_dance_data(song_name, mp4_s3_key)
        
        logger.info(f"Request {unique_id} processed successfully.")
        fbx_file = convert_to_fbx(pkl_url=pkl_url, song_name=song_name)
        s3_url = upload_to_s3(fbx_file)
        save_dance_data(song_name, s3_url)
        pop_queue()
        return s3_url
    except Exception as e:
        logger.error(f"An error occurred while processing request {unique_id}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")