# Restful API for Contract Management System

## Requirements
python3.6+

## Run Server
```sh
pip3 install -r requirements.txt
python3 manage.py migrate
python3 manage.py runserver
```
default addr and port: http://localhost:8000

## API usage
- /clients/  
- /clients/\<id\>/
- /contracts/  
- /contracts/\<id\>/

**See full document and examples at /doc/**

## Todo
- add data validation to models
- add user register/login and permission control
- more functions