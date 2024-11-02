from pathlib import Path
from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
from apps.config import config
from dotenv import load_dotenv
from flask_login import LoginManager

load_dotenv() 

# SQLAlchemyをインスタンス化
db = SQLAlchemy()
csrf = CSRFProtect()

# LoginManagerをインスタンス化、未ログイン時のリダイレクト先を指定
login_manager = LoginManager()
login_manager.login_view = "auth.signup"
# ログイン後の表示メッセージ
login_manager.login_message = ""



def create_app(config_key):
    # Flaskインスタンスを生成
    app = Flask(__name__)
    
    app.config.from_object(config[config_key])
    
    # SQLAlchemyと連携
    db.init_app(app)
    # Migrateと連携
    Migrate(app, db)
    
    csrf.init_app(app)
    
    login_manager.init_app(app)
    
    # crudアプリ
    from apps.crud import views as crud_views
    app.register_blueprint(crud_views.crud, url_prefix="/crud")
    
    # auth(認証)アプリ
    from apps.auth import views as auth_views
    app.register_blueprint(auth_views.auth, url_prefix="/auth")
    
    # 物体検知アプリ
    from apps.detector import views as dt_views
    app.register_blueprint(dt_views.dt)
    
    return app