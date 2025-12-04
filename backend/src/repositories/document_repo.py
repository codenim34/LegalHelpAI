class DocumentRepository:
    """
    Abstracts file storage operations.
    """
    
    def __init__(self, storage_dir="data/uploads"):
        self.storage_dir = storage_dir

    def save_file(self, file):
        """
        Save an uploaded file to the local filesystem.
        """
        pass

    def get_file_path(self, filename):
        """
        Get the absolute path of a stored file.
        """
        pass
