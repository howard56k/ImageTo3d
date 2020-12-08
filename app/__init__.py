from flask import Flask
from redis import Redis
from rq import Queue
import os

app = Flask(__name__)

q = Queue(connection=Redis(host=os.getenv("REDIS_HOST", '127.0.0.1'),port=os.getenv("REDIS_PORT", '6379')))

from app import views
