from flask import Blueprint, request, redirect, url_for, flash, render_template, session, current_app
from werkzeug.security import generate_password_hash, check_password_hash
from app.model import User
from app import db
from itsdangerous import URLSafeTimedSerializer

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():

    if 'user_id' in session:
        return redirect(url_for('dashboard.dashboard'))
  
    if request.method == 'POST':
        email = request.form.get('email')
        email = email.lower().strip()
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()

        if  user is None or not check_password_hash(user.password, password):
            flash('Invalid email or password', "danger")
            return redirect(url_for('auth.login'))
        
        session['user_id'] = user.id
        flash('Logged in successfully!', "success")
        return redirect(url_for('dashboard.dashboard'))
    
    return render_template('login.html')

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if 'user_id' in session:
        return redirect(url_for('dashboard.dashboard'))

    if request.method == 'POST':
        email = request.form.get('email')
        email = email.lower().strip()
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')

        if password != confirm_password:
            flash('Passwords do not match', "danger")
            return redirect(url_for('auth.register'))   
        
        existing_user = User.query.filter_by(email=email).first()
        
        if existing_user:
            flash('Account already exist', "danger")
            return redirect(url_for('auth.register'))
        
        if len(password) < 6:
            flash("Password must be at least 6 characters", "danger")
            return redirect(url_for('auth.register'))
        
        # create new user
        hashed_password = generate_password_hash(password)    

        new_user = User(email=email, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        session['user_id'] = new_user.id

        flash('Account created successfully', "success")
        return redirect(url_for('auth.login'))
    
    return render_template('register.html')

@auth_bp.route("/logout")
def logout():
    session.pop('user_id', None)
    flash("Logout successfully", "success")
    return redirect(url_for('auth.login'))


@auth_bp.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    if 'user_id' in session:
        return redirect(url_for('dashboard.dashboard'))

    if request.method == 'POST':
        email = request.form.get('email')
        email = email.lower().strip()

        user = User.query.filter_by(email=email).first()

        if user:
            s = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
            token = s.dumps(user.email, salt='password-reset-salt')
            reset_url = url_for('auth.reset_password', token=token, _external=True)
            # In production, send this link via email. For now, flash it for convenience.
            flash(f'Password reset link: {reset_url}', 'info')
        else:
            # Don't reveal whether the email exists
            flash('If the email exists, a reset link has been sent', 'info')

        return redirect(url_for('auth.login'))

    return render_template('forgot_password.html')


@auth_bp.route('/reset-password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    try:
        s = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
        email = s.loads(token, salt='password-reset-salt', max_age=3600)
    except Exception:
        flash('The reset link is invalid or has expired', 'danger')
        return redirect(url_for('auth.login'))

    if request.method == 'POST':
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')

        if password != confirm_password:
            flash('Passwords do not match', 'danger')
            return redirect(url_for('auth.reset_password', token=token))

        if len(password) < 6:
            flash('Password must be at least 6 characters', 'danger')
            return redirect(url_for('auth.reset_password', token=token))

        user = User.query.filter_by(email=email).first()
        if not user:
            flash('User not found', 'danger')
            return redirect(url_for('auth.register'))

        user.password = generate_password_hash(password)
        db.session.commit()

        flash('Password has been reset. You can login now.', 'success')
        return redirect(url_for('auth.login'))

    return render_template('reset_password.html', token=token)