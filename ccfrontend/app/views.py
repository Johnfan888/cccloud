# -*- coding:utf-8 -*-
import json
import os
import string
import datetime
import urllib
import urllib2
import requests
from requests import get,post,session
import sys
import time
reload(sys)
sys.setdefaultencoding('utf-8')

from string import strip

from flask import (
    render_template, flash, redirect, session, url_for, request, g)
from flask_login import (
    login_user, logout_user, current_user, login_required)
from forms import (
    LoginForm, SignUpForm, PublishBlogForm, AboutMeForm,
    ManageForm,CreateForm,ModifyForm,Delete_vmForm,Delete_UserForm,
    Vm_security_groupForm,Vm_cloud_volumeForm,Add_vm_security_groupForm,
    Add_vm_cloud_volumeForm,Delete_cloudvolumeForm,Delete_securitygroupForm,
    Modify_usertypeForm,Vm_snapshootForm,Add_vm_snapshootForm,
    Recover_snapshootForm,Delete_snapshootForm,vm_powerForm)
from models import (
    User, Post, ROLE_USER, ROLE_ADMIN,VM_information,cloud_volume,security_group,snapshoot_information)
from utils import PER_PAGE

from app import app, db, lm
import models
import urllib
import httplib



import xml.dom.minidom
dom = xml.dom.minidom.parse((os.path.abspath('./conf/http_json.xml')))
root = dom.documentElement
login = root.getElementsByTagName('login')
data = login[0]
port_value = data.getAttribute("port")
ip_value = data.getAttribute("ip")
path_value = data.getAttribute("path")

headerdata = {"Host":ip_value,"Connection":"Keep-Alive",
              "Content-Type":"application/x-www-form-urlencoded"}
conn = httplib.HTTPConnection(ip_value)








@lm.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
@app.route('/index')
def index():
    user = 'Man'
    posts = None

    return render_template(
        "index.html",
        title="Home",
        user=user
        )






@app.route('/error')
def error():


    return render_template(
        "error.html",
        title="error",

        )

@app.route('/sucessful')
def sucessful():


    return render_template(
        "sucessful.html",
        title="sucessful",

        )








@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect('index')

    form = LoginForm()
#    user = User()
    if form.validate_on_submit():
        user_name = request.form.get('user_name')
        user_password = request.form.get('user_passwd')
        register_check = User.query.filter(db.and_(
            User.nickname == user_name, User.password == user_password)).first()

        if register_check:

            user = User.login_check(request.form.get('user_name'))
            login_user(user)
            user.last_seen = datetime.datetime.now()
            try:
                db.session.add(user)
                db.session.commit()
            except:
                flash("The Database error!")
                return redirect('/login')

            flash('Your name: ' + request.form.get('user_name'))
            flash('remember me? ' + str(request.form.get('remember_me')))
            return redirect(url_for("users", user_id=current_user.id))

        else:
            flash('Login failed, Your name or password is error !!!')
            return redirect('/login')

    return render_template(
        "login.html",
        title="logining",
        form=form)













@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))



@app.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    form = SignUpForm()
    user = User()
    if form.validate_on_submit():
        user_password = request.form.get('user_passwd')
        user_name = request.form.get('user_name')

        user_email = request.form.get('user_email')


        register_check = User.query.filter(db.or_(
            User.nickname == user_name, User.email == user_email)).first()
        if register_check:
            flash("error: The user's name or email already exists!")
            return redirect('/sign-up')

        if len(user_name) and len(user_email):
            user.nickname = user_name
            user.password = user_password
            user.email = user_email
            user.role = ROLE_USER
            try:
                db.session.add(user)
                db.session.commit()

            except:
                flash("The Database error!")
                return redirect('/sign-up')

            flash("Sign up successful!")
            return redirect('/sucessful')

    return render_template(
        "sign_up.html",
        form=form)












@app.route('/manage/<int:user_id>', defaults={'page':1}, methods=["POST", "GET"])
@app.route('/manage/<int:user_id>/page/<int:page>', methods=['GET', 'POST'])
@login_required
def manage(user_id, page):
    form = ManageForm()
    user_type = User.query.filter_by(id=current_user.id).first()
    if user_type.role == 1:

      select_=VM_information.query.all()
      machines = []
      for i in range(len(select_)):

          machines.append({'ID':i, 'hostname' : select_[i].VM_name,'hostid' : select_[i].VM_id,
                         'imagename' : select_[i].image,'ip' : select_[i].ip,
                         'floating_IP': select_[i].floating_ip,'status': select_[i].status,
                         'key': select_[i].key,'flavor': select_[i].flavor})
    else:
        select_=VM_information.query.filter_by(nickname=current_user.nickname).all()
        machines = []
        for i in range(len(select_)):

            machines.append({'ID':i,'hostname' : select_[i].VM_name,'hostid' : select_[i].VM_id,
                         'imagename' : select_[i].image,'ip' : select_[i].ip,
                         'floating_IP': select_[i].floating_ip,'status': select_[i].status,
                         'key': select_[i].key,'flavor': select_[i].flavor})
    if user_id != current_user.id and (current_user.role != 1) :
        flash("Sorry, you can only manage your profile!", "error")
        return redirect("/index")

    #if form.validate_on_submit():


    if request.form.get('submit')=='start':
        flash(machines.hostname)


        return render_template("sucessful.html")

    return render_template(
        "manage.html",
        form=form,
        machines = machines,
        user_id=user_id
        )







@app.route('/user/<int:user_id>', defaults={'page':1}, methods=["POST", "GET"])
@app.route('/user/<int:user_id>/page/<int:page>', methods=['GET', 'POST'])
@login_required
def users(user_id, page):
    form = AboutMeForm()
    if user_id != current_user.id:
        flash("Sorry, you can only view your profile!", "error")
        return redirect("/index")

    # pagination = user.posts.paginate(page, PER_PAGE, False).items
    pagination = Post.query.filter_by(
        user_id = current_user.id
        ).order_by(
        db.desc(Post.timestamp)
        ).paginate(page, PER_PAGE, False)
    return render_template(
        "user.html",
        form=form,
        pagination=pagination)



@app.route('/vm_power/<int:user_id>',  methods=["POST", "GET"])

