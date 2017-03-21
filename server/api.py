# coding: utf-8

__author__ = 'qinanlan <qinanlan@domob.com>'

import os
import json
from flask import jsonify, request
from flask import render_template
from . import app

BASE_URL = os.path.realpath(os.path.dirname(__file__))

@app.route('/home', methods=['GET'])
def home():
    return render_template('driver_route.html')

@app.route('/api/map', methods=['POST'])
def get_map():
    city = request.form['city']
    json_url = os.path.join(BASE_URL, 'static/data', '%s.json' % city)
    with open(json_url) as json_file:
        data = json.load(json_file)
    return jsonify(data)

@app.route('/api/query', methods=['POST'])
def query():
    driver_id = request.form['driver_id']
    date = request.form['date']

    res = json.dumps({'pick_route': [[116.418757, 39.917544],
                                     [116.195445, 39.914601],
                                     [116.666665, 40.111111],
                                     [116.851111, 40.371111],


                                    ],
                      'charge_route': [[116.252911, 39.542020],
                                       [116.363391, 39.967860],
                                       [116.777777, 40.222222],


                                    ]})
    return jsonify(res)