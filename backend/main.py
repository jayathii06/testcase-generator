from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from llm_client import call_qwen, extract_json
from prompts import build_test_gen_prompt

app = FastAPI(title="AI Test Case Generator")

# Allow Streamlit frontend (different port) to call this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


class CodeInput(BaseModel):
    java_code: str


@app.get("/")
def health_check():
    return {"status": "ok", "message": "Test Case Generator API is running"}


@app.post("/generate-tests")
def generate_tests(payload: CodeInput):
    if not payload.java_code.strip():
        return {"error": "No code provided"}

    prompt = build_test_gen_prompt(payload.java_code)
    raw_response = call_qwen(prompt)
    parsed = extract_json(raw_response)
    return parsed
