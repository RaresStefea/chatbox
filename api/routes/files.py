from pathlib import Path

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from db.database import get_db
from db.models import FileRecord, UserRecord
from utils.get_user import get_current_user
from utils import file_operations

UPLOAD_DIR = Path("files")

router = APIRouter(prefix="/files", tags=["files"])


@router.post("", status_code=status.HTTP_201_CREATED)
async def upload_file(
    file: UploadFile = File(...),
    current_user: UserRecord = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if not file.filename:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Filename is required",
        )

    content = await file.read()

    file_info = file_operations.save_upload_file(
        file_content=content, filename=file.filename, user_id=current_user.id
    )

    record = FileRecord(
        user_id=current_user.id,
        original_name=file_info["original_name"],
        stored_name=file_info["random_name"],
        path=file_info["path"],
        content_type=file.content_type or "application/octet-stream",
        size=len(content),
    )
    db.add(record)
    db.commit()
    db.refresh(record)

    return {
        "id": record.id,
        "filename": record.original_name,
        "content_type": record.content_type,
        "size": record.size,
        "path": record.path,
    }


@router.get("")
def list_files(
    current_user: UserRecord = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    records = db.query(FileRecord).filter(FileRecord.user_id == current_user.id).all()
    return [
        {
            "id": r.id,
            "filename": r.original_name,
            "content_type": r.content_type,
            "size": r.size,
            "created_at": r.created_at,
        }
        for r in records
    ]


@router.get("/{file_id}")
def get_file(
    file_id: int,
    current_user: UserRecord = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    record = (
        db.query(FileRecord)
        .filter(FileRecord.id == file_id, FileRecord.user_id == current_user.id)
        .first()
    )

    if not record:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="File not found"
        )

    return {
        "id": record.id,
        "filename": record.original_name,
        "content_type": record.content_type,
        "size": record.size,
        "created_at": record.created_at,
    }


@router.delete("/{file_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_file(
    file_id: int,
    current_user: UserRecord = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    record = (
        db.query(FileRecord)
        .filter(FileRecord.id == file_id, FileRecord.user_id == current_user.id)
        .first()
    )

    if not record:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="File not found"
        )

    Path(record.path).unlink(missing_ok=True)
    db.delete(record)
    db.commit()


@router.get("/{file_id}/content")
def get_file_content(
    file_id: int,
    current_user: UserRecord = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    record = (
        db.query(FileRecord)
        .filter(FileRecord.id == file_id, FileRecord.user_id == current_user.id)
        .first()
    )

    if not record:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="File not found"
        )

    file_path = Path(record.path)
    if not file_path.exists():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="File not found on disk"
        )

    return FileResponse(
        path=str(file_path),
        media_type=record.content_type,
        filename=record.original_name,
    )
