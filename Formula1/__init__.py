import os 
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'f1_secret_key_123'
    
    
    basedir = os.path.abspath(os.path.dirname(__file__))
    
    db_path = os.path.join(os.path.dirname(basedir), 'f1_database.db')
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + db_path
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)

    login_manager.login_view = 'core.login'
    login_manager.login_message_category = 'info'

    
    from Formula1.models import User, Driver 

    from Formula1.core.routes import core
    from Formula1.driver.routes import driver
    app.register_blueprint(core)
    app.register_blueprint(driver)

    with app.app_context():
        db.create_all()

    return app