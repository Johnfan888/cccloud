# -*- coding:utf-8 -*-

from flask_wtf import FlaskForm
from wtforms import TextField, BooleanField, SubmitField, TextAreaField, PasswordField,SelectField
from wtforms.validators import Required, Email, Length


class LoginForm(FlaskForm):
    user_passwd = PasswordField('password', validators=[
        Required(), Length(min=6)])
    user_name = TextField('user name', validators=[
        Required(), Length(max=15)])
    remember_me = BooleanField('remember me', default=False)
    submit = SubmitField('Log in')


class SignUpForm(FlaskForm):
    user_passwd = TextField('password', validators=[
        Required(), Length(min=6)])
    user_name = TextField('user name', validators=[
        Required(), Length(max=15)])
    user_email = TextField('user email', validators=[
        Email(), Required(), Length(max=128)])
    submit = SubmitField('Sign up')


class PublishBlogForm(FlaskForm):
    body = TextAreaField('blog content', validators=[Required()])
    submit = SubmitField('Submit')


class AboutMeForm(FlaskForm):
    describe = TextAreaField('about me', validators=[
        Required(), Length(max=140)])
    submit = SubmitField('YES!')


class ManageForm(FlaskForm):
    submit = SubmitField('modify')


class Delete_cloudvolumeForm(FlaskForm):
    VMname = SelectField('VM`s name', validators=[ Required(),Length(max=15)])
    Cloudvolumename = SelectField('cloudvolume`s name', validators=[ Required(),Length(max=15)])
    submit = SubmitField('submit')


class Modify_usertypeForm(FlaskForm):
    USERname = SelectField('user`s name', validators=[ Required(),Length(max=15)])
    USERtypename = SelectField('usertype`s name', validators=[ Required(),Length(max=15)])
    submit = SubmitField('submit')



class Delete_securitygroupForm(FlaskForm):
    VMname = SelectField('VM`s name', validators=[ Required(),Length(max=15)])
    Securitygroupname = SelectField('securitygroupname`s name', validators=[ Required(),Length(max=15)])
    submit = SubmitField('submit')

class Delete_snapshootForm(FlaskForm):
    VMname = SelectField('VM`s name', validators=[ Required(),Length(max=15)])
    Snapshootname = SelectField('Snapshoot name', validators=[ Required(),Length(max=15)])
    submit = SubmitField('submit')


class Recover_snapshootForm(FlaskForm):
    VMname = SelectField('VM`s name', validators=[ Required(),Length(max=15)])
    Snapshootname = SelectField('Snapshoot name', validators=[ Required(),Length(max=15)])
    submit = SubmitField('submit')

class Delete_vmForm(FlaskForm):
    VMname = SelectField('VM`s name', validators=[ Required(),Length(max=15)])
    submit = SubmitField('submit')


class vm_powerForm(FlaskForm):
    VMname = SelectField('VM`s name', validators=[ Required(),Length(max=15)])
    submit1 = SubmitField('submit1')
    submit2 = SubmitField('submit2')
    submit3 = SubmitField('submit3')
    submit4 = SubmitField('submit4')

class Vm_security_groupForm(FlaskForm):
    VMname = SelectField('VM`s name', validators=[ Required(),Length(max=15)])
    submit = SubmitField('submit')

class Vm_snapshootForm(FlaskForm):
    VMname = SelectField('VM`s name', validators=[ Required(),Length(max=15)])
    submit = SubmitField('submit')


class Vm_cloud_volumeForm(FlaskForm):
    VMname = SelectField('VM`s name', validators=[ Required(),Length(max=15)])
    submit = SubmitField('submit')

class Add_vm_security_groupForm(FlaskForm):
    VMname = SelectField('VM`s name', validators=[ Required(),Length(max=15)])
    Securitygroupname = SelectField('Securitygroup name', validators=[ Required(),Length(max=15)])
    Securitygrouptypename = SelectField('Securitygrouptype name', validators=[ Required(),Length(max=15)])
    submit = SubmitField('submit')

class Add_vm_snapshootForm(FlaskForm):
    VMname = SelectField('VM`s name', validators=[ Required(),Length(max=15)])
    snapshoot_name = TextField('snapshoot_name', validators=[
        Required(), Length(max=15)])

    PickupAddress = TextAreaField("PickupAddress", validators=[Length(max=150)])
    submit = SubmitField('submit')

class Add_vm_cloud_volumeForm(FlaskForm):
    VMname = SelectField('VM`s name', validators=[ Required(),Length(max=15)])
    Cloudvolumename = SelectField('Cloudvolume name', validators=[ Required(),Length(max=15)])
    Cloudvolumenametypename = SelectField('Cloudvolumenametype name', validators=[ Required(),Length(max=15)])
    submit = SubmitField('submit')


class Delete_UserForm(FlaskForm):
    UserName = SelectField('User`s name', validators=[ Required(),Length(max=15)])
    submit = SubmitField('submit')



'''
class CreateForm(Form):
    name = TextField('name',validators=[ Required()])
    submit = SubmitField('create')
'''







class CreateForm(FlaskForm):
    vm_number = TextField('vm_number', validators=[
        Required(), Length(min=1)])
    vm_rent_time = TextField('vm_rent_time', validators=[
        Required(), Length(min=1)])

    vm_name = TextField('vm_name', validators=[
        Required(), Length(max=15)])
    client_mac = TextField('client_mac', validators=[
        Required(), Length(max=15)])
    VMnetwork = SelectField('VMnetwork', validators=[
        Required(), Length(max=15)])
    VMfloatingip = SelectField('VMfloatingip', validators=[
         Length(max=15)])
    VMflavor = SelectField('VMflavor', validators=[
        Required(), Length(max=15)])
    VMkey = SelectField('VMkey', validators=[
        Required(), Length(max=15)])
    VMimage = SelectField('VMimage', validators=[
        Required(), Length(max=15)])
    VMimage_type = SelectField('VMimage_type', validators=[
        Required(), Length(max=15)])
    PickupAddress = TextAreaField("PickupAddress", validators=[Length(max=150)])
    submit = SubmitField('create')





class ModifyForm(FlaskForm):
    '''
    vm_volume = TextField('vm_volume', validators=[
        Required(), Length(min=1)])
    vm_rent_time = TextField('vm_rent_time', validators=[
        Required(), Length(min=1)])

    vm_name = TextField('vm_name', validators=[
        Required(), Length(max=15)])
    client_mac = TextField('client_mac', validators=[
        Required(), Length(max=15)])

    vm_flavor = TextField('vm_flavor', validators=[
        Required(), Length(max=15)])

    submit = SubmitField('modify')
'''
    vm_volume = TextField('vm_volume', validators=[
        Length(max=8)])
    vm_rent_time = TextField('vm_rent_time', validators=[
         Length(max=8)])

    vm_name = TextField('vm_name', validators=[
         Length(max=15)])
    client_mac = TextField('client_mac', validators=[
         Length(max=25)])

    VMname = SelectField('VMname', validators=[Required(),
         Length(max=25)])

    VMflavor = SelectField('VMflavor', validators=[
         Length(max=15)])


    VMfloatingip = SelectField('VMfloatingip', validators=[
         Length(max=15)])
    submit = SubmitField('modify')
