import wtforms
from wtforms.validators import Email,Length,EqualTo,InputRequired
from model import UserModel,EmailCaptchaModel
from exts import db
#From: 验证前端提交的数据是否符合要求
class RegisterForm(wtforms.Form):

    #1.固定格式验证
    #邮箱格式确认
    email = wtforms.StringField(validators=[Email(message="邮箱格式错误！")])
    #验证码长度为4
    captcha = wtforms.StringField(validators=[Length(min=4, max=4, message="验证码格式错误")])
    #用户名3-20位， 密码6-20位
    username = wtforms.StringField(validators=[Length(min=3,max=20, message="用户名格式错误")])
    password = wtforms.StringField(validators=[Length(min=6,max=20, message="密码格式错误")])
    password_confirm = wtforms.StringField(validators=[EqualTo("password", message="二次密码输入不匹配")])

    #2.自定义验证：
    #A) 邮箱是否被注册
    #B) 验证码是否匹配
    def validate_email(self, field):  #field是什么？如果验证的是email，field就是email。如果验证的是验证码，field就是验证码
        email = field.data
        user = UserModel.query.filter_by(email=email).first()
        #在db里找，如果这个email已经存在，就报错
        if user:
            raise wtforms.ValidationError(message="该邮箱已经被注册！")

    def validate_captcha(self, field):  #self代表当前的对象,也就是RegisterForm
        captcha = field.data
        email = self.email.data
        captcha_model = EmailCaptchaModel.query.filter_by(email=email, captcha=captcha).first()
        #如果数据库中找不到，验证码错误
        if not captcha_model:
            raise wtforms.ValidationError(message="验证码不匹配")
        # #如果找到了，那么就删除
        # else:
        #     db.session.delete(captcha_model)
        #     db.session.commit()

class LoginForm(wtforms.Form):
    email = wtforms.StringField(validators=[Email(message="邮箱格式错误！")])
    password = wtforms.StringField(validators=[Length(min=6, max=20, message="密码格式错误")])


class QuestionForm(wtforms.Form):
    title = wtforms.StringField(validators=[Length(min=3, max=100, message="标题格式错误")])
    content = wtforms.StringField(validators=[Length(min=3, message="内容格式错误")])
    #为什么不需要验证authorid/create_time？因为他们是自动生成的，不会有错误

class AnswerForm(wtforms.Form):
    content = wtforms.StringField(validators=[Length(min=3, message="内容格式错误")])
    question_id = wtforms.IntegerField(validators=[InputRequired(message="必须要传入问题id")])




