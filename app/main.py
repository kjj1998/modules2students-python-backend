"""
Main module of the module2student Python backend
"""
from fastapi import FastAPI
from routers import module # pylint: disable=import-error
from routers import student # pylint: disable=import-error
from routers import auth # pylint: disable=import-error

app = FastAPI()

app.include_router(module.router)
app.include_router(student.router)
app.include_router(auth.router)

@app.get("/")
async def root():
    """
    API root endpoint
    """
    return { "message": "Hello Bigger Applications!"}
