from fastapi import FastAPI
from fastapi import Path, Query
from typing import Annotated


app = FastAPI()


@app.get("/")
async def welcome() -> dict:
    return {"message": "Hello World"}


@app.get("/hello/{user}")
async def welcome_user(user: str) -> dict:
    return {"user": f'Hello {user}'}


@app.get("/order/{order_id}")
async def order(order_id: int) -> dict:
    return {"id": order_id}


@app.get("/user/{username}")
async def login(
        username: Annotated[
            str, Path(min_length=3, max_length=15, description='Enter your username',
                      example='permin0ff')],
        first_name: Annotated[
            str | None, Query(max_length=10, pattern="^J|s$")] = None) -> dict:
    return {"user": username, "Name": first_name}


@app.get("/employee/{name}/company/{company}")
async def get_employee(name: str, department: str, company: str) -> dict:
    return {"Employee": name, "Company": company, "Department": department}


@app.get("/user")
async def search(people: Annotated[list[str], Query()]) -> dict:
    return {"user": people}