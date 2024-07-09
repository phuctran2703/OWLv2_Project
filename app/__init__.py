from flask import Flask
from app.views import user_views, product_views
from app.models import db

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')

    db.init_app(app)

    app.register_blueprint(user_views.bp)
    app.register_blueprint(product_views.bp)

    return app
