from itsdangerous import URLSafeSerializer

from myapp import db, auth
from flask import current_app as app, g


student_addresses=db.Table('student_addresses',
        db.Column('student_id',db.Integer,db.ForeignKey('student_info1.id'),primary_key=True),
        db.Column('address_id', db.Integer,db.ForeignKey('student_address.id'), primary_key=True)
)

class Student(db.Model):
    __tablename__='student_info1'
    id = db.Column('id',db.Integer, primary_key=True, autoincrement=True)
    firstname = db.Column('firstname',db.String(64), index=True, unique=True)
    lastname = db.Column('lastname', db.String(64), index=True, unique=True)
    email = db.Column('email',db.String(120), unique=True)
    password = db.Column('password',db.String(128))
    studentforeignkey=db.relationship('Userdetails',backref='student_info1',lazy=True,uselist=False,cascade="all,delete")
    addresses = db.relationship('Address',secondary=student_addresses, backref='student_info1', lazy='joined',cascade="all,delete")

    def to_representation(self):
        if self.studentforeignkey:#true if a:
            studentforeignkey = self.studentforeignkey.to_representation()
        else:
            studentforeignkey = {}

        addresses =[x.to_representation() for x in self.addresses]

        return {
            "firstname" : self.firstname,
             "lastname" : self.lastname,
             "email":self.email,
              "password":self.password,
              "phone":studentforeignkey,
              "city":addresses
        }

    def generate_auth_token(self):
        s = URLSafeSerializer(app.config['SECRET_KEY'])
        return s.dumps({'id': self.id})

class Userdetails(db.Model):
        __tablename__ = 'student_phone'
        id = db.Column('id', db.Integer, primary_key=True, autoincrement=True)
        mobile = db.Column('mobile', db.Integer)
        fk_id = db.Column('fk_id', db.Integer, db.ForeignKey('student_info1.id'), nullable=False)

        def to_representation(self):
            # return  self.mobile
            return{
            'phone':self.mobile
             }


class Address(db.Model):
        __tablename__ = 'student_address'
        id = db.Column('id', db.Integer, primary_key=True, autoincrement=True)
        city = db.Column('city', db.String(64),nullable=True)

        def to_representation(self):
            return {
            'city':self.city
             }








# class Student(db.Model):
#     id=db.Column(db.Integer,primary_key=True)
#     firstname=db.Column(db.String(50))
#     lastname=db.Column(db.String(100))
#     email=db.Column(db.String(120))
#
#
#     def __repr__(self):
#         return {
#             'firstname':self.firstname,
#             'lastname':self.lastname,
#             'email':self.email
#
#         }


