# Web Hard Service Project

    Online file storing and sharing service for light users.
    Focuses on storing documents such as pdf, epub, txt.
    Will be using FastAPI, SqlAlchemy, Mysql, Redis,

## Features

- User creation

- User authentication (JWT)

- Upload / Download of files

- NEXT PHASE: Organizing files in folders

- NEXT PHASE: Share files via link

## Structure

- API : FastAPI + pydantic, SQLAlchemy (async)
- DB : MySQL (metadata) (Alembic later)
- Object Storaget : MinIO -> S3
- Background Worker : Redis (+ Dramatiq later)
