import logging
import betterlogging as bl
import uvicorn
from fastapi import FastAPI, APIRouter

from src import routes
from src.common.config import Config
from src.common.misc.dependencies import override_dependencies
from src.common.misc.shutdown import register_shutdown_events
from src.common.utilities.database.session import create_session_factory

log = logging.getLogger(__name__)


def main():
    config = Config.from_env()
    bl.basic_colorized_config(level=config.misc.log_level)
    log.info('Starting...')

    db_engine, session_factory = create_session_factory(config.db.sqlalchemy_uri, config.misc.log_level)
    app = FastAPI(redoc_url=None)
    router = APIRouter()

    override_dependencies(app, config, session_factory)
    register_shutdown_events(app, db_engine)

    routes.register(router)
    app.include_router(router)

    uvicorn.run(app, host='0.0.0.0', port=8000)


if __name__ == "__main__":
    main()
