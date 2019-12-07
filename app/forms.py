from flask_wtf import FlaskForm
from datetime import date
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField
from wtforms_components import TimeField, DateField, DateRange, DateTimeField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from app.models import User

class LoginForm(FlaskForm):
    """
    Input forms used on the login page.
    """
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember')
    submit = SubmitField('Sign In')

class CreateEventForm(FlaskForm):
    """
    Input forms used on the event page.
    """
    title = StringField('Title', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    date = DateField('Date', validators=[DataRequired(), DateRange(min=date.today())])
    startTime = TimeField('Start Time', validators=[DataRequired()])
    endTime = TimeField('End Time', validators=[DataRequired()])
    submit = SubmitField('Create Event')
    
class EditEventForm(FlaskForm):
    """
    Input forms used on the edit event page.
    """
    title = StringField('Title', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    date = DateField('Date', validators=[DataRequired(), DateRange(min=date.today())])
    startTime = TimeField('Start Time', validators=[DataRequired()])
    endTime = TimeField('End Time', validators=[DataRequired()])
    submit = SubmitField('Edit Event')

class DeleteEventForm(FlaskForm):
    """
    Input form used to delete an event.
    """
    title = StringField('Title', validators=[DataRequired()], description="Enter Event to Delete")
    submit = SubmitField('Delete Event')

class AddFriend(FlaskForm):
    """
    Input form used to add a friend.
    """
    username = StringField('Username', validators=[DataRequired()], description="Enter Friends Username")
    search = SubmitField('Add')

class RegistrationForm(FlaskForm):
    """
    Input form used on registration page
    """
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')

class ScheduleForm(FlaskForm):
    """
    Submit button used on the schedule page.
    """
    submit = SubmitField("Submit")