from pathlib import Path
from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
from apps.config import config

# SQLAlchemyをインスタンス化
db = SQLAlchemy()
csrf = CSRFProtect()

def create_app(config_key):
    # Flaskインスタンスを生成
    app = Flask(__name__)
    
    app.config.from_object(config[config_key])
    
    # SQLAlchemyと連携
    db.init_app(app)
    # Migrateと連携
    Migrate(app, db)
    
    csrf.init_app(app)
    
    from apps.crud import views as crud_views
    
    app.register_blueprint(crud_views.crud, url_prefix="/crud")
    
    return app