from flask import Flask,session,g
import config
from exts import db,mail
from model import UserModel
from blueprints.qa import bp as qa_bp
from blueprints.auth import bp as auth_bp
from flask_migrate import Migrate

app = Flask(__name__)

#绑定配置文件

#配置1：config
#之前是app.config['SQLALCHEMY_DATABASE_URI'] = config...
#from_object会自动读取config里的信息
app.config.from_object(config)

#配置2：db
db.init_app(app)  #这句话是什么意思呢？我们在exts里创建了一个空的db，然后现在我们要把app传进去，就需要用到init_app
mail.init_app(app)

migrate = Migrate(app,db)

#配置3：blueprint
app.register_blueprint(qa_bp) # 用blueprint做模块化

app.register_blueprint(auth_bp)

#我们现在要做的是用session提取user id,然后从数据库中得到这个用户，等到了login1的时候直接用就行了
#那这个时候需要把user存在哪里呢？我们需要一个全局变量-- g
#hook函数
#before request/ before_first_request /after_request：函数会在正常流程中插进去
@app.before_request
def my_before_request():
    user_id = session.get("user_id") #flask以及解密好了
    if user_id:
        user = UserModel.query.get(user_id)
        setattr(g, "user",user)
    else:
        setattr(g, "user", None)

#为什么需要这个呢？这是模板中的变量
@app.context_processor
def my_context_processor():
    return {"user": g.user}







if __name__ == '__main__':
    app.run(port=8000,debug=True,host='0.0.0.0')