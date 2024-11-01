from apps.app import db
from apps.auth.forms import SignUoForm
from apps.crud.models import User
from flask import Blueprint, render_template, flash, url_for, redirect, request
from  flask_login import login_user

# Blueprintを使ってauthを生成する
auth = Blueprint(
    "auth",
    __name__,
    template_folder="templates",
    static_folder="static"
)

@auth.route("/")
def index():
    return render_template("auth/index.html")

@auth.route("/signup", methods=["GET", "POST"])
def signup():
    # SignUpFormをインスタンス化する
    form = SignUoForm()
    if form.validate_on_submit():
        user = User(
            username=form.username.data,
            email=form.email.data,
            password=form.password.data,
        )
        
        # メールアドレス重複チェック
        if user.is_duplicate_email():
            flash("指定のメールアドレスは登録済みです。")
            return redirect(url_for("auth.signup"))
        
        # ユーザー情報を登録
        db.session.add(user)
        db.session.commit()
        # ユーザー情報セッションに格納する
        login_user(user)
        # GETパラメータにnextキーが存在し、値がない場合はユーザーの一覧ページへリダイレクト
        next_ = request.args.get("next")
        if next_ is None or not next_.startswith("/"):
            next_ = url_for("crud.users")
        return redirect(next_)
    
    return render_template("auth/signup.html", form=form)
        
        