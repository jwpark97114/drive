from fastapi import FastAPI, Request, Depends, HTTPException
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession


app = FastAPI()

templates = Jinja2Templates(directory="templates")


@app.get("/")
async def front_page():
    return {"hi"}