@login_required
def vm_power(user_id):
    form = vm_powerForm()

    user_type = User.query.filter_by(id=current_user.id).first()
    if user_type.role == 1:
        select_vms =  VM_information.query.all()
    else:
        select_vms =  VM_information.query.filter_by(nickname=current_user.nickname).all()
    result = {}
    i = 0
    while  i< len(select_vms):
        result[i+1] = select_vms[i].VM_name
        i = i+1
    vms_into_json = json.dumps(result,ensure_ascii=False)
    VM_Names = json.loads(vms_into_json).values()

    if request.method == "POST":
      #if form.validate_on_submit():
        if  request.form.get('submit1')=='start':
            VMname = request.form.get('VMname')
            VMid = VM_information.query.filter(db.and_(VM_information.VM_name == VMname, VM_information.nickname == current_user.nickname)).first()
            start_data = {'ins_id':VMid.VM_id}
            start_data_urlencode = urllib.urlencode(start_data)
            requrl_security = "http://"+ip_value+"/"+path_value+"/"+"istl_nova_startIns.py"
            conn.request(method="POST",url=requrl_security,body=start_data_urlencode,headers = headerdata)
            response = conn.getresponse()
            res= response.read()
            conn.close()
            time.sleep(8)
            resultstatus=VM_information.query.filter_by(VM_id=VMid.VM_id).first()
            if res.strip() == "sucessful":
                status_data = {'ins_id':VMid.VM_id}
                status_data_urlencode = urllib.urlencode(status_data)
                requrl_security = "http://"+ip_value+"/"+path_value+"/"+"istl_query_host_status.py"
                conn.request(method="POST",url=requrl_security,body=status_data_urlencode,headers = headerdata)
                response = conn.getresponse()
                res_status= response.read()

                conn.close()
                try:
                        resultstatus.status=res_status.strip()
                        db.session.commit()
                except:
                        flash("The Database error!")
                        return redirect('/error')
                flash("start vm sucessful")
                return render_template("sucessful.html",)
            else:
                flash("openstack error , start vm fail")
                return redirect('/error')
        if  request.form.get('submit2')=='hang_up':
            VMname = request.form.get('VMname')
            VMid = VM_information.query.filter(db.and_(VM_information.VM_name == VMname, VM_information.nickname == current_user.nickname)).first()

            start_data = {}
            start_data['ins_id']=VMid.VM_id
            print start_data
            #start_data1 = json.dumps(start_data)
            start_data_urlencode = urllib.urlencode(start_data)
            requrl_security = "http://"+ip_value+"/"+path_value+"/"+"istl_nova_suspendIns.py"
            conn.request(method="POST",url=requrl_security,body=start_data_urlencode,headers = headerdata)
            response = conn.getresponse()
            res= response.read()
            conn.close()

            time.sleep(10)
            #resultstatus=VM_information.query.filter_by(VM_id=VMid).first()
            if res.strip() == "sucessful":
                status_data = {'ins_id':VMid.VM_id}
                status_data_urlencode = urllib.urlencode(status_data)
                requrl_security = "http://"+ip_value+"/"+path_value+"/"+"istl_query_host_status.py"
                conn.request(method="POST",url=requrl_security,body=status_data_urlencode,headers = headerdata)
                response = conn.getresponse()
                res_status= response.read()
                print res_status.strip()
                conn.close()
                resultstatus=VM_information.query.filter_by(VM_id=VMid.VM_id).first()
                try:
                        resultstatus.status=res_status.strip()
                        db.session.commit()
                except:
                        flash("The Database error!")
                        return redirect('/error')
                flash("hang_up vm sucessful")
                return render_template("sucessful.html")
            else:
                flash("openstack error , hang_up vm fail")
                return redirect('/error')
        if  request.form.get('submit3')=='recover':
            VMname = request.form.get('VMname')
            VMid = VM_information.query.filter(db.and_(VM_information.VM_name == VMname, VM_information.nickname == current_user.nickname)).first()
            start_data = {'ins_id':VMid.VM_id}
            start_data_urlencode = urllib.urlencode(start_data)
            requrl_security = "http://"+ip_value+"/"+path_value+"/"+"istl_nova_resumeIns.py"
            conn.request(method="POST",url=requrl_security,body=start_data_urlencode,headers = headerdata)
            response = conn.getresponse()
            res= response.read()
            conn.close()
            time.sleep(8)
            resultstatus=VM_information.query.filter_by(VM_id=VMid.VM_id).first()
            if res.strip() == "sucessful":
                status_data = {'ins_id':VMid.VM_id}
                status_data_urlencode = urllib.urlencode(status_data)
                requrl_security = "http://"+ip_value+"/"+path_value+"/"+"istl_query_host_status.py"
                conn.request(method="POST",url=requrl_security,body=status_data_urlencode,headers = headerdata)
                response = conn.getresponse()
                res_status= response.read()

                conn.close()
                try:
                        resultstatus.status=res_status.strip()
                        db.session.commit()
                except:
                        flash("The Database error!")
                        return redirect('/error')
                flash("recover vm sucessful")
                return render_template("sucessful.html",)
            else:
                flash("openstack error , recover vm fail")
                return redirect('/error')
        if  request.form.get('submit4')=='shutdown':
            VMname = request.form.get('VMname')
            VMid = VM_information.query.filter(db.and_(VM_information.VM_name == VMname, VM_information.nickname == current_user.nickname)).first()
            start_data = {'ins_id':VMid.VM_id}
            start_data_urlencode = urllib.urlencode(start_data)
            requrl_security = "http://"+ip_value+"/"+path_value+"/"+"istl_nova_stopIns.py"
            conn.request(method="POST",url=requrl_security,body=start_data_urlencode,headers = headerdata)
            response = conn.getresponse()
            res= response.read()
            conn.close()
            print res.strip()
            time.sleep(8)
            resultstatus=VM_information.query.filter_by(VM_id=VMid.VM_id).first()
            if res.strip() == "sucessful":
                status_data = {'ins_id':VMid.VM_id}
                status_data_urlencode = urllib.urlencode(status_data)
                requrl_security = "http://"+ip_value+"/"+path_value+"/"+"istl_query_host_status.py"
                conn.request(method="POST",url=requrl_security,body=status_data_urlencode,headers = headerdata)
                response = conn.getresponse()
                res_status= response.read()

                conn.close()
                try:
                        resultstatus.status=res_status.strip()
                        db.session.commit()
                except:
                        flash("The Database error!")
                        return redirect('/error')
                flash("shutdown vm sucessful")
                return render_template("sucessful.html",)
            else:
                flash("openstack error , shutdown vm fail")
                return redirect('/error')
    return render_template(
        "vm_power.html",
        form=form ,
        user_id=user_id,
        VM_Names=VM_Names
        )



@app.route('/delete_vm/<int:user_id>',  methods=["POST", "GET"])

