# config.py

import secrets
import datetime


class Config:
    MYSQL_HOST = 'localhost'
    MYSQL_USER = 'root'
    MYSQL_PASSWORD = ''
    MYSQL_PORT = 3307
    MYSQL_DB = 'todo'
    JWT_SECRET_KEY = secrets.token_hex(32)
    JWT_EXPIRATION_DELTA = datetime.timedelta(
        hours=1)  # Token expires in 1 hour
