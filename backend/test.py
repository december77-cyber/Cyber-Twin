from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI()

@app.get("/")
def post_sth():
    return {"message": "Hello sigma"}


@app.get("/html", response_class=HTMLResponse, include_in_schema=False)
def some_text():
    return f"<h1>Hello skibidi<h1>"

@app.post("/analyze-post")
def my_analysis_function():
    