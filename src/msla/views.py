from msla import app, db
from flask import render_template, session, redirect, request, url_for, abort
from msla.utils import *
from .models import *
from .pagination import Pagination
import os

#prevent csrf
@app.before_request
def csrf():
	if isauth() and request.method == "POST":
		if session['nonce'] != request.form.get('nonce'):
			abort(403)

@app.route("/")
@app.route("/home")
def home():
	if isauth():
		name = session['username']
		ipadd = ipaddress()
		disk = diskUsage()
		whoConnect = who()
		for d in range(len(disk)):
			disk[d] = disk[d].split(" ")
		return render_template("home.html", ipadd=ipadd, disk=disk, whoConnect=whoConnect)
	else:
		return redirect("/login")

@app.route("/analytics/", defaults={'page': 1})
@app.route('/analytics/page/<int:page>')
def analytics(page):
	if not isauth():
		return redirect('/login')
		
	logs = Log.query.slice((page-1)*100,page*100)
	db.session.close()
	if not logs:
		abort(404)
		
	count = getTotal()
	PER_PAGE = app.config['PER_PAGE']
	pagination = Pagination(page, PER_PAGE, count)
	app.jinja_env.globals['url_for_other_page'] = url_for_other_page
	return render_template("analytics.html",logs=logs,pagination=pagination)

@app.route("/report")
def report():
	if isauth():
		attack = getAttack()
		totalAttack = getTotal()
		osAttack = getOs()
		date = getDate()
		browser = getBrowser()
		srcIP = getSrcIP()
		return render_template("report.html",
							attack=attack,
							totalAttack=totalAttack,
							osAttack=osAttack,
							date = date,
							browser = browser,
							srcIP = srcIP)
	else:
		redirect("/login")

@app.route("/log")
def log():
	if isauth():
		fileUpload = FileUpload.query.all() #get list file upload from database
		db.session.close()
		return render_template('log.html', fileUpload=fileUpload)
	else:
		redirect("/login")

