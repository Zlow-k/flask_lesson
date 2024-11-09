import os
import shutil

import pytest

from apps.app import create_app, db

from apps.crud.models import User
from apps.detector.models import UserImage, UserImageTag

@pytest.fixture
def fixture_app():
    # セットアップ処理
    # テスト用のコンフィグを使うためにい引数を設定
    app = create_app("testing")
    
    # データベースを利用するための宣言
    app.app_context().push()
    
    # テスト用のテーブル作成
    with app.app_context():
        db.create_all()
        
    os.mkdir(app.config["UPLOAD_FOLDER"])
    
    yield app
    
    User.query.delete()
    
    UserImage.query.delete()
    
    UserImageTag.query.delete()
    
    shutil.rmtree(app.config["UPLOAD_FOLDER"])
    
    db.session.commit()
    
@pytest.fixture
def client(fixture_app):
    return fixture_app.test_client()