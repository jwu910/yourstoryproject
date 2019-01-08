from app import db
from werkzeug import check_password_hash, generate_password_hash
import datetime

class Account(db.Model):
    __tablename__   = 'account'

    id              = db.Column(db.Integer, primary_key=True, nullable=False)
    created_on      = db.Column(db.DateTime, default=datetime.datetime.utcnow, unique=False, nullable=False)
    email           = db.Column(db.String(120), index=True, unique=True, nullable=False)
    last_login      = db.Column(db.Date, unique=False, nullable=True)
    password_hash   = db.Column(db.String(128))
    username        = db.Column(db.String(48), index=True, unique=True, nullable=False)

    def __init__(self, email, last_login, password, username):
        """
        Class constructor
        """
        self.created_on = datetime.datetime.utcnow()
        self.email  = email.lower()
        self.last_login  = last_login
        self.set_password(password)
        self.username = username

    def set_password(self, password):
        self.password_hash   = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    @staticmethod
    def get_accounts():
        return Account.query.all()

    @staticmethod
    def get_account(id):
        return Account.query.get(id)

    def to_json(self):
        return {
            'id': self.id,
            'created_on': self.created_on,
            'email': self.email,
            'last_login': self.last_login,
            'username': self.username
        }

    def __repr__(self):
        return '<Account {}>'.format(self.username)