@login_required
def delete_vm(user_id):
    form = Delete_vmForm()
    headerdata = {"Host":ip_value,"Connection":"Keep-Alive",
              "Content-Type":"application/x-www-form-urlencoded"}
    conn = httplib.HTTPConnection(ip_value)
    user_type = User.query.filter_by(id=current_user.id).first()
    if user_type.role == 1:
        select_vms =  VM_information.query.all()
    else:
        select_vms =  VM_information.query.filter_by(nickname=current_user.nickname).all()
    result = {}
    i = 0
    while  i< len(select_vms):
        result[i+1] = select_vms[i].VM_name
        i = i+1
    vms_into_json = json.dumps(result,ensure_ascii=False)
    VM_Names = json.loads(vms_into_json).values()

    if request.method == "POST":

      #if form.validate_on_submit():
        VMname = request.form.get('VMname')
        #select_info = VM_information.query.filter_by(VM_name=VMname).first()
        select_info = VM_information.query.filter(db.and_(
                VM_information.VM_name == VMname, VM_information.nickname == current_user.nickname)).first()
        delete_vm_id = select_info.VM_id
        delete_vm_floatingip = select_info.floating_ip
        delete_vm_name = VM_information.query.filter_by(VM_id=select_info.VM_id).first()
        delete_vm_securitygroup = security_group.query.filter_by(VM_id=select_info.VM_id).all()
        delete_vm_cloudvolume = cloud_volume.query.filter_by(VM_id=select_info.VM_id).all()
        delete_snapshoot_information = snapshoot_information.query.filter_by(VM_id=select_info.VM_id).all()
        delete_data = {'ins_name':VMname,'floating_ip':delete_vm_floatingip,'ins_id':delete_vm_id}
        delete_data_urlencode = urllib.urlencode(delete_data)
        requrl_dIns = "http://"+ip_value+"/"+path_value+"/"+"istl_nova_deleteIns.py"
        conn.request(method="POST",url=requrl_dIns,body=delete_data_urlencode,headers = headerdata)
        response = conn.getresponse()
        res= response.read()
        if res.strip() == "sucessful":
            try:
                flash("ok")
                db.session.delete(delete_vm_name)
                for i in range(len(delete_vm_securitygroup)):
                    db.session.delete(delete_vm_securitygroup[i])
                flash("ok")
                for i in range(len(delete_vm_cloudvolume)):
                    db.session.delete(delete_vm_cloudvolume[i])
                for i in range(len(delete_snapshoot_information)):
                    db.session.delete(delete_snapshoot_information[i])

                db.session.commit

                return render_template("sucessful.html",)
            except:
                flash("Database error")
                return render_template("error.html",)
        else:
            flash("openstack error")
            return redirect('/error')


    #conn.close()
    return render_template(
        "delete_vm.html",
        form=form ,
        user_id=user_id,
        VM_Names=VM_Names
        )






@app.route('/delete_cloud_volume/<int:user_id>',  methods=["POST", "GET"])

@login_required
def delete_cloud_volume(user_id):
    headerdata = {"Host":ip_value,"Connection":"Keep-Alive",
              "Content-Type":"application/x-www-form-urlencoded"}
    conn = httplib.HTTPConnection(ip_value)

    form = Delete_cloudvolumeForm()
    user_type = User.query.filter_by(id=current_user.id).first()
    if user_type.role == 1:
        select_vms =  VM_information.query.all()
    else:
        select_vms =  VM_information.query.filter_by(nickname=current_user.nickname).all()
    result = {}
    i = 0
    while  i< len(select_vms):
        result[i+1] = select_vms[i].VM_name
        i = i+1
    vms_into_json = json.dumps(result,ensure_ascii=False)
    VM_Names = json.loads(vms_into_json).values()


    requrl_vn = "http://"+ip_value+"/"+path_value+"/"+"istl_query_allvolumename.py"
    conn.request(method="POST",url=requrl_vn,headers = headerdata)
    response_vn = conn.getresponse()
    json_volumename = response_vn.read()
    Cloudvolume_Names = json.loads(json_volumename).values()


    if request.method == "POST":

        Cloudvolumename = request.form.get('Cloudvolumename')

      #if form.validate_on_submit():
        if  request.form.get('submit')=='submit':
            VMname = request.form.get('VMname')
            VMid = VM_information.query.filter(db.and_(VM_information.VM_name == VMname, VM_information.nickname == current_user.nickname)).first()
            volume_data = {'ins_id':VMid.VM_id,'Cloudvolumename':Cloudvolumename}
            volume_data_urlencode = urllib.urlencode(volume_data)
            requrl_security = "http://"+ip_value+"/"+path_value+"/"+"istl_delete_cloudvolume.py"
            conn.request(method="POST",url=requrl_security,body=volume_data_urlencode,headers = headerdata)
            response = conn.getresponse()
            res= response.read()
            if res.strip() == "sucessful":
                delete_vm_cloudvolume = cloud_volume.query.filter(db.and_(
                    cloud_volume.cloud_volume_name == Cloudvolumename, cloud_volume.VM_name == VMname)).first()
                if delete_vm_cloudvolume:
                    try:
                        db.session.delete(delete_vm_cloudvolume)
                        db.session.commit

                        return render_template("sucessful.html",)
                    except:
                        return render_template("error.html")
                else :
                    flash("你好，请你再次确认该云主机是否挂载这个硬盘!")
                    return render_template("error.html",)
            else:
                flash("openstack error")
                return render_template("error.html",)



    return render_template(
        "delete_cloud_volume.html",
        form=form ,
        user_id=user_id,
        VM_Names=VM_Names,
        Cloudvolume_Names=Cloudvolume_Names
        )




@app.route('/modify_user_type/<int:user_id>',  methods=["POST", "GET"])

@login_required
def modify_user_type(user_id):
    form = Modify_usertypeForm()
    select_users =  User.query.all()
    result = {}
    i = 0
    while  i< len(select_users):
        result[i+1] = select_users[i].nickname
        i = i+1
    users_into_json = json.dumps(result,ensure_ascii=False)
    User_Names = json.loads(users_into_json).values()
    USERname = request.form.get('USERname')
    usertypes_into_json = '{"name":"***","name1":"****","name2":"*****","name3":"******"}'
    Usertype_Names = json.loads(usertypes_into_json).values()

    USERtypename = request.form.get('USERtypename')
    if request.method == "POST":

        if  request.form.get('submit')=='submit':
            result_user = User.query.filter_by(nickname=USERname).first()
            try:
                result_user.type= USERtypename
                db.session.commit()

                return render_template("sucessful.html",)
            except:
                return render_template("error.html")

    return render_template(
        "modify_user_type.html",
        form=form ,
        user_id=user_id,
        User_Names=User_Names,
        Usertype_Names=Usertype_Names
        )









@app.route('/delete_security_group/<int:user_id>',  methods=["POST", "GET"])

@login_required
def delete_security_group(user_id):
    headerdata = {"Host":ip_value,"Connection":"Keep-Alive",
              "Content-Type":"application/x-www-form-urlencoded"}
    conn = httplib.HTTPConnection(ip_value)

    form = Delete_securitygroupForm()
    user_type = User.query.filter_by(id=current_user.id).first()
    if user_type.role == 1:
        select_vms =  VM_information.query.all()
    else:
        select_vms =  VM_information.query.filter_by(nickname=current_user.nickname).all()
    result = {}
    i = 0
    while  i< len(select_vms):
        result[i+1] = select_vms[i].VM_name
        i = i+1
    vms_into_json = json.dumps(result,ensure_ascii=False)
    VM_Names = json.loads(vms_into_json).values()


    requrl_s = "http://"+ip_value+"/"+path_value+"/"+"istl_query_securitygroup.py"
    conn.request(method="POST",url=requrl_s,headers = headerdata)
    response_s = conn.getresponse()
    json_security_group = response_s.read()
    Securitygroup_Names = json.loads(json_security_group).values()
    #Cloudvolumename = request.form.get('Cloudvolumename')

    if request.method == "POST":

        Securitygroupname = request.form.get('Securitygroupname')

      #if form.validate_on_submit():
        if  request.form.get('submit')=='submit':
            VMname = request.form.get('VMname')
            VMid = VM_information.query.filter(db.and_(VM_information.VM_name == VMname, VM_information.nickname == current_user.nickname)).first()
            security_data = {'ins_id':VMid.VM_id,'Securitygroupname':Securitygroupname}
            security_data_urlencode = urllib.urlencode(security_data)
            requrl_security = "http://"+ip_value+"/"+path_value+"/"+"istl_delete_securitygroup.py"
            conn.request(method="POST",url=requrl_security,body=security_data_urlencode,headers = headerdata)
            response = conn.getresponse()
            res= response.read()
            if res.strip() == "sucessful":
                delete_vm_securitygroup = security_group.query.filter(db.and_(
                    security_group.security_group_name == Securitygroupname, security_group.VM_name == VMname)).first()
                if delete_vm_securitygroup:
                    try:
                        db.session.delete(delete_vm_securitygroup)
                        db.session.commit

                        return render_template("sucessful.html",)
                    except:
                        return render_template("error.html")
                else :
                    flash("你好，请你再次确认该云主机是否已经添加这个安全组!")
                    return render_template("error.html",)
            else:
                flash("openstack error")
                return render_template("error.html",)



    return render_template(
        "delete_security_group.html",
        form=form ,
        user_id=user_id,
        VM_Names=VM_Names,
        Securitygroup_Names=Securitygroup_Names
        )






