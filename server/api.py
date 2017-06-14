# coding: utf-8

__author__ = 'qinanlan <qinanlan@domob.com>'

import os
import json
import csv
from datetime import datetime
from math import sin, cos, sqrt, atan2, radians
from openpyxl import Workbook
from flask import jsonify, request
from flask import render_template
from . import app

BASE_URL = os.path.realpath(os.path.dirname(__file__))
R = 6373.0
MORNING_PEAK_FROM = '08:00:00'
MORNING_PEAK_TO = '10:30:00'
EVENING_PEAK_FROM = '17:00:00'
EVENING_PEAK_TO = '20:30:00'
morning_peak_from = datetime.strptime('%s' % MORNING_PEAK_FROM,
                                      '%H:%M:%S')
morning_peak_to = datetime.strptime('%s' % MORNING_PEAK_TO,
                                    '%H:%M:%S')
evening_peak_from = datetime.strptime('%s' % EVENING_PEAK_FROM,
                                      '%H:%M:%S')
evening_peak_to = datetime.strptime('%s' % EVENING_PEAK_TO,
                                    '%H:%M:%S')

@app.route('/long-order', methods=['GET'])
def long_order():
    return render_template('long-order.html')


@app.route('/home3', methods=['GET'])
def home3():
    return render_template('week-route.html')


def judge_distance(start_long, start_la, finish_long, finish_la):
    long1 = radians(float(start_long))
    la1 = radians(float(start_la))
    long2 = radians(float(finish_long))
    la2 = radians(float(finish_la))

    dlong = long2 - long1
    dla = la2 - la1
    a = sin(dla/2)**2 + cos(la1)*cos(la2)*sin(dlong/2)**2
    c = 2*atan2(sqrt(a), sqrt(1-a))

    distance = R*c
    if distance < 5:
        return 0
    elif 5 <= distance < 10:
        return 1
    else:
        return 2


@app.route('/api/all-order', methods=['POST'])
def all_order():
    count = 1
    date = request.form['date']
    res = []
    while True:
        try:
            filename = BASE_URL + '/' + str(date) + '-' + str(count) + '.csv'
            with open(filename) as f:
                f_csv = csv.reader(f)
                for line in f_csv:
                    start_time = line[4]
                    start_long = line[5]
                    start_lat = line[6]
                    finish_time = line[7]
                    finish_long = line[8]
                    finish_lat = line[9]
                    res.append({
                        start_time: start_time,
                        start_long: start_long,
                        start_lat: start_lat,
                        finish_time: finish_time,
                        finish_long: finish_long,
                        finish_lat: finish_lat
                    })
            count += 1
        except:
            break


@app.route('/api/period-intensity-day', methods=['POST'])
def period_intensity_day():
    res = {
        'morning': {
            'receive_nodes': {
                'name': '接单时间',
                'data': []
            },
            'start_nodes': {
                'name': '行程开始时间',
                'data': []
            },
            'finish_nodes': {
                'name': '行程结束时间',
                'data': []
            }
        },
        'evening': {
            'receive_nodes': {
                'name': '接单时间',
                'data': []
            },
            'start_nodes': {
                'name': '行程开始时间',
                'data': []
            },
            'finish_nodes': {
                'name': '行程结束时间',
                'data': []
            }
        },
        'flat': {
            'receive_nodes': {
                'name': '接单时间',
                'data': []
            },
            'start_nodes': {
                'name': '行程开始时间',
                'data': []
            },
            'finish_nodes': {
                'name': '行程结束时间',
                'data': []
            }
        }
    }
    driver_id = request.form['driver_id']
    date = request.form['date']
    filename = BASE_URL + '/' + str(driver_id)+'.csv'
    with open(filename) as f:
        f_csv = csv.reader(f)
        headers = next(f_csv)
        for line in f_csv:
            current_date = ''.join(line[4].split()[0].split('-'))
            if current_date == date:
                receive_time = line[4]
                receive_datetime = datetime.strptime('%s' % receive_time.split()[1],
                                                     '%H:%M:%S')
                receive_long = line[5]
                receive_la = line[6]
                start_time = line[7]
                start_long = line[8]
                start_la = line[9]
                finish_time = line[10]
                finish_long = line[11]
                finish_la = line[12]
                if (receive_datetime - morning_peak_from).total_seconds() > 0 and \
                   (morning_peak_to - receive_datetime).total_seconds() > 0:
                    res['morning']['receive_nodes']['data'].append({
                        'time': receive_time,
                        'coord': [float(receive_long), float(receive_la)]
                    })
                    res['morning']['start_nodes']['data'].append({
                        'time': start_time,
                        'coord': [float(start_long), float(start_la)]
                    })
                    res['morning']['finish_nodes']['data'].append({
                        'time': finish_time,
                        'coord': [float(finish_long), float(finish_la)]
                    })
                elif (receive_datetime - evening_peak_from).total_seconds() > 0 and \
                     (evening_peak_to - receive_datetime).total_seconds() > 0:
                    res['evening']['receive_nodes']['data'].append({
                        'time': receive_time,
                        'coord': [float(receive_long), float(receive_la)]
                    })
                    res['evening']['start_nodes']['data'].append({
                        'time': start_time,
                        'coord': [float(start_long), float(start_la)]
                    })
                    res['evening']['finish_nodes']['data'].append({
                        'time': finish_time,
                        'coord': [float(finish_long), float(finish_la)]
                    })
                else:
                    res['flat']['receive_nodes']['data'].append({
                        'time': receive_time,
                        'coord': [float(receive_long), float(receive_la)]
                    })
                    res['flat']['start_nodes']['data'].append({
                        'time': start_time,
                        'coord': [float(start_long), float(start_la)]
                    })
                    res['flat']['finish_nodes']['data'].append({
                        'time': finish_time,
                        'coord': [float(finish_long), float(finish_la)]
                    })
    return jsonify(json.dumps(res))


