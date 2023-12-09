from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def root():
    return "Hola FastAPI!"

@app.get("/url")
async def root():
    return { "url_linkedIn" :"https://www.linkedin.com/in/sergio-alexander-huayllas-tirado-977b24218/"}