@app.route('/delete_snapshoot/<int:user_id>',  methods=["POST", "GET"])

@login_required
def delete_snapshoot(user_id):
    headerdata = {"Host":ip_value,"Connection":"Keep-Alive",
              "Content-Type":"application/x-www-form-urlencoded"}
    conn = httplib.HTTPConnection(ip_value)

    form = Delete_snapshootForm()
    user_type = User.query.filter_by(id=current_user.id).first()
    if user_type.role == 1:
        select_vms =  VM_information.query.all()
    else:
        select_vms =  VM_information.query.filter_by(nickname=current_user.nickname).all()
    result = {}
    i = 0
    while  i< len(select_vms):
        result[i+1] = select_vms[i].VM_name
        i = i+1
    vms_into_json = json.dumps(result,ensure_ascii=False)
    VM_Names = json.loads(vms_into_json).values()

    requrl_sn = "http://"+ip_value+"/"+path_value+"/"+"istl_query_snapshootname.py"
    conn.request(method="POST",url=requrl_sn,headers = headerdata)
    response_sn = conn.getresponse()
    json_snapshoot = response_sn.read()
    Snapshoot_Names = json.loads(json_snapshoot).values()


    if request.method == "POST":
      #if form.validate_on_submit():
        if  request.form.get('submit')=='submit':
            VMname = request.form.get('VMname')
            Snapshootname = request.form.get('Snapshootname')
            VMid = VM_information.query.filter(db.and_(VM_information.VM_name == VMname, VM_information.nickname == current_user.nickname)).first()
            Snapshoot_data = {'ins_id':VMid.VM_id,'Snapshootname':Snapshootname}
            Snapshoot_data_urlencode = urllib.urlencode(Snapshoot_data)
            requrl_security = "http://"+ip_value+"/"+path_value+"/"+"istl_delete_snapshoot.py"
            conn.request(method="POST",url=requrl_security,body=Snapshoot_data_urlencode,headers = headerdata)
            response = conn.getresponse()
            res= response.read()
            if res.strip() == "sucessful":
                delete_vm_snapshoot = snapshoot_information.query.filter(db.and_(
                    snapshoot_information.snapshoot_name == Snapshootname, snapshoot_information.VM_name == VMname)).first()
                if delete_vm_snapshoot:
                    try:
                        db.session.delete(delete_vm_snapshoot)
                        db.session.commit
                        flash("删除快照:"+Snapshootname)
                        return render_template("sucessful.html",)
                    except:
                        return render_template("error.html")
                else :
                    flash("你好，该云主机没有这个快照!")
                    return render_template("error.html",)
            else :
                    flash("openstack error")
                    return render_template("error.html",)
    return render_template(
        "delete_snapshoot.html",
        form=form ,
        user_id=user_id,
        VM_Names=VM_Names,
        Snapshoot_Names=Snapshoot_Names
        )





@app.route('/recover_snapshoot/<int:user_id>',  methods=["POST", "GET"])

@login_required
def recover_snapshoot(user_id):
    form = Recover_snapshootForm()
    headerdata = {"Host":ip_value,"Connection":"Keep-Alive",
              "Content-Type":"application/x-www-form-urlencoded"}
    conn = httplib.HTTPConnection(ip_value)

    user_type = User.query.filter_by(id=current_user.id).first()
    if user_type.role == 1:
        select_vms =  VM_information.query.all()
    else:
        select_vms =  VM_information.query.filter_by(nickname=current_user.nickname).all()
    result = {}
    i = 0
    while  i< len(select_vms):
        result[i+1] = select_vms[i].VM_name
        i = i+1
    vms_into_json = json.dumps(result,ensure_ascii=False)
    VM_Names = json.loads(vms_into_json).values()
    VMname = request.form.get('VMname')
    '''
    json_snapshoot = '{"name":"snapshoot_1","name1":"snapshoot_2"}'
    Snapshoot_Names = json.loads(json_snapshoot).values()
    '''
    requrl_sn = "http://"+ip_value+"/"+path_value+"/"+"istl_query_snapshootname.py"
    conn.request(method="POST",url=requrl_sn,headers = headerdata)
    response_sn = conn.getresponse()
    json_snapshoot = response_sn.read()
    Snapshoot_Names = json.loads(json_snapshoot).values()


    flash(VMname)
    if request.method == "POST":

        if  request.form.get('submit')=='submit':
            VMname = request.form.get('VMname')
            Snapshootname = request.form.get('Snapshootname')
            VMid = VM_information.query.filter(db.and_(VM_information.VM_name == VMname, VM_information.nickname == current_user.nickname)).first()
            Snapshoot_data = {'ins_id':VMid.VM_id,'Snapshootname':Snapshootname}
            Snapshoot_data_urlencode = urllib.urlencode(Snapshoot_data)
            requrl_security = "http://"+ip_value+"/"+path_value+"/"+"istl_recover_snapshoot.py"
            conn.request(method="POST",url=requrl_security,body=Snapshoot_data_urlencode,headers = headerdata)
            response = conn.getresponse()
            res= response.read()
            if res.strip() == "sucessful":

                flash("恢复到快照:"+Snapshootname)
                return render_template("sucessful.html")
            else:
                flash("openstack error")
                return render_template("error.html")

    return render_template(
        "recover_snapshoot.html",
        form=form ,
        user_id=user_id,
        VM_Names=VM_Names,
        Snapshoot_Names=Snapshoot_Names
        )



@app.route('/add_vm_security_group/<int:user_id>',  methods=["POST", "GET"])

