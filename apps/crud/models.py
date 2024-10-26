from datetime import datetime

from apps.app import db
from werkzeug.security import generate_password_hash

# db.Modelを継承したUserクラスを作成
class User(db.Model):
    __tablename__ = "users"
    # カラムの定義
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, index=True)
    email = db.Column(db.String, index=True, unique=True)
    password_hash = db.Column(db.String)
    create_at = db.Column(db.Datetime, default=datetime.now)
    updated_at = db.Column(
        db.Datetime, default=datetime.now, onupdate=datetime.now
    )
    
    # パスワードをセットするためのプロパティ
    @property
    def password(self):
        raise AttributeError("読み取り不可")
    
    # パスワードをセットするためのセッター関数でハッシュ化したPWをセットする
    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)