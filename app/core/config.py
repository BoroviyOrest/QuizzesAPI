import os

MONGODB_URL = os.getenv("MONGODB_URL")  # deploying without docker-compose
if MONGODB_URL is None:
    MONGO_HOST = os.getenv('MONGO_HOST', 'localhost')
    MONGO_PORT = int(os.getenv('MONGO_PORT', 27017))
    MONGO_USER = os.getenv('MONGO_USER', 'admin')
    MONGO_PASS = os.getenv('MONGO_PASSWORD', 'password')
    MONGO_DB = os.getenv('MONGO_DB', 'spanishQuizzesAPI')

    MONGODB_URL = f'mongodb://{MONGO_USER}:{MONGO_PASS}@{MONGO_HOST}:{MONGO_PORT}/{MONGO_DB}'

MAX_CONNECTIONS_COUNT = int(os.getenv("MAX_CONNECTIONS_COUNT", 10))
MIN_CONNECTIONS_COUNT = int(os.getenv("MIN_CONNECTIONS_COUNT", 10))
