from datetime import datetime, timedelta

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.testing import db

from app.core.db_config import settings
from app.models.admin_model import AdminModel
from app.models.user_model import UserModel

oauth2_admin = OAuth2PasswordBearer(tokenUrl="admin/auth")
oauth2_customer = OAuth2PasswordBearer(tokenUrl="customer/auth")


def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now() + expires_delta
    else:
        expire = datetime.now() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM
    )
    return encoded_jwt


async def get_current_customer(token: str = Depends(oauth2_customer)):
    return await verify_token(token, UserModel)


async def get_current_admin(token: str = Depends(oauth2_admin)):
    return await verify_token(token, AdminModel)


async def verify_token(token: str, model):
    try:
        payload = jwt.decode(
            token,
            settings.JWT_SECRET_KEY,
            algorithms=[settings.JWT_ALGORITHM]
        )
        email = payload.get("sub")
        if not email:
            raise HTTPException(status_code=401, detail="Invalid token")

        customer = db.query(model).filter(model.email == email).first()
        if not customer:
            raise HTTPException(status_code=401, detail="User not found")

        return customer
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
