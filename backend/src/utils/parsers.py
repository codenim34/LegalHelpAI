from pypdf import PdfReader
import docx
from PIL import Image
import google.generativeai as genai
from src.core.config import settings
from src.core.logging_config import get_logger
from src.core.exceptions import UnsupportedFileTypeError, DocumentProcessingError

logger = get_logger(__name__)

class FileParser:
    """
    Handles parsing of different file types (PDF, DOCX, Images).
    """
    
    def __init__(self):
        """Initialize Gemini for vision tasks."""
        if settings.GOOGLE_API_KEY:
            try:
                genai.configure(api_key=settings.GOOGLE_API_KEY)
                self.vision_model = genai.GenerativeModel('gemini-2.5-flash')
                logger.info("Vision model initialized for image parsing")
            except Exception as e:
                logger.warning(f"Failed to initialize vision model: {e}")
                self.vision_model = None
        else:
            logger.warning("GOOGLE_API_KEY not set. Image parsing will not be available.")
            self.vision_model = None
    
    @staticmethod
    def parse_pdf(file_path: str) -> str:
        """
        Extract text from a PDF file.
        
        Args:
            file_path: Path to the PDF file
            
        Returns:
            str: Extracted text from all pages
        """
        try:
            logger.debug(f"Parsing PDF: {file_path}")
            reader = PdfReader(file_path)
            text = ""
            for page in reader.pages:
                text += page.extract_text() + "\n"
            logger.debug(f"Extracted {len(text)} characters from PDF")
            return text.strip()
        except Exception as e:
            logger.error(f"Failed to parse PDF {file_path}: {e}")
            raise DocumentProcessingError(f"Failed to parse PDF: {e}")

    @staticmethod
    def parse_docx(file_path: str) -> str:
        """
        Extract text from a DOCX file.
        
        Args:
            file_path: Path to the DOCX file
            
        Returns:
            str: Extracted text from all paragraphs
        """
        try:
            logger.debug(f"Parsing DOCX: {file_path}")
            doc = docx.Document(file_path)
            text = "\n".join([paragraph.text for paragraph in doc.paragraphs])
            logger.debug(f"Extracted {len(text)} characters from DOCX")
            return text.strip()
        except Exception as e:
            logger.error(f"Failed to parse DOCX {file_path}: {e}")
            raise DocumentProcessingError(f"Failed to parse DOCX: {e}")
    
    def parse_image(self, file_path: str) -> str:
        """
        Extract text from an image using Gemini Vision.
        
        Args:
            file_path: Path to the image file
            
        Returns:
            str: Extracted text from the image
        """
        if not self.vision_model:
            logger.error("Vision model not available for image parsing")
            raise DocumentProcessingError("Gemini API key not configured for vision tasks")
        
        try:
            logger.debug(f"Parsing image with vision model: {file_path}")
            
            # Open image
            image = Image.open(file_path)
            
            # Use Gemini Vision to extract text
            prompt = """
            Extract all text from this image. If it's a legal document, preserve the structure and formatting.
            Include all text visible in the image, including headers, body text, and any footnotes.
            If the text is in Bengali (বাংলা), preserve it exactly as shown.
            """
            
            response = self.vision_model.generate_content([prompt, image])
            text = response.text.strip()
            logger.debug(f"Extracted {len(text)} characters from image")
            return text
        except Exception as e:
            logger.error(f"Failed to parse image {file_path}: {e}")
            raise DocumentProcessingError(f"Failed to parse image: {e}")
    
    def parse(self, file_path: str) -> str:
        """
        Auto-detect file type and parse accordingly.
        
        Args:
            file_path: Path to the file
            
        Returns:
            str: Extracted text
        """
        logger.info(f"Parsing file: {file_path}")
        file_lower = file_path.lower()
        
        if file_lower.endswith('.pdf'):
            return self.parse_pdf(file_path)
        elif file_lower.endswith('.docx'):
            return self.parse_docx(file_path)
        elif file_lower.endswith(('.png', '.jpg', '.jpeg', '.webp', '.heic', '.heif')):
            return self.parse_image(file_path)
        else:
            logger.error(f"Unsupported file type: {file_path}")
            raise UnsupportedFileTypeError(f"Unsupported file type: {file_path}")