@app.route('/api/period-intensity-start', methods=['POST'])
def period_intensity_start():
    res = {
        'morning': {
            'start_nodes': {
                'name': '行程开始时间',
                'data': []
            },
        },
        'evening': {
            'start_nodes': {
                'name': '行程开始时间',
                'data': []
            },
        },
        'flat': {
            'start_nodes': {
                'name': '行程开始时间',
                'data': []
            },
        }
    }
    driver_id = request.form['driver_id']
    start_date = request.form['start_date']
    end_date = request.form['end_date']
    filename = BASE_URL + '/' + str(driver_id)+'.csv'
    with open(filename) as f:
        f_csv = csv.reader(f)
        headers = next(f_csv)
        for line in f_csv:
            start_time = line[7]
            start_datetime = datetime.strptime('%s' % start_time.split()[1],
                                               '%H:%M:%S')
            start_long = line[8]
            start_la = line[9]
            if (start_datetime - morning_peak_from).total_seconds() > 0 and \
               (morning_peak_to - start_datetime).total_seconds() > 0:
                res['morning']['start_nodes']['data'].append({
                    'time': start_time,
                    'coord': [float(start_long), float(start_la)]
                })
            elif (start_datetime - evening_peak_from).total_seconds() > 0 and \
                 (evening_peak_to - start_datetime).total_seconds() > 0:
                res['evening']['start_nodes']['data'].append({
                    'time': start_time,
                    'coord': [float(start_long), float(start_la)]
                })
            else:
                res['flat']['start_nodes']['data'].append({
                    'time': start_time,
                    'coord': [float(start_long), float(start_la)]
                })
    return jsonify(json.dumps(res))


@app.route('/api/period-intensity-end', methods=['POST'])
def period_intensity_end():
    res = {
        'morning': {
            'end_nodes': {
                'name': '行程开始时间',
                'data': []
            },
        },
        'evening': {
            'end_nodes': {
                'name': '行程开始时间',
                'data': []
            },
        },
        'flat': {
            'end_nodes': {
                'name': '行程开始时间',
                'data': []
            },
        }
    }
    driver_id = request.form['driver_id']
    filename = BASE_URL + '/' + str(driver_id)+'.csv'
    with open(filename) as f:
        f_csv = csv.reader(f)
        headers = next(f_csv)
        for line in f_csv:
            start_time = line[7]
            start_datetime = datetime.strptime('%s' % start_time.split()[1],
                                               '%H:%M:%S')
            finish_long = line[11]
            finish_la = line[12]
            if (start_datetime - morning_peak_from).total_seconds() > 0 and \
               (morning_peak_to - start_datetime).total_seconds() > 0:
                res['morning']['end_nodes']['data'].append({
                    'time': start_time,
                    'coord': [float(finish_long), float(finish_la)]
                })
            elif (start_datetime - evening_peak_from).total_seconds() > 0 and \
                 (evening_peak_to - start_datetime).total_seconds() > 0:
                res['evening']['end_nodes']['data'].append({
                    'time': start_time,
                    'coord': [float(finish_long), float(finish_la)]
                })
            else:
                res['flat']['end_nodes']['data'].append({
                    'time': start_time,
                    'coord': [float(finish_long), float(finish_la)]
                })
    return jsonify(json.dumps(res))


