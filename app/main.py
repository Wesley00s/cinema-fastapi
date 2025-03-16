import uvicorn

from app.core.app_config import get_application
from app.core.init_pages import init_pages
from app.database.init_models import init_database_models
from app.core.init_routers import init_routers

init_database_models()
app = get_application()
init_routers(app)
init_pages(app)

if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000)
