【デバッグ時ユーザ情報】
<!-- Admin -->
email: hoge@hoge.com
password: hogehoge

【Developer情報】
<!-- Launch server with -->
py manage.py runserver 8080

<!-- models.py編集後忘れずに	 -->
py manage.py makemigrations
py manage.py migrate 

<!-- dbの中身が見たい場合(sqlite3のインストールが必要) -->
py manage.py dbshell 

<!-- migration時に沼ったらデータベースを削除 -->
migrationsファイル内の__init__.py以外をすべて削除
db.sqlite3を削除
再度makemigrationsとmigrateを実行
migrateを再度実行したばあい、py manage.py createsuperuserで再度スーパーユーザを作る
