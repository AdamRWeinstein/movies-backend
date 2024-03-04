from extensions import db, bcrypt
from flask_login import UserMixin

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))

    # Relationships
    reviews = db.relationship('Review', backref='author', lazy='dynamic')
    favorites = db.relationship('Favorite', backref='user', lazy='dynamic')

    # Methods for setting and verifying password would go here (using Werkzeug or similar)
    @classmethod
    def register_user(cls, username, email, password):
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        user = cls(username=username, email=email, password_hash=hashed_password)
        db.session.add(user)
        db.session.commit()

    @classmethod
    def authenticate_user(cls, email, password):
        user = cls.query.filter_by(email=email).first()
        if user and bcrypt.check_password_hash(user.password_hash, password):
            return user
        return None

class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    sentiment = db.Column(db.String(3))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    movie_id = db.Column(db.Integer, db.ForeignKey('movie.id'), nullable=False)

class Favorite(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    movie_id = db.Column(db.Integer, db.ForeignKey('movie.id'), nullable=False)

    # Unique constraint to ensure a user can't favorite the same movie multiple times
    __table_args__ = (db.UniqueConstraint('user_id', 'movie_id', name='_user_movie_uc'),)