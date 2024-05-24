from utils import *
from fastapi import UploadFile
import os
import sys
from abc import ABC, abstractmethod
from typing import Generator, List
import pandas as pd
from data import Summary
from pandas import DataFrame
import re

if not os.path.exists(UPLOAD_DIRECTORY):
    os.makedirs(UPLOAD_DIRECTORY)

def choose_controller(file_type : FileType):
    if file_type == FileType.TEXT:
        return TXTController()
    

class ParsingError(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)

class FileController (ABC):

    def __init__(self):
        pass

    @staticmethod
    async def save_file(file: UploadFile, file_location: str):
        '''
        function to save file from upcomming HTTP POST call
        '''
        file_size = 0
        with open(file_location, "wb") as buffer:
            for chunk in iter(lambda: file.file.read(MAX_BATCH_SIZE), b""):
                file_size += len(chunk)
                if file_size > MAX_FILE_SIZE:
                    buffer.close()
                    os.remove(file_location)
                    raise MemoryError("File too large")
                buffer.write(chunk)
        return file_size
    
    @abstractmethod
    def _cut_file(self, filename: str) -> Generator:
        pass

    @abstractmethod
    def _parse(self, file_content) -> pd.DataFrame:
        pass

    def process_file(self, file_location: str, data_summary: Summary):
        '''
        function taking file location and cutting it on smaller batches to analyze
        '''

        batch_generator = self._cut_file(file_location)
        first_batch = next(batch_generator)
        data = self._parse(first_batch)
        self._process_first_batch(data, data_summary)

        for batch in batch_generator:
            data = self._parse(batch)
            self._process_batch(data, data_summary)

    @abstractmethod
    def _process_first_batch(self, data: DataFrame, data_summary: Summary):
        pass

    @abstractmethod
    def _process_batch(self, data: DataFrame, data_summary: Summary):
        pass
    

class TXTController(FileController):

    def __init__(self):
        super().__init__()
        self.separator: str = None 

    def _find_separator_txt(self, filename: str):
        '''
        specifies the separator used in txt file inbetween values
        '''

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


    def _cut_file(self, filename: str):
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
            if current_size > 0:
                yield current_lines

    def _parse(self, file_content: List[str]) -> pd.DataFrame:
        try:
            data = [line.split() for line in file_content]
            for row in data:
                for i in range(len(row)):
                    if row[i].isdigit():
                        row[i] = int(row[i])
                    elif re.fullmatch(r'^-?\d+\.\d+$', row[i]) or re.fullmatch(r'-?\d+(\.\d+)?[eE]-?\d+', row[i]): 
                        row[i] = float(row[i])
        except Exception as e:
            raise ParsingError(f'Parsing file went wrong - {str(e)}')
        data = pd.DataFrame(data)
        return data
    
    def _process_first_batch(self, data: DataFrame, data_summary: Summary):
        if data.shape[0] > 1 and data_summary.has_column_names(data):
            names = data.iloc[0]
            data = data.drop(index=0)
            data = data.reset_index(drop=True)
        else:
            names = [f"col{i}" for i in range(len(data.columns))]
        for column, name in zip(data, names):
            data_summary.add_new_column(data[column], name)

    def _process_batch(self, data: DataFrame, data_summary: Summary):
        for idx, column in enumerate(data):
            data_summary.update_column(idx, data[column])
    


    
