from fastapi import FastAPI, Request, Depends, HTTPException
from . import config
from . import models
from .database import Base, engine, session_local
from sqlalchemy.orm import session
from .database import Base, engine
from .depends import get_db, get_current_user
from .routes import auth as routes_auth
from .models import User


# from fastapi.templating import Jinja2Templates


app = FastAPI(title=f"{config.APP_NAME}({config.APP_ENV})")


# later almebic
@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine)


@app.get("/")
async def front_page():
    return {
        "ok": True,
        "service": config.APP_NAME,
        "env": config.APP_ENV,
        "port": config.PORT,
    }


@app.get("/checkUser")
def check_user(cur_user: User = Depends(get_current_user)):
    return {"id": cur_user.id, "email": cur_user.email}


app.include_router(routes_auth.router)
