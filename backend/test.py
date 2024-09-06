# check if creating docs
#    - check if added to db
#    - check if added to index

# check if searching works
#    - check if < 20
#    - check for errors

# check deleting doc
#    - check if deleted from db
#    - check if deleted from index

import requests



WEBSITE_URL = 'http://localhost:8000'
ELASTIC_URL = 'http://localhost:9200'
test_obj = {'text': 'text', 'rubrics': ['VK', 'Inst']}



def test_check_creating_doc():
    x = requests.post(WEBSITE_URL + '/create_doc', json = {'text': 'text', 'rubrics': ['VK', 'Inst']})
    obj_uuid = x.json()['document']['id']
    assert x.status_code == 200
    x = requests.get(WEBSITE_URL + f'/get_document/{obj_uuid}')
    assert x.status_code == 200 
    assert x.json()['id'] == obj_uuid 
    x = requests.get(f'{ELASTIC_URL}/documents/_doc/{obj_uuid}')
    assert x.json()['found'] == True

def test_check_deleting_doc():
    x = requests.post(WEBSITE_URL + '/create_doc', json = test_obj)
    obj_uuid = x.json()['document']['id']
    x = requests.delete(WEBSITE_URL + f'/remove_doc/{obj_uuid}')
    assert requests.get(WEBSITE_URL + f'/get_document/{obj_uuid}').status_code == 404
    x = requests.get(f'{ELASTIC_URL}/documents/_doc/{obj_uuid}')

    assert x.json()['found'] == False

