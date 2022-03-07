from flask import Flask, render_template,request
from flask_sqlalchemy import SQLAlchemy
import string
from sqlalchemy import ForeignKey, create_engine
from sqlalchemy.engine import URL
import psycopg2
import requests
import string
import random
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
    slot = db.Column('f_slot',db.Integer, primary_key = True)
    epoch = db.Column('epoch',db.Integer)
    proposer = db.Column('f_proposer', db.Integer)
    # status = db.Column('status',db.String)
    # root = db.Column('f_root',db.Unicode)
    # ats_included = db.relationship('Attestation', backref = 'inclusion')
    # ats_targeted = db.relationship('Attestation', backref = 'target')

class Committee(db.Model):
    __tablename__ = 't_beacon_committees'
    slot = db.Column('f_slot', db.Integer, primary_key = True)
    index = db.Column('f_index', db.Integer, primary_key = True)
    committee = db.Column('f_committee', db.String)

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
    def bits(self):
        bits = ''
        for m in self.aggregation_bits:
            bits = bits + bin(m[0])[2:].zfill(8)
        return bits
    def blocks(self):
        root = ''
        for m in self.beacon_block_root:
            root = root + bin(m[0])[2:].zfill(8)
        return root
    def committee(self):
        return Committee.query.filter_by(slot = self.slot, index = self.committee_index).first().committee


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
    return render_template('overview.html',epoch = json.dumps(epochs),justify=json.dumps(justified))

@app.route('/validator/<int:index>',methods=['GET'])
def validator(index):
    ats = Attestation.query.filter(Attestation.inclusion_slot.in_(range(index*32,(index+1)*32))).order_by(Attestation.inclusion_slot,Attestation.inclusion_index).all()
    
    # val为选定epoch中，投否定票或missed（没有投票）的参与者集合
    val = []
    print(list(set(ats[-16].committee()) - set(ats[-16].aggregation_indices)))
    for a in ats:
        val = val + list(set(a.committee()) - set(a.aggregation_indices))
        # print(list(set(a.committee()) - set(a.aggregation_indices)))
        j = 0
        while j < len(a.aggregation_indices):
            if a.bits()[j] == '0':
                val.append(a.aggregation_indices[j])
            j += 1
    val = list(set(val))

    records = []
    for i in range(index-1, index-3,-1):
        record = {}
        attest = Attestation.query.filter(Attestation.inclusion_slot.in_(range(i*32,(i+1)*32))).all()
        record['epoch'] = i
        validators = []
        for v in val:
            vali = {}
            vali['validator_index'] = v
            vali['vote'] = -1
            for a in attest:
                if v in a.aggregation_indices:
                    vali['vote'] = eval(a.bits()[a.aggregation_indices.index(v)])
                else:
                    continue
            validators.append(vali)
        record['validator'] = validators
        print(record)
        records.append(record)
    return render_template('exp.html', data = json.dumps(records), val_error = json.dumps(val))


@app.route('/slot/<int:index>',methods=['GET'])
def slot(index):
    slots = []
    for s in range(index*32,(index+1)*32):
        ats = Attestation.query.filter_by(inclusion_slot=s).all()
        temp = {}
        temp['at_number'] = 0
        temp['block'] = ats[0].block_root
        for t in ats:
            bits = ''
            for m in temp.aggregation_bits:
                bits = bits + bin(m[0])[2:].zfill(8)
            root = ''
            for m in t.beacon_block_root:
                root = root + bin(m[0])[2:].zfill(8)
            temp['at_number'] += len(t.aggregation_indices)

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
            bits = bits + bin(m[0])[2:].zfill(8)
        s['aggregation_bits'] = bits
        s['aggregation_indices'] = temp.aggregation_indices
        root = ''
        for m in temp.beacon_block_root:
            root = root + bin(m[0])[2:].zfill(8)
        s['beacon_block_root'] = root
        
        attest.append(s)
        i = i + 1
        temp = ats.filter_by(inclusion_index=i).first()
    return render_template('slot.html', attestation = json.dumps(attest))


@app.route('/index')
def index():
    return "Hello World"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=12346, debug=True)
