from flask import Blueprint, request, jsonify, render_template, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from forms.auth_forms import RegistrationForm, LoginForm, ForgotPasswordForm, ResetPasswordForm
from models.user import User
from controllers.auth_controller import (
    register_user, 
    login_user as login_user_controller,
    send_reset_email,
    verify_reset_token,
    reset_user_password
)

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@auth_bp.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    form = ForgotPasswordForm()
    if form.validate_on_submit():
        try:
            send_reset_email(form.email.data)
            flash('📧 Reset instructions sent to your email.', 'info')
            return redirect(url_for('auth.login'))
        except Exception as e:
            flash(str(e), 'danger')
    return render_template('forgot_password.html', form=form)

@auth_bp.route('/reset-password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    user = verify_reset_token(token)
    if not user:
        flash('⛔ Invalid or expired token.', 'danger')
        return redirect(url_for('auth.forgot_password'))
    
    form = ResetPasswordForm()
    if form.validate_on_submit():
        try:
            reset_user_password(user, form.password.data)
            flash('✅ Password successfully reset. Please log in.', 'success')
            return redirect(url_for('auth.login'))
        except Exception as e:
            flash(str(e), 'danger')
    return render_template('reset_password.html', form=form)

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm(data=request.json) if request.is_json else RegistrationForm()

    if form.validate_on_submit():
        try:
            user_data = register_user(form)
            if request.is_json:
                return jsonify(user_data), 201
            flash('✅ Registration successful! Please log in.', 'success')
            return redirect(url_for('auth.login'))
        except Exception as e:
            if request.is_json:
                return jsonify({'error': str(e)}), 400
            flash(str(e), 'danger')

    return render_template('register.html', form=form)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm(data=request.json) if request.is_json else LoginForm()

    if form.validate_on_submit():
        try:
            login_data = login_user_controller(form)
            user = User.query.filter_by(email=form.email.data).first()
            login_user(user)
            flash('🎉 Login successful!', 'success')
            return redirect(url_for('dashboard'))
        except Exception as e:
            flash(str(e), 'danger')

    return render_template('login.html', form=form)

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('🔓 Logged out successfully.', 'info')
    return redirect(url_for('index'))
