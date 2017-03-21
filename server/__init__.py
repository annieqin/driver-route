# coding: utf-8

__author__ = 'qinanlan <qinanlan@domob.com>'

from flask import Flask

app = Flask(__name__, static_url_path='/static')

import api