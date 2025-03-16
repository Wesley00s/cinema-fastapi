from pydantic import BaseModel


class AdminImageSchema(BaseModel):
    admin_id: str
    image_data: str

    class Config:
        from_attributes = True
