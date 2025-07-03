import os
import shutil
import uuid
from typing import Optional
from fastapi import UploadFile, HTTPException
from app.core.config import settings


async def save_upload_file(file: UploadFile, folder: Optional[str] = None) -> str:
    """
    Save an uploaded file to the uploads directory and return the path
    
    Args:
        file: The uploaded file
        folder: Optional subfolder within the uploads directory
    
    Returns:
        str: The file path relative to the static directory
    """
    if not file:
        raise HTTPException(status_code=400, detail="No file provided")
    
    # Generate a unique filename to prevent conflicts
    file_ext = os.path.splitext(file.filename)[1] if file.filename else ""
    unique_filename = f"{uuid.uuid4()}{file_ext}"
    
    # Create the directory path
    upload_dir = os.path.join(settings.STATIC_PATH, settings.UPLOAD_FOLDER)
    if folder:
        upload_dir = os.path.join(upload_dir, folder)
    
    os.makedirs(upload_dir, exist_ok=True)
    
    # Save the file
    file_path = os.path.join(upload_dir, unique_filename)
    
    try:
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
    finally:
        await file.close()
    
    # Return the path relative to the static directory
    relative_path = os.path.join(settings.UPLOAD_FOLDER, folder or "", unique_filename) if folder else os.path.join(settings.UPLOAD_FOLDER, unique_filename)
    return relative_path


def delete_file(file_path: str) -> bool:
    """
    Delete a file from the uploads directory
    
    Args:
        file_path: The path to the file relative to the static directory
    
    Returns:
        bool: True if the file was deleted, False otherwise
    """
    full_path = os.path.join(settings.STATIC_PATH, file_path)
    
    if os.path.exists(full_path):
        os.remove(full_path)
        return True
    return False
