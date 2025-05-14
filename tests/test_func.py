import sqlite3
from fastapi.testclient import TestClient
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from main import app

client = TestClient(app)

def setup_db():
    connector = sqlite3.connect('basa.db')
    cursor = connector.cursor()
    cursor.execute("DROP TABLE IF EXISTS logins")
    cursor.execute("DROP TABLE IF EXISTS user_tasks")
    connector.commit()
    connector.close()

def test_register():
    response = client.post("/register", data={"login": "knadovec", "password": "123"}, follow_redirects=False)
    assert response.status_code == 303

def test_login_success():
    response = client.post("/login", data={"login": "knadovec", "password": "123"}, follow_redirects=False)
    assert response.status_code == 303

def test_register_sushestv():
    response = client.post("/register", data={"login": "knadovec", "password": "123"}, follow_redirects=False)
    assert response.status_code == 303

def test_login_fail():
    response = client.post("/login", data={"login": "neknadovec", "password": "1234"})
    assert response.status_code == 200

def test_create():
    response = client.post("/create_task",data={"task_name": "Matan","task_status": "Активная","task_prioritet": 3,"task_opis": "Описание","name": "user"}, follow_redirects=False)
    assert response.status_code == 303

def test_well():
    response = client.get("/well?name=knadovec")
    assert response.status_code == 200

def test_find():
    response = client.post("/find", data={"string": "Matan"})
    assert response.status_code == 200

def test_find_nesush_task():
    response = client.post("/find", data={"string": "Tralalelo-tralala"})
    assert response.status_code == 200

def test_sort_by_priority():
    response = client.get("/priority")
    assert response.status_code == 200

def test_sort_by_status():
    response = client.get("/status")
    assert response.status_code == 200

def test_sort_by_name():
    response = client.get("/name")
    assert response.status_code == 200

def test_sort_by_date():
    response = client.get("/data")
    assert response.status_code == 200

def test_delete():
    connector = sqlite3.connect("basa.db")
    cursor = connector.cursor()
    cursor.execute("SELECT task_id FROM user_tasks WHERE task_name = ?", ("Matan",))
    id = cursor.fetchone()[0]
    connector.close()
    response = client.post(f"/delete_task/{id}", follow_redirects=False)
    assert response.status_code == 303

def test_well_empty():
    connection = sqlite3.connect("basa.db")
    cursor = connection.cursor()
    cursor.execute("DELETE FROM user_tasks")
    connection.commit()
    connection.close()
    response = client.get("/well?name=knadovec")
    assert response.status_code == 200
