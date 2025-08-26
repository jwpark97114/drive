from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import select
from fastapi.security import OAuth2PasswordRequestForm

from ..schemas import UserCreate, UserOut, Token, UserLogin, FileIn, FileList, FileOut
from ..models import User, File
from ..depends import get_db, get_current_user
from ..auth import hash_password, verify_password, create_access_token
from typing import List
from ..utils.s3 import presign_get, presign_put
from ..cache import cache_delete, cache_get_json, cache_set_json
from ..utils.s3 import convert2_public

router = APIRouter(prefix="/files", tags=["files"])


@router.post("/presign-upload")
def presign_upload(
    filename: str = Query(...),
    content_type: str = Query("application/octet-stream"),
    current_user: User = Depends(get_current_user),
):
    key = f"{current_user.id}/{filename}"
    url = presign_put(key, content_type)
    # url = convert2_public(url)
    return {"key": key, "upload_url": url}


@router.post(
    "/complete_upload", response_model=FileOut, status_code=status.HTTP_201_CREATED
)
def complete_upload(
    file: FileIn,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    newFile = File(
        owner_user_id=current_user.id,
        key=file.key,
        filename=file.filename,
        size_b=file.size_b,
        content_type=file.content_type,
    )

    db.add(newFile)
    db.commit()
    db.refresh(newFile)
    cache_delete(f"files:list:{current_user.id}")
    return newFile


@router.get("/", response_model=FileList)
def file_list(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    ttl=200,
):
    cache_k = f"files:list:{current_user.id}:limit={ttl}"
    cache = cache_get_json(cache_k)
    if cache is not None:
        return {"files": cache}

    f_list: List[File] = (
        db.query(File)
        .filter(File.owner_user_id == current_user.id)
        .order_by(File.created_at.desc())
        .limit(200)
        .all()
    )

    indiv_files = [
        {
            "id": f.id,
            "filename": f.filename,
            "size_b": f.size_b,
            "content-type": f.content_type,
            "created_at": f.created_at,
            "key": f.key,
        }
        for f in f_list
    ]

    cache_set_json(cache_k, indiv_files, ttl=90)

    return {"files": f_list}


@router.get("/{file_id}/presign-download")
def presign_download(
    file_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)
):
    target_file = (
        db.query(File)
        .filter(File.id == file_id, File.owner_user_id == current_user.id)
        .first()
    )
    if not target_file:
        raise HTTPException(404, detail="File does not exist")
    url = presign_get(target_file.key)
    return {"download_url": url}
