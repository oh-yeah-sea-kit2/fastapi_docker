# fastapi_docker

## コマンド
- pipenv shell
- pipenv run python app.py
- pipenv install {library_name}

### pipenv環境でアプリ立ち上げ
- pipenv run uvicorn app:app --reload

### pytest実行
- pipenv run pytest

## 今後の予定
- herokuデプロイ(docker-compose)
- FastAPIとPostgreSQLをつなぐ
- FastAPIからSQLAlchemyを使う
- [flask ページネーション](https://www.ravness.com/2019/07/flaskpaginate/)
- [IPで制限をかける。](https://qiita.com/takuya-andou/items/32a3002aa951b835871b)
- Firebase Authenticationを使う

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

