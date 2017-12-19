# -*- coding:utf-8  -*-
'''
from app import db

ROLE_USER = 0
ROLE_ADMIN = 1


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nickname = db.Column(db.String(15), index=True, unique=True)
    email = db.Column(db.String(128), index=True, unique=True)
    role = db.Column(db.SmallInteger, default=ROLE_USER)
    posts = db.relationship('Post', backref='author', lazy='dynamic')
    passwd = db.Column(db.String(128),nullable=False)

    about_me = db.Column(db.String(140))
    last_seen = db.Column(db.DateTime)

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return unicode(self.id)

    def is_admin(self):
        return self.role == ROLE_ADMIN

    @classmethod
    def get_users(cls):
        users = User.query.all()
        return users

    @classmethod
    def login_check(cls, user_name,user_passwd):
        user = cls.query.filter(db.or_(
            User.nickname == user_name)).first()
        if user is not None and user.passwd==user_passwd:
            return user
        else:
            return None

    def __repr__(self):
        return '<User %r>' % (self.nickname)


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(200))
    timestamp = db.Column(db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Post %r>' % (self.body)
'''
# -*- coding:utf-8  -*-

from app import db
ROLE_USER = 0
ROLE_ADMIN = 1


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nickname = db.Column(db.String(15), index=True, unique=True)
    email = db.Column(db.String(128), index=True, unique=True)
    role = db.Column(db.SmallInteger, default=ROLE_USER)
    posts = db.relationship('Post', backref='author', lazy='dynamic')
    password = db.Column(db.Integer)
    type = db.Column(db.String(10),default='***')
    about_me = db.Column(db.String(140))
    last_seen = db.Column(db.DateTime)

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return unicode(self.id)

    def is_admin(self):
        return self.role == ROLE_ADMIN

    @classmethod
    def get_users(cls):
        users = User.query.all()
        return users

    @classmethod
    def login_check(cls, user_name):
        user = cls.query.filter(db.or_(
            User.nickname == user_name, User.email == user_name)).first()

        if not user:
            return None

        return user

    def __repr__(self):
        return '<User %r>' % (self.nickname)


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(200))
    timestamp = db.Column(db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Post %r>' % (self.body)
class VM_information(db.Model):
    VM_id = db.Column(db.String(64), primary_key=True)
    nickname = db.Column(db.String(32))
    VM_name = db.Column(db.String(32),nullable=False)
    client_mac = db.Column(db.String(64), unique=True, nullable=False)
    ip = db.Column(db.String(32), nullable=False)
    floating_ip = db.Column(db.String(32))
    key = db.Column(db.String(32),nullable=False)
    image = db.Column(db.String(32), nullable=False)
    image_type = db.Column(db.String(10), nullable=False)
    status = db.Column(db.String(32), nullable=False)
    flavor = db.Column(db.String(32), nullable=False)
    rent_time = db.Column(db.Integer)
    def __init__(self, VM_id,nickname,VM_name, client_mac,ip,floating_ip,key,image,image_type,status,flavor, rent_time):
        self.VM_id = VM_id
        self.nickname = nickname
        self.VM_name = VM_name
        self.client_mac = client_mac
        self.ip = ip
        self.floating_ip = floating_ip
        self.key = key
        self.image = image
        self.image_type = image_type
        self.status = status
        self.flavor = flavor
        self.rent_time = rent_time




class security_group(db.Model):
    security_group_id = db.Column(db.Integer, primary_key=True)
    VM_id = db.Column(db.String(64), db.ForeignKey('VM_information.VM_id'), nullable=False)
    VM_name = db.Column(db.String(32), nullable=False)
    security_group_name = db.Column(db.String(64), nullable=False)
    security_group_type = db.Column(db.String(64))
    def __init__(self, security_group_id,VM_id, VM_name,security_group_name,security_group_type):
        self.security_group_id = security_group_id
        self.VM_id = VM_id
        self.VM_name = VM_name
        self.security_group_name = security_group_name
        self.security_group_type = security_group_type




class cloud_volume(db.Model):
    cloud_volume_id = db.Column(db.Integer, primary_key=True)
    VM_id = db.Column(db.String(64),db.ForeignKey('VM_information.VM_id'),  nullable=False)
    VM_name = db.Column(db.String(32), nullable=False)
    cloud_volume_name = db.Column(db.String(64), nullable=False)
    cloud_volume_type = db.Column(db.String(64), nullable=False)
    cloud_volume_size = db.Column(db.Integer,nullable=False)
    def __init__(self, cloud_volume_id,VM_id, VM_name,cloud_volume_name,cloud_volume_type,cloud_volume_size):
        self.cloud_volume_id = cloud_volume_id
        self.VM_id = VM_id
        self.VM_name = VM_name
        self.cloud_volume_name = cloud_volume_name
        self.cloud_volume_type = cloud_volume_type
        self.cloud_volume_size = cloud_volume_size





class snapshoot_information(db.Model):
    snapshoot_id = db.Column(db.Integer, primary_key=True)
    VM_id = db.Column(db.String(64),db.ForeignKey('VM_information.VM_id'), nullable=False)
    VM_name = db.Column(db.String(32), nullable=False)
    snapshoot_name = db.Column(db.String(64), nullable=False)
    snapshoot_describe = db.Column(db.String(200))


    def __init__(self, snapshoot_id,VM_id, VM_name,snapshoot_name,snapshoot_describe):
        self.snapshoot_id = snapshoot_id
        self.VM_id = VM_id
        self.VM_name = VM_name
        self.snapshoot_name = snapshoot_name
        self.snapshoot_describe = snapshoot_describe
