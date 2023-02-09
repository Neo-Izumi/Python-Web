from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path

db = SQLAlchemy()
DB_NAME = "database.db"

# this is a fuction that is no longer necessary because from flask-sqlalchemy 3, sqlalchemy will not overwrite the existing database
# def create_database(app):
#     if not path.exists('website/' + DB_NAME):
#         db.create_all(app=app)
#         print("Database created successfully!")

def create_app():
    app = Flask(__name__)
    app.secret_key = 'super secret key'
    app.config['SECRET-KEY'] = 'this is a secret key for encrypt my cookies and session data related to my website.'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)
    
    from .views import views 
    from .auth import auth  
    
    app.register_blueprint(views, url_prefix = "/")
    app.register_blueprint(auth, url_prefix = "/")
    
    from . import models
    
    with app.app_context():
        db.create_all()
    
    return app