from enum import Enum

UPLOAD_DIRECTORY = "./uploaded_files/"

# in MB
max_file_size = 1_000
# założenie - minimalnie jeden rząd musi się zmieścić w batchu
max_batch_size = 400

# do realnego użytku należy odkomentować zamianę z B na MB
MAX_FILE_SIZE = max_file_size * 1024 * 1024
MAX_BATCH_SIZE = max_batch_size * 1024 * 1024


class FileType (Enum):
    TEXT = 'txt'
    CSV = 'csv'
    JSON = 'json'




