from flask import Blueprint, render_template, request, redirect, url_for, flash
import requests
from models.city import CityModel

weather_blueprint = Blueprint('weather', __name__)


@weather_blueprint.route('/')
@weather_blueprint.route('/index')
def index_get():
    cities = CityModel.query.all()

    url = "http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=fc33e01b4524acec78a01bc1f55826db"

    weather_data = []

    for city in cities:
        r = requests.get(url.format(city.city_name)).json()

        weather = {
            'city': city.city_name,
            'temperature': r['main']['temp'],
            'description': r['weather'][0]['description'],
            'icon': r['weather'][0]['icon']
        }

        weather_data.append(weather)

    return render_template('weather.html', weather_data=weather_data)


@weather_blueprint.route('/', methods=['POST'])
@weather_blueprint.route('/index', methods=['POST'])
def index_post():
    new_city = request.form['city_name']

    # prevent blank
    if new_city:
        city_exists = CityModel.check_city_exists(new_city)

        if not city_exists:
            new_city_obj = CityModel.check_city_valid(new_city)
            if new_city_obj:
                new_city_obj.save_to_db()
            else:
                flash("This city does not exist!", "error")
        else:
            flash("This city is already shown!", "error")

        flash("City has been successfully added!", "info")

    return redirect(url_for('weather.index_get'))


@weather_blueprint.route('/delete/<string:name>')
def delete_city(name):
    CityModel.req_delete(name)
    return redirect(url_for('weather.index_get'))
