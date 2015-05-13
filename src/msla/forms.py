from flask.ext.wtf import Form
from flask import session
from wtforms import TextField, PasswordField, BooleanField, SubmitField, validators
from msla import db
from .models import Users
from passlib.hash import bcrypt_sha256
from .utils import sha512
import os

class LoginForm(Form):
	user = TextField('User',[validators.DataRequired('Please provide a valid user.')])
	password = PasswordField('Password', [validators.DataRequired(), validators.Length(min=8, message=(u'Please give a longer password'))])
	submit = SubmitField("Login")

	def __init__(self, *args, **kwargs):
		Form.__init__(self, *args, **kwargs)

	def validate(self):
		if not Form.validate(self):
			return False
	
		user = Users.query.filter_by(user = self.user.data).first()
		if user and bcrypt_sha256.verify(self.password.data, user.password):
			try:
				session.regenerate() # NO SESSION FIXATION FOR YOU
			except:
				pass # TODO: Some session objects don't implement regenerate :(
			session['username'] = user.user
			session['id'] = user.id
			session['nonce'] = sha512(os.urandom(10))
			db.session.close()
			return True
		else:
			db.session.close()
			return False
