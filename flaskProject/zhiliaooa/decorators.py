from functools import wraps
from flask import g, redirect, url_for

def login_required(func):
    #保留func的信息
    @wraps(func)
    #func(a,b,c)
    # func(1,2,c=3), 1,2 --> args, c=3 --> kwargs
    def inner(*arg, **kwargs):
        if g.user:   #如果是登录的用户
            return func(*arg, **kwargs)
        else:   #如果没登录，跳转到登录界面
            return redirect(url_for("auth.login"))
    return inner

#如何理解装饰器呢？
#@login_required
#def public_question(question_id):
#   pass
#  ---等同于--
# login_required(public_question)(question_id)
# login_required(public_question)这是一个函数，返回的是inner，然后把question_id传进inner再做判断
