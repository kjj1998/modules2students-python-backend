"""
Main module of the module2student Python backend
"""
from fastapi import FastAPI
from routers.modules import modules # pylint: disable=import-error
from routers.students import students # pylint: disable=import-error

app = FastAPI()

app.include_router(modules.router)
app.include_router(students.router)

@app.get("/")
async def root():
    """
    API root endpoint
    """
    return { "message": "Hello Bigger Applications!"}
