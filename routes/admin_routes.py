from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from models.user import User, db
from utils.decorators import admin_required
from werkzeug.security import generate_password_hash
import json

admin_bp = Blueprint('admin_bp', __name__, url_prefix='/admin')

@admin_bp.route('/users')
@login_required
@admin_required
def manage_users():
    users = User.query.all()
    # เตรียม permissions ที่เป็น object
    user_data = []
    for user in users:
        try:
            perms = json.loads(user.permissions or '{}')
        except:
            perms = {}
        user_data.append({
            'id': user.id,
            'username': user.username,
            'role': user.role,
            'permissions': perms,
            'recent_page': user.recent_page
        })

    return render_template('admin_users.html', users=user_data)

@admin_bp.route('/add_user', methods=['GET', 'POST'])
@login_required
@admin_required
def add_user():
    if request.method == 'POST':
        hashed = generate_password_hash(request.form['password'], method='pbkdf2:sha256')
        new_user = User(
            username=request.form['username'],
            password=hashed,
            role=request.form['role']
        )
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('admin_bp.manage_users'))
    return render_template('add_user.html')

@admin_bp.route('/delete_user/<int:id>')
@login_required
@admin_required
def delete_user(id):  #????
    user = User.query.get_or_404(id)
    if user.id == current_user.id:
        flash("You can't delete yourself.")
        return redirect(url_for('admin_bp.manage_users'))
    db.session.delete(user)
    db.session.commit()
    flash("User deleted successfully.")
    return redirect(url_for('admin_bp.manage_users'))

@admin_bp.route('/edit_permissions/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_permissions(id):
    user = User.query.get_or_404(id)
    if request.method == 'POST':
        # รับค่าจาก checkbox form
        permissions = {
            'index': 'index' in request.form,
            'dashboard': 'dashboard' in request.form,
            'admin_users': 'admin_users' in request.form,
            'logout': 'logout' in request.form
        }
        user.permissions = json.dumps(permissions)
        db.session.commit()
        flash("Permissions updated.")
        return redirect(url_for('admin_bp.manage_users'))
    current_perms = json.loads(user.permissions or '{}')
    return render_template('edit_permissions.html', user=user, perms=current_perms)

