from flask import Blueprint, render_template,request, jsonify,redirect,url_for,session
from exts import mail,db
from flask_mail import Message
import string,random
from model import EmailCaptchaModel, UserModel
from .forms import RegisterForm, LoginForm
from werkzeug.security import generate_password_hash,check_password_hash


# /auth
bp = Blueprint("auth", __name__, url_prefix="/auth")  #url_prefix就是说url都是auth开头

#/auth/login
@bp.route("/login", methods=["GET","POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    else:
        form = LoginForm(request.form)
        if form.validate():
            email = form.email.data
            password = form.password.data   #因为是加密过的密码，不能直接用
            user = UserModel.query.filter_by(email=email).first()
            if not user:
                print("邮箱在数据库中不存在！")
                return redirect(url_for("auth.login"))
            #如果用户是存在的，需要拿密码对比
            if check_password_hash(pwhash=user.password, password=password):
                #cookie中不适合存放太多数据，可以用来授权登录
                #flask中的session，是经过加密后存储在cookie当中的
                #浏览器得到你的cookie后，下一次就知道是你在登录了
                session['user_id'] = user.id
                return redirect("/")
            else:
                print("密码错误")
                return redirect(url_for("auth.login"))

        else:
            print(form.errors)
            return redirect(url_for("auth.login"))


#regitser 要做两件事情：1.返回首页模板 2.按到"立即注册"时，需要把所有的东西都提交上去
# GET: 从服务器获取数据，渲染首页
# POST：把数据交给服务器
@bp.route("/register",methods=["GET","POST"])
def register():
    #问题：怎么知道用户提交的验证码和我们发出去的是匹配的
    if request.method == 'GET':
        return render_template("register.html")
    else: #if method == post
        #这一步验证用户提交的邮箱和验证码对应且格式正确
        #什么是request.form？在register.html中，所有的input，也就是用户在框里输入的东西，都在"form"的下面。
        #所以request.form就能得到所有的用户input(email,username,...),然后再放到RegisterForm里做一个验证
        form = RegisterForm(request.form)   #创建一个RegisterForm的对象，然后我们可以用它所有的method来做一个验证
        if form.validate():  #它会自动调用里面写的所有validate方法
            #这一步我们会把注册的user数据传入数据库
            email = form.email.data
            username = form.username.data
            password = form.password.data
            user = UserModel(email=email, username=username,password=generate_password_hash(password))
            db.session.add(user)
            db.session.commit()
            return redirect(url_for("auth.login"))
        else:
            print(form.errors)
            return redirect(url_for("auth.register"))

@bp.route('/logout')
def logout():
    #退出登录就只要把cookie里的session清掉
    session.clear()
    return redirect("/")



#如果没有指定method，默认是get
@bp.route("/captcha/email")
def get_email_captcha():
    # /captcha/email/<email>
    # /captcha/email?email=xxx@qq.com
    #第一步：得到用户邮箱
    email = request.args.get('email')
    #第二步：产生验证码:4/6随机数组、字母、数组和字母组合
    source = string.digits*4                 #0123456789 这样的有四个
    captcha = random.sample(source, 4)       #随机取4位
    captcha = "".join(captcha)
    #第三步：发送验证码到email
    message = Message(subject="知了传课注册验证码", recipients=[email], body=f"您的验证码是{captcha}")
    mail.send(message)
    #第四步：存储验证码到数据库
    email_captcha = EmailCaptchaModel(email=email, captcha=captcha)
    db.session.add(email_captcha)
    db.session.commit()
    return jsonify({"code":200, "message":"", "data":None})



    
