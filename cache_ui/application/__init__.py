from flask import Flask
from flask_redis import FlaskRedis

redis_client = FlaskRedis(decode_responses=True)

def create_app():

    app = Flask(__name__, instance_relative_config=False)
    app.config.from_object('config.Config')

    #Initialize redis instance with settings
    redis_client.init_app(app)

    with app.app_context():

        from . import routes

        return app