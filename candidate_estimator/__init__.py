"""Main entry point
"""
from pyramid.config import Configurator
from sqlalchemy import engine_from_config
from sqlalchemy.orm import sessionmaker

from candidate_estimator.model import initialize_sql


def db(request):
    maker = request.registry.dbmaker
    session = maker()

    def cleanup(request):
        if request.exception is not None:
            session.rollback()
        else:
            session.commit()
        session.close()

    request.add_finished_callback(cleanup)
    return session


def main(global_config, **settings):
    config = Configurator(settings=settings)
    engine = engine_from_config(settings)       # prefix='sqlalchemy.' used in .ini file
    initialize_sql(engine)
    config.registry.dbmaker = sessionmaker(bind=engine)
    config.add_request_method(db, reify=True)   # request.db contains SQLAlchemy session
    config.include("cornice")
    config.scan("candidate_estimator.views")
    return config.make_wsgi_app()
