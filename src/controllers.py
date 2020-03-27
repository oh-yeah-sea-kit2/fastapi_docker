from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import HTTPBasic, HTTPBasicCredentials

from starlette.templating import Jinja2Templates
from starlette.requests import Request
from starlette.status import HTTP_401_UNAUTHORIZED

import db
from models import User, Task

import hashlib
import re

pattern = re.compile(r'\w{4,20}')  # 任意の4~20の英数字を示す正規表現
pattern_pw = re.compile(r'\w{6,20}')  # 任意の6~20の英数字を示す正規表現
pattern_mail = re.compile(r'^\w+([-+.]\w+)*@\w+([-.]\w+)*\.\w+([-.]\w+)*$')  # e-mailの正規表現


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


async def register(request: Request):
    if request.method == 'GET':
        return templates.TemplateResponse('register.html',
                                          {'request': request,
                                           'username': '',
                                           'error': []})
    if request.method == 'POST':
        data = await request.form()
        username = data.get('username')
        password = data.get('password')
        password_tmp = data.get('password_tmp')
        mail = data.get('mail')

        error = []
        tmp_user = db.session.query(User).filter(User.username == username).first()
        # 怒涛のエラー処理
        if tmp_user is not None:
            error.append('同じユーザ名のユーザが存在します。')
        if password != password_tmp:
            error.append('入力したパスワードが一致しません。')
        if pattern.match(username) is None:
            error.append('ユーザ名は4~20文字の半角英数字にしてください。')
        if pattern_pw.match(password) is None:
            error.append('パスワードは6~20文字の半角英数字にしてください。')
        if pattern_mail.match(mail) is None:
            error.append('正しくメールアドレスを入力してください。')
        if error:
            return templates.TemplateResponse(
                'register.html',
                {
                    'request': request,
                    'username': username,
                    'error': error
                }
            )
        user = User(username, password, mail)
        db.session.add(user)
        db.session.commit()
        db.session.close()
        return templates.TemplateResponse(
            'complete.html',
            {
                'request': request,
                'username': username
            }
        )

        
