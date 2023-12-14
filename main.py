from fastapi import FastAPI
from routers import products,users
from fastapi.staticfiles import StaticFiles

app = FastAPI()

#Routers
app.include_router(products.router)
app.include_router(users.router)

app.mount("/static", StaticFiles(directory="static"),name="static")


@app.get("/")
async def root():
    return "Hola FastAPI!"

@app.get("/url")
async def root():
    return { "url_linkedIn" :"https://www.linkedin.com/in/sergio-alexander-huayllas-tirado-977b24218/"}