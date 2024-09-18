from fastapi import APIRouter, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
import os
import subprocess
from app.services.s3_service import upload_to_s3
from app.utils.file_processing import save_upload_file
from app.core.config import settings

router = APIRouter()

@router.post("/process-music/")
async def process_music(file: UploadFile = File(...)):
    try:
        # Save uploaded file
        wav_file_path = await save_upload_file(file)

        # Prepare output path
        filename = os.path.splitext(os.path.basename(wav_file_path))[0]
        output_mp4_path = os.path.join(os.path.dirname(__file__), f'renders/test_{filename}.mp4')

        # Run the EDGE script
        subprocess.run(
            [
                "python", "test.py",
                "--music_dir", os.path.dirname(wav_file_path),
                "--save_motions",
                "--motion_save_dir", os.path.dirname(wav_file_path)
            ],
            check=True
        )

        # Upload to S3
        mp4_url = upload_to_s3(output_mp4_path, settings.AWS_BUCKET_NAME)

        # Clean up temporary files
        os.remove(wav_file_path)
        os.remove(output_mp4_path)

        return {"message": "Files processed and uploaded successfully", "files": {"mp4": mp4_url}}

    except subprocess.CalledProcessError as e:
        raise HTTPException(status_code=500, detail=f"EDGE script execution failed: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")
