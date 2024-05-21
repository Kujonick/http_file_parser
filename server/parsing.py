import pandas as pd
import json
import io
from fastapi import UploadFile, HTTPException
from typing import List
from utils import FileType

class ParsingError(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)

class Parser:
    
    def __init__(self, file_type):
        self.parse: function = None
        if self.file_type == FileType.CSV:
            self._parse = self._parse_csv
        elif self.file_type == FileType.JSON:
            self._parse = self._parse_json
        elif self.file_type == FileType.TEXT:
            self._parse = self._parse_txt

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
        try:
            self._parse(file_content)
        except Exception as e:
            raise ParsingError(str(e))
        
    