@login_required
def add_vm_security_group(user_id):
    form = Add_vm_security_groupForm()
    headerdata = {"Host":ip_value,"Connection":"Keep-Alive",
              "Content-Type":"application/x-www-form-urlencoded"}
    conn = httplib.HTTPConnection(ip_value)

    user_type = User.query.filter_by(id=current_user.id).first()
    if user_type.role == 1:
        select_vms =  VM_information.query.all()
    else:
        select_vms =  VM_information.query.filter_by(nickname=current_user.nickname).all()
    result = {}
    i = 0
    while  i< len(select_vms):
        result[i+1] = select_vms[i].VM_name
        i = i+1
    vms_into_json = json.dumps(result,ensure_ascii=False)
    VM_Names = json.loads(vms_into_json).values()
    '''
    json_security_group = '{"name":"group_1","name1":"group_2"}'
    Security_group_Names = json.loads(json_security_group).values()
    '''
    requrl_s = "http://"+ip_value+"/"+path_value+"/"+"istl_query_securitygroup.py"
    conn.request(method="POST",url=requrl_s,headers = headerdata)
    response_s = conn.getresponse()
    json_security_group = response_s.read()
    Security_group_Names = json.loads(json_security_group).values()
    '''
    json_security_group_type = '{"name":"smtp","name1":"dns"}'
    Security_group_type_Names = json.loads(json_security_group_type).values()
    '''
    requrl_sn = "http://"+ip_value+"/"+path_value+"/"+"istl_query_securitygroupname.py"
    conn.request(method="POST",url=requrl_sn,headers = headerdata)
    response_sn = conn.getresponse()
    json_security_group_type = response_sn.read()
    Security_group_type_Names = json.loads(json_security_group_type).values()

    if request.method == "POST" :
        flash("okok")
      #if form.validate_on_submit():
        VMname = request.form.get('VMname')
        VMsecurity_group = request.form.get('Securitygroupname')
        VMsecurity_group_type = request.form.get('Securitygrouptypename')
        if  request.form.get('submit')=='submit':
            VMid = VM_information.query.filter(db.and_(VM_information.VM_name == VMname, VM_information.nickname == current_user.nickname)).first()
            security_data = {'ins_id':VMid.VM_id,'Securitygroupname':VMsecurity_group,'Securitygrouptypename':VMsecurity_group_type}
            security_data_urlencode = urllib.urlencode(security_data)
            requrl_security = "http://"+ip_value+"/"+path_value+"/"+"istl_add_securitygroup.py"
            conn.request(method="POST",url=requrl_security,body=security_data_urlencode,headers = headerdata)
            response = conn.getresponse()
            res= response.read()
            #list_response = res.split()
            #status = list_response[1]
            status = res.strip()

            if status == "sucessful":
                try:

                    inset = security_group(security_group_id=VMsecurity_group,VM_id = VMid.VM_id, VM_name = VMname,
                                        security_group_name = VMsecurity_group,
                                        security_group_type = VMsecurity_group_type)
                    db.session.add(inset)
                    db.session.commit()

                    return render_template("sucessful.html",)
                except:
                    flash("database error")
                    return render_template("error.html",)
            else:
                flash("openstack error")
                return render_template("error.html",)



    return render_template(
        "security_group.html",
        form=form ,
        user_id=user_id,
        VM_Names=VM_Names,
        Security_group_Names = Security_group_Names,
        Security_group_type_Names =Security_group_type_Names
        )




@app.route('/add_snapshoot/<int:user_id>',  methods=["POST", "GET"])

@login_required
def add_snapshoot(user_id):
    form = Add_vm_snapshootForm()

    user_type = User.query.filter_by(id=current_user.id).first()
    if user_type.role == 1:
        select_vms =  VM_information.query.all()
    else:
        select_vms =  VM_information.query.filter_by(nickname=current_user.nickname).all()
    result = {}
    i = 0
    while  i< len(select_vms):
        result[i+1] = select_vms[i].VM_name
        i = i+1
    vms_into_json = json.dumps(result,ensure_ascii=False)
    VM_Names = json.loads(vms_into_json).values()

    if request.method == "POST" :

      #if form.validate_on_submit():
        VMname = request.form.get('VMname')
        VMsnapshoot = request.form.get('snapshoot_name')
        describe = request.form.get('PickupAddress')

        if  request.form.get('submit')=='submit':
            VMid = VM_information.query.filter(db.and_(VM_information.VM_name == VMname, VM_information.nickname == current_user.nickname)).first()
            snapshoot_data = {'ins_id':VMid.VM_id,'snapshoot_name':VMsnapshoot}
            snapshoot_data_urlencode = urllib.urlencode(snapshoot_data)
            requrl_snapshoot = "http://"+ip_value+"/"+path_value+"/"+"istl_add_snapshoot.py"
            conn.request(method="POST",url=requrl_snapshoot,body=snapshoot_data_urlencode,headers = headerdata)
            response = conn.getresponse()
            res= response.read()
            list_response = res.split()
            status = list_response[1]

            if status == "sucessful":
                try:

                    inset = snapshoot_information(snapshoot_id=list_response[0],VM_id = VMid.VM_id, VM_name = VMname,
                                        snapshoot_name = VMsnapshoot,
                                        snapshoot_describe = describe)
                    db.session.add(inset)
                    db.session.commit()

                    return render_template("sucessful.html",)
                except:
                    return render_template("error.html",)
            else:
                flash("openstack error")
                return render_template("error.html")



    return render_template(
        "add_snapshoot.html",
        form=form ,
        user_id=user_id,
        VM_Names=VM_Names,


        )



@app.route('/add_vm_cloud_volume/<int:user_id>',  methods=["POST", "GET"])

@login_required
def add_vm_cloud_volume(user_id):
    form = Add_vm_cloud_volumeForm
    headerdata = {"Host":ip_value,"Connection":"Keep-Alive",
              "Content-Type":"application/x-www-form-urlencoded"}
    conn = httplib.HTTPConnection(ip_value)

    user_type = User.query.filter_by(id=current_user.id).first()
    if user_type.role == 1:
        select_vms =  VM_information.query.all()
    else:
        select_vms =  VM_information.query.filter_by(nickname=current_user.nickname).all()
    result = {}
    i = 0
    while  i< len(select_vms):
        result[i+1] = select_vms[i].VM_name
        i = i+1
    vms_into_json = json.dumps(result,ensure_ascii=False)
    VM_Names = json.loads(vms_into_json).values()


    requrl_vn = "http://"+ip_value+"/"+path_value+"/"+"istl_query_volumename.py"
    conn.request(method="POST",url=requrl_vn,headers = headerdata)
    response_vn = conn.getresponse()
    json_volumename = response_vn.read()
    Cloud_volume_Names = json.loads(json_volumename).values()


    requrl_vt = "http://"+ip_value+"/"+path_value+"/"+"istl_query_volumetype.py"
    conn.request(method="POST",url=requrl_vt,headers = headerdata)
    response_vt = conn.getresponse()
    json_volumetype= response_vt.read()
    Cloud_volume_type_Names = json.loads(json_volumetype).values()
    if request.method == "POST" :

      #if form.validate_on_submit():
        VMname = request.form.get('VMname')
        VMcloud_volume = request.form.get('Cloudvolumename')
        VMcloud_volume_type = request.form.get('Cloudvolumetypename')

        if  request.form.get('submit')=='submit':

            VMid = VM_information.query.filter(db.and_(VM_information.VM_name == VMname, VM_information.nickname == current_user.nickname)).first()
            cloudgroup_data = {'ins_id':VMid.VM_id,'Cloudvolumename':VMcloud_volume}
            cloudgroup_data_urlencode = urllib.urlencode(cloudgroup_data)
            requrl_cloudgroup = "http://"+ip_value+"/"+path_value+"/"+"istl_add_cloudvolume.py"
            conn.request(method="POST",url=requrl_cloudgroup,body=cloudgroup_data_urlencode,headers = headerdata)
            response = conn.getresponse()
            res= response.read()
            #list_response = res.split()
            #status = list_response[2]
            status = res.strip()
            print status
            if status == "sucessful":
                try:

                    inset = cloud_volume(cloud_volume_id=VMcloud_volume,VM_id = VMid.VM_id, VM_name = VMname,
                                        cloud_volume_name = VMcloud_volume,
                                        cloud_volume_type = VMcloud_volume_type,
                                        cloud_volume_size = 10)
                    db.session.add(inset)
                    db.session.commit()

                    return render_template("sucessful.html",)
                except:
                    return render_template("error.html",)
            else:
                flash("openstack error")
                return render_template("error.html",)



    return render_template(
        "cloud_volume.html",
        form=form ,
        user_id=user_id,
        VM_Names=VM_Names,
        Cloud_volume_Names = Cloud_volume_Names,
        Cloud_volume_type_Names =Cloud_volume_type_Names
        )







