import pytest
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from app import app, db

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
        yield client
        with app.app_context():
            db.drop_all()

def test_home_page_loads(client):
    """Home page should return 200"""
    response = client.get('/')
    assert response.status_code == 200

def test_add_transaction(client):
    """Adding a transaction should redirect back to home"""
    response = client.post('/add', data={
        'item': 'Test salary',
        'amount': '500000',
        'type': 'Income'
    }, follow_redirects=True)
    assert response.status_code == 200

def test_delete_transaction(client):
    """Deleting a transaction should redirect back to home"""
    client.post('/add', data={
        'item': 'To delete',
        'amount': '1000',
        'type': 'Expense'
    }, follow_redirects=True)
    response = client.post('/delete/1', follow_redirects=True)
    assert response.status_code == 200
    
def test_edit_transaction(client):
    """Editing a transaction should update it and redirect home"""
    client.post('/add', data={
        'item': 'Old item',
        'amount': '1000',
        'type': 'Expense'
    }, follow_redirects=True)
    response = client.post('/edit/1', data={
        'item': 'Updated item',
        'amount': '2000',
        'type': 'Income'
    }, follow_redirects=True)
    assert response.status_code == 200