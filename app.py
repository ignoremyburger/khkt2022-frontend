from flask import Flask
from flask_login import LoginManager

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///database.db"
app.config['SECRET_KEY'] = "QUD0QHB282"

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"