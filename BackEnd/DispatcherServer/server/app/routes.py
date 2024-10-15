from flask import Blueprint, render_template, redirect, url_for, request, flash, session ,jsonify,abort
from .extensions import db, bcrypt
from .models import User,Server
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo
from dotenv import load_dotenv
import os
import redis
import requests

bp = Blueprint('routes', __name__)

# Connect to Redis
redis_host = os.getenv('REDIS_HOST', 'redis')
redis_port = int(os.getenv('REDIS_PORT', 6379))
redis_client = redis.Redis(host=redis_host, port=redis_port, db=0)

SECRET_KEY = os.getenv('SECRET_KEY', 'default_secret_key')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class ChangePasswordForm(FlaskForm):
    new_email = StringField('New Email', validators=[Email()])
    old_password = PasswordField('Current Password', validators=[DataRequired()])
    new_password = PasswordField('New Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm New Password', validators=[DataRequired(), EqualTo('new_password')])
    submit = SubmitField('Change Password')

def login_required(f):
    from functools import wraps
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('routes.login'))
        return f(*args, **kwargs)
    return decorated_function

@bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password_hash, form.password.data):
            session['user_id'] = user.id
            flash('Login successful!', 'success')
            if ( user.password_change ) :
                return redirect(url_for('routes.index'))

            return redirect(url_for('routes.change_password'))
        else:
            flash('Login failed. Check your email and/or password.', 'danger')
    return render_template('login.html', form=form)

@bp.route('/change_password', methods=['GET', 'POST'])
@login_required
def change_password():
    form = ChangePasswordForm()
    if form.validate_on_submit():
        user = User.query.get(session['user_id'])
        if user and bcrypt.check_password_hash(user.password_hash, form.old_password.data):
            if form.new_email.data:
                user.email = form.new_email.data
            user.set_password(form.new_password.data)
            user.password_change = True

            db.session.commit()
            flash('Password updated successfully!', 'success')
            return redirect(url_for('routes.index'))
        else:
            flash('Current password is incorrect.', 'danger')
    return render_template('change_password.html', form=form)

@bp.route('/')
@login_required
def index():
    servers = Server.query.all()
    return render_template('index.html', servers=servers)

@bp.route('/logout')
def logout():
    session.pop('user_id', None)
    flash('You have been logged out.', 'info')
    return redirect(url_for('routes.login'))


@bp.route('/add_server', methods=['POST'])
@login_required
def add_server():
    address = request.form.get('address')
    port = request.form.get('port')
    if address:
        if Server.query.filter_by(address=address).first():
            flash('Server already exists.', 'warning')
        else:
            new_server = Server(address=address,port=port)
            db.session.add(new_server)
            db.session.commit()
            flash('Server added successfully.', 'success')
    else:
        flash('Invalid data.', 'danger')
    return redirect(url_for('routes.index'))

@bp.route('/remove_server/<int:id>', methods=['POST'])
@login_required
def remove_server(id):
    server = Server.query.get(id)
    if server:
        db.session.delete(server)
        db.session.commit()
        flash('Server deleted successfully.', 'success')
    else:
        flash('Server not found.', 'danger')
    return redirect(url_for('routes.index'))





def get_available_server():
    try:
        total_submissions = int(redis_client.get('total_submissions') or 0)
        servers = Server.query.all()
        if not servers:
            return None
        server_index = total_submissions % len(servers)
        selected_server = servers[server_index]
        return {'ip_address': selected_server.address,'port':selected_server.port}
    except Exception as e:
        print(f"Error selecting server: {e}")
        return None

@bp.route('/submit_question', methods=['POST'])
def submit_submissions():
    try:
        total_submissions = redis_client.incr('total_submissions')
        data = request.json
        print("data in dispacher ",data)
        required_fields = ['code', 'language', 'timeLimit', 'question', 'input', 'submissionId']

        if not all(field in data for field in required_fields):
            return jsonify({'error': 'Missing required fields'}), 400

        server = get_available_server()
        if not server:
            return jsonify({'error': 'No available servers'}), 500

        server_ip = server['ip_address']
        server_port = server['port']

        server_url = f"http://{server_ip}:{server_port}/core/submit/"  
        
        response = requests.post(server_url, json=data)
        json_response = response.json() 

        return jsonify({'msg': json_response.get('msg')}), response.status_code

    except Exception as e:
        return jsonify({'msg': str(e)}), 500