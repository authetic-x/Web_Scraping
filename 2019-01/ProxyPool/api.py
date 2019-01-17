from db import RedisClient
from flask import Flask, g

app = Flask(__name__)

def get_conn():
    if not hasattr(g, 'redis'):
        g.redis = RedisClient()
    return g.redis

@app.route('/')
def index():
    return '<h1>Welcome to ProxyPool</h1>'

@app.route('/random')
def random():
    conn = get_conn()
    return conn.random()

@app.route('/count')
def count():
    conn = get_conn()
    return str(conn.count())

if __name__ == '__main__':
    app.run()