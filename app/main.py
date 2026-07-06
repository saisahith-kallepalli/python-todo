from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise
from api.routes.todo import todo_router


app = FastAPI()
app.include_router(todo_router)


@app.get("/")
def index():
    return {"status": "todo app running"}


register_tortoise(
    app,
    db_url="sqlite://toodo.db",
    modules={"models": ["api.models.todo"]},
    generate_schemas=True,
    add_exception_handlers=True,
)
