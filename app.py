from datetime import datetime, date

from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
db = SQLAlchemy(app)

#データの絡むを指定していく
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(30), nullable=False)
    detail = db.Column(db.String(100))
    due = db.Column(db.DateTime, nullable=False)


#トップページ
#ここのmethodsで作成フォームからのPOSTを受け取る
@app.route('/', methods=['GET', 'POST'])
def index():
    #このページアクセスしたとき
    if request.method == 'GET':
        posts = Post.query.order_by(Post.due).all()
        return render_template('index.html', posts=posts, today=date.today())
    #フォームを新しく作成したとき
    else:
        title = request.form.get('title')
        detail = request.form.get('detail')
        due = request.form.get('due')

        due = datetime.strptime(due, '%Y-%m-%d')
        #新規作成を保存
        new_post = Post(title=title, detail=detail, due=due)

        #↓2行で，データベースに追加
        db.session.add(new_post)
        db.session.commit()

        return redirect('/')

#タスク作成
@app.route('/create')
def create():
    return render_template('create.html')

#タスク詳細 idごとに開けるようにする
@app.route('/detail/<int:id>')
def read(id):
    post = Post.query.get(id)
    return render_template('detail.html', post=post)

#タスクの編集
@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    post = Post.query.get(id)
    #アクセスしたとき
    if request.method == 'GET':
        return render_template('update.html', post=post)
    #編集した場合，dbを更新
    else:   #POSTなら
        post.title = request.form.get('title')
        post.detail = request.form.get('detail')
        post.due = datetime.strptime(request.form.get('due'), '%Y-%m-%d')

        db.session.commit()
        return redirect('/')

#タスクの削除
@app.route('/delete/<int:id>')
def delete(id):
    post = Post.query.get(id)

    db.session.delete(post)
    db.session.commit()
    return redirect('/')



if __name__ == '__main__':
    app.run()
