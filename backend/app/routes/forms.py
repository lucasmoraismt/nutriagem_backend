import os
import asyncio
import logging
from dotenv import load_dotenv
from fastapi import APIRouter, HTTPException
from backend.app.models.FormData import FormData
from utils.promptHelper import generatePrompt
import google.generativeai as genai

#Load environment variables
load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env'))

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/forms", tags=["forms"])

@router.post("/")
async def analyze_form(formData: FormData):
  try:
    if not os.getenv("GEMINI_API_KEY"):
      raise ValueError("Missing API key configuration")

    genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

    llmPrompt = generatePrompt(formData)

    model = genai.GenerativeModel("gemini-1.5-flash")
    response = await asyncio.to_thread(model.generate_content, llmPrompt)

    if not response.text:
      raise ValueError("Empty response from AI model")

    return {
      "message": "Form processed successfully",
      "response": response.text
    }

  except ValueError as ve:
    logger.error(f"Validation error: {str(ve)}")
    raise HTTPException(status_code=400, detail=str(ve))
  except genai.errors.GoogleAPIError as ge:
    logger.error(f"Google API error: {str(ge)}")
    raise HTTPException(status_code=503, detail="AI service unavailable")
  except Exception as e:
    logger.error(f"Unexpected error: {str(e)}")
    raise HTTPException(status_code=500, detail="Internal server error")
