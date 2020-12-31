from flask import Flask, render_template, request, redirect, url_for, abort
from forms import FormularioRegistro, FormularioPost, FormularioLogin
from flask_login import LoginManager
from flask_login import current_user, login_user, logout_user , login_required 
from werkzeug.urls import url_parse
from flask_sqlalchemy import SQLAlchemy



app = Flask(__name__)

app.config['SECRET_KEY']='esta-sera-la-clave-secreta'

app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///miniblog.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

login_manager = LoginManager(app)
login_manager.login_view = "login"
db = SQLAlchemy(app)



#  ponemos las bases de datos
from flask_login import UserMixin
from slugify import slugify
from sqlalchemy.exc import IntegrityError
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model,UserMixin):
    
    __tablename__ = 'blog_user'

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(256), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    
    def __repr__(self):
        return f'<User {self.email}>'

    def set_password(self,password):
        self.password= generate_password_hash(password)
    
    def check_password(self,password):
        return check_password_hash(self.password, password)
    def save(self):
        if not self.id:
            db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_by_id(id):
        return User.query.get(id)
    @staticmethod
    def get_by_email(email):
        return User.query.filter_by(email=email).first()    



class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('blog_user.id', ondelete='CASCADE'), nullable=False)
    titulo = db.Column(db.String(256), nullable=False)
    sub_titulo = db.Column(db.String(256), unique=True, nullable=False)
    contenido = db.Column(db.Text)
    
    def __repr__(self):
        return f'<Post {self.titulo}>'
    
    def save(self):
        if not self.id:
            db.session.add(self)
        if not self.sub_titulo:
            self.sub_titulo = slugify(self.titulo)
        
        saved = False
        count = 0
        while not saved:
            try:
                db.session.commit()
                saved = True
            except IntegrityError:
                count += 1
                self.sub_titulo = f'{slugify(self.sub_titulo)}-{count}'
    
    def public_url(self):
        return url_for('mostrar_post', slug=self.sub_titulo)
    
    @staticmethod
    def get_by_slug(slug):
        return Post.query.filter_by(sub_titulo=slug).first()
    
    @staticmethod
    def get_all():
        return Post.query.all()





@app.route('/')
def index():
    posts = Post.get_all()
    return render_template("index.html", posts=posts)

@app.route('/p/<string:slug>')
def mostrar_post(slug):
    post = Post.get_by_slug(slug)
    if post is None:
        abort(404)
    return render_template('ver_post.html', post = post)


@app.route('/admin/post/', methods=['GET','POST'], defaults={'post_id':None})
@app.route('/admin/post/<int:post_id>/',methods=['GET','POST'])
@login_required
def post_form(post_id):
    form = FormularioPost()
    if form.validate_on_submit():
        titulo = form.titulo.data 
        contenido = form.contenido.data 

        post= Post(user_id=current_user.id, titulo =titulo, contenido=contenido)
        post.save()
        return redirect(url_for('index'))
    return render_template('admin/post_form.html',form=form)

@app.route('/registrar/',methods=['GET','POST'])
def show_registro_users():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
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
                next_page = url_for('index')
            return redirect(next_page)
    return render_template('registro_users.html', form=form, error=error)




@login_manager.user_loader
def load_user(user_id):
    return User.get_by_id(int(user_id))


# ponemos las rutas

@app.route('/login', methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = FormularioLogin()
    if form.validate_on_submit():
        user = User.get_by_email(form.email.data)
        if user is not None and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            next_page = request.args.get('next')
            if not next_page or url_parse(next_page).netloc != '':
                next_page = url_for('index')
            return redirect(next_page)
    return render_template('login_formulario.html',form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(port = 3000, debug = True)
    # http://localhost:3000