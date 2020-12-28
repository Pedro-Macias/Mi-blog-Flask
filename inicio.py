from flask import Flask 
from flask import render_template
from flask import request, redirect, url_for
from forms import FormularioRegistro, FormularioPost
app = Flask(__name__)

app.config['SECRET_KEY']='esta-sera-la-clave-secreta'

posts = []

@app.route('/')
def index():
    return render_template('index.html',posts=posts)

@app.route('/p/<string:slug>')
def mostrar_post(slug):
    return render_template('ver_post.html',slug_tittle=slug)


@app.route('/admin/post/', methods=['GET','POST'], defaults={'post_id':None})
@app.route('/admin/post/<int:post_id>/',methods=['GET','POST'])
def post_form(post_id):
    form = FormularioPost()
    if form.validate_on_submit():
        titulo = form.titulo.data 
        sub_titulo = form.sub_titulo.data 
        contenido = form.contenido.data 

        post={'titulo':titulo, 'sub_titulo':sub_titulo, 'contenido':contenido}
        posts.append(post)
        return redirect(url_for('index'))
    return render_template('admin/post_form.html',form=form)

@app.route('/registrar/',methods=['GET','POST'])
def show_registro_users():
    form = FormularioRegistro()
    if form.validate_on_submit():
        nombre = form.nombre.data
        email =  form.email.data 
        password = form.password.data 
        
        next = request.args.get('next',None)
        if next:
            return redirect(next)
        return redirect(url_for('index'))
    return render_template('registro_users.html',form=form)

if __name__ == '__main__':
    app.run(port = 3000, debug = True)
    # http://localhost:3000