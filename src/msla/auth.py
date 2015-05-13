from msla import app, db
from flask import render_template, session, redirect, request, url_for
from msla.utils import *
from .models import *
from .forms import LoginForm

@app.route("/login", methods=["GET","POST"])
def login():
	if isauth():
		return redirect('/')
	form = LoginForm()
	if request.method == 'POST':
		errors = []
		# validating user
		if form.validate() == True:
			return redirect('/')
		else:
			errors.append("That account doesn't seem to exist")
			db.session.close()
		return render_template('login.html', errors=errors, form=form)
	else:
		db.session.close()
		return render_template('login.html', form=form)

@app.route("/logout")
def logout():
	session.clear()
	return redirect('/')
