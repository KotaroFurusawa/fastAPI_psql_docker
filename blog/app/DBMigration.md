# dbのマイグレーション方法
1. `models.py`を編集する
2. `alembic revision -m {ファイル名}`をこのディレクトリで実行
3. `migration/versions`の中に生成されたファイルを編集する
4. `alembic upgrade head`をこのディレクトリで実行

本当は、`--autogenerate`で実行したいけれど、なぜか同期されない...
### 参考：
1. https://qiita.com/penpenta/items/c993243c4ceee3840f30
2. http://nekopachi.net/2021/02/25/post-349/?amp=1
3. https://libproc.com/fastapi-define-model-and-migration/