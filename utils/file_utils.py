"""
File Text Extraction Utilities
Supports: PDF (.pdf), Word (.docx, .doc)
"""

import fitz  # PyMuPDF
import docx
from typing import Optional
import os

class FileTextExtractor:
    """Extract text from various file formats"""
    
    @staticmethod
    def extract_from_pdf(file_path: str) -> Optional[str]:
        """
        Extract text from PDF file using PyMuPDF.
        
        Args:
            file_path: Path to PDF file
        
        Returns:
            Extracted text or None if failed
        """
        try:
            doc = fitz.open(file_path)
            text_parts = []
            
            for page in doc:
                text_parts.append(page.get_text())
            
            full_text = "\n".join(text_parts)
            doc.close()
            
            print(f"✅ Extracted {len(full_text)} chars from PDF ({len(text_parts)} pages)")
            return full_text
            
        except Exception as e:
            print(f"❌ PDF extraction failed: {e}")
            return None
    
    @staticmethod
    def extract_from_docx(file_path: str) -> Optional[str]:
        """
        Extract text from DOCX file.
        
        Args:
            file_path: Path to DOCX file
        
        Returns:
            Extracted text or None if failed
        """
        try:
            doc = docx.Document(file_path)
            text_parts = []
            
            for paragraph in doc.paragraphs:
                if paragraph.text.strip():
                    text_parts.append(paragraph.text)
            
            full_text = "\n".join(text_parts)
            
            print(f"✅ Extracted {len(full_text)} chars from DOCX ({len(text_parts)} paragraphs)")
            return full_text
            
        except Exception as e:
            print(f"❌ DOCX extraction failed: {e}")
            return None
    
    @staticmethod
    def extract_text(file_path: str) -> Optional[str]:
        """
        Auto-detect file type and extract text.
        
        Args:
            file_path: Path to file (PDF or DOCX)
        
        Returns:
            Extracted text or None if failed
        """
        if not os.path.exists(file_path):
            print(f"❌ File not found: {file_path}")
            return None
        
        file_ext = os.path.splitext(file_path)[1].lower()
        
        if file_ext == '.pdf':
            return FileTextExtractor.extract_from_pdf(file_path)
        elif file_ext in ['.docx', '.doc']:
            return FileTextExtractor.extract_from_docx(file_path)
        else:
            print(f"❌ Unsupported file type: {file_ext}")
            return None
    
    @staticmethod
    def get_word_count(text: str) -> int:
        """Get word count from text"""
        return len(text.split())
    
    @staticmethod
    def validate_text(text: str, min_words: int = 50) -> bool:
        """
        Validate extracted text has sufficient content.
        
        Args:
            text: Extracted text
            min_words: Minimum word count required
        
        Returns:
            True if valid, False otherwise
        """
        if not text or not text.strip():
            print("❌ Validation failed: Empty text")
            return False
        
        word_count = FileTextExtractor.get_word_count(text)
        
        if word_count < min_words:
            print(f"⚠️ Warning: Only {word_count} words (min: {min_words})")
            return True  # Still proceed but warn
        
        print(f"✅ Text validation passed: {word_count} words")
        return True
