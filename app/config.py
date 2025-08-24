import os
from dotenv import load_dotenv


load_dotenv()

APP_NAME = os.getenv("APP_NAME", "WebHard")
APP_ENV = os.getenv("APP_ENV", "dev")
PORT = int(os.getenv("PORT", "8000"))
JWT_SECRET = os.getenv("JWT_SECRET")
JWT_ALG = os.getenv("JWT_ALG")
JWT_EXPIRE_MINUTES = int(os.getenv("JWT_EXPIRE_MINUTES"))