@app.route('/vm_security_group/<int:user_id>',  methods=["POST", "GET"])

@login_required
def vm_security_group(user_id):
    form = Vm_security_groupForm()
    user_type = User.query.filter_by(id=current_user.id).first()
    if user_type.role == 1:
        select_vms =  VM_information.query.all()
    else:
        select_vms =  VM_information.query.filter_by(nickname=current_user.nickname).all()
    result = {}
    i = 0
    while  i< len(select_vms):
        result[i+1] = select_vms[i].VM_name
        i = i+1
    vms_into_json = json.dumps(result,ensure_ascii=False)
    VM_Names = json.loads(vms_into_json).values()

    if request.method == "POST":

      #if form.validate_on_submit():
        VMname = request.form.get('VMname')
        if  request.form.get('submit')=='submit':
            select_=security_group.query.filter_by(VM_name=VMname).all()
            machines = []
            for i in range(len(select_)):

                machines.append({'ID':i,'hostname' : select_[i].VM_name,
                                'security group name' : select_[i].security_group_name,
                                'security group type' : select_[i].security_group_type})



        return render_template(
        "vm_security_group.html",
        form=form ,
        user_id=user_id,
        VM_Names=VM_Names,
        machines=machines
        )


    return render_template(
        "vm_security_group.html",
        form=form ,
        user_id=user_id,
        VM_Names=VM_Names
        )






@app.route('/vm_snapshoot/<int:user_id>',  methods=["POST", "GET"])

@login_required
def vm_snapshoot(user_id):
    form = Vm_snapshootForm()
    user_type = User.query.filter_by(id=current_user.id).first()
    if user_type.role == 1:
        select_vms =  VM_information.query.all()
    else:
        select_vms =  VM_information.query.filter_by(nickname=current_user.nickname).all()
    result = {}
    i = 0
    while  i< len(select_vms):
        result[i+1] = select_vms[i].VM_name
        i = i+1
    vms_into_json = json.dumps(result,ensure_ascii=False)
    VM_Names = json.loads(vms_into_json).values()

    if request.method == "POST":

      #if form.validate_on_submit():
        VMname = request.form.get('VMname')
        if  request.form.get('submit')=='inquire':
            select_=snapshoot_information.query.filter_by(VM_name=VMname).all()
            machines = []
            for i in range(len(select_)):

                machines.append({'ID':i,'hostname' : select_[i].VM_name,
                                'snapshoot name' : select_[i].snapshoot_name,
                                'snapshoot describe' : select_[i].snapshoot_describe})



        return render_template(
        "snapshoot.html",
        form=form ,
        user_id=user_id,
        VM_Names=VM_Names,
        machines=machines
        )


    return render_template(
        "snapshoot.html",
        form=form ,
        user_id=user_id,
        VM_Names=VM_Names
        )





@app.route('/vm_cloud_volume/<int:user_id>',  methods=["POST", "GET"])

@login_required
def vm_cloud_volume(user_id):
    form = Vm_cloud_volumeForm()
    user_type = User.query.filter_by(id=current_user.id).first()
    if user_type.role == 1:
        select_vms =  VM_information.query.all()
    else:
        select_vms =  VM_information.query.filter_by(nickname=current_user.nickname).all()
    result = {}
    i = 0
    while  i< len(select_vms):
        result[i+1] = select_vms[i].VM_name
        i = i+1
    vms_into_json = json.dumps(result,ensure_ascii=False)
    VM_Names = json.loads(vms_into_json).values()

    if request.method == "POST":

      #if form.validate_on_submit():
        VMname = request.form.get('VMname')
        if  request.form.get('submit')=='submit':
            select_=cloud_volume.query.filter_by(VM_name=VMname).all()
            machines = []
            for i in range(len(select_)):

                machines.append({'ID':i,'hostname' : select_[i].VM_name,
                                'cloud volume name' : select_[i].cloud_volume_name,
                                'cloud volume type' : select_[i].cloud_volume_type,
                                 'cloud volume size' : select_[i].cloud_volume_size})




        return render_template(
        "vm_cloud_volume.html",
        form=form ,
        user_id=user_id,
        VM_Names=VM_Names,
        machines=machines
        )


    return render_template(
        "vm_cloud_volume.html",
        form=form ,
        user_id=user_id,
        VM_Names=VM_Names
        )



@app.route('/delete_user/<int:user_id>',  methods=["POST", "GET"])

@login_required
def delete_user(user_id):

    form = Delete_UserForm()
    select_names =  User.query.filter_by(role=0).all()
    result = {}
    i = 0
    while  i< len(select_names):
        result[i+1] = select_names[i].nickname
        i = i+1


    names_into_json = json.dumps(result,ensure_ascii=False)

    USER_Names = json.loads(names_into_json).values()

    if request.method == "POST":

      if  request.form.get('submit')=='submit':
        UserName = request.form.get('UserName')

        delete_user_name = User.query.filter_by(nickname=UserName).first()
        delete_Vm_Iformation = VM_information.query.filter_by(nickname=UserName).all()




        for i in range(len(delete_Vm_Iformation)):

            select_info = VM_information.query.filter(db.and_(
                    VM_information.VM_name == delete_Vm_Iformation[i].VM_name, VM_information.nickname == UserName)).first()
            delete_vm_id = select_info.VM_id
            delete_vm_name = VM_information.query.filter_by(VM_id=select_info.VM_id).first()
            delete_vm_securitygroup = security_group.query.filter_by(VM_id=select_info.VM_id).all()
            delete_vm_cloudvolume = cloud_volume.query.filter_by(VM_id=select_info.VM_id).all()
            delete_snapshoot_information = snapshoot_information.query.filter_by(VM_id=select_info.VM_id).all()

            delete_data = {'ins_name':delete_Vm_Iformation[i].VM_name,'ins_id':delete_vm_id}
            delete_data_urlencode = urllib.urlencode(delete_data)
            requrl_dIns = "http://"+ip_value+"/"+path_value+"/"+"istl_nova_deleteIns.py"
            conn.request(method="POST",url=requrl_dIns,body=delete_data_urlencode,headers = headerdata)
            response = conn.getresponse()
            res= response.read()
            if res.strip() == "sucessful":
                try:

                    db.session.delete(delete_vm_name)
                    for j in range(len(delete_vm_securitygroup)):
                        db.session.delete(delete_vm_securitygroup[j])

                    for k in range(len(delete_vm_cloudvolume)):
                        db.session.delete(delete_vm_cloudvolume[k])
                    for g in range(len(delete_snapshoot_information)):
                        db.session.delete(delete_snapshoot_information[g])

                    db.session.commit


                except:
                    flash("Database error")
                    return render_template("error.html",)
            else:
                flash("openstack error")
                return redirect('/error')

        try:

                db.session.delete(delete_user_name)

                db.session.commit

        except:
                return render_template("error.html")

        flash("sucessful!!!")
        return render_template("sucessful.html")


    return render_template(
        "delete_user.html",
        form=form ,
        user_id=user_id,
        USER_Names=USER_Names
        )




