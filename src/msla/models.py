from flask.ext.sqlalchemy import SQLAlchemy
from passlib.hash import bcrypt_sha256
from msla import db, app
import os

db = SQLAlchemy()

class FileUpload(db.Model):
	"""
	Log file location on server
	"""
	__tablename__='upload'
	id = db.Column(db.Integer, primary_key=True)
	path = db.Column(db.String())
	filename = db.Column(db.String())
	im = db.Column(db.String(5))

	def __init__(self, path, filename):
		self.path = path
		self.filename = filename
		self.im = 'False'

	def getPathFile(self):
		# return 
		return os.path.join(path, filename)

class Users(db.Model):
	__tablename__ = 'users'
	id = db.Column(db.Integer, primary_key=True)
	user = db.Column(db.String(100), unique=True)
	password = db.Column(db.String(128))
	
	def __init__(self, user, password):
		self.user = user
		self.password = bcrypt_sha256.encrypt(password)

	def __repr__(self):
		return '<user %r>' % self.user

class Log(db.Model):
	"""
	Log information
	"""
	__tablename__= 'log'
	
	id = db.Column(db.Integer, primary_key=True)
	date = db.Column(db.String())
	time = db.Column(db.String())
	source_ip = db.Column(db.String())
	source_port = db.Column(db.String())
	dest_ip = db.Column(db.String())
	dest_port = db.Column(db.String())
	get_adr = db.Column(db.String())
	os = db.Column(db.String())
	browser = db.Column(db.String())
	message = db.Column(db.String())
	detailed_message = db.Column(db.String())

	def __init__(self, date, time, source_ip, source_port, dest_ip, dest_port, get_adr, os, browser, message, detailed_message):
		self.date = date
		self.time = time
		self.source_ip = source_ip
		self.source_port = source_port
		self.dest_ip = dest_ip
		self.dest_port = dest_port
		self.get_adr = get_adr
		self.os = os
		self.browser = browser
		self.message = message
		self.detailed_message = detailed_message

	def __repr__(self):
		return '<log %r>' % self.date

