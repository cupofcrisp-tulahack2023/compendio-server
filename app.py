from flask import Flask
from flask_bcrypt import Bcrypt
from flask_migrate import Migrate
from flask_login import LoginManager
from personalpage.views import personal_app
from database import db

login_manager = LoginManager()
login_manager.session_protection = "strong"
login_manager.login_view = "login"
login_manager.login_message_category = "info"



migrate = Migrate()
bcrypt = Bcrypt()


app = Flask(__name__)
app.register_blueprint(personal_app)
app.secret_key = 'secret-key'
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///database.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

login_manager.init_app(app)
db.init_app(app)
migrate.init_app(app, db)
bcrypt.init_app(app)

