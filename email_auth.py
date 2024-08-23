import random
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user
from flask_mail import Message
from models import User
from app import db, mail

auth = Blueprint('auth', __name__)

def generate_code():
    return str(random.randint(100000, 999999))

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        user = User.query.filter_by(email=email).first()
        if not user:
            user = User(email=email)
            db.session.add(user)
            db.session.commit()
        
        code = generate_code()
        user.login_code = code
        user.code_expiry = datetime.utcnow() + timedelta(minutes=2)
        db.session.commit()

        msg = Message('Your Login Code', sender='your-email@example.com', recipients=[email])
        msg.body = f'Your login code is: {code}. This code will expire in 2 minutes.'
        mail.send(msg)

        return redirect(url_for('auth.verify_code', user_id=user.id))

    return render_template('login.html')

@auth.route('/verify_code/<int:user_id>', methods=['GET', 'POST'])
def verify_code(user_id):
    user = User.query.get(user_id)
    if request.method == 'POST':
        code = request.form['code']
        if user.login_code == code and datetime.utcnow() < user.code_expiry:
            login_user(user)
            return redirect(url_for('event_list'))
        else:
            flash('Invalid or expired code')
    
    return render_template('verify_code.html')