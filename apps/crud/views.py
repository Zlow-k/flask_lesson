from apps.crud.forms import UserFrom
from flask import Blueprint, render_template, redirect, url_for
from apps.app import db
from apps.crud.models import User

# Blueprintでcrudアプリを生成する
crud = Blueprint(
    "crud",
    __name__,
    template_folder="templates",
    static_folder="static"
)

# indexエンドポイントを作成そindex.htmlを返す
@crud.route("/")
def index():
    return render_template("crud/index.html")

@crud.route("/sql")
def sql():
    db.session.query(User).all()
    return "コンソールログを確認してください"

@crud.route("/user/new", methods=["GET", "POST"])
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