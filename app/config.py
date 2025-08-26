import os
from dotenv import load_dotenv


load_dotenv()

APP_NAME = os.getenv("APP_NAME", "WebHard")
APP_ENV = os.getenv("APP_ENV", "dev")
PORT = int(os.getenv("PORT", "8000"))
JWT_SECRET = os.getenv("JWT_SECRET")
JWT_ALG = os.getenv("JWT_ALG")
JWT_EXPIRE_MINUTES = int(os.getenv("JWT_EXPIRE_MINUTES"))
S3_ENDPOINT_URL = os.getenv("S3_ENDPOINT_URL")  # for minIO change for S3
S3_ACCESS_KEY = os.getenv("S3_ACCESS_KEY")
S3_SECRET_KEY = os.getenv("S3_SECRET_KEY")
S3_REGION = os.getenv("S3_REGION")
S3_BUCKET = os.getenv("S3_BUCKET")
S3_USE_SSL = os.getenv("S3_USE_SSL")
REDIS_URL = os.getenv("REDIS_URL")
S3_PUBLIC_ENDPOINT = os.getenv("S3_PUBLIC_ENDPOINT")