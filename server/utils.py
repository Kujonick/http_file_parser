from enum import Enum

UPLOAD_DIRECTORY = "./uploaded_files/"

# in MB
MAX_BATCH_SIZE = 50 
MAX_FILE_SIZE = 1_000

max_file_size = MAX_FILE_SIZE * 1024 * 1024
max_batch_size = MAX_BATCH_SIZE * 1024 * 1024


class FileType (Enum):
    TEXT = 1
    CSV = 2
    JSON = 3




