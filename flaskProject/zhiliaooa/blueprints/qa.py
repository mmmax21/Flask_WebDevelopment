from flask import Blueprint,request,render_template,g,redirect,url_for
from .forms import QuestionForm,AnswerForm
from model import QuestionModel,AnswerModel
from exts import db
from decorators import login_required
bp = Blueprint("qa",__name__, url_prefix="/") #为什么用根路径？因为首页需要展示qa

# http://127.0.0.1:8000
@bp.route('/')
def index():
    #用时间排序，最新的放在上面
    questions = QuestionModel.query.order_by(QuestionModel.create_time.desc()).all()
    return render_template("index.html", questions=questions)


@bp.route('/qa/public', methods=['GET','POST'])
@login_required
def public_question():
    if request.method == 'GET':
        return render_template("public_question.html")
    else:
        form = QuestionForm(request.form)
        if form.validate():
            title = form.title.data
            content = form.content.data
            #因为在request前就已经用hook得到那个user了，所以这里author可以直接从g里的读取
            question = QuestionModel(title=title, content=content, author=g.user)
            db.session.add(question)
            db.session.commit()
            # todo: 跳转到问答的详情页
            return redirect('/')
        else:
            print(form.errors)
            return redirect(url_for("qa.public_question"))


@bp.route('/qa/detail/<qa_id>')
def qa_detail(qa_id):
    question = QuestionModel.query.get(qa_id)
    return render_template("detail.html", question=question)

@bp.route('/answer/public', methods= ['POST'])
@login_required
def public_answer():
    print(request.form.get('question_id'))
    form = AnswerForm(request.form)
    if form.validate():
        content = form.content.data
        question_id = form.question_id.data
        #那么author该怎么读取呢？因为发布问题的只能是登录用户，那就可以用g.user.id
        answer = AnswerModel(content= content, question_id = question_id,author_id=g.user.id )
        db.session.add(answer)
        db.session.commit()
        return redirect(url_for("qa.qa_detail", qa_id=question_id))
    else:
        print(form.errors)
        return redirect(url_for("qa.qa_detail",qa_id=request.form.get("question_id")))

@bp.route('/search')
def search():
    # /search?q=flask -- 用这个
    # /search/<q>
    # post, request.form
    q = request.args.get('q')
    questions = QuestionModel.query.filter(QuestionModel.title.contains(q)).all() #把所有标题中带有q的问题都搜索出来
    return render_template("index.html",questions=questions)