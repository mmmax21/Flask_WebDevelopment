from datetime import datetime

from flask import Flask, render_template
#render template是渲染模版，把html传到前端，使得网页有像百度搜索窗口的样子
app = Flask(__name__)


##定义user
class User:
    def __init__(self,username,email):
        self.username = username
        self.email = email
##diy filter
def datetime_format(value, format="%Y年%m月%d日 %H:%M"):
    return value.strftime(format)

#add new new filter to the template, 1st param is the function of filter, 2nd param is the name
app.add_template_filter(datetime_format,"dformat")

@app.route('/')
def hello_world():
    user = User(username = "max",email="max@qq.com")
    person = {
        "username" : "Lainey",
        "email":"zlf@qq.com"
    }
    return render_template("index.html",user=user,person=person)

#什么是过滤器？在把user和person扔给html之前我们可能会把他们放到函数里进行处理,这就叫做过滤器
@app.route('/filter')
def filter_demo():
    user = User(username="max", email="mmmax@qq.com")
    mytime = datetime.now()
    return render_template("filter.html",user=user,mytime=mytime)


## 我们把url中得到的参数传给html，后端会在html中渲染
## 传blog_id, username
@app.route('/blog/<blog_id>')
def blog_detail(blog_id):
    return render_template("blog_detail.html", blog_id=blog_id,username ="知了")

# 模板继承
@app.route('/child1')
def child1():
    return render_template("child1.html")

@app.route('/child2')
def child2():
    return render_template("child1.html")


#static是做什么的？我们为了让界面好看，需要加入静态和动态的图片，用CSS，JS文件传输，他们都放在static里
@app.route('/static')
def static_demo():
    return render_template("static.html")


if __name__ == '__main__':
    host = "0.0.0.0"
    port = 8000
    app.run(debug=True, host=host, port=port)