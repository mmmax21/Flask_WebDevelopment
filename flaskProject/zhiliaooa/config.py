SECRET_KEY = "dwadawdjakhdsjkdh;pp"

#数据库配置
HOSTNAME = "127.0.0.1"
PORT=3306
USERNAME = "root"
PASSWORD = "louxiao123"
DATABASE = "zhiliaooa_course"
DB_URI = f"mysql+pymysql://{USERNAME}:{PASSWORD}@{HOSTNAME}:{PORT}/{DATABASE}?charset=utf8mb4"
SQLALCHEMY_DATABASE_URI = DB_URI

#邮箱配置
MAIL_SERVER = "smtp.qq.com"
MAIL_USE_SSL = True
MAIL_PORT = 465
MAIL_USERNAME ="578402979@qq.com"
MAIL_PASSWORD = "fgxokvnpkobmbded"
MAIL_DEFAULT_SENDER = "578402979@qq.com"



