from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_mail import Mail

migrate = Migrate()
db = SQLAlchemy()
mail = Mail()
