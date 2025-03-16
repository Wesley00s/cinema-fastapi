from pydantic import BaseModel


class ResetPasswordSchema(BaseModel):
    email: str
    new_password: str
