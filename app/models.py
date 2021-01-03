from flask import url_for
from slugify import slugify
from sqlalchemy.exc import IntegrityError

from app import db

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
        return url_for('public.show_post', slug=self.sub_titulo)
    
    @staticmethod
    def get_by_slug(slug):
        return Post.query.filter_by(sub_titulo=slug).first()
    
    @staticmethod
    def get_all():
        return Post.query.all()
