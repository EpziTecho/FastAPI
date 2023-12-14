from fastapi import APIRouter

router = APIRouter(prefix="/products",
                   tags=["products"],
                   responses={404: {"description": "Not found"}})

products_list = ["Producto 1", "Producto 2", "Producto 3"]

@router.get("/")
async def products():
    return products_list
        

@router.get("/{id}")
async def products(id: int):
    return products_list[id]