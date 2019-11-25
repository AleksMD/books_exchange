from flask import Flask
from extensions import db, migrate
from config import get_config
from api.blueprints import (book_blueprint,
                            library_blueprint,
                            user_blueprint)


def create_app(env='dev'):
    app = Flask(__name__)
    app.config.from_object(get_config(env))
    db.init_app(app)

    app.register_blueprint(user_blueprint)
    app.register_blueprint(book_blueprint)
    app.register_blueprint(library_blueprint)
    db.create_all(app=app)
    migrate.init_app(app, db)
    return app


if __name__ == '__main__':
    create_app('dev').run()
