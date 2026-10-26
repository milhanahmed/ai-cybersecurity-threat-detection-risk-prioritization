"""Regression checks against instructor feedback using an isolated database."""
import os
from pathlib import Path
import pytest
from fastapi.testclient import TestClient
from src.api.app import app
AUTH = ('analyst', 'test-only-long-password')
@pytest.fixture
def client(monkeypatch, tmp_path):
    monkeypatch.setenv('CYBER_USERNAME', AUTH[0])
    monkeypatch.setenv('CYBER_PASSWORD', AUTH[1])
    monkeypatch.setenv('CYBER_DB_PATH', str(tmp_path/'regression.db'))
    from src.database import database
    monkeypatch.setattr(database, "DB_PATH", str(tmp_path/"regression.db"))
    database.init_db()
    client = TestClient(app)
    client.auth = AUTH
    return client
@pytest.fixture
def event():
    return dict(event_id='W8-DEMO',timestamp='2026-10-26T12:00:00Z',source='vpn-gateway',
        event_type='login_failure',failed_attempts=8,known_bad_ip=1,privileged_account=1,
        severity=.9,business_impact=.8)
@pytest.mark.parametrize('field,value', [('event_id','  '),('timestamp','not-a-date'),
    ('failed_attempts',-1),('known_bad_ip',2),('event_type','unsupported'),
    ('privileged_account',2),('source',' '),('severity',1.1),('business_impact',-.1),
    ('failed_attempts',1.5),('event_id','x'*129)])
def test_invalid_domain_values_rejected(client,event,field,value):
    event[field]=value
    assert client.post('/analyze',json=event).status_code==422
    assert client.get('/events').json()['events']==[]
@pytest.mark.parametrize('path',['/events','/'])
def test_anonymous_read_denied(client,path):
    r=client.get(path,auth=None);assert r.status_code==401
    assert r.headers['www-authenticate'].startswith('Basic')
def test_anonymous_submission_denied(client,event):
    assert client.post('/analyze',json=event,auth=None).status_code==401
@pytest.mark.parametrize('auth',[('wrong',AUTH[1]),(AUTH[0],'incorrect'),('µser','incorrect')])
def test_wrong_credentials_denied(client,auth):
    assert client.get('/events',auth=auth).status_code==401
def test_missing_configuration_fails_closed(client,monkeypatch):
    monkeypatch.delenv('CYBER_PASSWORD')
    assert client.get('/events').status_code==503
def test_short_password_fails_closed(client,monkeypatch):
    monkeypatch.setenv('CYBER_PASSWORD','short')
    assert client.get('/events').status_code==503
def test_authorized_pipeline_and_persistence(client,event):
    r=client.post('/analyze',json=event);assert r.status_code==200
    assert r.json()['risk_score']==87.42 and r.json()['priority']=='high'
    assert client.get('/events').json()['events'][0]['event_id']==event['event_id']
def test_normalized_text(client,event):
    event['event_id']='  trimmed  '
    assert client.post('/analyze',json=event).json()['event_id']=='trimmed'
def test_markup_is_stored_literally(client,event):
    event['event_id']='<b>literal marker</b>'
    assert client.post('/analyze',json=event).status_code==200
    assert client.get('/events').json()['events'][0]['event_id']=='<b>literal marker</b>'
def test_dashboard_safe_rendering(client):
    html=client.get('/').text
    assert 'cell.textContent = String(value)' in html and 'tr.innerHTML' not in html
    assert 'readResponse' in html and 'aria-live="polite"' in html
