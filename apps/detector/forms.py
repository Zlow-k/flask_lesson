from flask_wtf.file import FileAllowed, FileField, FileRequired
from flask_wtf.form import FlaskForm
from wtforms.fields.simple import SubmitField

class UploadImageForm(FlaskForm):
    image = FileField(
        validators=[
            FileRequired("画像ファイルを指定してください。"),
            FileAllowed(["png", "jpg", "jpeg"],
            "サポートされていない画像形式です。"),
        ]
    )
    submit = SubmitField("アップロード")
    
class DetectorForm(FlaskForm):
    submit = SubmitField("検知")