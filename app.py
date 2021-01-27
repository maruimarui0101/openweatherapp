from flask import Flask, render_template
from db import db
from app_blueprints import weather_blueprint
import os
from models.city import CityModel


app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///weather.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# for message flashing
app.config['SECRET_KEY'] = 'secretkey'
app.register_blueprint(weather_blueprint)


@app.before_first_request
def create_tables():
    db.create_all()


if __name__ == "__main__":
    db.init_app(app)
    app.run(host="0.0.0.0", port=8080)
