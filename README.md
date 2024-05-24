# http_file_parser #
Aplication meant to read and show information about text files send to it. 
Using FastAPI to run endpoint in python.

## Instalation ##
### With git clone ###
Clone the repository on your local machine

`git clone https://github.com/Deevo87/AWS-IAM-Role-Policy-validator`

Go to the project directory

`cd server`

use pip to install needed libraries

`pip install -r requirements.txt`

## Starting up endpoint ##

start app using

`uvicorn main:app --reload`

## sending file ##
- txt files must be separated by one of symbols: `",", "\t", ";", " ", ":", "/", "\\"`
- csv ---
- json ---

--------------------------
then if you want to send file, you might use already written client

from main directory go to client

`cd client`

set up file directory in client.py file, and specify its type (txt only now)

then run it by

`python main.py`



## How it works ##
The main purpose of the application is file analysis. It is prepared to handle larger volumes of data by reading it in chunks of a specified size (dictated by 'MAX_BATCH_SIZE'). The assumption is that at least one row of the table (ideally several for good numerical properties, with a minimum variance requiring at least 2) fits into memory.   File being read updates statistics in `Summary` class, and after reading all of it whole information is send to client

#### _maybe_ future features ####
- reading csv, json and other files
- prometheus to monitor server
- more statistics
