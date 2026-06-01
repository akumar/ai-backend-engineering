from datetime import UTC, datetime, timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext  # type: ignore[import-untyped]
from pydantic import BaseModel

from app.config import settings

router = APIRouter()

# Simple in-memory user "store" for demo purposes
fake_users_db: dict[str, dict[str, str]] = {}

# Use `sha256_crypt` here because the environment's bcrypt build
# caused compatibility errors with passlib (bcrypt backend issues
# raised during password hashing). For this demo/testing setup
# `sha256_crypt` is an acceptable secure fallback. If you prefer
# bcrypt, install a compatible `bcrypt` wheel for your Python
# installation and change this to `schemes=["bcrypt"]`.
pwd_context = CryptContext(schemes=["sha256_crypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")


# Pydantic schemas
class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None


class User(BaseModel):
    username: str


class UserInDB(User):
    hashed_password: str


class UserCreate(BaseModel):
    username: str
    password: str


# Password utilities
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)  # type: ignore[no-any-return]


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)  # type: ignore[no-any-return]


# Auth helpers
def get_user(username: str) -> UserInDB | None:
    user = fake_users_db.get(username)
    if user:
        return UserInDB(**user)
    return None


def authenticate_user(username: str, password: str) -> UserInDB | None:
    user = get_user(username)
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user


def create_access_token(
    data: dict[str, str], expires_delta: timedelta | None = None
) -> str:
    to_encode = data.copy()
    expire = datetime.now(UTC) + (
        expires_delta
        if expires_delta
        else timedelta(minutes=settings.access_token_expire_minutes or 30)
    )
    to_encode.update({"exp": expire})
    secret_key = settings.secret_key or "change-me"
    algorithm = settings.algorithm or "HS256"
    encoded_jwt = jwt.encode(to_encode, secret_key, algorithm=algorithm)
    return encoded_jwt


async def get_current_user(token: str = Depends(oauth2_scheme)) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    secret_key = settings.secret_key or "change-me"
    algorithm = settings.algorithm or "HS256"
    try:
        payload = jwt.decode(token, secret_key, algorithms=[algorithm])
        username: str | None = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = get_user(username=token_data.username or "")
    if user is None:
        raise credentials_exception
    return User(username=user.username)


# Routes
@router.post("/register", response_model=User, status_code=201)
async def register(user: UserCreate):
    if user.username in fake_users_db:
        raise HTTPException(status_code=400, detail="User already exists")
    hashed = get_password_hash(user.password)
    fake_users_db[user.username] = {
        "username": user.username,
        "hashed_password": hashed,
    }
    return User(username=user.username)


@router.post("/login", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/protected")
async def protected_route(current_user: User = Depends(get_current_user)):
    return {"message": "Protected data", "user": current_user.username}
