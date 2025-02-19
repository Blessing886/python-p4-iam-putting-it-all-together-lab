from sqlalchemy.orm import validates, relationship
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy_serializer import SerializerMixin
from config import db, bcrypt

class User(db.Model, SerializerMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    _password_hash = db.Column(db.String, nullable=False)
    image_url = db.Column(db.String, default="https://example.com/default-profile.png")
    bio = db.Column(db.String, default="This user has no bio.")


    recipes = relationship('Recipe', backref='user', lazy=True, cascade="all, delete-orphan")

    @hybrid_property
    def password_hash(self):
        raise AttributeError("Password hash is not accessible.")

    @password_hash.setter
    def password_hash(self, password):
        if not password or len(password.strip()) == 0:
            raise ValueError("Password cannot be empty.")
        self._password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

    @validates('username')
    def validate_username(self, key, username):
        if not username:
            raise ValueError("Username must be present.")
        return username

class Recipe(db.Model, SerializerMixin):
    __tablename__ = 'recipes'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    instructions = db.Column(db.String, nullable=False)
    minutes_to_complete = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    @validates('title')
    def validate_title(self, key, title):
        if not title:
            raise ValueError("Title must be present.")
        return title

    @validates('instructions')
    def validate_instructions(self, key, instructions):
        if not instructions or len(instructions) < 50:
            raise ValueError("Instructions must be at least 50 characters long.")
        return instructions