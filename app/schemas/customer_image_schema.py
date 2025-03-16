from pydantic import BaseModel


class CustomerImageSchema(BaseModel):
    customer_id: str
    image_data: str

    class Config:
        from_attributes = True