@app.route('/api/period-intensity-week', methods=['POST'])
def period_intensity_week():
    res = {
        'morning': {
            'receive_nodes': {
                'name': '接单时间',
                'data': []
            },
            'start_nodes': {
                'name': '行程开始时间',
                'data': []
            },
            'finish_nodes': {
                'name': '行程结束时间',
                'data': []
            }
        },
        'evening': {
            'receive_nodes': {
                'name': '接单时间',
                'data': []
            },
            'start_nodes': {
                'name': '行程开始时间',
                'data': []
            },
            'finish_nodes': {
                'name': '行程结束时间',
                'data': []
            }
        },
        'flat': {
            'receive_nodes': {
                'name': '接单时间',
                'data': []
            },
            'start_nodes': {
                'name': '行程开始时间',
                'data': []
            },
            'finish_nodes': {
                'name': '行程结束时间',
                'data': []
            }
        }
    }
    driver_id = request.form['driver_id']
    start_date = request.form['start_date']
    end_date = request.form['end_date']
    filename = BASE_URL + '/' + str(driver_id)+'.csv'
    with open(filename) as f:
        f_csv = csv.reader(f)
        headers = next(f_csv)
        for line in f_csv:
            receive_time = line[4]
            receive_datetime = datetime.strptime('%s' % receive_time.split()[1],
                                                 '%H:%M:%S')
            receive_long = line[5]
            receive_la = line[6]
            start_time = line[7]
            start_long = line[8]
            start_la = line[9]
            finish_time = line[10]
            finish_long = line[11]
            finish_la = line[12]
            if (receive_datetime - morning_peak_from).total_seconds() > 0 and \
               (morning_peak_to - receive_datetime).total_seconds() > 0:
                res['morning']['receive_nodes']['data'].append({
                    'time': receive_time,
                    'coord': [float(receive_long), float(receive_la)]
                })
                res['morning']['start_nodes']['data'].append({
                    'time': start_time,
                    'coord': [float(start_long), float(start_la)]
                })
                res['morning']['finish_nodes']['data'].append({
                    'time': finish_time,
                    'coord': [float(finish_long), float(finish_la)]
                })
            elif (receive_datetime - evening_peak_from).total_seconds() > 0 and \
                 (evening_peak_to - receive_datetime).total_seconds() > 0:
                res['evening']['receive_nodes']['data'].append({
                    'time': receive_time,
                    'coord': [float(receive_long), float(receive_la)]
                })
                res['evening']['start_nodes']['data'].append({
                    'time': start_time,
                    'coord': [float(start_long), float(start_la)]
                })
                res['evening']['finish_nodes']['data'].append({
                    'time': finish_time,
                    'coord': [float(finish_long), float(finish_la)]
                })
            else:
                res['flat']['receive_nodes']['data'].append({
                    'time': receive_time,
                    'coord': [float(receive_long), float(receive_la)]
                })
                res['flat']['start_nodes']['data'].append({
                    'time': start_time,
                    'coord': [float(start_long), float(start_la)]
                })
                res['flat']['finish_nodes']['data'].append({
                    'time': finish_time,
                    'coord': [float(finish_long), float(finish_la)]
                })
    return jsonify(json.dumps(res))


