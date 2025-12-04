import os
from pathlib import Path
import shutil

class DocumentRepository:
    """
    Abstracts file storage operations.
    """
    
    def __init__(self, storage_dir="data/uploads"):
        self.storage_dir = Path(storage_dir)
        # Create directory if it doesn't exist
        self.storage_dir.mkdir(parents=True, exist_ok=True)

    async def save_file(self, file) -> str:
        """
        Save an uploaded file to the local filesystem.
        
        Args:
            file: UploadFile object from FastAPI
            
        Returns:
            str: Path to the saved file
        """
        file_path = self.storage_dir / file.filename
        
        # Save file
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        return str(file_path)

    def get_file_path(self, filename: str) -> str:
        """
        Get the absolute path of a stored file.
        
        Args:
            filename: Name of the file
            
        Returns:
            str: Absolute path to the file
        """
        return str(self.storage_dir / filename)
