from app.database.database import engine
from app.models import (
    user_model,
    admin_model,
    admin_image_model,
    customer_model,
    customer_image_model,
    movie_model,
    movie_images_model,
    room_model,
    seat_model,
    session_model,
    ticket_model
)


def init_database_models():
    user_model.Base.metadata.create_all(bind=engine)
    admin_model.UserModel.metadata.create_all(bind=engine)
    admin_image_model.AdminImageModel.metadata.create_all(bind=engine)
    customer_model.UserModel.metadata.create_all(bind=engine)
    customer_image_model.CustomerImageModel.metadata.create_all(bind=engine)
    movie_model.Base.metadata.create_all(bind=engine)
    movie_images_model.MovieImagesModel.metadata.create_all(bind=engine)
    room_model.Base.metadata.create_all(bind=engine)
    seat_model.Base.metadata.create_all(bind=engine)
    session_model.Base.metadata.create_all(bind=engine)
    ticket_model.Base.metadata.create_all(bind=engine)
