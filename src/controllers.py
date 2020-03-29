from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import HTTPBasic, HTTPBasicCredentials

from starlette.templating import Jinja2Templates
from starlette.requests import Request
from starlette.status import HTTP_401_UNAUTHORIZED

import db
from models import User, Task

import hashlib
import re

from mycalendar import MyCalendar
from datetime import datetime, timedelta

from auth import auth
from starlette.responses import RedirectResponse

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
    username = auth(credentials)

    today = datetime.now()
    next_w = today + timedelta(days=7)

    # dbよりユーザ名と一致するデータを取得
    user = db.session.query(User).filter(User.username == 'admin').first()

    if user is not None:
        task = db.session.query(Task).filter(Task.user_id == user.id).all()
    else:
        task = []
    db.session.close()
    
    """ [new] カレンダー関連 """
    # カレンダーをHTML形式で取得
    cal = MyCalendar(username,
                     {t.deadline.strftime('%Y%m%d'): t.done for t in task})  # 予定がある日付をキーとして渡す
    
    cal = cal.formatyear(today.year, 4)  # カレンダーをHTMLで取得

    # 直近のタスクだけでいいので、リストを書き換える
    task = [t for t in task if today <= t.deadline <= next_w]
    links = [t.deadline.strftime('/todo/' + username + '/%Y/%m/%d') for t in task]  # 直近の予定リンク
    
    res = templates.TemplateResponse(
        'admin.html',
        {
            'request': request,
            'user': user,
            'task': task,
            'links': links,
            'calender': cal
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

def detail(request: Request, username, year, month, day,
    credentials: HTTPBasicCredentials = Depends(security)):
    """URLパターンは引数で取得可能"""
    username_tmp = auth(credentials)
    if username_tmp != username:
        return RedirectResponse("/")
    
    user = db.session.query(User).filter(User.username == username).first()
    task = db.session.query(Task).filter(Task.user_id == user.id).all()
    db.session.close()

    theday = '{}{}{}'.format(year, month.zfill(2), day.zfill(2))
    task = [t for t in task if t.deadline.strftime('%Y%m%d') == theday]
    
    res = templates.TemplateResponse('detail.html',
        {
            'request': request,
            'username': username,
            'task': task,
            'year': year,
            'month': month,
            'day': day
        }
    )
    return res

async def done(request: Request, credentials: HTTPBasicCredentials = Depends(security)):
    username = auth(credentials)
    user = db.session.query(User).filter(User.username == username).first()
    task = db.session.query(Task).filter(Task.user_id == user.id).all()

    data = await request.form()
    t_dones = data.getlist('done[]')
    for t in task:
        if str(t.id) in t_dones:
            t.done = True
    db.session.commit()
    db.session.close()

    return RedirectResponse('/admin')

async def add(request: Request, credentials: HTTPBasicCredentials = Depends(security)):
    username = auth(credentials)

    user = db.session.query(User).filter(User.username == username).first()

    data = await request.form()
    year = int(data['year'])
    month = int(data['month'])
    day = int(data['day'])
    hour = int(data['hour'])
    minute = int(data['minute'])

    deadline = datetime(year=year, month=month, day=day, hour=hour, minute=minute)
    task = Task(user.id, data['content'], deadline)
    db.session.add(task)
    db.session.commit()
    db.session.close()

    return RedirectResponse('/admin')

def delete(request: Request, task_id, credentials: HTTPBasicCredentials = Depends(security)):
    username = auth(credentials)
    user = db.session.query(User).filter(User.username == username).first()
    
    task = db.session.query(Task).filter(Task.id == task_id).first()
    # UserIDが異なればリダイレクト
    if task.user_id != user.id:
        return RedirectResponse('/admin')
    
    # 削除してコミット
    db.session.delete(task)
    db.session.commit()
    db.session.close()

    return RedirectResponse('/admin')
