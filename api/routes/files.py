from pathlib import Path

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status

from db.models import UserRecord
from utils.get_user import get_current_user
from utils import file_operations

UPLOAD_DIR = Path("files")

router = APIRouter(prefix="/files", tags=["files"])


@router.post("", status_code=status.HTTP_201_CREATED)
async def upload_file(
    file: UploadFile = File(...),
    current_user: UserRecord = Depends(get_current_user),
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

    # TODO:
    """
    - store a DB record for the file
    - create remaining roots (list files, retreife file retreive file content)
    """

    return {
        "filename": file_info["original_name"],
        "content_type": file.content_type or "application/octet-stream",
        "size": len(content),
        "path": file_info["path"],
    }
