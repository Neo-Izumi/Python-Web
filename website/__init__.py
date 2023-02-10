from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from os import path

db = SQLAlchemy()
DB_NAME = "database.db"

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
        
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)
    
    @login_manager.user_loader
    def load_user(id):
        return models.User.query.get_or_404(int(id))
    
    return app









# this is a fuction that is no longer necessary because from flask-sqlalchemy 3, sqlalchemy will not overwrite the existing database
# def create_database(app):
#     if not path.exists('website/' + DB_NAME):
#         db.create_all(app=app)
#         print("Database created successfully!")



# Query tests for the database
# with app.app_context():
#         db.create_all()
#         users = models.User.query.all()
#         for user in users:
#             print(user.email)
#             print(user.first_name)
#             print(user.last_name)
#             print('--------------------------------')