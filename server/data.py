from utils import FileType

class Data ():
    def __init__(self, file_type: FileType):
        self.file_type = file_type
        self.special_columns = set()
        self.text_columns = set()
        self.numerical_columns = set()