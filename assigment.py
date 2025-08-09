from flask import Flask, render_template, request, redirect, url_for, session,make_response
from flask_cors import CORS
from flask_mysqldb import MySQL
from pytz import timezone
from datetime import datetime
from dateutil import parser 
import pytz
import json
from json import JSONEncoder
from werkzeug.utils import secure_filename




app = Flask(__name__)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'assignment_management'
CORS(app) 
 
app.secret_key = 'your secret key'
mysql = MySQL(app)
now_utc = datetime.now(timezone('UTC'))
now_asia = now_utc.astimezone(timezone('Asia/Kolkata'))


@app.route('/home',methods=['GET', 'POST'])
def home():
    return render_template('login.html')

@app.route('/hregister',methods=['GET', 'POST'])
def hregister():
    return render_template('registration.html')

@app.route('/student_reg',methods=['GET', 'POST'])
def student_reg():
    return render_template('student-form.html')


@app.route('/faculty_reg',methods=['GET', 'POST'])
def faculty_reg():
    return render_template('faculty-form.html')

@app.route('/student_log',methods=['GET', 'POST'])
def student_log():
    return render_template('student-login.html')

@app.route('/faculty_log',methods=['GET', 'POST'])
def faculty_log():
    return render_template('faculty-login.html')

@app.route('/student_log2',methods=['GET', 'POST'])
def student_log2():
    return render_template('student-login2.html')

@app.route('/faculty_enroll',methods=['GET', 'POST'])
def faculty_enroll():
    return render_template('faculty-login2.html')

@app.route('/faculty_eval',methods=['GET', 'POST'])
def faculty_eval():
    return render_template('faculty_evaluation.html')

@app.route('/faculty_uplo',methods=['GET', 'POST'])
def faculty_uplo():
    return render_template('faculty_uploadation.html')


@app.route('/student_assign_uplo',methods=['GET', 'POST'])
def student_assign_uplo():
    return render_template('stu_assignment_upload.html')


@app.route('/student_marks_view',methods=['GET', 'POST'])
def student_marks_view():
    return render_template('stu_marks_view.html')

import hashlib
@app.route('/student_reg1', methods=['GET','POST'])
def student_reg1():
    uname=request.form.get('uname')
    usn=request.form.get('usn')
    email=request.form.get('email')
    pwd=request.form.get('pwd')
    
    cursor=mysql.connection.cursor()
    #pwd = hashlib.md5(pwd.encode('utf-8')).digest()
    cursor.execute(''' INSERT INTO student(name,student_id,email_id,password) VALUES(%s,%s,%s,MD5(%s))''',(uname,usn,email,pwd))
    mysql.connection.commit()
    cursor.close()
    return "success"

@app.route('/faculty_reg1', methods=['GET','POST'])
def faculty_reg1():
    fname=request.form.get('fname')
    faculty_id=request.form.get('faculty_id')
    email=request.form.get('email')
    pwd=request.form.get('pwd')
    
    cursor=mysql.connection.cursor()
    #pwd = hashlib.md5(pwd.encode('utf-8')).digest()
    cursor.execute(''' INSERT INTO faculty(faculty_name,faculty_id,email_id,password) VALUES(%s,%s,%s,MD5(%s))''',(fname,faculty_id,email,pwd))
    mysql.connection.commit()
    cursor.close()
    return "success"


@app.route('/student_log1', methods=['GET', 'POST'])

def student_log1():
    uname=request.form.get('uname')
    pwd=request.form.get('pwd')
    cursor=mysql.connection.cursor()
    cursor.execute(''' SELECT student_id FROM student WHERE name=%s and password=MD5(%s)''',(uname,pwd))
    row=cursor.fetchone()
    cursor.close()
    student_id=str(row[0])
    if row:
        
            response = make_response("success") # We can also render new page with render_template
            response.set_cookie('student_id',student_id)
            return response
        
        
    else:
        return "Failed to login"


@app.route('/faculty_log1', methods=['GET', 'POST'])

def faculty_log1():
    fname=request.form.get('fname')
    pwd=request.form.get('pwd')
    cursor=mysql.connection.cursor()
    cursor.execute(''' SELECT * FROM faculty WHERE faculty_name=%s and password=MD5(%s)''',(fname,pwd))
    row=cursor.fetchone()
    cursor.close()
    faculty_id=str(row[0])
    if row:
        
            response = make_response("success") # We can also render new page with render_template
            response.set_cookie('faculty_id',faculty_id)
            return response
        
        
    else:
        return "Failed to login"



