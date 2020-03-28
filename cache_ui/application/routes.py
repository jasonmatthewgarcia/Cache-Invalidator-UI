from flask import current_app as app
from flask import render_template, redirect, url_for, request
from . import redis_client

from loguru import logger
from random import randint
import json

@app.route('/')
def load_cache():
    cache_data = []
    for key in redis_client.scan_iter('*'):
        model = key.split(':')[0]
        cache_record = {
            'model': model,
            'key': key,
            'value': redis_client.get(key),
            'ttl': redis_client.pttl(key)
        }
        cache_data.append(cache_record)

    return render_template('index.html', items=cache_data)

@app.route('/', methods=['POST'])
def delete_cache():
    key = request.form.get('key')
    if key:
        redis_client.delete(key)
    else:
        redis_client.flushall()
        
    return redirect(url_for('load_cache'))

@app.route('/sample')
def sample_page():
    return render_template('test.html')

@app.route('/seed', methods=['POST'])
def seed():
    cache_keys = [
        'entities:1234', 'taskgroups:111', 'taskgroups:222', 
        'taskgroups:333', 'interventions:111', 'interventions:222',
        'interventions:333'
    ]
    cache_data = {
        key: {'some_data': randint(1,1000)} for key in cache_keys
    }

    redis_client.flushall()
    for key, value in cache_data.items():
        redis_client.set(key, json.dumps(value), ex=10000)

    return redirect(url_for('load_cache'))
