
from sqlalchemy.orm import validates
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy_serializer import SerializerMixin


from config import db, bcrypt


class User(db.Model, SerializerMixin):
    __tablename__ = 'users'

    serialize_rules = ('-recipes.user_id',)

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    _password_hash = db.Column(db.String)
    image_url = db.Column(db.String)
    bio = db.Column(db.String)

    recipes = db.relationship('Recipe', back_populates='user', cascade='all, delete-orphan')

    @validates('username')
    def validate_username(self, key, username):
        names = [user.username for user in User.query.all()]
        if username == '':
            raise ValueError('name invalid')
        elif username in names:
            raise ValueError('name is invalid')
        return username

    @hybrid_property
    def password_hash(self):
        raise AttributeError('Error no accessing password')

    @password_hash.setter
    def password_hash(self, password):
        # utf-8 encoding and decoding is required in python 3
        password_hash = bcrypt.generate_password_hash(
            password.encode('utf-8'))
        self._password_hash = password_hash.decode('utf-8')

    def authenticate(self, password):
        self._password_hash = bcrypt.generate_password_hash(password.encode('utf-8'))
        return bcrypt.check_password_hash(
            self._password_hash, password.encode('utf-8'))
    
    

    

class Recipe(db.Model, SerializerMixin):
    __tablename__ = 'recipes'

    serialize_rules = ('-user.recipes',)

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    instructions = db.Column(db.String, db.CheckConstraint('len(instructions) >= 50'), nullable=False)
    minutes_to_complete = db.Column(db.Integer)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    user = db.relationship('User', back_populates='recipes')

    @validates('instructions')
    def validate_instructions(self, key, instruction):
        if len(instruction) < 50:
            raise ValueError('Instructions too short')
        return instruction
   