from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, IntegerField


class TopCities(FlaskForm):
    city_name = StringField('City Name')
    city_rank = IntegerField('City Rank')
    is_visited = BooleanField('Visited')
    comments = StringField('Comments')
    submit = SubmitField('Submit')