@app.route('/modify/<int:user_id>', methods=['GET', 'POST'])
def modify(user_id):
    form =ModifyForm()
    headerdata = {"Host":ip_value,"Connection":"Keep-Alive",
              "Content-Type":"application/x-www-form-urlencoded"}
    conn = httplib.HTTPConnection(ip_value)
    user_type = User.query.filter_by(id=current_user.id).first()
    if user_type.role == 1:
        select_vms =  VM_information.query.all()
    else:
        select_vms =  VM_information.query.filter_by(nickname=current_user.nickname).all()
    result_dict = {}
    i = 0
    while  i< len(select_vms):
        result_dict[i+1] = select_vms[i].VM_name
        i = i+1
    vms_into_json = json.dumps(result_dict,ensure_ascii=False)
    VM_Names = json.loads(vms_into_json).values()

    requrl_ip = "http://"+ip_value+"/"+path_value+"/"+"istl_query_host_floatingip.py"
    conn.request(method="POST",url=requrl_ip,headers = headerdata)
    response_ip = conn.getresponse()
    json_floatingip = response_ip.read()
    VM_Floatingips = json.loads(json_floatingip).values()



    requrl_f = "http://"+ip_value+"/"+path_value+"/"+"istl_query_host_flavor.py"
    conn.request(method="POST",url=requrl_f,headers = headerdata)
    response_f = conn.getresponse()
    json_flavor = response_f.read()
    VM_Flavors = json.loads(json_flavor).values()

    #if form.validate_on_submit():
    if request.method == "POST":
        if  request.form.get('submit')=='submit':
            vm_name = request.form.get('vm_name')
            client_mac = request.form.get('client_mac')
            current_VMname = request.form.get('VMname')
            vm_rent_time = request.form.get('vm_rent_time')
            VMfloatingip = request.form.get('VMfloatingip')
            vm_flavor = request.form.get('VMflavor')
            result = VM_information.query.filter(db.and_(VM_information.VM_name == current_VMname, VM_information.nickname == current_user.nickname)).first()
            modify_vmid = result.VM_id
            result1 = cloud_volume.query.filter_by(VM_id=modify_vmid).first()
            result2 = security_group.query.filter_by(VM_id=modify_vmid).first()
            #result3 = snapshoot_information.query.filter_by(VM_id=modify_vmid).first()
                #result = VM_information.query.filter_by(VM_name=current_VMname).first()
                #if  request.form.get('submit')=='submit':

            if len(vm_name):
                modify_data = {'ins_id':modify_vmid,'ins_newname':vm_name}
                modify_data_urlencode = urllib.urlencode(modify_data)
                requrl_mIns = "http://"+ip_value+"/"+path_value+"/"+"istl_nova_modifyInsname.py"
                conn.request(method="POST",url=requrl_mIns,body=modify_data_urlencode,headers = headerdata)
                response_mIns = conn.getresponse()
                res= response_mIns.read()
                conn.close()
                print res
                if res.strip() == "sucessful" :
                    try:
                        result.VM_name=vm_name
                        result1.VM_name=vm_name
                        result2.VM_name=vm_name
                        #result3.VM_name=vm_name
                        db.session.commit()
                    except:
                        flash("The Database error!")
                        return redirect('/error')
                else:
                    flash("openstack error")
                    return redirect('/error')

            if len(client_mac):
                try:
                    result.client_mac=client_mac
                    db.session.commit()
                except:
                    flash("The Database error!")
                    return redirect('/error')
            if len(vm_rent_time):
                try:
                    result.rent_time=vm_rent_time
                    db.session.commit()
                except:
                    flash("The Database error!")
                    return redirect('/error')

            if len(vm_flavor) and vm_flavor != result.flavor:
                modify_data = {'ins_id':modify_vmid,'flavor':vm_flavor}
                modify_data_urlencode = urllib.urlencode(modify_data)
                requrl_mIns = "http://"+ip_value+"/"+path_value+"/"+"istl_nova_modifyInsflavor.py"
                conn.request(method="POST",url=requrl_mIns,body=modify_data_urlencode,headers = headerdata)
                response_mIns = conn.getresponse()
                res= response_mIns.read()
                conn.close()
                print res
                if res.strip() == "sucessful" :

                    try:
                        result.flavor=vm_flavor
                        db.session.commit()
                    except:
                        flash("The Database error!")
                        return redirect('/error')
                else:
                    flash(res.strip())
                    return redirect('/error')
            '''
            if len(VMfloatingip) and VMfloatingip != result.floating_ip:
                modify_data = {'ins_id':modify_vmid,'old_floating_ip':result.floating_ip,'floating_ip':VMfloatingip}
                modify_data_urlencode = urllib.urlencode(modify_data)
                requrl_mIns = "http://"+ip_value+"/"+path_value+"/"+"istl_nova_modifyInsfip.py"
                conn.request(method="POST",url=requrl_mIns,body=modify_data_urlencode,headers = headerdata)
                response_mIns = conn.getresponse()
                res= response_mIns.read()
                conn.close()
                if res.strip() == "sucessful" :

                    try:
                        result.floating_ip=VMfloatingip
                        db.session.commit()
                    except:
                        flash("The Database error!")
                        return redirect('/error')
                else:
                    flash(res.strip())
                    return redirect('/error')
            else:
                flash("modify vm fail")
                return redirect('/error')
            '''
            flash("modify successful!")
            return render_template("sucessful.html")

    #conn.close()
    return render_template(
        "modify.html",
        form=form,
        user_id=user_id,
        VM_Names=VM_Names,
        VM_Flavors=VM_Flavors,
        VM_Floatingips=VM_Floatingips)