@app.route('/courseinsert', methods =['GET', 'POST'])
def courseinsert():
    
    cname = request.form.get('cname')
    cid = request.form.get('cid')
    cdts = request.form.get('cdts')

    #print(date_object)
    cursor = mysql.connection.cursor()
    cursor.execute(''' INSERT INTO course(course_name,course_id,credits) VALUES(%s,%s,%s)''',(cname,cid,cdts))
    mysql.connection.commit()
    cursor.close()
    return "Inserted successfully"


@app.route('/coursenroll', methods =['GET', 'POST'])
def coursenroll():
    
    
    cid = request.form.get('course')
    sid=request.cookies.get('student_id')

    #print(date_object)
    cursor=mysql.connection.cursor()
    cursor.execute(''' SELECT * FROM enrolls WHERE course_id=%s and student_id=%s''',(cid,sid))
    row=cursor.fetchone()
    cursor.close()
    if row:
        return "Already enrolled"
    cursor = mysql.connection.cursor()
    cursor.execute(''' INSERT INTO enrolls(student_id,course_id) VALUES(%s,%s)''',(sid,cid))
    mysql.connection.commit()
    cursor.close()
    return "Inserted successfully"

@app.route('/cshow', methods =['GET', 'POST'])
def cshow():
    
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM course")
    row_headers=[x[0] for x in cursor.description] 
    DBData = cursor.fetchall() 
    cursor.close()
    json_data=[]
    rstr="<table border><tr>"
    for r in row_headers:
        rstr=rstr+"<th>"+r+"</th>"
    rstr=rstr+"<th>Update</th><th>Delete</th></tr>"
    cnt=0
    cid=-1
    for result in DBData:
        cnt=0
        ll=['A','B','C','D','E','F','G','H','I','J','K']
        for row in result:
            if cnt==0:
                cid=row
                rstr=rstr+"<td>"+str(row)+"</td>" 
            elif cnt==3:
                rstr=rstr+"<td>"+"<input type=date id="+str(ll[cnt])+str(cid)+" value=\""+str(row)+"\"></td>"  
            else:
                rstr=rstr+"<td>"+"<input type=text id="+str(ll[cnt])+str(cid)+" value=\""+str(row)+"\"></td>"     
            cnt+=1
            
        rstr+="<td><a><i class=\"fa fa-edit\" aria-hidden=\"true\" onclick=update('"+str(cid)+"')></i></a></td>"
        rstr+="<td><a><i class=\"fa fa-trash\" aria-hidden=\"true\" onclick=del('"+str(cid)+"')></i></a></td>"
        
        rstr=rstr+"</tr>"
    
    rstr=rstr+"</table>"
    rstr=rstr+'''
    <script type=\"text/javascript\">
    function update(cid)
    {
       cname=$("#B"+cid).val();
       cdts=$("#C"+cid).val();
       $.ajax({
        url: \"/courseupdate\",
        type: \"POST\",
        data: {cid:cid,cname:cname,cdts:cdts},
        success: function(data){    
        alert(data);
        loadcourse();
        }
       });
    }
   
    function del(cid)
    {
    $.ajax({
        url: \"/coursedelete\",
        type: \"POST\",
        data: {cid:cid},
        success: function(data){
            alert(data);
            loadcourse();
        }
        });
    }
    function loadcourse(){

       $.ajax({
        url: 'http://127.0.0.1:5000/cshow',
        type: 'POST',
        success: function(data){
          $('#cshow').html(data);
        }
      });
    }
    
    
    </script>

'''
    return rstr

