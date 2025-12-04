from pypdf import PdfReader
import docx

class FileParser:
    """
    Handles parsing of different file types (PDF, DOCX).
    """
    
    @staticmethod
    def parse_pdf(file_path: str) -> str:
        """
        Extract text from a PDF file.
        
        Args:
            file_path: Path to the PDF file
            
        Returns:
            str: Extracted text from all pages
        """
        reader = PdfReader(file_path)
        text = ""
        for page in reader.pages:
            text += page.extract_text() + "\n"
        return text.strip()

    @staticmethod
    def parse_docx(file_path: str) -> str:
        """
        Extract text from a DOCX file.
        
        Args:
            file_path: Path to the DOCX file
            
        Returns:
            str: Extracted text from all paragraphs
        """
        doc = docx.Document(file_path)
        text = "\n".join([paragraph.text for paragraph in doc.paragraphs])
        return text.strip()
    
    @staticmethod
    def parse(file_path: str) -> str:
        """
        Auto-detect file type and parse accordingly.
        
        Args:
            file_path: Path to the file
            
        Returns:
            str: Extracted text
        """
        if file_path.endswith('.pdf'):
            return FileParser.parse_pdf(file_path)
        elif file_path.endswith('.docx'):
            return FileParser.parse_docx(file_path)
        else:
            raise ValueError(f"Unsupported file type: {file_path}")
