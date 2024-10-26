from pathlib import Path
from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

# SQLAlchemyをインスタンス化
db = SQLAlchemy()


def create_app():
    # Flaskインスタンスを生成
    app = Flask(__name__)
    
    app.config.from_mapping(
        SECRET_KEY="2AZSMss3p5QPbcY2hBsJ",
        SQLALCHEMY_DATABASE_URI=\
            f"sqlite:///{Path(__file__).parent.parent / 'local.sqlite'}",
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        SQLALCHEMY_ECHO=True
    )
    # SQLAlchemyと連携
    db.init_app(app)
    # Migrateと連携
    Migrate(app, db)
    
    from apps.crud import views as crud_views
    
    app.register_blueprint(crud_views.crud, url_prefix="/crud")
    
    return app