@app.route('/ecshow', methods =['GET', 'POST'])
def ecshow():
    
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM enrolls")
    row_headers=[x[0] for x in cursor.description] 
    DBData = cursor.fetchall() 
    cursor.close()
    json_data=[]
    rstr="<table border><tr>"
    for r in row_headers:
        rstr=rstr+"<th>"+r+"</th>"
    rstr=rstr+"<th>Delete</th></tr>"
    cnt=0
    cid=-1
    for result in DBData:
        cnt=0
        ll=['A','B','C','D','E','F','G','H','I','J','K']
        for row in result:
            if cnt==0:
                sid=row
                rstr=rstr+"<td>"+str(row)+"</td>" 
            elif cnt==1:
                cid=row
                rstr=rstr+"<td>"+str(row)+"</td>"
            
            cnt+=1
            
        
        rstr+="<td><a><i class=\"fa fa-trash\" aria-hidden=\"true\" onclick=del('"+str(cid)+"',"+str(sid)+")></i></a></td>"
        
        rstr=rstr+"</tr>"
    
    rstr=rstr+"</table>"
    rstr=rstr+'''
    <script type=\"text/javascript\">
    
    function del(cid,sid)
    {
    $.ajax({
        url: \"/enrolldelete\",
        type: \"POST\",
        data: {cid:cid,sid:sid},
        success: function(data){
            alert(data);
            loadenrolledcourses();
        }
        });
    }
    function loadenrolledcourses(){

       $.ajax({
        url: 'http://127.0.0.1:5000/ecshow',
        type: 'POST',
        success: function(data){
          $('#ecr').html(data);
        }
      });
    }
    
    
    </script>

'''
    return rstr

@app.route('/courseupdate', methods =['GET', 'POST'])
def courseupdate():
    
    cid=request.form.get('cid')
    cname = request.form.get('cname')
    cdts = request.form.get('cdts')

    cursor = mysql.connection.cursor()
    cursor.execute(''' UPDATE course SET course_name=%s,credits=%s WHERE course_id=%s''',(cname,cdts,cid))
    mysql.connection.commit()
    cursor.close()
    return "Updated successfully"




@app.route('/coursedelete', methods =['GET', 'POST'])
def coursedelete():
    
    cid=request.form.get('cid')
    cursor = mysql.connection.cursor()
    cursor.execute(''' DELETE FROM course WHERE course_id=%s''',(cid,))
    mysql.connection.commit()
    cursor.close()
    return "Deleted successfully"

@app.route('/enrolldelete', methods =['GET', 'POST'])
def enrolldelete():
    
    cid=request.form.get('cid')
    sid=request.form.get('sid')
    cursor = mysql.connection.cursor()
    cursor.execute(''' DELETE FROM enrolls WHERE course_id=%s and student_id=%s''',(cid,sid))
    mysql.connection.commit()
    cursor.close()
    return "Deleted successfully"


@app.route('/userlogin', methods=['GET', 'POST'])

def userlogin():
    uname=request.form.get('uname')
    pwd=request.form.get('pwd')
    cursor=mysql.connection.cursor()
    cursor.execute(''' SELECT * FROM user WHERE uname=%s and pwd=MD5(%s)''',(uname,pwd))
    row=cursor.fetchone()
    cursor.close()
    if row:
        
            return ("successfully logged")
        
        
    else:
        return "Failed to login"

@app.route('/login', methods=['GET','POST'])
def login():
    return render_template('userlogin.html')

@app.route('/adminlogin', methods=['GET'])
def adminlogin():
    return render_template('adminlogin.html')


@app.route('/admin', methods =['GET', 'POST'])
def admin():
    
    username = request.form.get('uname')
    password = request.form.get('psw')
    print(username, password)
    if username == 'admin' and password == 'ppp':
        #return redirect(url_for('adminlogin', username=username))
        return ('success')
    else:
        return ('Login failed')
    
@app.route('/deptinsert', methods =['GET', 'POST'])
def deptinsert():
    
    dname = request.form.get('dname')
    dloc = request.form.get('dloc')
    sdate = request.form.get('sdate')
    
    date_object = parser.parse(sdate)
    sdate = date_object.astimezone(pytz.timezone('Asia/Kolkata')) 
    #print(date_object)
    cursor = mysql.connection.cursor()
    cursor.execute(''' INSERT INTO dept(dname,dloc,sdate) VALUES(%s,%s,%s)''',(dname,dloc,sdate))
    mysql.connection.commit()
    cursor.close()
    return "Inserted successfully"

@app.route('/rtinsert', methods =['GET', 'POST'])

def rtinsert():
    rtname=request.form.get('rtname')
    rtdes=request.form.get('rtdes')

    cursor=mysql.connection.cursor()
    cursor.execute(''' INSERT INTO resourcetype(rtype,rtdesc) VALUES(%s,%s)''',(rtname,rtdes))
    mysql.connection.commit()
    cursor.close()
    return "Inserted successfully"

