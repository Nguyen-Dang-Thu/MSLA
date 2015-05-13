MSLA - MOD SECURITY LOG AUDIT
=======
#Introduce

This is a small flask app for parse modsec_audit.log.

#Overview
![System monitor.jpg]
(/img/up1.png)
<div style="align-center;"> System Monitor</div>
![Report.jpg]
(/img/up2.png)
->Report Page<-
![Analytics.jpg]
(/img/up2.png)
->Analytics<-
![Log Manager.jpg]
(/img/up2.png)
->Log Manager<-

#Install
 1. `sudo ./prepare.sh` to install dependencies using apt.
 2. Install sqlsever, create a user, import modsec.sql to database.
 3. Change [src/config.py](https://github.com/Nguyen-Dang-Thu/MSLA/blob/master/src/config.py) line 8: kma:thudayne to your database user and password
 4. `./run.py` to run modsec