@app.route('/api/time-filter-week', methods=['POST'])
def time_filter_week():
    res = {
        'realtime': {
            'receive_nodes': {
                'name': '接单时间',
                'data': []
            },
            'start_nodes': {
                'name': '行程开始时间',
                'data': []
            },
            'finish_nodes': {
                'name': '行程结束时间',
                'data': []
            }
        },
        'appointment': {
            'start_nodes': {
                'name': '行程开始时间',
                'data': []
            },
            'finish_nodes': {
                'name': '行程结束时间',
                'data': []
            }
        }
    }
    driver_id = request.form['driver_id']
    start_date = request.form['start_date']
    end_date = request.form['end_date']
    from_time = request.form['from_time']
    to_time = request.form['to_time']
    from_datetime = datetime.strptime('%s' % from_time,
                                      '%H:%M:%S')
    to_datetime = datetime.strptime('%s' % to_time,
                                    '%H:%M:%S')
    filename = BASE_URL + '/' + str(driver_id)+'.csv'
    realtime_i = 0
    appoint_i = 0
    with open(filename) as f:
        f_csv = csv.reader(f)
        headers = next(f_csv)
        for line in f_csv:
            receive_time = line[4]
            receive_datetime = datetime.strptime('%s' % receive_time.split()[1],
                                                 '%H:%M:%S')
            if (receive_datetime - from_datetime).total_seconds() > 0 and \
               (to_datetime - receive_datetime).total_seconds() > 0:
                receive_long = line[5]
                receive_la = line[6]
                start_time = line[7]
                start_long = line[8]
                start_la = line[9]
                finish_time = line[10]
                finish_long = line[11]
                finish_la = line[12]
                if not int(line[2]):  # 实时单
                    res['realtime']['receive_nodes']['data'].append(
                        {'id': realtime_i, 'time': receive_time,
                         'coord': [float(receive_long), float(receive_la)]}
                        )
                    res['realtime']['start_nodes']['data'].append(
                        {'id': realtime_i, 'time': start_time,
                         'coord': [float(start_long), float(start_la)]}
                    )
                    res['realtime']['finish_nodes']['data'].append(
                        {'id': realtime_i, 'time': finish_time,
                         'coord': [float(finish_long), float(finish_la)]}
                    )
                else:  # 预约单
                    appoint_i += 1
                    res['appointment']['start_nodes']['data'].append(
                        {'time': start_time,
                         'coord': [float(start_long), float(start_la)]}
                    )
                    res['appointment']['finish_nodes']['data'].append(
                        {'time': finish_time,
                         'coord': [float(finish_long), float(finish_la)]}
                    )
    return jsonify(json.dumps(res))

@app.route('/api/time-filter-day', methods=['POST'])
def time_filter_day():
    res = {
        'realtime': {
            'receive_nodes': {
                'name': '接单时间',
                'data': []
            },
            'start_nodes': {
                'name': '行程开始时间',
                'data': []
            },
            'finish_nodes': {
                'name': '行程结束时间',
                'data': []
            }
        },
        'appointment': {
            'start_nodes': {
                'name': '行程开始时间',
                'data': []
            },
            'finish_nodes': {
                'name': '行程结束时间',
                'data': []
            }
        }
    }
    driver_id = request.form['driver_id']
    date = request.form['date']
    from_time = request.form['from_time']
    to_time = request.form['to_time']
    from_datetime = datetime.strptime('%s %s' % (date, from_time),
                                      '%Y%m%d %H:%M:%S')
    to_datetime = datetime.strptime('%s %s' % (date, to_time),
                                    '%Y%m%d %H:%M:%S')
    filename = BASE_URL + '/' + str(driver_id)+'.csv'
    realtime_i = 0
    appoint_i = 0
    with open(filename) as f:
        f_csv = csv.reader(f)
        headers = next(f_csv)
        for line in f_csv:
            current_date = ''.join(line[4].split()[0].split('-'))
            if current_date == date:
                receive_time = line[4].split(' ')[1]
                receive_datetime = datetime.strptime('%s %s' % (date, receive_time),
                                                     '%Y%m%d %H:%M:%S')
                if (receive_datetime - from_datetime).total_seconds() > 0 and \
                   (to_datetime - receive_datetime).total_seconds() > 0:
                    receive_long = line[5]
                    receive_la = line[6]
                    start_time = line[7].split(' ')[1]
                    start_long = line[8]
                    start_la = line[9]
                    finish_time = line[10].split(' ')[1]
                    finish_long = line[11]
                    finish_la = line[12]
                    if not int(line[2]):  # 实时单
                        realtime_i += 1
                        res['realtime']['receive_nodes']['data'].append(
                            {'id': realtime_i, 'time': receive_time,
                             'coord': [float(receive_long), float(receive_la)]}
                        )
                        res['realtime']['start_nodes']['data'].append(
                            {'id': realtime_i, 'time': start_time,
                             'coord': [float(start_long), float(start_la)]}
                        )
                        res['realtime']['finish_nodes']['data'].append(
                            {'id': realtime_i, 'time': finish_time,
                             'coord': [float(finish_long), float(finish_la)]}

                            )
                    else:  # 预约单
                        appoint_i += 1
                        res['appointment']['start_nodes']['data'].append(
                            {'time': start_time,
                             'coord': [float(start_long), float(start_la)]}
                        )
                        res['appointment']['finish_nodes']['data'].append(
                            {'time': finish_time,
                             'coord': [float(finish_long), float(finish_la)]}
                        )
    return jsonify(json.dumps(res))