@app.route('/rinsert', methods =['GET', 'POST'])
def rinsert():
    
    
    rname = request.form.get('rname')
    rdes=request.form.get('rdes')
    rtid=request.form.get('rrtid')
    ravalue=request.form.get('ravalue')
    rstatus=request.form.get('rstatus')
    f = request.files['rfile']       
    filename = secure_filename(f.filename)
    now = datetime.now()
    dt_string = now.strftime("%d%m%Y%H%M%S")
    rimg=dt_string+"_"+filename
    f.save("static/resources/" + rimg)
    cursor = mysql.connection.cursor()
    cursor.execute(''' INSERT INTO resource(rname,rdesc,rtid,avalue,rimg,rstatus) VALUES(%s,%s,%s,%s,%s,%s)''',(rname,rdes,rtid,ravalue,rimg,rstatus))
    mysql.connection.commit()
    cursor.close()
    return "Inserted successfully"


@app.route('/deptupdate', methods =['GET', 'POST'])
def deptupdate():
    
    did=request.form.get('did')
    dname = request.form.get('dname')
    dloc = request.form.get('dloc')
    sdate = request.form.get('sdate')
    
    date_object = parser.parse(sdate)
    sdate = date_object.astimezone(pytz.timezone('Asia/Kolkata')) 
    #print(date_object)
    cursor = mysql.connection.cursor()
    cursor.execute(''' UPDATE dept SET dname=%s,dloc=%s,sdate=%s WHERE did=%s''',(dname,dloc,sdate,did))
    mysql.connection.commit()
    cursor.close()
    return "Updated successfully"

@app.route('/rtupdate', methods =['GET', 'POST'])
def rtupdate():
    
    rtid=request.form.get('rtid')
    rtype = request.form.get('rtname')
    rtdesc = request.form.get('rtdes')
    
    cursor = mysql.connection.cursor()
    cursor.execute(''' UPDATE resourcetype SET rtype=%s,rtdesc=%s WHERE rtid=%s''',(rtype,rtdesc,rtid))
    mysql.connection.commit()
    cursor.close()
    return "Updated successfully"


@app.route('/deptdelete', methods =['GET', 'POST'])
def deptdelete():
    
    did=request.form.get('did')
    cursor = mysql.connection.cursor()
    cursor.execute(''' DELETE FROM dept WHERE did=%s''',(did,))
    mysql.connection.commit()
    cursor.close()
    return "Deleted successfully"

@app.route('/rtdelete', methods =['GET', 'POST'])
def rtdelete():
    
    rtid=request.form.get('rtid')
    cursor = mysql.connection.cursor()
    cursor.execute(''' DELETE FROM resourcetype WHERE rtid=%s''',(rtid,))
    mysql.connection.commit()
    cursor.close()
    return "Deleted successfully"

@app.route('/rdelete', methods =['GET', 'POST'])
def rdelete():
    
    rid=request.form.get('rid')
    cursor = mysql.connection.cursor()
    cursor.execute(''' DELETE FROM resource WHERE rid=%s''',(rid,))
    mysql.connection.commit()
    cursor.close()
    return "Deleted successfully"

@app.route('/rtnameshow', methods =['GET', 'POST'])

def rtnameshow():
    
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM resourcetype")
    DBData = cursor.fetchall() 
    cursor.close()
    
    rtnames=''
    for result in DBData:
        print(result)
        rtnames+="<option value="+str(result[0])+">"+result[1]+"</option>"
    return rtnames    
        
@app.route('/getassignmentids', methods =['GET', 'POST'])

def getassignmentids():
    
    cursor = mysql.connection.cursor()
    cid=request.form.get('cid')
    cursor.execute("SELECT * FROM assignment where assignment.cid=%s",(cid,))
    DBData = cursor.fetchall() 
    cursor.close()
    
    rtnames=''
    for result in DBData:
        print(result)
        rtnames+="<option value="+str(result[0])+">"+result[1]+"</option>"
    return rtnames   
