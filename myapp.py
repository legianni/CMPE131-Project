from flask import Flask
from flask import render_template
from form import LoginInput
from form import AddFriend


app = Flask(__name__)
app.config['SECRET_KEY'] = 'some-key'


@app.route('/calendar')
def calendar():
    return render_template('calendar.html')


@app.route('/login')
def login():
    form = LoginInput()
    return render_template('login.html', form=form)


@app.route('/friends')
def friends():
    form = AddFriend()
    return render_template('friends.html', form=form)


if __name__ == '__main__':
    app.run()
