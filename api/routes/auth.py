from app.auth.user import verify_password
from fastapi import Depends
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from fastapi import APIRouter, status, HTTPException
from api.schemas.user import UserCreate, UserResponse, Token
from api.models.user import User
from app.auth.user import get_password_hash, create_access_token
import uuid


auth_router = APIRouter(prefix="/api/user", tags=["User"])


@auth_router.post("/signup", response_model=UserResponse)
async def create_user(body: UserCreate):
    print(body)
    exist = await User.filter(username=body.username).exists()
    if exist:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User found")
    else:
        body.password = get_password_hash(body.password)
        row = await User.create(id=str(uuid.uuid4()), **body.dict(exclude_unset=True))

        return row


@auth_router.post(
    "/login",
    response_model=Token,
)
async def login(body: OAuth2PasswordRequestForm = Depends()):
    print(body)
    user = await User.get_or_none(username=body.username)
    if user is None or not verify_password(body.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials"
        )
    else:
        token = create_access_token(
            data={
                "sub": str(user.id)
            }
        )
        return {"access_token": token, "token_type": "bearer"}
