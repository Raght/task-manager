from flask import Blueprint, render_template, request, session, redirect, url_for, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required, current_user
from ...model.Users import Users
from ...extensions import db, login_manager
from ...services.UserService import UserService

auth_bp = Blueprint('auth', __name__, static_folder='../../static', template_folder='../../templates')
login_manager.login_view = 'auth.login'
login_manager.login_message = 'Log in required.'


def session_login():
    session['name'] = current_user.name
    session['email'] = current_user.email
    session['logged_in'] = True

def session_logout():
    session['logged_in'] = False
    session['name'] = None

@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        email = request.form.get('email')
        
        if Users.query.filter_by(name=username).first():
            flash('Username already taken', category='error')
            return render_template('register.html')
        if Users.query.filter_by(email=email).first():
            flash('Email already taken', category='error')
            return render_template('register.html')

        password_hash = generate_password_hash(password, method='pbkdf2:sha256')

        new_user = Users(name=username, passwordHash=password_hash, email=email)
        db.session.add(new_user)
        db.session.commit()

        login_user(new_user)
        session_login()

        flash('Register successful.', category='success')
        return redirect(url_for('index'))

    return render_template('register.html')


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = Users.query.filter_by(name=username).first()

        if user and check_password_hash(user.passwordHash, password):
            login_user(user)
            session_login()

            flash('You have successfully logged in.', category='success')
            return redirect(url_for('index'))
        else:
            flash('Invalid username or password.', category='error')
            return render_template('login.html')

    return render_template('login.html')


@auth_bp.route('/profile')
@auth_bp.route('/profile/<int:user_id>')
def profile(user_id=None):
    if user_id is None:
        if not current_user.is_authenticated:
            flash('Select a user profile or log in.', category='error')
            return redirect(url_for('auth.login'))
        user_id = current_user.id

    try:
        user = UserService.get_user(user_id)
    except ValueError as e:
        flash(str(e), category='error')
        return redirect(url_for('index'))

    is_own_profile = current_user.is_authenticated and current_user.id == user.id
    return render_template('profile.html', user=user, is_own_profile=is_own_profile)


@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    session_logout()
    flash('You have successfully logged out.', category='success')
    return redirect(url_for('index'))