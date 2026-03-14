from pathlib import Path
from typing import List

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from db.models import FileRecord
from utils import file_operations


def create_file_record(
    db: Session,
    user_id: int,
    filename: str,
    content: bytes,
    content_type: str,
) -> FileRecord:
    file_info = file_operations.save_upload_file(
        file_content=content, filename=filename, user_id=user_id
    )

    record = FileRecord(
        user_id=user_id,
        original_name=file_info["original_name"],
        stored_name=file_info["random_name"],
        path=file_info["path"],
        content_type=content_type or "application/octet-stream",
        size=len(content),
    )
    db.add(record)
    db.commit()
    db.refresh(record)
    return record


def get_file(db: Session, file_id: int, user_id: int) -> FileRecord:
    record = (
        db.query(FileRecord)
        .filter(FileRecord.id == file_id, FileRecord.user_id == user_id)
        .first()
    )

    if not record:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="File not found")

    return record


def list_files(db: Session, user_id: int) -> List[FileRecord]:
    return db.query(FileRecord).filter(FileRecord.user_id == user_id).all()


def delete_file(db: Session, file_id: int, user_id: int) -> None:
    record = get_file(db, file_id, user_id)

    Path(record.path).unlink(missing_ok=True)
    db.delete(record)
    db.commit()
