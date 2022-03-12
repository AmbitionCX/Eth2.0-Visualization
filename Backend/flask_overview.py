from flask import Flask, render_template,request
from flask_sqlalchemy import SQLAlchemy
import string
from sqlalchemy import create_engine, true
from sqlalchemy.engine import URL
import random
import json
import psycopg2
import requests
import json
import math
import datetime

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

'''class c_epoch_status(db.Model):
    __tablename__='c_epoch_status'
    epoch = db.Column('f_epoch', db.Integer, primary_key = True)
    active_balance = db.Column('f_active_balance',db.Integer)
    attesting_balance = db.Column('f_attesting_balance',db.Integer)
    target_correct_balance = db.Column('f_target_correct_balance', db.Integer)
    head_correct_balance = db.Column('f_head_correct_balance', db.Integer)'''

class Block(db.Model):
    __tablename__ = 't_blocks'
    slot = db.Column('f_slot',db.Integer,primary_key = True)
    deposit = db.Column('f_eth1_deposit_count',db.Integer)
    
    # epoch = db.Column('epoch',db.Integer)
    # proposer = db.Column('f_proposer', db.Integer)
    # canonical = db.Column('f_canonical', db.BOOLEAN)
    # status = db.Column('status',db.String)
    # root = db.Column('f_root',db.Unicode)
    # ats_included = db.relationship('Attestation', backref = 'inclusion')
    #ats_targeted = db.relationship('Attestation', backref = 'target')

class c_block_status(db.Model):
    __tablename__ = 'c_block_status'
    slot = db.Column('f_slot',db.Integer,primary_key = True)
    canonical = db.Column('f_canonical', db.BOOLEAN)

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
    
@app.route('/allOverview')
def allOverview():
    #新表
    # data1= c_block_status.query.order_by(-c_block_status.slot).limit(60000*32)
    # data2 = data1[::-1] 
    # canonical = []
  
        
    # for i in range(math.ceil(len(data2)/8160)):
    #     count = 0
    #     for d in data2[8160*i:8160*(i+1):1]:
    #         if not d.canonical == True:
    #             count+=1
            
    #     canonical.append(count) 

    data2= Block.query.order_by(Block.slot).limit(32*255*100)
    canonical = []
    deposit = []
    dayData1 = []
    for i in range(math.ceil((data2[-1].slot)/8160)):

        
        canonical.append([])
    for i in data2:
        canonical[math.floor((i.slot)/8160)].append(i.slot)


    # for i in data2:
    #     canonical.append(i.slot)
    deposit = []
    for i in range(math.ceil((data2[-1].slot)/32)):
        deposit.append([])
    
    for i in data2:
        
        deposit[math.floor((i.slot)/32)].append(i.deposit)
    deposit1 = []
    for i in range(len(deposit)):
        deposit1.append([])
        deposit1[i] = sum(deposit[i])
        
    deposits = []
   
    for j in range(math.ceil(len(deposit1)/255)):
        deposits.append([])
        for i in deposit1[j*255:(j+1)*255]:
            deposits[j].append(i)


    for i in range(len(canonical)):
        s = {}
        add_day=datetime.timedelta(i)
        first_day = datetime.datetime(2020,12,1)
        s['day'] = datetime.datetime.strftime(first_day+add_day,'%Y-%m-%d')
        s['canonical'] =8160-len(canonical[i])
        s['deposits'] = deposits[i]
        dayData1.append(s)





    



    # data = Epoch.query.order_by(Epoch.epoch).limit(510)
    # epochs = []
    # for d in data:
    #     s = {}
    #     s['epoch'] = d.epoch
    #     s['active_balance'] = d.active_balance/1000000000
    #     s['attesting_balance'] = d.attesting_balance/1000000000
    #     s['target_correct_balance'] = d.target_correct_balance/1000000000
    #     s['head_correct_balance'] = d.head_correct_balance/1000000000 
    #     epochs.append(s)
    # dayData = []
    # for j in range(math.ceil(len(epochs)/255)):
    #     s1={}
        
    #     s1['active_balance']=0
    #     s1['active_balance'] =0
    #     s1['attesting_balance'] =0
    #     s1['target_correct_balance'] =0
    #     s1['head_correct_balance']=0
    #     s1['details'] = []
    #     s1['canonical'] = canonical[j]
        
    #     for i in epochs[j*255:(j+1)*255]:


    #         add_day=datetime.timedelta(j)
    #         first_day = datetime.datetime(2020,12,1)
    #         s1['day'] = datetime.datetime.strftime(first_day+add_day,'%a, %d %b %Y %H:%M:%S %z')

    #         s1['active_balance'] += i['active_balance']
    #         s1['attesting_balance'] += i['attesting_balance']
    #         s1['target_correct_balance'] += i['target_correct_balance']
    #         s1['head_correct_balance'] += i['head_correct_balance']
    #         s1['details'].append(i)
      
    #     dayData.append(s1)

    return render_template('allOverview.html',dayData = json.dumps(dayData1))


@app.route('/overview') #2
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

@app.route('/slot') #4
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
    data1= c_block_status.query.order_by(-c_block_status.slot).limit(70000)
    data = data1[::-1] 
    canonical = []
  
        
    for i in range(math.ceil(len(data)/8160)):
        count = 0
        for d in data[8160*i:8160*(i+1)]:
            if not d.canonical == true:
                count+=1
            
        canonical.append(count) 



    return render_template('exp.html',canonical = json.dumps(canonical))


@app.route('/index')
def index():
    return "Hello World"

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=12346, debug=True)
