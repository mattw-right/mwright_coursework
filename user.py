'''
class User():
    '''The User class, which allows for the username and password to be set and checked. It can be loaded from and into
    the central database'''

    def set_username(self, username):
        '''Validates and sets the username'''
        if validate_username(username):
            self.username = username
        else:
            raise('That username is not valid, check validate.py for the validation rules')

    def set_password(self, password):
        '''Validates and sets the password'''
        if validate_password(password):
            self.hash = generate_password_hash(password)
        else:
            raise ('That password is not valid, check validate.py for the validation rules')

    def check_password(self, password_to_be_checked):
        '''Checks the hash of the password against the hash stored for the user'''
        return check_password_hash(self.hash, password_to_be_checked)

'''
from flask.ext.sqlalchemy import SQLAlchemy

db = SQLAlchemy()

#...

class User(db.Model):
    """An admin user capable of viewing reports.

    :param str email: email address of user
    :param str password: encrypted password for the user

    """
    __tablename__ = 'user'

    email = db.Column(db.String, primary_key=True)
    password = db.Column(db.String)
    authenticated = db.Column(db.Boolean, default=False)

    def is_active(self):
        """True, as all users are active."""
        return True

    def get_id(self):
        """Return the email address to satisfy Flask-Login's requirements."""
        return self.email

    def is_authenticated(self):
        """Return True if the user is authenticated."""
        return self.authenticated

    def is_anonymous(self):
        """False, as anonymous users aren't supported."""
        return False
