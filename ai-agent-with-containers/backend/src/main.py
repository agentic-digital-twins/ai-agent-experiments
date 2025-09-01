import os
from contextlib import asynccontextmanager

from fastapi import FastAPI

from api.db import init_db
from api.chat.routing import router as chat_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup code
    init_db()
    yield
    # Any cleanup code can go here

app = FastAPI(lifespan=lifespan)
app.include_router(chat_router, prefix="/api/chats")

MY_TEST_VAR_INT = os.environ.get("MY_TEST_VAR_INT", "default_value int")
MY_TEST_VAR_STR = os.environ.get("MY_TEST_VAR_STR", "default_value str")    
API_KEY = os.environ.get("API_KEY", "default_key value")

if not API_KEY or API_KEY == "default_key value":
    raise ValueError("API_KEY environment variable is not set or has the default value.")   

@app.get("/")
def read_index():
    return {"message": "Hello, World!", "MY_TEST_VAR_INT": MY_TEST_VAR_INT, "MY_TEST_VAR_STR": MY_TEST_VAR_STR  }