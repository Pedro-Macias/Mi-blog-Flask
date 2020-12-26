from flask import Flask 
from flask import render_template

app = Flask(__name__)

posts = []

@app.route('/')
def index():
    return render_template('index.html',num_posts=len(posts))

@app.route('/p/<string:slug>')
def mostrar_post(slug):
    return render_template('ver_post.html',slug_tittle=slug)


@app.route('/admin/post/')
@app.route('/admin/post/<int:post_id>/')
def post_form(post_id=None):
    return render_template('admin/post_form.html',post_id=post_id)



if __name__ == '__main__':
    app.run(port = 3000, debug = True)
    # http://localhost:3000