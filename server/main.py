from fastapi import FastAPI, File, UploadFile, HTTPException
import os
import shutil
from server.utils import *
from controller import FileController
app = FastAPI()


def find_file_type(file : UploadFile):
    if file.content_type == 'text/csv':
        return FileType.CSV
    if file.content_type == 'application/json':
        return FileType.JSON
    if file.content_type == 'text/plain':
        return FileType.TEXT
    raise NotImplementedError



@app.post("/uploadfile/")
async def upload_file(file: UploadFile = File(...)):

    file_type = find_file_type(file)
    file_controller = FileController(file_type)

    file_location = os.path.join(UPLOAD_DIRECTORY, file.filename)
    try:
        await file_controller.save_file(file, file_location)
    except MemoryError as e: 
        raise HTTPException(status_code=413, detail=str(e))
    

