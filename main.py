from fastapi import FastAPI, File, UploadFile, HTTPException, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from markitdown import MarkItDown
import tempfile
import os
from typing import Optional
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="MarkItDown API",
    description="Convert various file formats to Markdown using Microsoft's MarkItDown library",
    version="1.0.0"
)

# Security
security = HTTPBearer()

# Configuration - You can set this via environment variables
API_TOKEN = os.getenv("API_TOKEN", "your-secret-token-here")

# Initialize MarkItDown
md_converter = MarkItDown(enable_plugins=False)

def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)) -> str:
    """Verify the API token"""
    if credentials.credentials != API_TOKEN:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return credentials.credentials

@app.get("/")
async def root():
    """Root endpoint with basic info"""
    return {
        "message": "MarkItDown API",
        "description": "Convert various file formats to Markdown",
        "version": "1.0.0",
        "supported_formats": [
            "PowerPoint (.pptx)",
            "Word (.docx)",
            "Excel (.xlsx, .xls)",
            "PDF (.pdf)",
            "Images (with OCR)",
            "Audio files (with transcription)",
            "HTML",
            "Text-based formats (CSV, JSON, XML)",
            "ZIP files",
            "EPubs",
            "And more..."
        ]
    }

@app.post("/convert")
async def convert_file_to_markdown(
    file: UploadFile = File(...),
    token: str = Depends(verify_token)
):
    """
    Convert uploaded file to Markdown
    
    Args:
        file: The file to convert (supports various formats)
        
    Returns:
        JSON response with the markdown content
    """
    if not file.filename:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No file provided"
        )
    
    # Log the conversion request
    logger.info(f"Converting file: {file.filename} (Content-Type: {file.content_type})")
    
    try:
        # Read the file content
        file_content = await file.read()
        
        # Create a temporary file to work with
        with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(file.filename)[1]) as temp_file:
            temp_file.write(file_content)
            temp_file_path = temp_file.name
        
        try:
            # Convert the file using MarkItDown
            result = md_converter.convert(temp_file_path)
            
            # Clean up the temporary file
            os.unlink(temp_file_path)
            
            return {
                "success": True,
                "filename": file.filename,
                "file_size": len(file_content),
                "markdown": result.text_content,
                "metadata": {
                    "title": getattr(result, 'title', None),
                    "content_length": len(result.text_content)
                }
            }
            
        except Exception as conversion_error:
            # Clean up the temporary file in case of error
            if os.path.exists(temp_file_path):
                os.unlink(temp_file_path)
            
            logger.error(f"Conversion error for {file.filename}: {str(conversion_error)}")
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=f"Failed to convert file: {str(conversion_error)}"
            )
            
    except Exception as e:
        logger.error(f"Error processing file {file.filename}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error: {str(e)}"
        )

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "markitdown-api"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8003,
        reload=True
    )