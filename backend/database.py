from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import Session
from sqlalchemy import Column, String, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.types import ARRAY
from datetime import datetime as dt
from elasticsearch import Elasticsearch

SQLALCHEMY_DATABASE_URL = "postgresql://postgres:postgres@db:5432/postgres"
ELASTIC_PASSWORD = "OVd9PgwIZr1+uTnU=ude"

# Create the client instance
es = Elasticsearch(
    "http://es01:9200",
    #ca_certs="./http_ca.crt",
    basic_auth=("elastic", ELASTIC_PASSWORD)
)

es.indices.create(index="documents", ignore=400)

engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
session = Session()
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class Document(Base):
    __tablename__ = "documents"
    id = Column(String, name="id", primary_key=True)
    rubrics = Column(ARRAY(String))
    text = Column(String, nullable=False)
    created_date = Column(DateTime, default=dt.utcnow)




def get_document_data(db: Session, document_id: str):
    return db.query(Document).filter(Document.id == document_id).first()


def create_document(db: Session, uuid: str, text: str, rubrics: list, datetime_field: dt):
    document = Document(id = uuid, text = text, rubrics = rubrics, created_date = datetime_field)
    db.add(document)
    db.commit()
    db.refresh(document)
    return document

def delete_document(db: Session, id: str):
    document = db.query(Document).filter(Document.id == id).first()
    db.delete(document)
    db.commit()

def drop_db_command(db: Session):
    Base.metadata.drop_all(bind=engine)
    