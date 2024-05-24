from utils import FileType

import numpy as np
from typing import Dict, List, Any, Protocol
from enum import Enum
import pandas as pd
from pandas import DataFrame, Series
from pandas.api.types import is_numeric_dtype
from abc import ABC, abstractmethod


class DataType(Enum):
    NUMERIC = 'numeric'
    STRING = 'string'

class _Column():
    unique_max_number = 100

    def __init__(self, name: str, data: Series) -> None:
        self.name = name
        self.special = False
        self.unique_values = set()
        self.words_used = 0
        self.chars_used = 0
        self.not_na_number = 0
        self.update(data, first=True)

    def _count_words(self, value):
        if pd.isna(value):
            return
        value = str(value)
        self.words_used += len(value.split(' '))
        self.chars_used += len(value)

    def update(self, data: Series, first: bool=False) -> None:
        self.not_na_number += int(data.notna().sum())

        data.apply(self._count_words)
            
        if len(self.unique_values) == self.unique_max_number:
            return    
        for value in data:
            if value not in self.unique_values:
                self.unique_values.add(value)
                if len(self.unique_values) == self.unique_max_number:
                    break
        
    def to_dict(self) -> dict:
        return {
        "type" : DataType.STRING,
        "special" : self.special,
        "unique_values" : list(self.unique_values),
        "not_na_number" : self.not_na_number
        }

special_numeric_names = {'PESEL', 'ID', 'PHONE'}

class _NumericColumn(_Column):
    def __init__(self, name: str, data: Series) -> None:
        self.broken = False
        self.mean = 0
        self.var = 0
        super().__init__(name, data)
        
        
    def update(self, data: Series, first: bool=False) -> None:
        

        if first:
            self.special = self._check_for_special(data, first=True)
            self.var = data.var()
            self.mean = data.mean()
            print(float(data.mean()))

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

                    print(self.mean)

        super().update(data, first)
        
    
    def to_dict(self) -> dict:
        result = super().to_dict()
        result["type"] = DataType.NUMERIC
        result["var"] = float(self.var) 
        result["broken"] = self.broken
        result["mean"] = float(self.mean)
        return result

    def _check_for_special(self, data, first=False) -> bool:
        if self.name.upper() in special_numeric_names:
            return True
        return 


def _is_numeric_with_name(series):
    series_copy = series.copy()

    marker = '_NaN_'
    series_copy = series_copy.replace(np.nan, marker)
    
    series_copy.pop(0)
    converted_series = pd.to_numeric(series_copy, errors='coerce')
    
    return not converted_series.isna().any()



class Summary():
    def __init__(self, file_type: FileType):
        self.file_type = file_type
        self.columns: List[_Column] = []
        
    @staticmethod
    def _create_column(data_type: DataType, name: str, data: Series) -> _Column:
        if data_type == DataType.NUMERIC:
            return _NumericColumn(name, data)
        return _Column(name, data)
    
    @staticmethod
    def has_column_names(data: DataFrame):
        # przejście iteracyjnie po kolumnach
        column_names = False
        numeric_columns = False
        
        for column in data.columns:
            if is_numeric_dtype(data[column]):
                numeric_columns = True
                continue
            if _is_numeric_with_name(data[column]):
                column_names = True
                break

        return column_names or not numeric_columns
    
    

    def add_new_column(self, data: Series, name: str=None):
        if is_numeric_dtype(data):
            data_type = DataType.NUMERIC
        else:
            data_type = DataType.STRING

        self.columns.append(self._create_column(data_type, name, data))


    def update_column(self, column_idx: int, data : Series):
        self.columns[column_idx].update(data)    


    def to_dict(self) -> dict:
        result = {
            "file_type" : self.file_type
        }
        for column in self.columns:
            result[column.name] = column.to_dict()

        result["words_used"] = sum([column.words_used for column in self.columns])
        result["chars_used"] = sum([column.chars_used for column in self.columns])    
            
        return result