@app.route('/api/query-week', methods=['POST'])
def query_week():
    res = {
        'realtime': {
            'receive_nodes': {
                'name': '接单时间',
                'data': []
            },
            'start_nodes': {
                'name': '行程开始时间',
                'data': []
            },
            'finish_nodes': {
                'name': '行程结束时间',
                'data': []
            }
        },
        'appointment': {
            'start_nodes': {
                'name': '行程开始时间',
                'data': []
            },
            'finish_nodes': {
                'name': '行程结束时间',
                'data': []
            }
        }
    }

    driver_id = request.form['driver_id']
    start_date = request.form['start_date']
    end_date = request.form['end_date']

    filename = BASE_URL + '/' + str(driver_id)+'.csv'
    with open(filename) as f:
        f_csv = csv.reader(f)
        headers = next(f_csv)
        date = start_date
        realtime_i = 1
        appointment_i = 1
        realtime_count = 0
        appoint_count = 0
        total = 0
        realtime_long = 0
        realtime_mid = 0
        realtime_short = 0
        appoint_long = 0
        appoint_mid = 0
        appoint_short = 0
        freetime = 0
        servetime = 0
        chargetime = 0
        last_finish_time = []
        flag = 0
        for line in f_csv:
            total += 1
            receive_time = line[4]
            receive_long = line[5]
            receive_la = line[6]
            start_time = line[7]
            start_long = line[8]
            start_la = line[9]
            finish_time = line[10]
            finish_long = line[11]
            finish_la = line[12]
            last_finish_time.append(finish_time)
            if not int(line[2]):  # 实时单
                realtime_count += 1
                current_date = ''.join(line[4].split()[0].split('-'))
                if date != current_date:
                    date = current_date
                    realtime_i = 1
                dis = judge_distance(float(start_long), float(start_la),
                                     float(finish_long), float(finish_la))
                if dis == 0:
                    realtime_short += 1
                elif dis == 1:
                    realtime_mid += 1
                else:
                    realtime_long += 1
                invalid = '0000-00-00 00:00:00'
                if start_time != invalid and finish_time != invalid and receive_time != invalid:
                    servetime += (datetime.strptime(finish_time, '%Y-%m-%d %H:%M:%S')-datetime.strptime(receive_time, '%Y-%m-%d %H:%M:%S')).total_seconds()/60
                    chargetime += (datetime.strptime(finish_time, '%Y-%m-%d %H:%M:%S')-datetime.strptime(start_time, '%Y-%m-%d %H:%M:%S')).total_seconds()/60
                    if flag:
                        if last_finish_time[-2] != invalid:
                            last_finish = last_finish_time[-2]
                            freetime += (datetime.strptime(receive_time, '%Y-%m-%d %H:%M:%S')-datetime.strptime(last_finish, '%Y-%m-%d %H:%M:%S')).total_seconds()/60
                    flag = 1

                res['realtime']['receive_nodes']['data'].append(
                    {'id': realtime_i, 'time': receive_time,
                     'coord': [float(receive_long), float(receive_la)]}
                )
                res['realtime']['start_nodes']['data'].append(
                    {'id': realtime_i, 'time': start_time,
                     'coord': [float(start_long), float(start_la)]}
                )
                res['realtime']['finish_nodes']['data'].append(
                    {'id': realtime_i, 'time': finish_time,
                     'coord': [float(finish_long), float(finish_la)]}
                )
                realtime_i += 1
            else:  # 预约单
                appoint_count += 1
                dis = judge_distance(float(start_long), float(start_la),
                                     float(finish_long), float(finish_la))
                if dis == 0:
                    appoint_short += 1
                elif dis == 1:
                    appoint_mid += 1
                else:
                    appoint_long += 1
                res['appointment']['start_nodes']['data'].append(
                    {'time': start_time,
                     'coord': [float(start_long), float(start_la)]}
                )
                res['appointment']['finish_nodes']['data'].append(
                    {'time': finish_time,
                     'coord': [float(finish_long), float(finish_la)]}
                )
        res['total'] = total
        res['realtime_long'] = realtime_long
        res['realtime_mid'] = realtime_mid
        res['realtime_short'] = realtime_short
        res['appoint_long'] = appoint_long
        res['appoint_mid'] = appoint_mid
        res['appoint_short'] = appoint_short
        res['freetime'] = round(freetime, 2)
        res['chargetime'] = round(chargetime, 2)
        res['servetime'] = round(servetime, 2)
        res['realtime_count'] = realtime_count
        res['appoint_count'] = appoint_count
        data_list = [total, realtime_long, realtime_mid, realtime_short,
                     appoint_long, appoint_mid, appoint_short,
                     round(chargetime, 2), round(servetime, 2)]
    return jsonify(json.dumps(res))


