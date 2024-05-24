from enum import Enum

UPLOAD_DIRECTORY = "./uploaded_files/"

# in MB
max_file_size = 1_000

# min is 150B for test.txt file
max_batch_size = 150

# for real use, uncomment converse into MB
MAX_FILE_SIZE = max_file_size * 1024 * 1024
MAX_BATCH_SIZE = max_batch_size #* 1024 * 1024

# analyzable data formats
class FileType (Enum):
    TEXT = 'txt'
    CSV = 'csv'
    JSON = 'json'




