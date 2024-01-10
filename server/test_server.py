from fastapi import FastAPI
from pydantic import BaseModel


test_app = FastAPI()


class Prompt(BaseModel):
    content: str


@test_app.get("/test")
def test_func():
    return {"My Name": "Huy Bui"}

@test_app.post("/process")
def process_text(user_prompt: Prompt):
    breakpoint()
    return None