@app.route('/deptshow', methods =['GET', 'POST'])
def deptshow():
    
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM dept")
    row_headers=[x[0] for x in cursor.description] 
    DBData = cursor.fetchall() 
    cursor.close()
    json_data=[]
    rstr="<table border><tr>"
    for r in row_headers:
        rstr=rstr+"<th>"+r+"</th>"
    rstr=rstr+"<th>Update</th><th>Delete</th></tr>"
    cnt=0
    did=-1
    for result in DBData:
        cnt=0
        ll=['A','B','C','D','E','F','G','H','I','J','K']
        for row in result:
            if cnt==0:
                did=row
                rstr=rstr+"<td>"+str(row)+"</td>" 
            elif cnt==3:
                rstr=rstr+"<td>"+"<input type=date id="+str(ll[cnt])+str(did)+" value="+str(row)+"></td>"  
            else:
                rstr=rstr+"<td>"+"<input type=text id="+str(ll[cnt])+str(did)+" value=\""+str(row)+"\"></td>"     
            cnt+=1
            
        rstr+="<td><a ><i class=\"fa fa-edit\" aria-hidden=\"true\" onclick=update("+str(did)+")></i></a></td>"
        rstr+="<td><a ><i class=\"fa fa-trash\" aria-hidden=\"true\" onclick=del("+str(did)+")></i></a></td>"
        
        rstr=rstr+"</tr>"
    
    rstr=rstr+"</table>"
    rstr=rstr+'''
    <script type=\"text/javascript\">
    function update(did)
    {
       dname=$("#B"+did).val();
       dloc=$("#C"+did).val();
       sdate=$("#D"+did).val();
       $.ajax({
        url: \"/deptupdate\",
        type: \"POST\",
        data: {did:did,dname:dname,dloc:dloc,sdate:sdate},
        success: function(data){    
        alert(data);
        loaddepartments();
        }
       });
    }
   
    function del(did)
    {
    $.ajax({
        url: \"/deptdelete\",
        type: \"POST\",
        data: {did:did},
        success: function(data){
            alert(data);
            loaddepartments();
        }
        });
    }
    function loaddepartments(){

       $.ajax({
        url: 'http://127.0.0.1:5000/deptshow',
        type: 'POST',
        success: function(data){
          $('#dshow').html(data);
        }
      });
    }
    
    
    </script>

'''
    return rstr


@app.route('/rtshow', methods =['GET', 'POST'])
def rtshow():
    
    cursor = mysql.connection.cursor()

    cursor.execute("SELECT * FROM resourcetype")
    row_headers=[x[0] for x in cursor.description] 
    DBData = cursor.fetchall() 
    cursor.close()
    json_data=[]
    rstr="<table border><tr>"
    for r in row_headers:
        rstr=rstr+"<th>"+r+"</th>"
    rstr=rstr+"<th>Update</th><th>Delete</th></tr>"
    cnt=0
    did=-1
    for result in DBData:
        cnt=0
        ll=['A','B','C','D','E','F','G','H','I','J','K']
        for row in result:
            if cnt==0:
                rtid=row
                rstr=rstr+"<td>"+str(row)+"</td>" 
           
            else:
                rstr=rstr+"<td>"+"<input type=text id="+str(ll[cnt])+str(rtid)+" value=\""+str(row)+"\"></td>"     
            cnt+=1
            
        rstr+="<td><a ><i class=\"fa fa-edit\" aria-hidden=\"true\" onclick=rupdate("+str(rtid)+")></i></a></td>"
        rstr+="<td><a ><i class=\"fa fa-trash\" aria-hidden=\"true\" onclick=rdel("+str(rtid)+")></i></a></td>"
        
        rstr=rstr+"</tr>"
    
    rstr=rstr+"</table>"
    rstr=rstr+'''
    <script type=\"text/javascript\">
    function rupdate(rtid)
    {
       //alert('aha no');
       rtname=$("#B"+rtid).val();
       rtdes=$("#C"+rtid).val();
       $.ajax({
        url: \"/rtupdate\",
        type: \"POST\",
        data: {rtid:rtid,rtname:rtname,rtdes:rtdes},
        success: function(data){
       
        alert(data);
        loadrtypes();
        }
       });
    }
   
    function rdel(rtid)
    {
    $.ajax({
        url: \"/rtdelete\",
        type: \"POST\",
        data: {rtid:rtid},
        success: function(data){
        alert(data);
        loadrtypes();
        }
        });
    }
   
    function loadrtypes(){
       $.ajax({
        url: 'http://127.0.0.1:5000/rtshow',
        type: 'POST',
        success: function(data){
          $('#rtshow').html(data);
        }
      });
    }
    
    
    </script>

'''
    return rstr
@app.route('/rupdate', methods=['GET', 'POST'])

def rupdate():
    rtid=request.form.get('rtid')
    rname=request.form.get('rname')
    rdes=request.form.get('rdes')
    ravalue=request.form.get('ravalue')
    rstatus=request.form.get('rstatus')
    rid=request.form.get('rid')
    cursor = mysql.connection.cursor()
    cursor.execute(''' UPDATE resource SET rname=%s,rdesc=%s,rtid=%s,avalue=%s,rstatus=%s WHERE rid=%s''',(rname,rdes,rtid,ravalue,rstatus,rid))
    mysql.connection.commit()
    cursor.close()
    return "Updated successfully"
