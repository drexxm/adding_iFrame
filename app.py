from flask import Flask, redirect, url_for, render_template, request
from config import Config
from models import db
from models.user import User
from models.task import Task
from routes.auth_routes import auth
from routes.task_routes import task_bp
from flask_login import LoginManager, current_user
from routes.admin_routes import admin_bp
from flask_migrate import Migrate
from urllib.parse import urlparse

app = Flask(__name__)
app.config.from_object('config.Config')

# ✅ Bind SQLAlchemy กับ app
db.init_app(app)

# หลังจาก db.init_app(app)
migrate = Migrate(app, db)

# ✅ Login Manager
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# ✅ Register Blueprints
app.register_blueprint(auth)
app.register_blueprint(task_bp)
app.register_blueprint(admin_bp)

with app.app_context():
    db.create_all()

@app.before_request
def track_user_page():
    if current_user.is_authenticated:
        path = request.path

        # ✅ เงื่อนไขกันไม่ให้บันทึกเฉพาะพวก static หรือ auth/logout/login
        skip_paths = ['/logout', '/login', '/register', '/static']
        if not any(path.startswith(skip) for skip in skip_paths):
            # ไม่เก็บ query string, เฉพาะ path
            current_user.recent_page = path
            db.session.commit()

@app.route('/')
def home():
    # return render_template("base.html") 
    if current_user.is_authenticated:
        return redirect(url_for('task_bp.index'))
    else:
        return redirect(url_for('auth.login'))