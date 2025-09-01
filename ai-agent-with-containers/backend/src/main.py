from fastapi import FastAPI
import os

app = FastAPI()

MY_TEST_VAR_INT = os.environ.get("MY_TEST_VAR_INT", "default_value int")
MY_TEST_VAR_STR = os.environ.get("MY_TEST_VAR_STR", "default_value str")    
API_KEY = os.environ.get("API_KEY", "default_key value")

if not API_KEY or API_KEY == "default_key value":
    raise ValueError("API_KEY environment variable is not set or has the default value.")   

@app.get("/")
def read_index():
    return {"message": "Hello, World!", "MY_TEST_VAR_INT": MY_TEST_VAR_INT, "MY_TEST_VAR_STR": MY_TEST_VAR_STR  }