@app.route('/create-vm', methods=['GET', 'POST'])
def create():
    form =CreateForm()
    select_=User.query.filter_by(id=current_user.id).first()
    headerdata = {"Host":ip_value,"Connection":"Keep-Alive",
              "Content-Type":"application/x-www-form-urlencoded"}
    conn = httplib.HTTPConnection(ip_value)

    if request.method == "POST":
    #if form.validate_on_submit():
        nickname = select_.nickname
        vm_name = request.form.get('vm_name')
        vm_number = request.form.get('vm_number')
        client_mac = request.form.get('client_mac')
        vm_network = request.form.get('VMnetwork')
        vm_rent_time = request.form.get('vm_rent_time')

        vm_key = request.form.get('VMkey')
        vm_image = request.form.get('VMimage')
        vm_flavor = request.form.get('VMflavor')
        filedata = request.form.get('PickupAddress')
        vm_image_type = request.form.get('VMimage_type')
        vm_float_ip = request.form.get('VMfloatingip')
        register_check = VM_information.query.filter(db.and_(
            VM_information.nickname == nickname, VM_information.VM_name == vm_name)).first()
        if register_check:
            flash("error: The user's name of vm already exists!")
            return redirect('/create-vm')


        create_data = {'ins_name':vm_name,'image':vm_image,'flavor':vm_flavor,
                       'key_name':vm_key,'network':vm_network,
                       'vm_number':vm_number,'filedata':filedata}

        if vm_image_type == "linux" :



            create_data_urlencode = urllib.urlencode(create_data)
            requrl_cIns = "http://"+ip_value+"/"+path_value+"/"+"istl_nova_createIns.py"
            conn.request(method="POST",url=requrl_cIns,body=create_data_urlencode,headers = headerdata)
            response_create = conn.getresponse()
            res_create= response_create.read()
            vm_id = res_create.strip()
            print vm_id
            time.sleep(10)
            conn.close()
            print "watting!"
            time.sleep(10)
        else:

            create_data_urlencode = urllib.urlencode(create_data)
            requrl_cIns = "http://"+ip_value+"/"+path_value+"/"+"istl_nova_createwinIns.py"
            conn.request(method="POST",url=requrl_cIns,body=create_data_urlencode,headers = headerdata)
            response_create = conn.getresponse()
            res_create= response_create.read()
            vm_id = res_create.strip()
            print vm_id
            time.sleep(10)
            conn.close()
            print "watting!"
            time.sleep(30)

        status_data = {'ins_id':vm_id}

        status_data_urlencode = urllib.urlencode(status_data)
        requrl_status = "http://"+ip_value+"/"+path_value+"/"+"istl_query_host_status.py"
        conn.request(method="POST",url=requrl_status,body=status_data_urlencode,headers = headerdata)
        response_status = conn.getresponse()
        res_status= response_status.read()
        vm_status = res_status.strip()
        conn.close()
        print vm_status

        float_data = {'ins_id':vm_id,'floating_ip':vm_float_ip}
        float_data_urlencode = urllib.urlencode(float_data)
        requrl_float = "http://"+ip_value+"/"+path_value+"/"+"istl_nova_addflaotip.py"
        conn.request(method="POST",url=requrl_float,body=float_data_urlencode,headers = headerdata)
        response_float = conn.getresponse()
        res_float= response_float.read()
        vm_float = res_float.strip()
        conn.close()
        print vm_float

        if vm_status == "ACTIVE" and vm_float=="sucessful":
            try:
                inset=VM_information(nickname = nickname, VM_name = vm_name, client_mac = client_mac,
                                     ip = vm_network,VM_id = vm_id,floating_ip = vm_float_ip,key = vm_key,
                                     image = vm_image,image_type = vm_image_type,status = vm_status,flavor = vm_flavor,
                                     rent_time = vm_rent_time)

                db.session.add(inset)
                db.session.commit()

            except:
                flash("The Database error!")
                return redirect('/error')

            flash("Sign up successful!")
            return render_template("sucessful.html")
        else:
            flash("create vm fail")
            return redirect('/error')





    requrl_i = "http://"+ip_value+"/"+path_value+"/"+"istl_query_host_image.py"
    conn.request(method="POST",url=requrl_i,headers = headerdata)
    response_i = conn.getresponse()
    json_image= response_i.read()
    VM_Images = json.loads(json_image).values()



    requrl_f = "http://"+ip_value+"/"+path_value+"/"+"istl_query_host_flavor.py"
    conn.request(method="POST",url=requrl_f,headers = headerdata)
    response_f = conn.getresponse()
    json_flavor = response_f.read()
    VM_Flavors = json.loads(json_flavor).values()




    requrl_n = "http://"+ip_value+"/"+path_value+"/"+"istl_query_host_network.py"
    conn.request(method="POST",url=requrl_n,headers = headerdata)
    response_n = conn.getresponse()
    json_network = response_n.read()
    VM_Networks = json.loads(json_network).values()



    requrl_ip = "http://"+ip_value+"/"+path_value+"/"+"istl_query_host_floatingip.py"
    conn.request(method="POST",url=requrl_ip,headers = headerdata)
    response_ip = conn.getresponse()
    json_floatingip = response_ip.read()
    VM_Floatingips = json.loads(json_floatingip).values()




    requrl_k = "http://"+ip_value+"/"+path_value+"/"+"istl_query_host_key.py"
    conn.request(method="POST",url=requrl_k,headers = headerdata)
    response_k = conn.getresponse()
    json_key = response_k.read()
    VM_Keys = json.loads(json_key).values()


    json_vm_image_type = '{"name1":"linux","name2":"windows"}'
    VM_Images_type = json.loads(json_vm_image_type).values()
    #conn.close()
    return render_template(
        "create.html",
        form=form,
        VM_Flavors=VM_Flavors,
        VM_Images=VM_Images,
        VM_Networks=VM_Networks,
        VM_Floatingips=VM_Floatingips,
        VM_Keys=VM_Keys,
        VM_Images_type=VM_Images_type)



@app.route('/publish/<int:user_id>', methods=["POST", "GET"])
@login_required
def publish(user_id):
    form = PublishBlogForm()
    posts = Post()
    if form.validate_on_submit():
        blog_body = request.form.get("body")
        if not len(strip(blog_body)):
            flash("The content is necessray!")
            return redirect(url_for("publish", user_id=user_id))
        posts.body = blog_body
        posts.timestamp = datetime.datetime.now()
        posts.user_id = user_id

        try:
            db.session.add(posts)
            db.session.commit()
        except:
            flash("Database error!")
            return redirect(url_for("publish", user_id=user_id))

        flash("Publish Successful!", "success")
        return redirect(url_for("publish", user_id=user_id))

    return render_template(
        "publish.html",
        form=form)





@app.route('/user/about-me/<int:user_id>', methods=["POST", "GET"])
@login_required
def about_me(user_id):
    user = User.query.filter(User.id == user_id).first()
    if request.method == "POST":
        content = request.form.get("describe")
        if len(content) and len(content) <= 140:
            user.about_me = content
            try:
                db.session.add(user)
                db.session.commit()
            except:
                flash("Database error!")
                return redirect(url_for("users", user_id=user_id))
        else:
            flash("Sorry, May be your data have some error.")
    return redirect(url_for("users", user_id=user_id))



@app.route('/admin/<int:user_id>', defaults={'des_user_id' : -1}, methods=['GET', 'POST'])
@app.route('/admin/<int:user_id>/<int:des_user_id>/', methods=['GET', 'POST'])
@login_required
def admin(user_id,des_user_id):
    users = User.get_users()
    if user_id != current_user.id:
        flash("bad request", "error")
        return redirect("/index")
    if request.method == "POST" and request.form['modify']=='delete':
        return redirect(url_for('manage', user_id = des_user_id))

    return render_template(
        "admin.html",
        users = users,
        )
