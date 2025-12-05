from pypdf import PdfReader
import docx
from PIL import Image
import google.generativeai as genai
import os

class FileParser:
    """
    Handles parsing of different file types (PDF, DOCX, Images).
    """
    
    def __init__(self):
        """Initialize Gemini for vision tasks."""
        api_key = os.getenv("GOOGLE_API_KEY")
        if api_key:
            genai.configure(api_key=api_key)
            self.vision_model = genai.GenerativeModel('gemini-2.5-flash')
        else:
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
    
    def parse_image(self, file_path: str) -> str:
        """
        Extract text from an image using Gemini Vision.
        
        Args:
            file_path: Path to the image file
            
        Returns:
            str: Extracted text from the image
        """
        if not self.vision_model:
            raise ValueError("Gemini API key not configured for vision tasks")
        
        # Open image
        image = Image.open(file_path)
        
        # Use Gemini Vision to extract text
        prompt = """
        Extract all text from this image. If it's a legal document, preserve the structure and formatting.
        Include all text visible in the image, including headers, body text, and any footnotes.
        If the text is in Bengali (বাংলা), preserve it exactly as shown.
        """
        
        response = self.vision_model.generate_content([prompt, image])
        return response.text.strip()
    
    def parse(self, file_path: str) -> str:
        """
        Auto-detect file type and parse accordingly.
        
        Args:
            file_path: Path to the file
            
        Returns:
            str: Extracted text
        """
        file_lower = file_path.lower()
        
        if file_lower.endswith('.pdf'):
            return self.parse_pdf(file_path)
        elif file_lower.endswith('.docx'):
            return self.parse_docx(file_path)
        elif file_lower.endswith(('.png', '.jpg', '.jpeg', '.webp', '.heic', '.heif')):
            return self.parse_image(file_path)
        else:
            raise ValueError(f"Unsupported file type: {file_path}")
