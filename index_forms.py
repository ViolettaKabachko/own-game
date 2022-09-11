from flask_wtf import FlaskForm
from wtforms import IntegerField
from wtforms.validators import InputRequired, NumberRange


class Menu(FlaskForm):
    width = IntegerField("Ширина поля", validators=[InputRequired(), NumberRange(min=3, max=30)])
    height = IntegerField("Высота поля", validators=[InputRequired(), NumberRange(min=3, max=30)])
