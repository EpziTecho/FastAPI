from fastapi import FastAPI, HTTPException
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

# path
@app.get("/user/{user_id}")
async def user(user_id: int):
    user = search_user(user_id)
    if user:
        return user
    else:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

# query
@app.get("/user/")
async def user(id: int):
    user = search_user(id)
    if user:
        return user
    else:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

@app.post("/user/",response_model=User, status_code=201)
async def create_user(user: User):
    existing_user = search_user(user.id)
    if existing_user:
        raise HTTPException(status_code=404, detail="Usuario ya existe")
    else:
        users_list.append(user)
        return user

@app.put("/user/")
async def update_user(user: User):
    found = False
    for index, saved_user in enumerate(users_list):
        if saved_user.id == user.id:
            users_list[index] = user
            found = True
    if not found:
        raise HTTPException(status_code=404, detail="No se actualizó el usuario")
    else:
        return user

@app.delete("/user/{id}")
async def delete_user(id: int):
    found = False
    for index, saved_user in enumerate(users_list):
        if saved_user.id == id:
            del users_list[index]
            found = True
    if not found:
        raise HTTPException(status_code=404, detail="No se eliminó el usuario")
    else:
        return {"message": "Usuario eliminado exitosamente"}

            
                      


def search_user(id):
    users = filter(lambda user:user.id == id, users_list)
    try:
        return list(users)[0]
    except:
        return {"message":"Usuario no encontrado"}



