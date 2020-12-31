from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, TextAreaField, BooleanField
from wtforms.validators import DataRequired, Email, Length

class FormularioRegistro(FlaskForm):
    nombre = StringField('Nombre', validators=[DataRequired(), Length(min=5, max=20)])
    email = StringField('Email', validators=[DataRequired(),Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit= SubmitField('Registrar')

class FormularioPost(FlaskForm):
    titulo = StringField('Titulo', validators=[DataRequired(), Length(min=10, max=50)])
    contenido= TextAreaField('Contenido')
    submit= SubmitField('Enviar')

class FormularioLogin(FlaskForm):
    email = StringField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Recuérdame')
    submit = SubmitField('Login')    
