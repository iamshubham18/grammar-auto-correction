
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from backend.model import correct_text, highlight_changes


# ==========================================
# FASTAPI APPLICATION
# ==========================================

app = FastAPI(
    title="Grammar Auto-Correction API",
    description="API powered by a fine-tuned T5-small model",
    version="1.0.0"
)


# ==========================================
# CORS CONFIGURATION
# ==========================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173"
    ],
    allow_credentials=False,
    allow_methods=["GET", "POST"],
    allow_headers=["Content-Type"]
)


# ==========================================
# REQUEST SCHEMA
# ==========================================

class CorrectionRequest(BaseModel):

    text: str = Field(
        min_length=1,
        max_length=5000,
        description="Text to correct"
    )


# ==========================================
# HEALTH CHECK
# ==========================================

@app.get("/api/health")
def health_check():

    return {
        "status": "success",
        "message": "Grammar Auto-Correction API is running"
    }


# ==========================================
# GRAMMAR CORRECTION
# ==========================================

@app.post("/api/correct")
def correct_grammar(request: CorrectionRequest):

    original_text = request.text

    if not original_text.strip():

        raise HTTPException(
            status_code=400,
            detail="Please enter some text."
        )

    try:

        corrected_text = correct_text(original_text)

        highlighted_html = highlight_changes(
            original_text,
            corrected_text
        )

        return {
            "status": "success",
            "original": original_text,
            "corrected": corrected_text,
            "highlighted_html": highlighted_html
        }

    except Exception as error:

        print(f"Correction error: {error}")

        raise HTTPException(
            status_code=500,
            detail="Unable to process the text. Please try again."
        )
