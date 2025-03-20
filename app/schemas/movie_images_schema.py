from pydantic import BaseModel


class MovieImagesSchema(BaseModel):
    movie_id: int
    poster_image_data: str
    backdrop_image_data: str

    class Config:
        from_attributes = True
