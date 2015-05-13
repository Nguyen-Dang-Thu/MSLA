from msla import app, db
from flask import render_template, session, redirect, request, abort
from msla.utils import *
from .models import Log
from .pagination import Pagination

@app.route('/importlog/<id>')
def importLog(id):
	if isauth():
		mes = parse_log(id)
		return mes
	else:
		abort(404)
@app.route('/deletelog/<id>')
def deletelog(id):
	if isauth():
		mes = deleteLog(id)
		return mes
	else:
		abort(404)
	
@app.route("/usage")
def usage():
	return str(cpu())+"|"+str(ram())
	
@app.route('/upload', methods=['POST'])
def upload():
	if isauth():
		files = request.files.getlist('files[]') #get file upload
		saveFile(files)
		return redirect("/log")
	else:
		abort(404)
		
@app.route('/search/', methods=['GET','POST'], defaults={'page': 1})
@app.route('/search/page/<int:page>')
def search(page):
	if not isauth():
		return redirect('/login')
		
	if request.method == 'POST':
		searchInfo = request.form['searchInfo']
		session['searchInfo'] = searchInfo
		searchColumn = request.form['column']
		session['searchColumn'] = searchColumn
		results = searchResult(searchColumn, searchInfo, page)
		db.session.close()
		count = searchCount(searchColumn, searchInfo)
		PER_PAGE = app.config['PER_PAGE']
		pagination = Pagination(page, PER_PAGE, count)
		app.jinja_env.globals['url_for_other_page'] = url_for_other_page
		return render_template("search.html", logs=results, pagination=pagination)
	else:
		if session['searchInfo']:
			searchInfo = session['searchInfo']
		else:
			searchInfo = ""
		if session['searchColumn']:
			searchColumn = session['searchColumn']
		else:
			searchColumn = ""
		count = searchCount(searchColumn, searchInfo)
		PER_PAGE = app.config['PER_PAGE']
		pagination = Pagination(page, PER_PAGE, count)
		app.jinja_env.globals['url_for_other_page'] = url_for_other_page
		results = searchResult(searchColumn, searchInfo, page)
		return render_template("search.html",logs=results,pagination=pagination)
