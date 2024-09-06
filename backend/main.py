import os
import csv
from uuid import uuid4, UUID
from typing import Union
from fastapi import FastAPI, Depends, Query, HTTPException
from schemas import TextInput, CreateDoc
from datetime import datetime
from database import *
from sqlalchemy import MetaData


app = FastAPI()
Base.metadata.create_all(bind=engine)





@app.get('/')
async def hello_world():
    return {'message': 'Hello World'}

@app.post('/create_doc')
async def create_doc(doc: CreateDoc, db: Session = Depends(get_db)):
    uuid = str(uuid4())
    datetime_field = datetime.now()
    document = {
        'id': uuid,
        'text': doc.text,
        'rubrics': doc.rubrics,
        'created_date': datetime_field
    }
    create_document(db, uuid, doc.text, doc.rubrics, datetime_field)
    es.index(index="documents", id=uuid, body={'text': doc.text, 'rubrics': doc.rubrics, 'created_date': datetime_field})
    return {'document': document}

@app.get('/get_document/{doc_id}')
async def get_document(doc_id: str, db: Session = Depends(get_db)):
    doc = get_document_data(db, doc_id)
    if doc is not None:
        return {'id': doc.id, 'text': doc.text, 'rubrics': doc.rubrics, 'created_date': doc.created_date}
    else:
        raise HTTPException(status_code=404, detail='document not found')

@app.get("/search")
def read_root(text: TextInput, db: Session = Depends(get_db)):
    search_query = {
        "query": {
            "match": {
                "text": f"{text}"
            }
        }
    }
    res = es.search(index="documents", body=search_query)['hits']['hits']
    items = []
    for item in res[:20]:
        if not item['_source']['text'] == 'text' and not item['_source']['rubrics'] == 'rubrics' and not item['_source']['created_date'] == 'created_date':
            items.append({'id': item['_id'], 'text': item['_source']['text'], 'rubrics': item['_source']['text'], 'created_date': datetime.strptime(item['_source']['created_date'], "%Y-%m-%d %H:%M:%S").timestamp()})
    sorted_items = sorted(items, key=lambda x: x['created_date'], reverse=True) 
    return {'results': sorted_items}

@app.post('/fullfill_table')
def fullfill_table(db: Session = Depends(get_db)):
    with open('posts.csv', newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        doc = {}
        rubrics = []
        for row in reader:
            try:
                id = str(uuid4())
                text, created_date, rubrics = row
                doc = {'text': text, 'rubrics': rubrics[2:-2].split(', ')}
                es.index(index="documents", id=id, body={'text': doc['text'], 'rubrics': doc['rubrics'], 'created_date': created_date})
                create_document(db, id, text, rubrics[2:-2].split(', '), datetime.strptime(created_date, "%Y-%m-%d %H:%M:%S"))
            except Exception as e:
                print(doc)
                print(created_date)
                print(e)
    return {'status': 'ok'}

@app.post('/drop_db')
def drop_db(db: Session = Depends(get_db)):
    drop_db_command(db)
    return {'status': 'ok'}

@app.delete("/remove_doc/{doc_id}")
def remove_doc(doc_id: str, db: Session = Depends(get_db)):
    doc = get_document_data(db, doc_id)
    if doc is not None:
        delete_document(db, doc_id)
        es.delete(index="documents", id=doc_id)
    return {"status": "ok"}