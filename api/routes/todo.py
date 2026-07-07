from app.websocket.websocket import manager
from fastapi import (
    APIRouter,
    status,
    HTTPException,
    Depends,
    WebSocket,
    WebSocketDisconnect,
)
from api.schemas.todo import GetToDo, PostToDo, PutToDo
from api.models.todo import Todo
from app.auth.user import get_current_user


todo_router = APIRouter(
    prefix="/api/todo", tags=["Todo"], dependencies=[Depends(get_current_user)]
)


@todo_router.get("/")
async def all_todos():
    data = Todo.all()
    return await GetToDo.from_queryset(data)


@todo_router.post("/create")
async def create_todo(body: PostToDo, current_user=Depends(get_current_user)):
    print(body)
    row = await Todo.create(**body.dict(exclude_unset=True), user=current_user.id)
    todo_data = dict(await GetToDo.from_tortoise_orm(row))
    await manager.send_personal_message(
        {"event": "todo_created", "data": todo_data}, current_user.id
    )
    return await GetToDo.from_tortoise_orm(row)


@todo_router.put("/update/{id}")
async def update_todo(id: int, body: PutToDo):
    current_user = Depends(get_current_user)
    data = body.dict(exclude_unset=True)
    exists = await Todo.filter(id=id).exists()
    if not exists:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found"
        )
    await Todo.filter(id=id, user=current_user).update(**data)
    updated_row = await Todo.get(id=id)
    todo_data = dict(await GetToDo.from_tortoise_orm(updated_row))
    await manager.send_personal_message(
        {"event": "todo_updated", "data": todo_data}, current_user.id
    )

    return todo_data


@todo_router.delete("/delete/{id}")
async def delete_todo(id: int):
    exists = Todo.filter(id=id).exists()
    if not exists:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found"
        )
    await Todo.filter(id=id).delete()
    return "Todo deleted successfully"


@todo_router.websocket("/ws/{user_id}")
async def websocket_endpoint(websocket: WebSocket, user=Depends(get_current_user)):
    await manager.connect(websocket, user.id)
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(websocket, user.id)
