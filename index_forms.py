from flask_wtf import FlaskForm
from wtforms import IntegerField
from wtforms.validators import InputRequired


class Menu(FlaskForm):
    width = IntegerField("Ширина поля", validators=[InputRequired()])
    height = IntegerField("Высота поля", validators=[InputRequired()])
