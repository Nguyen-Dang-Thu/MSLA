from flask import session, request, url_for
from msla import app, db
from .models import Log, FileUpload
from user_agents import parse
from werkzeug import secure_filename
from datetime import datetime
import hashlib
import psutil
import subprocess
import os, re

def searchResult(searchColumn, searchInfo, page):
	if searchColumn == "source_ip":
		results = db.session.query(Log).filter(Log.source_ip.like('%'+searchInfo+'%')).slice((page-1)*100,page*100)
	elif searchColumn == "date":
		results = db.session.query(Log).filter(Log.date.like('%'+searchInfo+'%')).slice((page-1)*100,page*100)
	elif searchColumn == "time":
		results = db.session.query(Log).filter(Log.time.like('%'+searchInfo+'%')).slice((page-1)*100,page*100)
	elif searchColumn == "source_port":
		results = db.session.query(Log).filter(Log.source_port.like('%'+searchInfo+'%')).slice((page-1)*100,page*100)
	elif searchColumn == "dest_ip":
		results = db.session.query(Log).filter(Log.dest_ip.like('%'+searchInfo+'%')).slice((page-1)*100,page*100)
	elif searchColumn == "dest_port":
		results = db.session.query(Log).filter(Log.dest_port.like('%'+searchInfo+'%')).slice((page-1)*100,page*100)
	elif searchColumn == "os":
		results = db.session.query(Log).filter(Log.os.like('%'+searchInfo+'%')).slice((page-1)*100,page*100)
	elif searchColumn == "message":
		results = db.session.query(Log).filter(Log.message.like('%'+searchInfo+'%')).slice((page-1)*100,page*100)
	elif searchColumn == "detailed_message":
		results = db.session.query(Log).filter(Log.detailed_message.like('%'+searchInfo+'%')).slice((page-1)*100,page*100)	
	else:
		results = db.session.query(Log).filter(Log.source_ip.like('%'+searchInfo+'%')|Log.date.like('%'+searchInfo+'%')|Log.time.like('%'+searchInfo+'%')|Log.source_port.like('%'+searchInfo+'%')|Log.dest_ip.like('%'+searchInfo+'%')|Log.dest_port.like('%'+searchInfo+'%')|Log.os.like('%'+searchInfo+'%')|Log.browser.like('%'+searchInfo+'%')|Log.message.like('%'+searchInfo+'%')|Log.detailed_message.like('%'+searchInfo+'%')).slice((page-1)*100,page*100)
	
	return results
	
def searchCount(searchColumn, searchInfo):
	if searchColumn == "source_ip":
		result = db.session.query(Log).filter(Log.source_ip.like('%'+searchInfo+'%')).count()
	elif searchColumn == "date":
		result = db.session.query(Log).filter(Log.date.like('%'+searchInfo+'%')).count()
	elif searchColumn == "time":
		result = db.session.query(Log).filter(Log.time.like('%'+searchInfo+'%')).count()
	elif searchColumn == "source_port":
		result = db.session.query(Log).filter(Log.source_port.like('%'+searchInfo+'%')).count()
	elif searchColumn == "dest_ip":
		result = db.session.query(Log).filter(Log.dest_ip.like('%'+searchInfo+'%')).count()
	elif searchColumn == "dest_port":
		result = db.session.query(Log).filter(Log.dest_port.like('%'+searchInfo+'%')).count()
	elif searchColumn == "os":
		result = db.session.query(Log).filter(Log.os.like('%'+searchInfo+'%')).count()
	elif searchColumn == "message":
		result = db.session.query(Log).filter(Log.message.like('%'+searchInfo+'%')).count()
	elif searchColumn == "detailed_message":
		result = db.session.query(Log).filter(Log.detailed_message.like('%'+searchInfo+'%')).count()
	else:
		result = db.session.query(Log).filter(Log.source_ip.like('%'+searchInfo+'%')|Log.date.like('%'+searchInfo+'%')|Log.time.like('%'+searchInfo+'%')|Log.source_port.like('%'+searchInfo+'%')|Log.dest_ip.like('%'+searchInfo+'%')|Log.dest_port.like('%'+searchInfo+'%')|Log.os.like('%'+searchInfo+'%')|Log.browser.like('%'+searchInfo+'%')|Log.message.like('%'+searchInfo+'%')|Log.detailed_message.like('%'+searchInfo+'%')).count()
		
	return result


def sha512(string):
    return hashlib.sha512(string).hexdigest()

