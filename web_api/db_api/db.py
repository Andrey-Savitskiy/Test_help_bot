from sqlalchemy_utils import database_exists, create_database
from sqlalchemy import create_engine, Integer, String, Column, DateTime, BigInteger
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
from loader import DB_HOST, DB_PASS, DB_USER, DB_DB


engine = create_engine(f"postgresql+psycopg2://{DB_USER}:{DB_PASS}@{DB_HOST}/{DB_DB}")

# engine = create_engine(f"postgresql+psycopg2://postgres:12345@localhost:5432/not_alisa_but_bot")

if not database_exists(engine.url):
    create_database(engine.url)

Base = declarative_base()

class FeedBacks(Base):
    __tablename__ = 'feedbacks'
    id = Column(Integer(), primary_key=True, autoincrement=True)
    tg_id = Column(BigInteger(), nullable=False)
    created_on = Column(DateTime(), default=datetime.now)
    username = Column(String(32), nullable=False)
    feedback = Column(String(), nullable=False)
    end = Column(String(4), nullable=False)
    photo = Column(String(64), default=False)

Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

