# fastapi_docker

## 気になること
- ログアウト機能をつけたい
- 参考URL
  - https://gist.github.com/nilsdebruin/8b36cd98c9949a1a87e3a582f70146f1

## コマンド
- pipenv shell
- pipenv run python app.py
- pipenv install {library_name}

### requirements.txtの生成
- pipenv lock -r > requirements.txt


### pipenv環境でアプリ立ち上げ
- pipenv run uvicorn app:app --reload

### pytest実行
- pipenv run pytest

## 今後の予定
- [x] herokuデプロイ(docker-compose)
- [ ] [FastAPI Tutorial: toDo Application](https://github.com/rightcode/FastAPITutrial)
- [ ] FastAPIとPostgreSQLをつなぐ
- [ ] FastAPIからSQLAlchemyを使う
- [ ] [flask ページネーション](https://www.ravness.com/2019/07/flaskpaginate/)
- [ ] [IPで制限をかける。](https://qiita.com/takuya-andou/items/32a3002aa951b835871b)
- [ ] Firebase Authenticationを使う

## 参考URL
- [RESTful APIをシュッと作る技術 - PythonとFastAPIでバックエンドを5時間ちょいで作ってみた
](https://shinyorke.hatenablog.com/entry/fastapi)
- [FastAPI公式ページ](https://fastapi.tiangolo.com/)
- [[FastAPI] Python製のASGI Web フレームワーク FastAPIに入門する](https://qiita.com/bee2/items/75d9c0d7ba20e7a4a0e9)
- [NoSQL×PaaSで運用するナレッジベース+WebAPI](https://qiita.com/1ntegrale9/items/c4f315f918bad7a0f180)

## URL
- http://localhost:3000
- http://localhost:3000/docs
- http://localhost:3000/redoc
- https://sheltered-mountain-37347.herokuapp.com/
- https://sheltered-mountain-37347.herokuapp.com/redoc
- https://sheltered-mountain-37347.herokuapp.com/docs

## チュートリアル
- [【第1回】FastAPIチュートリアル: ToDoアプリを作ってみよう【環境構築編】](https://rightcode.co.jp/blog/information-technology/fastapi-tutorial-todo-apps-environment)
- [【第2回】FastAPIチュートリアル: ToDoアプリを作ってみよう【モデル構築編】](https://rightcode.co.jp/blog/information-technology/fastapi-tutorial-todo-apps-model-building)
- [【第3回】FastAPIチュートリアル: toDoアプリを作ってみよう【認証・ユーザ登録編】](https://rightcode.co.jp/blog/information-technology/fastapi-tutorial-todo-apps-authentication-user-registration)
- [【第4回】FastAPIチュートリアル: toDoアプリを作ってみよう【管理者ページ改良編】](https://rightcode.co.jp/blog/information-technology/fastapi-tutorial-todo-apps-admin-page-improvement)
- [【第5回】FastAPIチュートリアル: toDoアプリを作ってみよう【予定詳細ページ作成編】](https://rightcode.co.jp/blog/information-technology/fastapi-tutorial-todo-apps-event-details-page-create)
- [【第6回】FastAPIチュートリアル: toDoアプリを作ってみよう【予定の追加・削除編】](https://rightcode.co.jp/blog/information-technology/fastapi-tutorial-todo-apps-event-add-delete)
- [【最終回】FastAPIチュートリアル: toDoアプリを作ってみよう【WebAPI編】](https://rightcode.co.jp/blog/information-technology/fastapi-tutorial-todo-apps-web-api-complete)


