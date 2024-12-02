from pydantic import BaseModel

from model.Role import Role


class User(BaseModel):
    email: str | None = None
    password: str | None = None
    first_name: str | None = None
    last_name: str | None = None
    address: str | None = None
    city: str | None = None
    state: str | None = None
    zip_code: str | None = None
    country: str | None = None
    role: Role | None = None

    model_config = {
        "arbitrary_types_allowed": True
    }