import pandas as pd
import json
import io
from fastapi import UploadFile, HTTPException
from typing import List
from utils import FileType



class Parser:

    def __init__(self, file_type):
        self.file_type : FileType= file_type

    @staticmethod
    def _parse_txt(file_content: List[str]) -> pd.DataFrame:
        data = [line.split() for line in file_content]
        return pd.DataFrame(data)

    @staticmethod
    def _parse_json(file_content) -> pd.DataFrame:
        data = json.loads(file_content)
        return pd.DataFrame(data)
    
    @staticmethod
    def _parse_csv(file_content) -> pd.DataFrame:
        data = pd.read_csv(io.StringIO(file_content.decode('utf-8')))
        return data

    def parse(self, file_content):

        if self.file_type == FileType.CSV:
            data = self._parse_csv(file_content)
        elif self.file_type == FileType.JSON:
            data = self._parse_json(file_content)
        elif self.file_type == FileType.TEXT:
            data = self._parse_txt(file_content)
        else:
            raise ImportError

    