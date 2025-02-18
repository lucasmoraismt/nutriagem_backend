from fastapi import APIRouter
from models import FormData
from utils.promptHelper import generatePrompt

router = APIRouter(prefix="/forms", tags=["forms"])

@router.post("/")
async def analyze_form(formData: FormData):
  # Generate LLM prompt
  llmPrompt = generatePrompt(formData)
  
  # Insert LLM integration here
  return {
    "message": "Form processed successfully",
    "llmPrompt": llmPrompt
  }
