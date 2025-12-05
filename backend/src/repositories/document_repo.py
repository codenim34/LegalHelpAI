import os
from pathlib import Path
import shutil
from src.core.config import settings
from src.core.logging_config import get_logger
from src.core.exceptions import FileStorageError

logger = get_logger(__name__)

class DocumentRepository:
    """
    Abstracts file storage operations.
    """
    
    def __init__(self, storage_dir=None):
        self.storage_dir = Path(storage_dir or settings.UPLOAD_DIR)
        # Create directory if it doesn't exist
        self.storage_dir.mkdir(parents=True, exist_ok=True)
        logger.debug(f"Document repository initialized. Storage dir: {self.storage_dir}")

    async def save_file(self, file) -> str:
        """
        Save an uploaded file to the local filesystem.
        
        Args:
            file: UploadFile object from FastAPI
            
        Returns:
            str: Path to the saved file
        """
        try:
            file_path = self.storage_dir / file.filename
            logger.debug(f"Saving file: {file.filename}")
            
            # Save file
            with open(file_path, "wb") as buffer:
                shutil.copyfileobj(file.file, buffer)
            
            logger.info(f"File saved successfully: {file_path}")
            return str(file_path)
        
        except Exception as e:
            logger.error(f"Failed to save file {file.filename}: {e}")
            raise FileStorageError(f"Failed to save file: {e}")

    def get_file_path(self, filename: str) -> str:
        """
        Get the absolute path of a stored file.
        
        Args:
            filename: Name of the file
            
        Returns:
            str: Absolute path to the file
        """
        return str(self.storage_dir / filename)
