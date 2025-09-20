import pytest
import json
from app.models import Data
from app import db


class TestDataRoutes:
    
    def test_insert_data_success(self, client, app):
        with app.app_context():
            response = client.post('/data', 
                                 data=json.dumps({'name': 'test_data'}),
                                 content_type='application/json')
            
            assert response.status_code == 200
            data = json.loads(response.data)
            assert data['message'] == 'Data inserted successfully'
            
            saved_data = Data.query.filter_by(name='test_data').first()
            assert saved_data is not None
            assert saved_data.name == 'test_data'
    
    def test_insert_data_duplicate(self, client, app):
        with app.app_context():
            existing_data = Data(name='existing_data')
            db.session.add(existing_data)
            db.session.commit()
            
            response = client.post('/data',
                                 data=json.dumps({'name': 'existing_data'}),
                                 content_type='application/json')
            
            assert response.status_code == 409
            data = json.loads(response.data)
            assert data['message'] == 'Data already exists'
    
    def test_insert_data_with_empty_name(self, client, app):
        with app.app_context():
            response = client.post('/data',
                                 data=json.dumps({'name': ''}),
                                 content_type='application/json')
            
            assert response.status_code == 200
            data = json.loads(response.data)
            assert data['message'] == 'Data inserted successfully'
    
    def test_insert_data_with_none_name(self, client, app):
        with app.app_context():
            response = client.post('/data',
                                 data=json.dumps({'name': None}),
                                 content_type='application/json')
            
            assert response.status_code == 200
            data = json.loads(response.data)
            assert data['message'] == 'Data inserted successfully'
    
    def test_insert_data_without_name_field(self, client, app):
        with app.app_context():
            response = client.post('/data',
                                 data=json.dumps({}),
                                 content_type='application/json')
            
            assert response.status_code == 200
            data = json.loads(response.data)
            assert data['message'] == 'Data inserted successfully'
    
    def test_insert_data_invalid_json(self, client, app):
        with app.app_context():
            response = client.post('/data',
                                 data='invalid json',
                                 content_type='application/json')
            
            assert response.status_code == 400
    
    def test_get_all_data_empty(self, client, app):
        with app.app_context():
            response = client.get('/data')
            
            assert response.status_code == 200
            data = json.loads(response.data)
            assert data == []
    
    def test_get_all_data_single_item(self, client, app):
        with app.app_context():
            test_data = Data(name='single_item')
            db.session.add(test_data)
            db.session.commit()
            
            response = client.get('/data')
            
            assert response.status_code == 200
            data = json.loads(response.data)
            assert len(data) == 1
            assert data[0]['name'] == 'single_item'
            assert data[0]['id'] == test_data.id
    
    def test_get_all_data_multiple_items(self, client, app):
        with app.app_context():
            data1 = Data(name='item1')
            data2 = Data(name='item2')
            data3 = Data(name='item3')
            db.session.add_all([data1, data2, data3])
            db.session.commit()
            
            response = client.get('/data')
            
            assert response.status_code == 200
            data = json.loads(response.data)
            assert len(data) == 3
            
            names = [item['name'] for item in data]
            assert 'item1' in names
            assert 'item2' in names
            assert 'item3' in names
    
    def test_delete_data_success(self, client, app):
        with app.app_context():
            test_data = Data(name='to_delete')
            db.session.add(test_data)
            db.session.commit()
            data_id = test_data.id
            
            response = client.delete(f'/data/{data_id}')
            
            assert response.status_code == 200
            data = json.loads(response.data)
            assert data['message'] == 'Data deleted successfully'
            
            deleted_data = Data.query.get(data_id)
            assert deleted_data is None
    
    def test_delete_data_not_found(self, client, app):
        with app.app_context():
            response = client.delete('/data/999')
            
            assert response.status_code == 404
            data = json.loads(response.data)
            assert data['message'] == 'Data not found'
    
    def test_delete_data_invalid_id(self, client, app):
        with app.app_context():
            response = client.delete('/data/invalid')
            
            assert response.status_code == 404
    
    def test_post_method_not_allowed_on_wrong_endpoint(self, client, app):
        with app.app_context():
            response = client.post('/data/1')
            assert response.status_code == 405
    
    def test_put_method_not_allowed(self, client, app):
        with app.app_context():
            response = client.put('/data')
            assert response.status_code == 405
    
    def test_patch_method_not_allowed(self, client, app):
        with app.app_context():
            response = client.patch('/data')
            assert response.status_code == 405
    
    def test_integration_create_get_delete(self, client, app):
        with app.app_context():
            response = client.post('/data',
                                 data=json.dumps({'name': 'integration_test'}),
                                 content_type='application/json')
            assert response.status_code == 200
            
            response = client.get('/data')
            assert response.status_code == 200
            data = json.loads(response.data)
            assert len(data) == 1
            item_id = data[0]['id']
            
            response = client.delete(f'/data/{item_id}')
            assert response.status_code == 200
            
            response = client.get('/data')
            assert response.status_code == 200
            data = json.loads(response.data)
            assert len(data) == 0