# AI Test Case Generator

Paste a Java method and get back JUnit test cases (normal, edge, and boundary scenarios) plus a time/space complexity analysis — powered entirely by a local LLM (Qwen2.5-1.5B via Ollama). No external API calls, no cost, runs fully offline.

## How it works

1. You paste a Java method into the UI.
2. The backend (FastAPI) builds a structured prompt and sends it to a locally running Qwen2.5-1.5B model via Ollama's REST API.
3. The model returns a JSON object containing a method summary, a list of test cases (with JUnit code), and a complexity breakdown.
4. The response is parsed defensively (handling cases where the model wraps JSON in markdown or adds stray text) and rendered in a Streamlit UI.

## Tech stack

- **Model:** Qwen2.5-1.5B-Instruct (quantized, ~1.3GB), served locally via [Ollama](https://ollama.com)
- **Backend:** FastAPI + Python, communicates with Ollama's local REST API
- **Frontend:** Streamlit
- **Parsing:** Defensive JSON extraction to handle inconsistent LLM output formatting

## Why local instead of an API-based LLM?

This project deliberately avoids cloud LLM APIs (OpenAI, Groq, etc.) to demonstrate local model deployment and inference — no internet dependency, no per-request cost, and full control over the inference environment.

## Setup

### 1. Install Ollama and pull the model
```bash
ollama pull qwen2.5:1.5b
```

### 2. Backend
```bash
cd backend
python -m venv venv
venv\Scripts\activate   # Windows
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

### 3. Frontend
```bash
cd frontend
pip install streamlit
streamlit run app.py
```

The app will open at `http://localhost:8501`. Make sure the backend (port 8000) is running first.

## Project structure
```
test-gen/
├── backend/
│   ├── main.py          # FastAPI app and /generate-tests endpoint
│   ├── llm_client.py     # Ollama API wrapper + defensive JSON parsing
│   ├── prompts.py        # Prompt template enforcing structured JSON output
│   └── requirements.txt
├── frontend/
│   └── app.py             # Streamlit UI
└── README.md
```

## Example

Input:
```java
public boolean isPrime(int n) {
    if (n <= 1) return false;
    for (int i = 2; i <= Math.sqrt(n); i++) {
        if (n % i == 0) return false;
    }
    return true;
}
```

Output includes test cases for n=1, n=2, negative numbers, and large primes, along with a complexity breakdown (O(√n) time, O(1) space).

## Future improvements
- Swap frontend to a lightweight HTML/JS UI
- Support languages beyond Java
- Add a confidence/self-check pass for generated test cases
