from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, TextAreaField, BooleanField
from wtforms.validators import DataRequired, Length

class FormularioPost(FlaskForm):
    titulo = StringField('Titulo', validators=[DataRequired(), Length(min=10, max=50)])
    contenido= TextAreaField('Contenido')
    submit= SubmitField('Enviar')