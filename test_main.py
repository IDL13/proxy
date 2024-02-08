import time

from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"msg": "Server started"}
    
def test_setting():
    setting_json = {"time_lock": 60, "request_limit": 60}
    
    response = client.post("/setting/", json = setting_json)
    assert response.status_code == 200
    assert response.json() == {"time_lock": 60, "request_limit": 60}
    
def test_remove():
    for i in range(60):
        response = client.get("/redirect/github.com", headers = {"X-Forwarded-For":"123.456.789.123"})
        assert response.status_code == 200 

    response = client.get("/redirect/github.com", headers = {"X-Forwarded-For":"123.456.789.123"})
    assert response.status_code == 429 
     
    response = client.get("/rm/123.456.789")
    assert response.status_code == 200
    assert response.json() == {"msg": "Ip addres unlock"}
    
    response = client.get("/redirect/github.com", headers = {"X-Forwarded-For":"123.456.789.123"})
    assert response.status_code == 200
    
def test_redirect():
    for i in range(59):
        response = client.get("/redirect/github.com", headers = {"X-Forwarded-For":"123.456.789.123"})
        assert response.status_code == 200 
    
    response = client.get("/redirect/github.com", headers = {"X-Forwarded-For":"123.456.789.123"})
    assert response.status_code == 429
    
    for j in range(59):
        response = client.get("/redirect/github.com", headers = {"X-Forwarded-For":"123.456.789.123"})
        assert response.status_code == 429
        time.sleep(1)
        
    response = client.get("/redirect/github.com", headers = {"X-Forwarded-For":"123.456.789.123"})
    assert response.status_code == 429

    
    
    
    