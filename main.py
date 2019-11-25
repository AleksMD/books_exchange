from flask import Flask
from extensions import db, migrate
from config import get_config


def create_app(env='test'):
    app = Flask(__name__)
    app.config.from_object(get_config(env))
    with app.app_context():
        db.init_app(app)
        migrate.init_app(app, db)

    return app


if __name__ == '__main__':
    create_app('dev').run()
