from fastapi import FastAPI, File, UploadFile, HTTPException
import os
import shutil
from utils import *
from controller import FileController, choose_controller, ParsingError
from data import Summary
app = FastAPI()

_file_translation = {
    'text/csv' : FileType.CSV,
    'application/json' : FileType.JSON,
    'text/plain' : FileType.TEXT
}

def find_file_type(file : UploadFile):
    type = _file_translation.get(file.content_type, None)
    if type: return type
    raise NotImplementedError(f"Wrong file type: {file.content_type}")



@app.post("/uploadfile/")
async def upload_file(file: UploadFile = File(...)):


    try:
        file_type = find_file_type(file)
        file_controller: FileController= choose_controller(file_type)

        file_location = os.path.join(UPLOAD_DIRECTORY, file.filename)
        await file_controller.save_file(file, file_location)

        data_summary = Summary(file_type)

        file_controller.process_file(file_location, data_summary)

        result = data_summary.to_dict()
        
        return result


    except MemoryError as e: 
        raise HTTPException(status_code=413, detail=str(e))
    
    except NotImplementedError as e: 
        raise HTTPException(status_code=415, detail=str(e))

    except ParsingError as e:
        raise HTTPException(status_code=422, detail=str(e))
    

    finally:
        os.remove(file_location)



    

