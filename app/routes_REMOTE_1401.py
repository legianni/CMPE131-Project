from flask import render_template, flash, redirect, url_for
from app import app
from app import db
from app.forms import LoginForm
from app.forms import RegistrationForm
from app.forms import AddFriend
from app.forms import CreateEventForm
from app.forms import ScheduleForm
from app.models import User
from app.models import Event
from flask_login import current_user, login_user
from flask_login import logout_user
from flask_login import login_required
from flask import request
from werkzeug.urls import url_parse

@app.route('/')
def landingPage():
    return render_template('landingpage.html') 

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
    return render_template('index.html', title='Home', posts=posts, status=current_user.status)

# route to login
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

# route to logout
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

# route to register a user
@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data, status=True)
        db.create_all()
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route('/calendar')
def calendar():
    print("hello")
    return render_template('calendar.html')

# route to display friends
@app.route('/friends')
def friends():
    form = AddFriend()
    # to get all the users use the command
    # users = User.query.all()
    # for user in users:

    # display users in reverse alphabetical order
    # User.query.filter_by(User.username.desc()).all()
    return render_template('friends.html', form=form)

# route to view the events of a user
@app.route('/event/view', methods=['GET', 'POST'])
def viewEvent():
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    # to view all events of a select user
    events = current_user.events.all()
    return render_template('viewEvent.html', title='View Events', events=events)

# route to create an event
@app.route('/event/create', methods=['GET', 'POST'])
def createEvent():
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    form = CreateEventForm()
    if form.validate_on_submit():
        date_in = form.date.data.strftime('%m/%d/%Y')
        startTime_in = form.startTime.data.strftime('%H:%M')
        endTime_in = form.endTime.data.strftime('%H:%M')
        print(current_user)
        event = Event(author=current_user, title=form.title.data, description=form.description.data, date=date_in, startTime=startTime_in, endTime=endTime_in)
        db.create_all()
        db.session.add(event)
        db.session.commit()
        flash('Congratulations, you have created an event!')
        return redirect(url_for('index'))
    return render_template('createEvent.html', title='Create Event', form=form)

# route to display the schedule. users will be able to update their schedule here
@app.route('/schedule/create', methods=['GET', 'POST'])
def createSchedule():
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    form = ScheduleForm()
    if form.validate_on_submit():
        flash('Congratulations, you have updated your schedule!')
        return redirect(url_for('index'))
    user = User.query.filter_by(username=current_user.username).first()
    availability = user.schedule
    return render_template('createSchedule.html', title='Create Schedule', availability=availability, form=form)

# route used to update the schedule of a user. This uses AJAX calls to retrieve data from the template
@app.route('/update/schedule', methods=['GET', 'POST'])
def updateSchedule():
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    if request.method == 'POST':
        data = request.json
        new_schedule = str(data)
        user = User.query.filter_by(username=current_user.username).first()
        user.schedule = new_schedule 
        db.session.commit()
    return redirect(url_for('index'))

# route used to update the status of a user [BUSY = red or FREE = green]
@app.route('/update/status', methods=['GET', 'POST'])
def updateStatus():
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    user = User.query.filter_by(username=current_user.username).first()
    user.status = not user.status
    db.session.commit()
    print(user.status)
    flash('Congratulations, you have updated your status!')
    return redirect(url_for('index'))

# DELETION
# if you want to delete a user in the database do
# users = User.query.all()
# for u in users:
#   db.session.delete(u)