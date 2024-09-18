from fastapi import UploadFile
import os
from tempfile import NamedTemporaryFile

async def save_upload_file(upload_file: UploadFile) -> str:
    try:
        suffix = os.path.splitext(upload_file.filename)[1]
        with NamedTemporaryFile(delete=False, suffix=suffix) as temp_file:
            temp_file.write(await upload_file.read())
            return temp_file.name
    except Exception as e:
        os.unlink(temp_file.name)
        raise e