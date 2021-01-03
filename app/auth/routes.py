from flask import render_template, redirect, url_for, request
from flask_login import current_user, login_user, logout_user
from werkzeug.urls import url_parse


from app import login_manager
from . import auth_bp
from .forms import FormularioRegistro, FormularioLogin
from .models import User

@auth_bp.route('/registrar/',methods=['GET','POST'])
def show_registro_users():
    if current_user.is_authenticated:
        return redirect(url_for('public.index'))
    form = FormularioRegistro()
    error = None
    if form.validate_on_submit():
        nombre = form.nombre.data
        email =  form.email.data 
        password = form.password.data 
        
        user = User.get_by_email(email)
        if user is not None:
            error =f'El Email {email} ya esta siendo utilizado '
        else:
            user = User(nombre=nombre, email=email)
            user.set_password(password)
            user.save()

            login_user(user,remember=True)
            next_page = request.args.get('next',None)
            if not next_page or url_parse(next_page).netloc != '':
                next_page = url_for('public.index')
            return redirect(next_page)
    return render_template('auth/registro_users.html', form=form, error=error)

@auth_bp.route('/login', methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('public.index'))
    form = FormularioLogin()
    if form.validate_on_submit():
        user = User.get_by_email(form.email.data)
        if user is not None and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            next_page = request.args.get('next')
            if not next_page or url_parse(next_page).netloc != '':
                next_page = url_for('public.index')
            return redirect(next_page)
    return render_template('auth/login_formulario.html',form=form)

@auth_bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('public.index'))

@login_manager.user_loader
def load_user(user_id):
    return User.get_by_id(int(user_id))


