from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
from flask_migrate import Migrate

app = Flask(__name__)

# Mysql 所在的主机名
HOSTNAME = "127.0.0.1"
# Mysql监听的端口号，默认3306
PORT=3306
# 连接mysql的用户名，读者用自己设置的
USERNAME = "root"
#连接mysql的密码，读者用自己的
PASSWORD = "louxiao123"
#mysql上创建的数据库名称
DATABASE = "database_learn"

app.config['SQLALCHEMY_DATABASE_URI']= f"mysql+pymysql://{USERNAME}:{PASSWORD}" \
                                       f"@{HOSTNAME}:{PORT}/{DATABASE}?charset=utf8mb4"

#在app.config中设置好连接数据库的信息
#然后使用SQLALchemy（app）创建一个db对象
#SQLALchemy会自动读取 app.config中连接数据库的信息,比如说用户名、密码、连接哪个数据库

db = SQLAlchemy(app)
#为什么需要migrate？因为在app里的代码没法实时更新到数据库。比如说在User里加一个email，db是不知道的
migrate = Migrate(app, db)

#ORM映射三部曲
#1. flask db init : 这步只需要执行一次
#2. flask db migrate : 识别ORM模型的改变，生成脚本, e.g.识别到email
#3. flask db upgrade : 运行迁移脚本，同步到数据库中



class User(db.Model):   #db.Model代表ORM模型,封装了很多和数据库交互的语句
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key =True, autoincrement=True) #新的id会自动加1
    username = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=True)
    signiture = db.Column(db.String(100), nullable=True)
# user = User(username="mmmax",password="123456")
#sql: insert user(username, password) values('mmmax','123456')

class Article(db.Model):
    __tablename__ = "article"
    id = db.Column(db.Integer, primary_key =True, autoincrement=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False) #string can only hold 255 bytes, but text can do more..

    #添加作者的外键
    author_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    # backref:自动给User模型增加一个article属性，用来获取文章列表
    author = db.relationship("User",backref ="articles")


article = Article(title= "learn flask", content="xxxx")
#relationship做了什么事呢？当我们查找author的时候，
# 它会自动到User表中寻找关联对象。也就是说它帮我们实现了下面第一行代码，使得我们可以直接运行以下第二行
# article.author = User.query.get(article.author_id)
# print(article.author)

with app.app_context():
    db.create_all() #把以上所有的表同步到数据库里


@app.route('/')
def hello_world():
    return 'hello world'

@app.route('/user/add')
def add_user():
    user = User(username="mmmax", password="12345")

    db.session.add(user)
    db.session.commit()
    return "user created successfully!"

@app.route('/user/query')
def query_user():
    #1.get:根据主键查找
    # user = User.query.get(1)
    # print(f"{user.id}:{user.username}-{user.password}")
    #2.filter_by
    # 返回一个queryset，是一个类array
    users = User.query.filter_by(username="mmmax")
    for user in users:
        print(user.username)
    return "user query successfully"

@app.route('/user/update')
def update_user():
    user = User.query.filter_by(username="mmmax").first()
    user.password = "222222"
    db.session.commit()
    return "data updated successfully"

@app.route('/user/delete')
def delete_user():
    user = User.query.get(1)
    db.session.delete(user)
    db.session.commit()
    return "data deleted successfully"

#article添加文章
@app.route('/article/add')
def article_add():
    article1 = Article(title ="learn flask", content="FlasXXXX")
    article1.author= User.query.get(2)

    article2 = Article(title="learn Django", content="Django XXXX")
    article2.author = User.query.get(2)

    #add to session
    db.session.add_all([article1, article2])
    #update to db
    db.session.commit()
    return "article added successfully"

@app.route('/article/query')
def query_article():
    user = User.query.get(2)
    #通过user对象访问它所有的文章
    for article in user.articles:
        print(article.title)

    return "文章查找成功"

if __name__ == '__main__':
    app.run(port=8000,debug=True,host='0.0.0.0')