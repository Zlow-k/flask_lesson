from apps.crud.forms import UserFrom
from flask import Blueprint, render_template, redirect, url_for
from apps.app import db
from apps.crud.models import User
from flask_login import login_required

# Blueprintでcrudアプリを生成する
crud = Blueprint(
    "crud",
    __name__,
    template_folder="templates",
    static_folder="static"
)

# indexエンドポイントを作成そindex.htmlを返す
@crud.route("/")
@login_required
def index():
    return render_template("crud/index.html")

@crud.route("/sql")
@login_required
def sql():
    db.session.query(User).all()
    return "コンソールログを確認してください"

@crud.route("/users/new", methods=["GET", "POST"])
@login_required
def create_user():
    form = UserFrom()
    if form.validate_on_submit():
        user = User(
            username=form.username.data,
            email = form.email.data,
            password = form.password.data,
        )
        db.session.add(user)
        db.session.commit()
        
        return redirect(url_for("crud.users"))
    return render_template("crud/create.html", form=form)

@crud.route("/users")
@login_required
def users():
    """ユーザーの一覧を取得する"""
    users = User.query.all()
    return render_template("crud/index.html", users=users)

@crud.route("/users/<user_id>", methods=["GET", "POST"])
@login_required
def edit_user(user_id):
    form = UserFrom()
    
    # Userモデルを利用してユーザーを取得する
    user = User.query.filter_by(id=user_id).first()
    
    # formからsubmitされた場合はユーザーを更新しユーザーの一覧画面へリダイレクトする
    if form.validate_on_submit():
        user.username = form.username.data
        user.email = form.email.data
        user.password = form.password.data
        db.session.add(user)
        db.session.commit()
        return redirect(url_for("crud.users"))
    
    return render_template("crud/edit.html", user=user, form=form)

@crud.route("/users/<user_id>/delete", methods=["POST"])
@login_required
def delete_user(user_id):
    user = User.query.filter_by(id=user_id).first()
    db.session.delete(user)
    db.session.commit()
    return redirect(url_for("crud.users"))