@app.route('/rshow', methods=['GET', 'POST'])

def rshow():
    cursor = mysql.connection.cursor()

    cursor.execute("SELECT * FROM resource")
    row_headers=[x[0] for x in cursor.description] 
    DBData = cursor.fetchall() 
    cursor.close()
    json_data=[]
    rstr="<table border><tr>"
    for r in row_headers:
        rstr=rstr+"<th>"+r+"</th>"
    rstr=rstr+"<th>Update</th><th>Delete</th></tr>"
    cnt=0
    did=-1
    for result in DBData:
        cnt=0
        ll=['A','B','C','D','E','F','G','H','I','J','K']
        for row in result:
            if cnt==0:
                rid=row
                rstr=rstr+"<td>"+str(row)+"</td>" 
            elif cnt==5:
                rfil="http://127.0.0.1:5000/static/resources/"+str(row)
                rstr=rstr+"<td>"+"<a href=\""+str(rfil)+"\" target=_blank>File</a></td>"
            else:
                rstr=rstr+"<td>"+"<input type=text id="+str(ll[cnt])+str(rid)+" value=\""+str(row)+"\"></td>"     
            cnt+=1
            
        rstr+="<td><a ><i class=\"fa fa-edit\" aria-hidden=\"true\" onclick=resupdate("+str(rid)+")></i></a></td>"
        rstr+="<td><a ><i class=\"fa fa-trash\" aria-hidden=\"true\" onclick=resdel("+str(rid)+")></i></a></td>"
        
        rstr=rstr+"</tr>"
    
    rstr=rstr+"</table>"
    rstr=rstr+'''
    <script type=\"text/javascript\">
    function resupdate(rid)
    {
       //alert('aha no');

       rname=$("#B"+rid).val();
       rdes=$("#C"+rid).val();
       rtid=$("#D"+rid).val();
       ravalue=$("#E"+rid).val();
       rstatus=$("#G"+rid).val();
       var fd=new FormData();
       fd.append('rname',rname);
       fd.append('rdes',rdes);
       fd.append('rtid',rtid);
       fd.append('ravalue',ravalue);
       fd.append('rstatus',rstatus);
       fd.append('rid',rid); 

       $.ajax({
        url: \"/rupdate\",
        type: \"POST\",
        data: fd,
        processData: false,
        contentType: false,
        success: function(data){
       
        alert(data);
        loadresources();
        }
       });
    }
   
    function resdel(rid)
    {
    $.ajax({
        url: \"/rdelete\",
        type: \"POST\",
        data: {rid:rid},
        success: function(data){
        alert(data);
        loadresources();
        }
        });
    }
   
    
    function loadresources(){
       $.ajax({
        url: 'http://127.0.0.1:5000/rshow',
        type: 'POST',
        success: function(data){
          $('#rshow').html(data);
        }
      });
    }
    
    
    </script>

'''
    return rstr

@app.route('/getcoursenames', methods =['GET', 'POST'])

def getcoursenames():
    
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM course")
    DBData = cursor.fetchall() 
    cursor.close()
    
    rtnames=''
    for result in DBData:
        print(result)
        rtnames+="<option value="+str(result[0])+">"+result[1]+"</option>"
    return rtnames  
  
@app.route('/getenrolledcoursenames', methods =['GET', 'POST'])

def getenrolledcoursenames():
    
    cursor = mysql.connection.cursor()
    sid=request.cookies.get('sid')
    cursor.execute("SELECT enrolls.course_id,course_name FROM enrolls,course where enrolls.course_id=course.course_id and student_id=%s",(sid,))
    DBData = cursor.fetchall() 
    cursor.close()
    
    rtnames=''
    for result in DBData:
        print(result)
        rtnames+="<option value="+str(result[0])+">"+result[1]+"</option>"
    return rtnames    

                              
@app.route('/adminav', methods =['GET', 'POST'])
def adminav():
    return render_template('adminnav.html')

