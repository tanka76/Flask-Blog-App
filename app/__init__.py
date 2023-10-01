import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from dotenv import load_dotenv
from flask_smorest import Api

db = SQLAlchemy()
ma = Marshmallow()
api = Api()



def create_app():
    """
    Create a Flask application instance and configure it.
    """
    app = Flask(
        __name__,
        template_folder="../templates/build",
        static_folder="../templates/build/static",
    )
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///blog.db"

    #swagger config
    app.config["PROPAGATE_EXCEPTIONS"] = True
    app.config["API_TITLE"] = "My API"
    app.config["API_VERSION"] = "v1"
    app.config["OPENAPI_VERSION"] = "3.0.2"
    app.config["OPENAPI_URL_PREFIX"]='/'
    app.config["OPENAPI_SWAGGER_UI_PATH"]='/swagger-ui'
    app.config["OPENAPI_SWAGGER_UI_URL"]='https://cdnjs.cloudflare.com/ajax/libs/swagger-ui/3.24.2/'

    #redoc
    app.config["OPENAPI_REDOC_PATH"]='/redoc-ui'
    app.config["OPENAPI_REDOC_URL"]='https://rebilly.github.io/ReDoc/releases/v1.x.x/redoc.min.js'

    


    api.init_app(app)


    from users import models

    # Initialize extensions
    db.init_app(app)
    ma.init_app(app)
    migrate = Migrate(app, db)

    register_blueprints(app=app)

    return app


def register_blueprints(app):
    from users.routes import bp as users_blueprint

    #we are registering using flask smorest.
    api.register_blueprint(users_blueprint)
    


def get_database_uri():
    """
    Construct the database URI based on environment variables.
    """
    database_name = os.getenv("DATABASE_NAME")
    database_username = os.getenv("DATABASE_USERNMAE")
    database_password = os.getenv("DATABASE_PASSWORD")
    host_name = os.getenv("HOST_NAME")
    db_port = os.getenv("DB_PORT")

    return f"postgres://{database_username}:{database_password}@{host_name}:{db_port}/{database_name}"