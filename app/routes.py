from flask import render_template, flash, redirect, url_for
from app import app
from app import db
from app.forms import LoginForm
from app.forms import RegistrationForm
from app.forms import AddFriend
from app.forms import CreateEventForm
from app.forms import EditEventForm
from app.forms import DeleteEventForm
from app.forms import ScheduleForm
from app.models import FriendRequest
from app.models import User
from app.models import Event
from app.models import Friend
from flask_login import current_user, login_user
from flask_login import logout_user
from flask_login import login_required
from flask import request
from werkzeug.urls import url_parse
import ast


@app.route('/')
def landingPage():
    return render_template('landingpage.html')


@app.route('/index')
@login_required
def index():
    # get all the friends of current user
    friends = current_user.friends.all()
    friendArr = []
    for friend in friends:
        user = User.query.filter_by(username=friend.friend_username).first()
        friendArr.append([friend.friend_username, user.status])
    return render_template('index.html', title='Home', status=current_user.status, friends=friendArr)

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
        user = User(username=form.username.data,
                    email=form.email.data, status=True)
        db.create_all()
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route('/calendar')
def calendar():
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    # to view all events of a select user
    events = current_user.events.all()

    return render_template('calendar.html', title='View Events', events=events)

# route to display friends
@app.route('/friends', methods=['GET', 'POST'])
def friends():
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    form = AddFriend()
    sentFriendRequest = False
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            # checks if this user is already a friend
            listOfFriends = Friend.query.filter_by(
                user_id=current_user.id).all()
            print(listOfFriends)
            isFriend = False
            for friend in listOfFriends:
                if friend.friend_username == user.username:
                    isFriend = True
            # checks if friend request has already been sent
            checkFriendRequest = FriendRequest.query.filter_by(
                requester_username=user.username).all()
            for friend in checkFriendRequest:
                if friend.friend_username == current_user.username:
                    sentFriendRequest = True
        # if all cases are valid
        if user and user != current_user:
            if isFriend:
                flash('Error. You are already friends with ' + user.username + '!')
                return redirect(url_for('friends'))
            elif sentFriendRequest:
                flash(
                    'Error. You have already sent a friend request to ' + user.username + '!')
                return redirect(url_for('friends'))
            else:
                friend_request = FriendRequest(
                    author=user, requester_username=user.username, friend_username=current_user.username, request_status=True)
                db.create_all()
                db.session.add(friend_request)
                db.session.commit()
                flash('You sent a friend request to ' + user.username + '!')
                return redirect(url_for('friends'))
        else:
            flash('Error. Please enter a valid username.')
            return redirect(url_for('friends'))

    # get all incoming friend requests
    friend_requests = current_user.friend_request.filter_by(
        requester_username=current_user.username).all()
    friendReq = []
    for friend in friend_requests:
        if friend.request_status:
            friendReq.append(friend.friend_username)
    print(friendReq)
    return render_template('friends.html', form=form, friends=friendReq)

# route to accept/decline friend request
@app.route('/friends/request', methods=['GET', 'POST'])
def updateFriendRequest():
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    if request.method == 'POST':
        data = request.json
        req_data = str(data).split('-')
        print("here")
        print(req_data)
        # update friends & friend request
        friendReq = FriendRequest.query.filter_by(
            requester_username=current_user.username).all()
        for friend in friendReq:
            if friend.requester_username == current_user.username and friend.friend_username == req_data[0]:
                print(friend.friend_username)
                db.session.delete(friend)
                db.session.commit()
        if req_data[1] == 'accept':
            friend = Friend(author=current_user, friend_username=req_data[0])
            temp_friend = User.query.filter_by(username=req_data[0]).all()
            friend = Friend(
                author=temp_friend[0], friend_username=current_user.username)
            db.create_all()
            db.session.add(friend)
            db.session.commit()
            flash('You have accepted ' + req_data[0] + "'s friend request!")
            return redirect(url_for('index'))
        flash('You have declined ' + req_data[0] + "'s friend request!")
    return redirect(url_for('index'))

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
        event = Event(author=current_user, title=form.title.data, description=form.description.data,
                      date=date_in, startTime=startTime_in, endTime=endTime_in)
        db.create_all()
        db.session.add(event)
        db.session.commit()
        flash('Congratulations, you have created an event!')
        return redirect(url_for('viewEvent'))
    return render_template('createEvent.html', title='Create Event', form=form)

# route to edit event
@app.route('/event/edit/<string:id>', methods=['GET','POST'])
def editEvent(id):
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    
    form = EditEventForm()
    if form.validate_on_submit():        
        date_in = form.date.data.strftime('%m/%d/%Y')
        startTime_in = form.startTime.data.strftime('%H:%M')
        endTime_in = form.endTime.data.strftime('%H:%M')
        print(current_user)
        event = Event.query.filter_by(id = id).join(User).filter_by(username=current_user.username).first()
        event.title = form.title.data
        event.description = form.description.data
        event.date = date_in
        event.startTime = startTime_in
        event.endTime = endTime_in
        db.session.commit()
        flash('Event edited')
        return redirect(url_for('viewEvent'))
    return render_template('editEvent.html', title='Edit Event', form=form)

# route to delete an event
@app.route('/event/delete/<int:id>', methods=['GET', 'POST'])
def deleteEvent(id):
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    event = Event.query.filter_by(id=id).first()
    db.session.delete(event)
    db.session.commit()
    flash('Event deleted')
    return redirect(url_for('viewEvent'))

# route to display the schedule. users will be able to update their schedule here
@app.route('/schedule/create', methods=['GET', 'POST'])
def createSchedule():
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    form = ScheduleForm()
    if form.validate_on_submit():
        flash('Congratulations, you have updated your schedule!')
        return redirect(url_for('createSchedule'))
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

# route used to retrieve schedule of a user
@app.route('/get/schedule/<string:user>', methods=['GET'])
def getSchedule(user):
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    if request.method == 'GET':
        user = User.query.filter_by(username=user).first()
        return user.schedule

# route used to update the status of a user [BUSY = red or FREE = green]
@app.route('/update/status', methods=['GET', 'POST'])
def updateStatus():
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    user = User.query.filter_by(username=current_user.username).first()
    user.status = not user.status
    db.session.commit()
    print(user.status)
    return redirect(url_for('index'))

# DELETION
# if you want to delete a user in the database do
# users = User.query.all()
# for u in users:
#   db.session.delete(u)
