from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

#inicia el server con: uvicorn users:app --reload

#Entidad user
class User(BaseModel):
    id: int
    name: str
    surname: str
    url: str
    age : int

users_list = [User(id=1,name="Sergio", surname="Huayllas", url="https://www.linkedin.com/in/sergio-alexander-huayllas-tirado-977b24218/", age=21),
        User(id=2,name="Jorge", surname="Gonzales", url="https://www.linkedin.com/in/jorge-gonzales-ramirez-8b0b0a1b4/", age=22),
        User(id=3,name="Jhon", surname="Caceres", url="https://www.linkedin.com/in/jhon-caceres-ramirez-8b0b0a1b4/", age=23)
        ]


# @app.get("/usersjson")
# async def usersjson():
#     return [
#         {"name":"Sergio", "surname":"Huayllas","url":"https://www.linkedin.com/in/sergio-alexander-huayllas-tirado-977b24218/","age":21},
#         {"name":"Jorge", "surname":"Gonzales","url":"https://www.linkedin.com/in/jorge-gonzales-ramirez-8b0b0a1b4/","age":22},
#         {"name":"Jhon", "surname":"Caceres","url":"https://www.linkedin.com/in/jhon-caceres-ramirez-8b0b0a1b4/","age":23},
#     ]


@app.get("/users")
async def users():
    return users_list
#path
@app.get("/user/{user_id}")
async def user(user_id: int):
    # users = filter(lambda user:user.id == user_id, users_list)
    # try:
    #     return list(users)[0]
    # except:
    #     return {"message":"Usuario no encontrado"}
    return search_user(user_id)
#query
@app.get("/user/")
async def user(id: int):
    # users = filter(lambda user:user.id == id, users_list)
    # try:
    #     return list(users)[0]
    # except:
    #     return {"message":"Usuario no encontrado"}
    return search_user(id)

def search_user(id):
    users = filter(lambda user:user.id == id, users_list)
    try:
        return list(users)[0]
    except:
        return {"message":"Usuario no encontrado"}

