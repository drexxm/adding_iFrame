from flask import Blueprint, render_template, request, redirect, url_for, flash
from models.user import User, db
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from urllib.parse import urlparse, urljoin

auth = Blueprint('auth', __name__)

def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and ref_url.netloc == test_url.netloc

@auth.route('/login', methods=['GET', 'POST'])
def login():
    next_page = request.args.get('next') or request.form.get('next')  # ✅ get next
    if request.method == 'POST':
        user = User.query.filter_by(username=request.form['username']).first()
        if user and check_password_hash(user.password, request.form['password']):
            login_user(user)
            if user.role == 'admin':
                flash("👑 Welcome, admin!")
                return redirect(url_for('admin_bp.manage_users')) 
            # ✅ Redirect to next if safe
            if next_page and is_safe_url(next_page):
                return redirect(next_page)
            flash(f"Welcome back, {user.username}!")
            return redirect(url_for('task_bp.index'))
        flash('Invalid credentials')
    return render_template('login.html')

@auth.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        hashed_pw = generate_password_hash(request.form['password'], 
                                           method='pbkdf2:sha256', 
                                           salt_length=8)
        new_user = User(username=request.form['username'], password=hashed_pw)
        db.session.add(new_user)
        db.session.commit()
        flash('Registration successful! Please login.')
        return redirect(url_for('auth.login'))
    return render_template('register.html')

@auth.route('/logout')
@login_required
def logout():
    current_user.recent_page = request.referrer  # หรือใส่จาก session
    db.session.commit()
    logout_user()
    return redirect(url_for('auth.login'))
