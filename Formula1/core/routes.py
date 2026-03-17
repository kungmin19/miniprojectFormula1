from flask import Blueprint, render_template, request, redirect, url_for, flash
from Formula1.models import db, User
from Formula1 import bcrypt
from flask_login import login_user, logout_user, current_user

core = Blueprint('core', __name__, template_folder='templates')

@core.route('/')
def index():
    return render_template('index.html')

@core.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('core.index'))
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        
        if User.query.filter_by(username=username).first():
            flash('ชื่อผู้ใช้ซ้ำ', 'danger')
        elif User.query.filter_by(email=email).first():
            flash('อีเมลนี้ถูกใช้ไปแล้ว', 'danger')
        else:
            hashed_pw = bcrypt.generate_password_hash(password).decode('utf-8')
            new_user = User(username=username, email=email, password=hashed_pw)
            db.session.add(new_user)
            db.session.commit()
            flash('สมัครสมาชิกสำเร็จ!', 'success')
            return redirect(url_for('core.login'))
    return render_template('register.html')

@core.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = User.query.filter_by(username=request.form.get('username')).first()
        if user and bcrypt.check_password_hash(user.password, request.form.get('password')):
            login_user(user)
            return redirect(url_for('core.index'))
        flash('เข้าสู่ระบบไม่สำเร็จ', 'danger')
    return render_template('login.html')

@core.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('core.index'))