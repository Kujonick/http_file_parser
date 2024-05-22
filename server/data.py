from utils import FileType

from typing import Dict, List, Any, Protocol
from enum import Enum
import pandas as pd
from pandas import DataFrame, Series
from pandas.api.types import is_numeric_dtype
from abc import ABC, abstractmethod


class DataType(Enum):
    NUMERIC = 1
    STRING = 2

class _Column():
    unique_max_number = 100

    def __init__(self, name: str, data: Series) -> None:
        self.name = name
        self.special = False
        self.unique_values = set()
        self.words_used = 0
        self.chars_used = 0
        self.not_na_number = 0

    def _count_words(self, value):
        if pd.isna(value):
            return
        value = str(value)
        self.words_used += len(value.split())
        self.chars_used += len(value)

    def update(self, data: Series, first: bool=False) -> None:
        self.not_na_number += data.notna().sum()

        data.apply(self._count_words)
            
        if len(self.unique_values) == self.unique_max_number:
            return    
        for value in data:
            if value not in self.unique_values:
                self.unique_values.add(value)
                if len(self.unique_values) == self.unique_max_number:
                    break
        
    def to_dict(self) -> dict:
        pass

special_numeric_names = {'PESEL', 'ID', 'PHONE'}

class _NumericColumn(_Column):
    def __init__(self, name: str, data: Series) -> None:
        super().__init__(name, data)
        self.update(data, first=True)
        self.broken = False
        self.mean = 0
        self.var = 0
        
    def update(self, data: Series, first: bool=False) -> None:
        

        if first:
            self.special = self._check_for_special(data, first=True)
            self.var = data.var()
            self.mean = data.mean()

        else:
            if not is_numeric_dtype(data):
                self.broken = True
            if not self.broken:
                
                self.special = self.special and self._check_for_special(data)

                # tu szybko matma eskalowała - 
                #   A zbiór przed
                #   B nowy zbiór

                # n_ - rozmiar zbioru
                n_a = self.not_na_number
                n_b = data.notna().sum()

                if n_b > 0:
                    # X_ - średnia zbioru
                    X_a = self.mean 
                    X_b = data.mean()
                    #  wariancja zbioru
                    sig_a = self.var
                    sig_b = data.var()

                    # new mean
                    self.mean = (n_a*X_a + n_b*X_b) / (n_a + n_b)

                    # kwadratowe odchylenia dla zbiorów
                    SSa = (n_a - 1)*sig_a
                    SSb = (n_b - 1)*sig_b

                    SS_w = SSa + SSb + (n_a*n_b)/ (n_a+n_b) * (X_a - X_b)**2
                    self.var = SS_w / (n_a + n_b - 1) 

        super().update(data, first)
        
    
    def to_dict(self) -> dict:
        pass

    def _check_for_special(self, data, first=False) -> bool:
        if self.name.upper() in special_numeric_names:
            return True
        return 







class Summary():
    def __init__(self, file_type: FileType):
        self.file_type = file_type
        self.columns: List[_Column] = []
    @staticmethod
    def _create_column(data_type: DataType, name: str, data: Series) -> _Column:
        if data_type == DataType.NUMERIC:
            return _NumericColumn(name, data)
        return _Column(name, data)


    def add_new_column(self, data_type: DataType, data: Series, name: str=None):
        if name is None:
            name = str(len(self.columns))
        self.columns.append(self._create_column(data_type, name, data))


    def update_column(self, column_idx: int | str, data : Series):
        self.columns[column_idx].update(data)