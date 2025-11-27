import PyPDF2
from agents import function_tool

@function_tool
def extract_text_from_pdf(file_path: str) -> str:
    """Extract text from a PDF file."""
    try:
        with open(file_path, "rb") as f:
            reader = PyPDF2.PdfReader(f)
            text = ""
            for page in reader.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text
            return text
    except Exception as e:
        return f"Error reading PDF: {e}"

@function_tool
def summarize_notes(text: str) -> str:
    """Return the text so LLM can summarize."""
    return text

@function_tool
def generate_quiz(text: str, quiz_type: str = "MCQ") -> dict:
    """Return input so LLM generates questions."""
    return {"quiz_type": quiz_type, "text": text}


