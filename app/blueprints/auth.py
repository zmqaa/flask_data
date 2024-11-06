from flask import Blueprint, render_template, session, redirect, url_for, flash
from flask_login import current_user, login_required, login_user, logout_user

from app.extensions import db
from app.models import User, File
from app.forms import LoginForm, RegisterForm

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            flash('登录成功')
            return redirect(url_for('main.index'))
        else:
            flash('用户或密码错误')
            return redirect(url_for('auth.login'))
    return render_template('login.html', form=form)

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            flash('用户名已被注册')
            return redirect(url_for('auth.register'))

        new_user = User(
            username = form.username.data,
            email = form.email.data
        )
        new_user.set_password(form.password.data)
        db.session.add(new_user)
        db.session.commit()
        flash('注册成功')
        return redirect(url_for('auth.login'))
    return render_template('register.html', form=form)

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('登出成功')
    return redirect(url_for('main.index'))

@auth_bp.route('/profile')
@login_required
def profile():
    user = User.query.filter_by(username=current_user.username).first()
    uploaded_files = File.query.filter_by(user_id=user.id).all()
    return render_template('profile.html', uploaded_files=uploaded_files)