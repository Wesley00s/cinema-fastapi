from pydantic import BaseModel


class MovieImageSchema(BaseModel):
    movie_id: str
    image_data: str

    class Config:
        from_attributes = True
