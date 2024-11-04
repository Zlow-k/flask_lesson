import uuid
from pathlib import Path

from apps.app import db
from apps.crud.models import User
from apps.detector.models import UserImage
from apps.detector.forms import UploadImageForm
from flask import (
    Blueprint,
    render_template,
    current_app,
    send_from_directory,
    redirect,
    url_for)
from flask_login import current_user, login_required

dt = Blueprint("detector", __name__, template_folder="templates")

@dt.route("/")
def index():
    # UserとUserImageをJoinして画像一覧を取得する
    user_images = (
        db.session.query(User, UserImage)
        .join(UserImage)
        .filter(User.id == UserImage.user_id)
        .all()
    )
    return render_template("detector/index.html", user_images=user_images)

@dt.route("/images/<path:filename>")
def image_file(filename):
    return send_from_directory(current_app.config["UPLOAD_FOLDER"], filename)

@dt.route("/upload", methods=["GET", "POST"])
@login_required
def upload_image():
    form = UploadImageForm()
    if form.validate_on_submit():
        # アップロードされた画像ファイルを取得
        file = form.image.data
        # ファイル名と拡張子を取得し、ファイル名をuuidに変換
        ext = Path(file.filename).suffix
        image_uuid_file_name = str(uuid.uuid4()) + ext
        
        # 画像を保存する 
        image_path = Path(
            current_app.config["UPLOAD_FOLDER"], image_uuid_file_name
        )
        file.save(image_path)
        
        # DBへ保存
        user_image = UserImage(
            user_id=current_user.id, image_path=image_uuid_file_name
        )
        db.session.add(user_image)
        db.session.commit()
        
        return redirect(url_for("detector.index"))
    return render_template("detector/upload.html", form=form)