from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import HTTPBasic, HTTPBasicCredentials

from starlette.templating import Jinja2Templates
from starlette.requests import Request
from starlette.status import HTTP_401_UNAUTHORIZED

import db
from models import User, Task

import hashlib

app = FastAPI(
    title='FastAPIでつくるtoDoアプリケーション',
    description='FastAPIチュートリアル：FastAPI(とstarlette)でシンプルなtoDoアプリを作りましょう．',
    version='0.9 beta'
)

security = HTTPBasic()

# new テンプレート関連の設定 (jinja2)
templates = Jinja2Templates(directory="templates")
jinja_env = templates.env  # Jinja2.Environment : filterやglobalの設定用
 
 
def index(request: Request):
    return templates.TemplateResponse('index.html', {'request': request})

def admin(request: Request, credentials: HTTPBasicCredentials = Depends(security)):
    # Basic認証
    username = credentials.username
    password = hashlib.md5(credentials.password.encode()).hexdigest()

    # dbよりユーザ名と一致するデータを取得
    user = db.session.query(User).filter(User.username == 'admin').first()
    if user is not None:
        task = db.session.query(Task).filter(Task.user_id == user.id).all()
    else:
        task = []
    
    db.session.close()

    # 該当ユーザなし
    if user is None or user.password != password:
        error = 'ユーザ名か、パスワードが異なっています'
        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED,
            detail=error,
            headers={"WWW-Authenticate": "Basic"},
        )

    res = templates.TemplateResponse(
        'admin.html', {
            'request': request,
            'user': user,
            'task': task,
        }
    )

    return res

