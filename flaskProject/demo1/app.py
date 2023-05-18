from flask import Flask,request

#使用Flask创建一个app对象
app = Flask(__name__)

#url组成： http[80]/https[443]://www.qq.com:44/path
#path之前的都是根路由，不需要修改

# 创建一个路由和视图函数的映射
@app.route('/')    #访问根路由，它会返回什么代码呢？返回 hello_world()
def hello_world():
    return "hello world"   #"hello world"返回给浏览器

@app.route('/profile')
def profile():
    return "个人中心"

@app.route('/blog/list')
def blog_list():
    return "博客列表"

#带参数的url case1:将参数固定到了path中
@app.route('/blog/int:<blog_id>')
def blog_detail(blog_id):
    return f"您访问的博客是{blog_id}"

#带参数的url case2：查询字符串传参
#diff with case1: 不需要在route里加入参数，传参更加灵活
# book/list -- 1st page
# book/list?page=2 -- 2nd page
@app.route('/book/list')
def book_list():
    #request.agrs: 类字典类型
    page = request.args.get("page",default=1, type=int)
    return f"您获取的是第{page}页列表"



#1. debug模式：可以看到报错，动态更新代码
#2. 修改host模式: 让局域网下其他电脑访问程序
#3. 修改端口

#如何理解端口号？电脑是一个酒店，每个房间都是一个服务，这个服务可能是邮箱，可能是微信，可能是qq
if __name__ == '__main__':
    host = "0.0.0.0"
    port = 8000
    app.run(debug=True,host=host, port=port)


