from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from models import db
import json

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

    # 🆔 Role ('user', 'admin')
    role = db.Column(db.String(10), default='user')

    # ✅ สิทธิ์หน้าแบบ object json
    permissions = db.Column(db.Text, default=json.dumps({
        "index": True,
        "dashboard": True,
        "admin_users": False,
        "logout": True
    }))

    # ✅ เก็บหน้าสุดท้ายที่เข้าก่อน logout
    recent_page = db.Column(db.String(100), nullable=True)