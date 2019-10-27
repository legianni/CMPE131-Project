from flask import Flask
rt Flask
from flask import render_template
import calendar


prmonthVal = calendar.calendar(2019,2,1,6)

myCal = calendar.HTMLCalendar(calendar.SUNDAY)
htmlValue = myCal.formatmonth(2009, 7)

myFlaskObj = Flask(__name__)

@myFlaskObj.route('/')
def hello():
    return render_template('index.html', htmlValue=htmlValue, prmonthVal = prmonthVal)
