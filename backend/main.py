from model import Laptop,Users
from database import SessionLocal,Base,engine
from fastapi import FastAPI, Depends, status,HTTPException
from pydantic import BaseModel
from typing import Annotated
from sqlalchemy.orm import Session

# Create tables if they don't exist
Base.metadata.create_all(bind=engine)

app = FastAPI()


class Registration(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: str
    password: str
    role: str
class Laptop_detail(BaseModel):
 
    brand:str
    model:str 
    processor:str
    ram :str
    storage :str
    price :float
    count:int

class Laptop_Sell(BaseModel):
    brand:str
    model:str

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]


@app.put("/registration",status_code=status.HTTP_201_CREATED)
async def registration_page(detail: Registration, db: db_dependency):
    registration_detail=Users(**detail.dict())
    db.add(registration_detail)
    db.commit()
    return {"status": "Registration Completed"}


@app.post("/login",status_code=status.HTTP_200_OK)
async def login(detail:Laptop_detail,db:db_dependency):
    if detail is None:
        raise HTTPException(status_code=401, detail='Authentication Failed')
    user=db.query(Users).filter(Users.email==detail.email).filter(Users.password==detail.password)

    if user is None:
        raise HTTPException(status_code=401, detail='Authentication Failed 2')
    return "Login Successfully"



@app.get("/all_users")
async def allUsers(db:db_dependency):
    users=db.query(Users).all()
    if not users:
        return {"message": "No users found"}

    # Build a list of user info dictionaries
    result = []
    for user in users:
        result.append({
            "First Name": user.first_name,
            "Last Name": user.last_name,
            "Email": user.email,
            "Role": user.role
        })

    return {"users": result}


@app.get("/all_Laptops")
async def all_Laptops(db:db_dependency):
    laptops=db.query(Laptop).all()
    if laptops is None:
        return {"message": "No laptops found"}

    # Build a list of user info dictionaries
    result = []
    for laptop in laptops:
        result.append({
            "Brand": laptop.brand,
            "Model": laptop.model,
            "Price": laptop.price,
            "Count": laptop.count
        })
         

    return {"Laptops": result}



@app.post("/add")
async def add_laptop(detail:Laptop_detail, db:db_dependency):
    # try:
    if detail is None:
        return {"message": "No Record Found"}
    try:
        laptops = Laptop(
            brand=detail.brand,
            model=detail.model,
            processor=detail.processor,
            ram=detail.ram,
            storage=detail.storage,
            price=detail.price,
            count=detail.count
        )

        db.add(laptops)
        db.commit()
        db.refresh(laptops)
        return {"message":"Laptops is add Successfully"}
    except:
        return {"message":"Please try again"}
    


@app.put("/sell")
async def sell_laptop(detail:Laptop_Sell, db:db_dependency):
    laptop = db.query(Laptop).filter(
        Laptop.brand == detail.brand,
        Laptop.model == detail.model
    ).all()

    if not laptop:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Laptop not found in inventory"
        )

    if laptop.count <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Laptop is out of stock"
        )
    if laptop.count < 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Insufficient stock to complete sale"
        )

    db.commit()
    db.refresh(laptop)

    return {
        "message": f"Sold {detail.quantity} {laptop.brand} {laptop.model}(s)",
        "remaining_stock": laptop.count,
        "price_per_unit": laptop.price,
        "total_sale_value": laptop.price * detail.quantity
        }


@app.put("/delete")
async def delete_laptop(detail:Laptop_Sell, db:db_dependency):
    laptop = db.query(Laptop).filter(
        Laptop.brand == detail.brand,
        Laptop.model == detail.model
    ).first()

    if not laptop:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Laptop not found in inventory"
        )

    db.delete(laptop)
    db.commit()

    return {
        "message": f"Laptop '{laptop.brand} {laptop.model}' deleted successfully from inventory."
    }