@app.route('/api/query-day', methods=['POST'])
def query_day():
    res = {
        'realtime': {
            'receive_nodes': {
                'name': '接单时间',
                'data': []
            },
            'start_nodes': {
                'name': '行程开始时间',
                'data': []
            },
            'finish_nodes': {
                'name': '行程结束时间',
                'data': []
            }
        },
        'appointment': {
            'start_nodes': {
                'name': '行程开始时间',
                'data': []
            },
            'finish_nodes': {
                'name': '行程结束时间',
                'data': []
            }
        }
    }
    driver_id = request.form['driver_id']
    date = request.form['date']
    filename = BASE_URL + '/' + str(driver_id)+'.csv'
    with open(filename) as f:
        f_csv = csv.reader(f)
        headers = next(f_csv)
        index = 1
        total = 0
        long = 0
        mid = 0
        short = 0
        freetime = 0
        servetime = 0
        chargetime = 0
        last_finish_time = []
        flag = 0
        for line in f_csv:
            current_date = ''.join(line[4].split()[0].split('-'))
            if current_date == date:
                total += 1
                receive_time = line[4].split(' ')[1]
                receive_long = line[5]
                receive_la = line[6]
                start_time = line[7].split(' ')[1]
                start_long = line[8]
                start_la = line[9]
                finish_time = line[10].split(' ')[1]
                finish_long = line[11]
                finish_la = line[12]
                realdes = int(line[13])
                realdes_long = line[14]
                realdes_la = line[15]

                last_finish_time.append(finish_time)

                dis = judge_distance(float(start_long), float(start_la),
                                     float(finish_long), float(finish_la))
                if dis == 0:
                    short += 1
                elif dis == 1:
                    mid += 1
                else:
                    long += 1

                if not int(line[2]):  # 实时单
                    if start_time != '00:00:00' and finish_time != '00:00:00' and receive_time != '00:00:00' and last_finish_time != '00:00:00':
                        servetime += (datetime.strptime(finish_time, '%H:%M:%S')-datetime.strptime(receive_time, '%H:%M:%S')).total_seconds()/60
                        chargetime += (datetime.strptime(finish_time, '%H:%M:%S')-datetime.strptime(start_time, '%H:%M:%S')).total_seconds()/60
                        if flag:
                            last_finish = last_finish_time[-2]
                            freetime += (datetime.strptime(receive_time, '%H:%M:%S')-datetime.strptime(last_finish, '%H:%M:%S')).total_seconds()/60
                        flag = 1
                    res['realtime']['receive_nodes']['data'].append({
                        'id': index,
                        'time': receive_time,
                        'coord': [float(receive_long), float(receive_la)],
                        'realdes': True if realdes else False
                    })
                    res['realtime']['start_nodes']['data'].append({
                        'id': index,
                        'time': start_time,
                        'coord': [float(start_long), float(start_la)],
                        'realdes': True if realdes else False
                    })
                    res['realtime']['finish_nodes']['data'].append({
                        'id': index,
                        'time': finish_time,
                        'coord': [float(finish_long), float(finish_la)],
                        'realdes': False
                    })

                    index += 1
                else:  # 预约单
                    res['appointment']['start_nodes']['data'].append(
                        {'time': start_time,
                         'coord': [float(start_long), float(start_la)]}
                    )
                    res['appointment']['finish_nodes']['data'].append(
                        {'time': finish_time,
                         'coord': [float(finish_long), float(finish_la)]}
                    )
        res['total'] = total
        res['long'] = long
        res['mid'] = mid
        res['short'] = short
        res['servetime'] = round(servetime, 2)
        res['chargetime'] = round(chargetime, 2)
        res['freetime'] = round(freetime, 2)

    return jsonify(json.dumps(res))


@app.route('/api/map', methods=['POST'])
def get_map():
    city = request.form['city']
    json_url = os.path.join(BASE_URL, 'static/data', '%s.json' % city)
    with open(json_url) as json_file:
        data = json.load(json_file)
    return jsonify(data)