from db import db
import requests


class CityModel(db.Model):
    __tablename__ = 'cities'
    URL = "http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=fc33e01b4524acec78a01bc1f55826db"

    id = db.Column(db.Integer, primary_key=True)
    city_name = db.Column(db.String(80), nullable=False)

    def __init__(self, city_name):
        self.city_name = city_name

    @staticmethod
    def check_city_exists(city_name):
        return CityModel.query.filter_by(city_name=city_name).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def remove_from_db(self):
        db.session.delete(self)
        db.session.commit()

    @staticmethod
    def get_weather_data(city):
        r = requests.get(CityModel.URL.format(city)).json()
        return r

    @classmethod
    def check_city_valid(cls, city_name):
        if cls.get_weather_data(city_name)['cod'] == 200:
            return cls(city_name=city_name)

    @staticmethod
    def req_delete(city_name):
        rem = CityModel.query.filter_by(city_name=city_name).first()
        db.session.delete(rem)
        db.session.commit()

