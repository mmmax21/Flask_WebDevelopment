from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
#为什么要单独放在exts里呢？为了解决循环引用
db = SQLAlchemy()
mail = Mail()
