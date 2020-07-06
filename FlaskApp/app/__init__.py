from flask import Flask

app = Flask(__name__)

if app.config["ENV"] == "production":
    app.config.from_object("app.config.ProductionConfig")
elif app.config["ENV"] == "testing":
    app.config.from_object("app.config.TestingConfig")
else:
    app.config.from_object("app.config.DevelopmentConfig")

from app import views
from app import admin_views
from app import error_handlers