from flask import Blueprint,jsonify,request,g
import json
from flask import current_app as app
from myapp import db,auth
from myapp.student_details.models import Student,Userdetails,Address
from itsdangerous import URLSafeSerializer

mod=Blueprint('student_details',__name__,url_prefix='/student')

@auth.verify_token
def verify_auth_token(token):
    print('----token', token)
    s = URLSafeSerializer(app.config['SECRET_KEY'])
    try:
        data = s.loads(token)
    except Exception:
        return False
    g.student = Student.query.get(data['id'])
    if g.student is None:
        return False
    return True


@mod.route('/login', methods=['POST'])
def login():
    request_data = request.get_json()
    firstname = request_data['firstname']
    password = request_data['password']
    student = Student.query.filter(Student.firstname == firstname and Student.password == password).first()
    token = student.generate_auth_token()
    reponse = token
    return jsonify(reponse), 200

@mod.route('/create_user', methods=['POST'])
def create_user():
    request_data=request.get_json()
    student=Student(
        firstname=request_data['firstname'],
        lastname=request_data['lastname'],
        email=request_data['email'],
        password=request_data['password']
      )
    db.session.add(student)
    db.session.commit()
    return 'Student has been created'

@mod.route('/add_user_detail', methods=['POST'])
def add_user_detail():
    request_data = request.get_json()
    user_detail = Userdetails(
        mobile=request_data['mobile'],
        fk_id=request_data['fk_id']
    )
    db.session.add(user_detail)
    db.session.commit()
    return 'Student mobile no. has been added.'

@mod.route('/add_address', methods=['POST'])
def add_address():
    request_data = request.get_json()
    fk_id=request_data['fk_id']
    address=Address(
        city=request_data['city']
    )
    student=Student.query.get(fk_id)
    student.addresses.append(address)
    db.session.commit()
    return 'Student Address has been added.'


@mod.route('/',methods=['GET'])
# @auth.login_required
def get_student():
    students=Student.query.all() #select * from student
    # print(students[1].firstname)
    # print(students[1].lastname)
    # print(students[1].email)
    response=[student.to_representation() for student in students]
    # response=[x.__repr__() for x in students]
    return jsonify(response)

@mod.route('/get_student/<student_id>',methods=['GET'])
def get_student_id(student_id):
    students=Student.query.get(int(student_id))
    response=students.to_representation()
    response.pop('email')
    """
    #Execute query using raw sql query
    result=db.engine.execute('Select * from student where id={}'.format(int(student_id))')
    for x in result:
      response={
        'firstname':x['firstname'],
        'lastname':x['lastname'],
        'email':x['email']
        }
        
    """
    return jsonify(response)


@mod.route('/get_student', methods=['GET'])
def get_student_by_firstname():
    firstname=request.args.get('firstname')
    student = Student.query.filter(Student.firstname==firstname).first()
    #below is the statement for and ,or conditions
    #student=Student.query.filter((Student.firstname==firstname)|(Student.email==email)).first()
    response = student.to_representation()
    return jsonify(response)

@mod.route('/update_student/<student_id>', methods=['PUT'])
def update_student(student_id):
    request_data=request.get_json()
    student = Student.query.get(int(student_id))
    student.email=request_data['email']
    db.session.commit()
    return 'Student has been updated'

@mod.route('/delete_student/<student_id>', methods=['DELETE'])
def delete_student(student_id):
    student = Student.query.get(int(student_id))
    db.session.delete(student)
    db.session.commit()
    return 'Student has been deleted'





