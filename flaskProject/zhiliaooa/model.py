from exts import db
from datetime import datetime

class UserModel(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key= True, autoincrement = True)
    username = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(300), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    join_time = db.Column(db.DateTime, default=datetime.now)  #因为我们需要传入一个函数，所以不是now()

class EmailCaptchaModel(db.Model):
    #存储 1）邮箱 2）验证码
    __tablename__ = "email_captcha"
    id = db.Column(db.Integer, primary_key= True, autoincrement = True)
    email = db.Column(db.String(100), nullable=False)
    captcha = db.Column(db.String(100), nullable= False)

class QuestionModel(db.Model):
    # 存储 1）邮箱 2）验证码
    __tablename__ = "question"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    create_time = db.Column(db.DateTime, default=datetime.now)

    author_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    author = db.relationship(UserModel, backref= "questions") #通过user能拿到他所有的question

class AnswerModel(db.Model):
    __tablename__ = "answer"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    content = db.Column(db.Text, nullable=False)
    create_time = db.Column(db.DateTime, default=datetime.now)

    #增加2个foreign key: 针对哪个问题；发布人
    question_id = db.Column(db.Integer, db.ForeignKey("question.id"))
    question = db.relationship(QuestionModel, backref = db.backref("answers",order_by=create_time.desc())) #通过question拿到所有answer
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    author = db.relationship(UserModel, backref = "answers")


