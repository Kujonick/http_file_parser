from server.utils import *
from fastapi import UploadFile
import os
import sys
from abc import ABC, abstractmethod
from typing import Generator

if not os.path.exists(UPLOAD_DIRECTORY):
    os.makedirs(UPLOAD_DIRECTORY)

def choose_controller(file_type : FileType):
    if file_type == FileType.TEXT:
        return TXTController
    

class FileController (ABC):

    def __init__(self):
        pass

    async def save_file(file: UploadFile, file_location: str):
        file_size = 0
        with open(file_location, "wb") as buffer:
            for chunk in iter(lambda: file.file.read(max_batch_size), b""):
                file_size += len(chunk)
                if file_size > MAX_FILE_SIZE:
                    buffer.close()
                    os.remove(file_location)
                    raise MemoryError("File too large")
                buffer.write(chunk)
        return file_size
    

    @abstractmethod
    def cut_file(self, filename: str) -> Generator:
        pass
    

class TXTController():

    def __init__(self):
        super.__init__()
        self.separator: str = None 

    def _find_separator_txt(self, filename: str):

        def change_line_to_dict(line):
            chars = {c : 0 for c in line}
            for c in line:
                chars[c] = chars[c] + 1
            return chars

        with open(filename, "r", encoding='utf-8') as f:
            line = f.readline()
            separators = [",", "\t", ";", " ", ":", "/", "\\"]
            sep = dict()
            chars = change_line_to_dict(line)
            for char in separators:
                if chars.get(char, None) != None:
                    sep[char] = chars.get(char, None) 
            
            while len(sep) > 1:
                line = f.readline()
                if line == '':
                    raise TypeError
                chars = change_line_to_dict(line)
                new_seps = dict()
                for c, v in chars:
                    if chars.get(c, 0) == v:
                        new_seps[c] = v
                sep = new_seps
            
        if len(sep) == 1:
            return sep.keys()[0]
        raise TypeError("Seperator not found in file")


    def cut_file(self, filename: str):
        with open(filename, "r", encoding='utf-8') as f:
            current_size = 0
            current_lines = []
            for line in f:
                if current_size + sys.getsizeof(line) > MAX_BATCH_SIZE:
                    yield current_lines
                    current_lines = []
                    current_size = 0

                current_lines.append(line)
                current_size += sys.getsizeof(line)