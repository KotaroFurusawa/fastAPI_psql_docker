import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = 'postgresql://{user}:{password}@{host}:{port}/{database}'.format(**{
    # 外部ファイルから引っ張ってくる
    'user': os.getenv("POSGRE_USER", 'admin'),
    'password': os.getenv("POSGRE_PASSWORD", 'admin'),
    'host': os.getenv("POSGRE_HOST", 'mypg'),
    'port': os.getenv("POSGRE_PORT", "5432"),
    'database': os.getenv("POSGRE_DATABASE", 'test_db')
})

engine = create_engine(DATABASE_URL)

sessionLocal = sessionmaker(bind=engine, autoflush=False)

Base = declarative_base()


def get_db():
    db = sessionLocal()
    try:
        yield db
    finally:
        db.close()