@app.route('/assigninsert', methods =['GET', 'POST'])
def assigninsert():
    
    course = request.form.get('course')
    aname = request.form.get('aname')
    maxmarks=request.form.get('maxmarks')
    fid=request.cookies.get('faculty_id')
    

    #ravalue=request.form.get('ravalue')
    #rstatus=request.form.get('rstatus')
    f = request.files['afile']       
    filename = secure_filename(f.filename)
    now = datetime.now()
    dt_string = now.strftime("%d%m%Y%H%M%S")
    rimg=dt_string+"_"+filename
    f.save("static/resources/" + rimg)
    iid=request.cookies.get('iid')
    cursor = mysql.connection.cursor()
    print(iid)
    cursor.execute(''' INSERT INTO assignment(assign_name,assign_marks, question,cid,fid) VALUES(%s,%s,%s,%s,%s)''',(aname,maxmarks,rimg,course,fid))
    mysql.connection.commit()
    cursor.close()
    return "Inserted successfully"

@app.route('/assignupo', methods =['GET', 'POST'])
def assignupo():
    
    aid = request.form.get('aid')
    
    sid=request.cookies.get('student_id')
    

    #ravalue=request.form.get('ravalue')
    #rstatus=request.form.get('rstatus')
    f = request.files['aafile']       
    filename = secure_filename(f.filename)
    now = datetime.now()
    dt_string = now.strftime("%d%m%Y%H%M%S")
    rimg=dt_string+"_"+filename
    f.save("static/submissions/" + rimg)
    
    cursor = mysql.connection.cursor()
    
    cursor.execute(''' INSERT INTO submissions(sid,aid,solution) VALUES(%s,%s,%s)''',(sid,aid,rimg))
    mysql.connection.commit()
    cursor.close()
    return "Inserted successfully"

@app.route('/ashow', methods=['GET', 'POST'])

def ashow():
    cursor = mysql.connection.cursor()
    fid=request.cookies.get('faculty_id')
    cursor.execute("SELECT * FROM assignment where fid=%s",(fid,))
    row_headers=[x[0] for x in cursor.description] 
    DBData = cursor.fetchall() 
    cursor.close()
    json_data=[]
    rstr="<table border><tr>"
    for r in row_headers:
        rstr=rstr+"<th>"+r+"</th>"
    rstr=rstr+"<th>Update</th><th>Delete</th></tr>"
    cnt=0
    did=-1
    for result in DBData:
        cnt=0
        ll=['A','B','C','D','E','F','G','H','I','J','K']
        for row in result:
            if cnt==0:
                rid=row
                rstr=rstr+"<td>"+str(row)+"</td>" 
            elif cnt==3:
                rfil="http://127.0.0.1:5000/static/resources/"+str(row)
                rstr=rstr+"<td>"+"<a href=\""+str(rfil)+"\" target=_blank>File</a></td>"
            else:
                rstr=rstr+"<td>"+"<input type=text id=M"+str(ll[cnt])+str(rid)+" value=\""+str(row)+"\"></td>"     
            cnt+=1
            
        rstr+="<td><a ><i class=\"fa fa-edit\" aria-hidden=\"true\" onclick=aupdate("+str(rid)+")></i></a></td>"
        rstr+="<td><a ><i class=\"fa fa-trash\" aria-hidden=\"true\" onclick=adel("+str(rid)+")></i></a></td>"
        
        rstr=rstr+"</tr>"
    
    rstr=rstr+"</table>"
    rstr=rstr+'''
    <script type=\"text/javascript\">
    function aupdate(rid)
    {
       //alert('aha no');

       aname=$("#MB"+rid).val();
       amarks=$("#MC"+rid).val();
      
       
       var fd=new FormData();
       fd.append('aname',aname);
       fd.append('amarks',amarks);
       
       
       fd.append('rid',rid); 

       $.ajax({
        url: \"/aupdate\",
        type: \"POST\",
        data: fd,
        processData: false,
        contentType: false,
        success: function(data){
       
        alert(data);
        loadassignments();
        }
       });
    }
   
    function adel(rid)
    {
    $.ajax({
        url: \"/adelete\",
        type: \"POST\",
        data: {rid:rid},
        success: function(data){
        alert(data);
        loadassignments();
        }
        });
    }
   
    
    function loadassignments(){
       $.ajax({
        url: 'http://127.0.0.1:5000/ashow',
        type: 'POST',
        success: function(data){
          $('#assgns').html(data);
        }
      });
    }
    
    
    </script>

'''
    return rstr


@app.route('/aushow', methods=['GET', 'POST'])

