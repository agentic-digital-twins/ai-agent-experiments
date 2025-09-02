import os
from langchain_openai import ChatOpenAI

OPENAI_BASE_URL = os.environ.get("OPENAI_BASE_URL", None)
OPENAI_MODEL_NAME = os.environ.get("OPENAI_MODEL_NAME", "ai/smollm2") 
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "unused-for-local")   
if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY environment variable is not set or has the default value.")


openai_params = {
    "model": OPENAI_MODEL_NAME,
    "api_key": OPENAI_API_KEY,
    "base_url": OPENAI_BASE_URL,
    "temperature": 0.7,
}

llm_base = ChatOpenAI(
    model=OPENAI_MODEL_NAME,
    api_key=OPENAI_API_KEY,
    base_url=OPENAI_BASE_URL,
    temperature=0.7,
)