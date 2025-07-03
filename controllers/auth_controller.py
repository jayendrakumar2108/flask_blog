from flask import url_for, current_app
from flask_mail import Message
from flask_jwt_extended import create_access_token
from models.user import User
from extensions import mail, db

def send_reset_email(email):
    user = User.query.filter_by(email=email).first()
    if not user:
        raise Exception("No account with that email.")
    
    token = user.get_reset_token()
    reset_url = url_for('auth.reset_password', token=token, _external=True)

    msg = Message(
        subject='🛡️ BlogiVerse - Reset Your Password',
        sender=current_app.config['MAIL_DEFAULT_SENDER'],
        recipients=[email]
    )

    msg.body = f'''
Hi {user.username},

We received a request to reset your password for your BlogiVerse account.

To reset your password, please click the link below:

{reset_url}

If you did not request a password reset, just ignore this email. This link will expire in 30 minutes.

– The BlogiVerse Team
'''

    msg.html = f'''
<p>Hi <b>{user.username}</b>,</p>
<p>We received a request to reset your password for your <b>BlogiVerse</b> account.</p>
<p>
    <a href="{reset_url}" style="padding:10px 20px; background:#007bff; color:white; text-decoration:none; border-radius:5px;">
        🔐 Reset Your Password
    </a>
</p>
<p>If you didn’t make this request, you can ignore this email.</p>
<p><small>This link will expire in <b>30 minutes</b>.</small></p>
<p>– The BlogiVerse Team</p>
'''

    mail.send(msg)

def verify_reset_token(token, expires_sec=1800):
    return User.verify_reset_token(token, expires_sec)

def reset_user_password(user, new_password):
    user.set_password(new_password)
    db.session.commit()

def register_user(form):
    if User.query.filter_by(email=form.email.data).first():
        raise Exception('Email already in use')
    if User.query.filter_by(username=form.username.data).first():
        raise Exception('Username already in use')

    role = form.role.data
    if role == 'admin' and form.email.data != 'admin@blogiverse.com':
        raise Exception('Unauthorized attempt to register as admin.')

    user = User(
        username=form.username.data,
        email=form.email.data,
        role=role
    )
    user.set_password(form.password.data)
    db.session.add(user)
    db.session.commit()
    return user.to_dict()


def login_user(form):
    user = User.query.filter_by(email=form.email.data).first()
    if not user or not user.check_password(form.password.data):
        raise Exception('Invalid email or password')
    if not user.is_active:
        raise Exception('Account is deactivated')

    access_token = create_access_token(identity=user.id, additional_claims={"roles": [user.role]})
    return {
        'access_token': access_token,
        'user': user.to_dict()
    }
