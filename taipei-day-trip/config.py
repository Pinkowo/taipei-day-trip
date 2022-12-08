import os
from dotenv import load_dotenv

# Configs
class Config:
    TESTING = False
    JSON_AS_ASCII = False
    TEMPLATES_AUTO_RELOAD = True
    JSON_SORT_KEYS = False
    
class ProductionConfig(Config):
    FLASK_ENV = 'production'
    DEBUG = False

class DevelopmentConfig(Config):
    ENV = 'development'
    DEBUG = True

# 從 .env 抓進來的秘密
load_dotenv()
DB_PW = os.getenv('DB_PASSWORD')
PR_KEY = os.getenv('PRIVATE_KEY')