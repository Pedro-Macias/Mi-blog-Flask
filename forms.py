from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, TextAreaField
from wtforms.validators import DataRequired, Email, Length

class FormularioRegistro(FlaskForm):
    nombre = StringField('Nombre', validators=[DataRequired(), Length(20)])
    email = StringField('Email', validators=[DataRequired(),Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit= SubmitField('Registrar')

class FormularioPost(FlaskForm):
    titulo = StringField('Titulo', validators=[DataRequired(), Length(20)])
    sub_titulo = StringField('Subtitulo', validators=[DataRequired(),Length(40)])
    contenido= TextAreaField('Contenido')
    submit= SubmitField('Enviar')    