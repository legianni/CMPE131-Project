from flask import render_template, flash, redirect, url_for
from app import app
from app import db
from app.forms import LoginForm
from app.forms import RegistrationForm
from app.forms import AddFriend
from app.forms import CreateEventForm
from app.models import User
from app.models import Event
from flask_login import current_user, login_user
from flask_login import logout_user
from flask_login import login_required
from flask import request
from werkzeug.urls import url_parse

@app.route('/')
@app.route('/index')
@login_required
def index():
    posts = [
        {
            'author': {'username': 'John'},
            'body': 'Beautiful day in Portland!'
        },
        {
            'author': {'username': 'Susan'},
            'body': 'The Avengers movie was so cool!'
        }
    ]
    return render_template('index.html', title='Home', posts=posts)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = LoginForm()
    if form.validate_on_submit():
        # look at first result first()
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        # return to page before user got asked to login
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')

        return redirect(next_page)
    return render_template('login.html', title='Sign in', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route('/calendar')
def calendar():
    return render_template('calendar.html')


@app.route('/friends')
def friends():
    form = AddFriend()
    return render_template('friends.html', form=form)

@app.route('/event/create', methods=['GET', 'POST'])
def createEvent():
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    form = CreateEventForm()
    if form.validate_on_submit():
        date_in = form.date.data.strftime('%Y/%m/%d')
        startTime_in = form.startTime.data.strftime('%H:%M:%S')
        endTime_in = form.endTime.data.strftime('%H:%M:%S')
        event = Event(title=form.title.data, description=form.description.data, date=date_in, startTime=startTime_in, endTime=endTime_in)
        db.create_all()
        db.session.add(event)
        db.session.commit()
        flash('Congratulations, you have created an event!')
        return redirect(url_for('index'))
    return render_template('createEvent.html', title='Create Event', form=form)