def aushow():
    cursor = mysql.connection.cursor()
    sid=request.cookies.get('student_id')
    cursor.execute("SELECT * FROM submissions where sid=%s",(sid,))
    row_headers=[x[0] for x in cursor.description] 
    DBData = cursor.fetchall() 
    cursor.close()
    json_data=[]
    rstr="<table border><tr>"
    for r in row_headers:
        rstr=rstr+"<th>"+r+"</th>"
    rstr=rstr+"<th>Delete</th></tr>"
    cnt=0
    did=-1
    for result in DBData:
        cnt=0
        ll=['A','B','C','D','E','F','G','H','I','J','K']
        for row in result:
            if cnt==0:
                sid=row
                rstr=rstr+"<td>"+str(row)+"</td>" 
            elif cnt==1:
                aid=row
                rstr=rstr+"<td>"+str(row)+"</td>"
            elif cnt==2:
                rfil="http://127.0.0.1:5000/static/submissions/"+str(row)
                rstr=rstr+"<td>"+"<a href=\""+str(rfil)+"\" target=_blank>File</a></td>"
            else:
                rstr=rstr+"<td>"+str(row)+"</td>"     
            cnt+=1
            
        
        rstr+="<td><a ><i class=\"fa fa-trash\" aria-hidden=\"true\" onclick=aadel("+str(sid)+","+str(aid)+")></i></a></td>"
        
        rstr=rstr+"</tr>"
    
    rstr=rstr+"</table>"
    rstr=rstr+'''
    <script type=\"text/javascript\">
    
    function aadel(sid,aid)
    {
    $.ajax({
        url: \"/aadelete\",
        type: \"POST\",
        data: {sid:sid,aid:aid},
        success: function(data){
        alert(data);
        loaduploadedassignments();
        }
        });
    }
   
    
    function loaduploadedassignments(){
       $.ajax({
        url: 'http://127.0.0.1:5000/aushow',
        type: 'POST',
        success: function(data){
          $('#aupo').html(data);
        }
      });
    }
    
    
    </script>

'''
    return rstr

@app.route('/getassignmentdetails', methods=['GET', 'POST'])

def getassignmentdetails():
    cursor = mysql.connection.cursor()
    aid=request.form.get('aid')
    cursor.execute("SELECT * FROM assignment where assignment_id=%s",(aid,))
    row_headers=[x[0] for x in cursor.description] 
    DBData = cursor.fetchall() 
    cursor.close()
    json_data=[]
    rstr="<table border><tr>"
    for r in row_headers:
        rstr=rstr+"<th>"+r+"</th>"
    
    cnt=0
    did=-1
    rstr+="</tr>"
    for result in DBData:
        cnt=0
        ll=['A','B','C','D','E','F','G','H','I','J','K']
        for row in result:
            if cnt==0:
                rid=row
                rstr=rstr+"<td>"+str(row)+"</td>" 
            elif cnt==3:
                rfil="http://127.0.0.1:5000/static/resources/"+str(row)
                rstr=rstr+"<td>"+"<a href=\""+str(rfil)+"\" target=_blank>File</a></td>"
            else:
                rstr=rstr+"<td>"+"<input type=text id=M"+str(ll[cnt])+str(rid)+" value=\""+str(row)+"\"></td>"     
            cnt+=1
            
        
        
        rstr=rstr+"</tr>"
    
    rstr=rstr+"</table>"
    
    return rstr

@app.route('/aupdate', methods=['GET', 'POST'])

def mupdate():
    mid=request.form.get('rid')
    aname=request.form.get('aname')
    amarks=request.form.get('amarks')
    
    cursor = mysql.connection.cursor()
    cursor.execute(''' UPDATE assignment SET assign_name=%s,assign_marks=%s WHERE assignment_id=%s''',(aname,amarks,mid))
    mysql.connection.commit()
    cursor.close()
    return "Updated successfully"

@app.route('/adelete', methods =['GET', 'POST'])
def adelete():
    
    rid=request.form.get('rid')
    cursor = mysql.connection.cursor()
    cursor.execute(''' DELETE FROM assignment WHERE assignment_id=%s''',(rid,))
    mysql.connection.commit()
    cursor.close()
    return "Deleted successfully"

@app.route('/aadelete', methods =['GET', 'POST'])
def aadelete():
    
    sid=request.form.get('sid')
    aid=request.form.get('aid')
    cursor = mysql.connection.cursor()
    cursor.execute(''' DELETE FROM submissions WHERE sid=%s and aid=%s''',(sid,aid))
    mysql.connection.commit()
    cursor.close()
    return "Deleted successfully"
if __name__ == '__main__':
    app.run(debug=True)