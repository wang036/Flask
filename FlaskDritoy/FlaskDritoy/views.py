"""
负责视图和路由
"""
import hashlib
from flask import request
from flask import redirect
from flask import render_template
from FlaskDritoy.main import app
from FlaskDritoy.models import *
from FlaskDritoy.main import session
from FlaskDritoy.forms import TeacherForm
from FlaskDritoy.main import csrf
from flask import jsonify


def loginValid(fun):
    """
    装饰器
    """

    def inner(*args, **kwargs):
        username = request.cookies.get("username")
        id = request.cookies.get("user_id")
        session_username = session.get("username")
        if username and id and session_username:
            if username == session_username:
                return fun(*args, **kwargs)
        return redirect("/login/")
    return inner


def setPassword(password):
    md5 = hashlib.md5()
    md5.update(password.encode())
    return md5.hexdigest()


@csrf.exempt
@app.route("/register/", methods=["GET", "POST"])
def register():
    """
    注册
    """
    if request.method == "POST":
        form_data = request.form
        username = form_data.get("username")
        password = form_data.get("password")
        identity = form_data.get("identity")
        user = User()
        user.username = username
        user.password = setPassword(password)
        user.identity = int(identity)
        user.save()
        return redirect("/login/")
    return render_template("register.html", **locals())


@csrf.exempt
@app.route("/login/", methods=["GET", "POST"])
def login():
    """
    登录
    """
    if request.method == "POST":
        form_data = request.form
        username = form_data.get("username")
        password = form_data.get("password")

        user = User.query.filter_by(username=username).first()
        if user:
            send_password = setPassword(password)
            db_password = user.password
            if send_password == db_password:
                # 进行跳转
                response = redirect("/index/")
                # 设置cookie
                response.set_cookie("username", username)
                response.set_cookie("user_id", str(user.id))
                # 设置session
                session["username"] = username
                # 返回跳转
                return response
    return render_template("login.html", **locals())


# @app.route('/userValid/', methods=["GET", "POST"])
# def UserVaild():
#     """
#     注册校验(get请求)
#     """
#     result = {'code': '', 'data': ''}
#     data = request.args.get('username')
#     if data:
#         user = User.query.filter_by(username=data).first()
#         if user:
#             result['code'] = 400
#             result['data'] = '用户名已经存在'
#         else:
#             result['code'] = 200
#             result['data'] = '用户名可以使用'
#     return jsonify(result)
@app.route('/userValid/', methods=["GET", "POST"])
def UserVaild():
    """
    注册校验(post请求)
    """
    result = {'code': '', 'data': ''}
    if request.method == "POST":
        data = request.form.get('username')
        if data:
            user = User.query.filter_by(username=data).first()
            if user:
                result['code'] = 400
                result['data'] = '用户名已经存在'
            else:
                result['code'] = 200
                result['data'] = '用户名可以使用'
    else:
        result['code'] = 400
        result['data'] = '请求错误'
    return jsonify(result)


@csrf.exempt
@app.route("/index/", methods=["GET", "POST"])
@loginValid
def index():
    students = Students.query.all()
    response = render_template("students_list.html", **locals())
    return response


@app.route("/logout/", methods=["GET", "POST"])
def logout():
    """
    退出
    """
    response = redirect("/login/")
    for key in request.cookies:
        response.delete_cookie(key)
    del session["username"]
    return response


@app.route("/student_list/", methods=["GET", "POST"])
def student_list():
    students = Students.query.all()
    response = render_template("students_list.html", **locals())
    return response


@csrf.exempt
@app.route("/add_teacher/", methods=["GET", "POST"])
def add_teacher():
    teacher_form = TeacherForm()
    if request.method == "POST":
        name = request.form.get('name')
        age = request.form.get('age')
        gender = request.form.get('gender')
        course = request.form.get('course')

        t = Teachers()
        t.name = name
        t.age = age
        t.gender = gender
        t.course_id = course
        t.save()
    return render_template("add_teacher.html", **locals())


@csrf.error_handler
@app.route('/csrf_403/')
def csrf_token_error(reason):
    print(reason)
    return render_template('csrf_403.html')