def deleteLog(fileID):
	fileUpload = db.session.query(FileUpload).filter_by(id=fileID).first() # select * from FileUpload where id=fileID limit 1
	if fileUpload:
		filename = os.path.join(fileUpload.path, fileUpload.filename)
		db.session.delete(fileUpload) #delete log location record
		db.session.commit()
		db.session.close()
		os.remove(filename) #delete log
		os.rmdir(fileUpload.path)
		return "Delete file successfully!"
	return "Error!"


def saveFile(files):
	for file in files:
		filename = secure_filename(file.filename) # prevent LFI attack
		if len(filename) <= 0:
						continue

		md5hash = hashlib.md5(os.urandom(64)).hexdigest()
		base = os.path.dirname(os.path.dirname(__file__))
		if not os.path.exists(os.path.join(base, app.config['UPLOAD_FOLDER'], md5hash)):
			os.makedirs(os.path.join(base, app.config['UPLOAD_FOLDER'], md5hash))
	
		file.save(os.path.join(base, app.config['UPLOAD_FOLDER'], md5hash, filename))
		fileUpload = FileUpload(os.path.join(base, app.config['UPLOAD_FOLDER'], md5hash), filename)
		db.session.add(fileUpload)
		db.session.commit()
		db.session.close()

def url_for_other_page(page):
	args = request.view_args.copy()
	args['page'] = page
	return url_for(request.endpoint, **args)

def getSrcIP():
	logs = db.session.query(Log.source_ip).order_by(Log.source_ip).distinct().slice(0,5)
	srcIP = []
	for log in logs:
		tg = {"name":"","number":""}
		if log.source_ip == "":
			tg['name'] = "Unknown"
		else:
			tg['name'] = log.source_ip
		rs = db.session.query(Log.id).filter_by(source_ip=log.source_ip).count()
		tg['number'] = rs
		srcIP.append(tg)
		db.session.close()
	return srcIP	

def getBrowser():
	logs = db.session.query(Log.browser).order_by(Log.browser).distinct()
	browser = []
	for log in logs:
		tg = {"name":"","number":""}
		tg['name'] = log.browser
		rs = db.session.query(Log.id).filter_by(browser=log.browser).count()
		tg['number'] = rs
		browser.append(tg)
	db.session.close()
	return browser

def getDate():
	logs = db.session.query(Log.date).distinct()
	date = []
	for log in logs:
		tg = {"name":"","number":""}
		if log.date == "":
			tg['name'] = "Unknown"
		else:
			tg['name'] = log.date
		rs = db.session.query(Log.id).filter_by(date=log.date).count()
		tg['number'] = rs
		date.append(tg)
	db.session.close()
	return date

def getOs():
	logs = db.session.query(Log.os).order_by(Log.os).distinct()
	os = []
	for log in logs:
		tg = {"name":"","number":""}
		tg['name'] = log.os
		rs = db.session.query(Log.id).filter_by(os=log.os).count()
		tg['number'] = rs
		os.append(tg)
	db.session.close()
	return os

def getAttack():
	logs = db.session.query(Log.message).order_by(Log.message).distinct().slice(0,3)
	attack = []
	for log in logs:
		tg = {"name":"","number":""}
		if log.message == "":
			tg['name'] = "Unknown"
		else:
			tg['name'] = log.message
		rs = db.session.query(Log.id).filter_by(message=log.message).count()
		tg['number'] = rs
		attack.append(tg)
	db.session.close()
	return attack

def getTotal():
	total = db.session.query(Log.id).count()
	db.session.close()
	return total

def isauth():
	if 'id' in session:
		return True
	else:
		return False

def bytes2human(n):
	# http://code.activestate.com/recipes/578019
	# >>> bytes2human(10000)
	# '9.8K'
	# >>> bytes2human(100001221)
	# '95.4M'
	symbols = ('K', 'M', 'G', 'T', 'P', 'E', 'Z', 'Y')
	prefix = {}
	for i, s in enumerate(symbols):
		prefix[s] = 1 << (i + 1) * 10
	for s in reversed(symbols):
		if n >= prefix[s]:
			value = float(n) / prefix[s]
			return '%.1f%s' % (value, s)
	return "%sB" % n


def diskUsage():
	result = []
	templ = "%s %s %s %s %s%% %s %s"
	for part in psutil.disk_partitions(all=False):
		if os.name == 'nt':
			if 'cdrom' in part.opts or part.fstype == '':
				# skip cd-rom drives with no disk in it; they may raise
				# ENOENT, pop-up a Windows GUI error for a non-ready
				# partition or just hang.
				continue
		usage = psutil.disk_usage(part.mountpoint)
		result.append((templ % (
			part.device,
			bytes2human(usage.total),
			bytes2human(usage.used),
			bytes2human(usage.free),
			int(usage.percent),
			part.fstype,
			part.mountpoint)))
			
	return result

