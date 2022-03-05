from flask import Flask, render_template,request
from flask_sqlalchemy import SQLAlchemy
import string
from sqlalchemy import create_engine
from sqlalchemy.engine import URL
import random
import json
import psycopg2
import requests
import json

url = 'http://10.192.9.11:9091/api/v1/query'
headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36'
}

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:password@10.192.9.11'
db = SQLAlchemy(app)

def str_to_array(str):
    str = str.lstrip('<')
    str = str.rstrip('>')
    str = str.split(',')
    return str

class Epoch(db.Model):
    __tablename__='t_epoch_summaries'
    epoch = db.Column('f_epoch', db.Integer, primary_key = True)
    active_balance = db.Column('f_active_balance',db.Integer)
    attesting_balance = db.Column('f_attesting_balance',db.Integer)
    target_correct_balance = db.Column('f_target_correct_balance', db.Integer)
    head_correct_balance = db.Column('f_head_correct_balance', db.Integer)

class Block(db.Model):
    __tablename__ = 't_blocks'
    slot = db.Column('f_slot',db.Integer,primary_key = True)
    epoch = db.Column('epoch',db.Integer)
    proposer = db.Column('f_proposer', db.Integer)
    # status = db.Column('status',db.String)
    # root = db.Column('f_root',db.Unicode)
   # ats_included = db.relationship('Attestation', backref = 'inclusion')
    #ats_targeted = db.relationship('Attestation', backref = 'target')

class Attestation(db.Model):
    __tablename__ = 't_attestations'
    inclusion_slot = db.Column('f_inclusion_slot', db.Integer, primary_key = True)
    inclusion_index = db.Column('f_inclusion_index', db.Integer,primary_key = True)
    slot = db.Column('f_slot', db.Integer)
    committee_index = db.Column('f_committee_index', db.Integer)
    aggregation_bits = db.Column('f_aggregation_bits', db.String)
    aggregation_indices = db.Column('f_aggregation_indices', db.String)
    beacon_block_root = db.Column('f_beacon_block_root', db.Integer)
    source_epoch = db.Column('f_source_epoch', db.Integer)
    target_epoch = db.Column('f_target_epoch', db.Integer)

class Validator(db.Model):
    __tablename__ = 't_validator_epoch_summaries'
    val = db.Column('f_validator_index', db.Integer, primary_key = True)
    epoch = db.Column('f_epoch', db.Integer)
    

@app.route('/overview')
def overview():
    data = Epoch.query.order_by(-Epoch.epoch).limit(180)
    epochs = []
    for d in data[::-1]:
        s = {}
        s['epoch'] = d.epoch
        s['active_balance'] = d.active_balance
        s['attesting_balance'] = d.attesting_balance
        s['target_correct_balance'] = d.target_correct_balance
        s['head_correct_balance'] = d.head_correct_balance
        epochs.append(s)
    param = {'query':'beacon_current_justified_epoch'}
    justified = eval(requests.get(url = url, params = param, headers = headers).json()['data']['result'][0]['value'][1])
    param = {'query':'beacon_finalized_epoch'}
    finalized = eval(requests.get(url = url, params = param, headers = headers).json()['data']['result'][0]['value'][1])
    return render_template('overview.html',epoch = epochs,justify = justified, finalize = finalized)

@app.route('/slot')
def slot():
    ats = Attestation.query.filter_by(inclusion_slot=174655)
    i = 0
    attest = []
    temp = ats.filter_by(inclusion_index=i).first()
    while temp:
        s = {}
        s['inclusion_slot'] = temp.inclusion_slot
        s['inclusion_index'] = temp.inclusion_index
        s['committee_index'] = temp.committee_index
        s['slot'] = temp.slot
        bits = ''
        for m in temp.aggregation_bits:
            bits = bits + bin(m[0])[2:]
        s['aggregation_bits'] = bits
        s['aggregation_indices'] = temp.aggregation_indices
        root = ''
        for m in temp.beacon_block_root:
            root = root + bin(m[0])[2:]
        s['beacon_block_root'] = root
        
        attest.append(s)
        i = i + 1
        temp = ats.filter_by(inclusion_index=i).first()
    return render_template('exp.html',attestation=attest)

@app.route('/exp')
def exp():
    data = Epoch.query.order_by(-Epoch.epoch).limit(180)
    epochs = []
    for d in data[::-1]:
        s = {}
        s['epoch'] = d.epoch
        s['active_balance'] = d.active_balance
        s['attesting_balance'] = d.attesting_balance
        s['target_correct_balance'] = d.target_correct_balance
        epochs.append(s)
    return render_template('exp.html',epoch = epochs)


@app.route('/index')
def index():
    return "Hello World"

if __name__ == '__main__':
    app.run(debug=True)
