from flask import Flask

def create_app():
    app = Flask(__name__)
    app.config['SECRET-KEY'] = 'this is a secret key for encrypt my cookies and session data related to my website'
    
    from .views import views 
    from .auth import auth 
    
    app.register_blueprint(views, url_prefix = "/")
    app.register_blueprint(auth, url_prefix = "/")
    
    return app