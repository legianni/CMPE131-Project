from flask import Flask
from flask import render_template

# uncomment line below once you have created the
# TopCities class inside the form.py file
from form import TopCities

app = Flask(__name__)
app.config['SECRET_KEY'] = 'some-key'


@app.route('/')
def home():
    name = 'Calvin'
    top_cities = ['Paris', 'London', 'Rome', 'Tahiti']
    title = 'Top Cities'
    form = TopCities()
    return render_template('home.html', title=title, name=name, top_cities=top_cities, form=form)


if __name__ == '__main__':
    app.run()
