from flask import render_template,  redirect, url_for
from flask_login import current_user, login_required 

from  app.models import Post
from . import admin_bp
from .forms import FormularioPost

@admin_bp.route('/admin/post/', methods=['GET','POST'], defaults={'post_id':None})
@admin_bp.route('/admin/post/<int:post_id>/',methods=['GET','POST'])
@login_required
def post_form(post_id):
    form = FormularioPost()
    if form.validate_on_submit():
        titulo = form.titulo.data 
        contenido = form.contenido.data 

        post= Post(user_id=current_user.id, titulo =titulo, contenido=contenido)
        post.save()
        return redirect(url_for('public.index'))
    return render_template('admin/post_form.html',form=form)