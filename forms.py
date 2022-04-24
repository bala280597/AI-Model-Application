from flask_wtf import FlaskForm
from wtforms import SubmitField, SelectField, IntegerField,FloatField
from wtforms.validators import DataRequired, NumberRange


class HouseForm(FlaskForm):
    Avg_Area_Income = FloatField(label='Area Income', validators=[DataRequired()])
    Avg_Area_House_Age = FloatField(label='House Age', validators=[DataRequired()])
    Avg_Area_Number_of_Rooms = FloatField(label='Number of Rooms', validators=[DataRequired()])
    Avg_Area_Number_of_Bedrooms = FloatField(label='Bedrooms', validators=[DataRequired()])
    Area_Population = FloatField(label='Population', validators=[DataRequired()])
    predict = SubmitField('Predict!')