def cpu():
	return psutil.cpu_percent(interval=1)

def ram():
	return psutil.virtual_memory().percent

def who():
	users = psutil.users()
	result = []
	for user in users:
		result.append("%-15s %-15s %s  (%s)" % (
			user.name,
			user.terminal or '-',
			datetime.fromtimestamp(user.started).strftime("%Y-%m-%d %H:%M"),
			user.host))
			
	return result

def ipaddress():
	ips =  subprocess.getoutput(["/sbin/ifconfig | grep -i \"inet\" | grep -iv \"inet6\" | " + "awk {'print $2'} | sed -ne 's/addr\:/ /p'"])
	iface = subprocess.getoutput(["/sbin/ifconfig | cut -d \" \" -f1"])
	ips = ips.split("\n")
	ifaces = []
	for i in iface.split("\n"):
		if i == "":
			pass
		else:
			ifaces.append(i)

	result = []
	for i in range(len(ips)):
		result.append(ifaces[i]+": "+ips[i])

	return result

def allowed_file(filename):
	return '.' in filename and \
		   filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']

def ua_parse(ua):
	user_agent = parse(ua)
	bname = user_agent.browser.family
	platform = user_agent.os.family
	version= user_agent.browser.version
	result = [bname, platform]
	return result
	

def parse_block(block, vals):
	matchDate = re.search(r'\d{2}/[JFMMJASOND]\w{2,}/\d{4}', block) #Date
	if matchDate:
		vals['date'] = matchDate.group()

	matchTime = re.search(r'\d{2}:\d{2}:\d{2} [\+\-]\d{4}', block) #Time
	if matchTime:
		vals['time'] = matchTime.group()

	matchIP = re.search(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3} \d{1,5} \d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3} \d{1,5}', block) #IP
	if matchIP:
		data = matchIP.group().split(" ")
		vals['srcIP'] = data[0]
		vals['srcPort'] = data[1]
		vals['destIP'] = data [2]
		vals['destPort'] = data[3]

	matchGet = re.search(r'(GET|POST) ((/\w+)?)+(/\w+(\.\w+)?)', block) #Get Address
	if matchGet:
		vals['getAdd'] = matchGet.group()

	matchUseragent = re.search(r'[Uu]ser-[aA]gent: .+', block)
	if matchUseragent:
		vals['userAgent']= matchUseragent.group()

	matchMes = re.findall(r'\[msg \".+\.\"\]', block)
	vals['mes'] = ''
	for mes in matchMes:
		vals['mes'] = vals['mes'] + mes[6:-2] + " | "
	vals['mes'] = vals['mes'][:-2]

	matchMes = re.search(r'-H--\s(Message:.+\s)+', block)
	vals['detailMes'] = ''
	if matchMes:
		vals['detailMes'] = matchMes.group()

	ua = ua_parse(vals['userAgent']) #parse userAgent : OS , Browser
	vals['os'] = ua[1]
	vals['browser'] = ua[0]
	newLog = Log(vals['date'], vals['time'], vals['srcIP'], vals['srcPort'], vals['destIP'], vals['destPort'], vals['getAdd'], vals['os'], vals['browser'],  vals['mes'], vals['detailMes'])
	db.session.add(newLog)
	db.session.commit()
	db.session.close()
	return vals

def parse_log(fileID):
	fileUpload = FileUpload.query.filter_by(id=fileID).first()
	db.session.close()
	if fileUpload:
		if fileUpload.im=='True': #check import to database
			return "File imported to database!"
		db.session.query(FileUpload).filter_by(id=fileID).update({'im': 'True'})
		db.session.commit()
		db.session.close()
		filename = os.path.join(fileUpload.path, fileUpload.filename)
	else:
		return "Error!"
	#get  phase information on log file
	if os.path.isfile(filename):
		i = 0
		error_block = ''
		val = {"date":"", "time":"", "srcIP":"", "srcPort":"", "destIP":"", "destPort":"", "getAdd":"", "os":"", "browser":"", "mes":"", "detailMes":"", "userAgent":""}
		for line in open(filename,"r"):
			match = re.search(r'^--[0-9a-fA-F]{8,}-[A-Z]--$', line.strip())
			if match:
				i += 1
			if match and i == 2:
				val = parse_block(error_block, val)
				error_block=""
				i=1
			error_block += line
		return "Import to database successfully!"
	else:
		return "Error!"
