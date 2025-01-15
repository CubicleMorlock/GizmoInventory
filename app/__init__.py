from flask import Flask

inventory_app = Flask(__name__)

from app import routes
