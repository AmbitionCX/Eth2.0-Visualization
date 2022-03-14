from flask import Flask, render_template,request
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import string
from sqlalchemy import ForeignKey, create_engine
from sqlalchemy.engine import URL
import psycopg2
import requests
import string
import math
import json
import simplejson
import datetime
import numpy as np

url = 'http://10.192.9.11:9091/api/v1/query'
headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36'
}

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:password@10.192.9.11'
db = SQLAlchemy(app)
CORS(app)

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
    deposit = db.Column('f_eth1_deposit_count',db.Integer,primary_key = True)

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
    target_correct = db.Column('f_target_correct', db.String)
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
        return Committee.query.filter_by(slot = self.slot, index = self.committee_index).first()

class Validator(db.Model):
    __tablename__ = 't_validator_epoch_summaries'
    val = db.Column('f_validator_index', db.Integer, primary_key = True)
    epoch = db.Column('f_epoch', db.Integer)

class Vote(db.Model):
    __tablename__ = 'c_main_table'
    slot = db.Column('f_slot', db.Integer, primary_key = True)
    epoch = db.Column('f_epoch', db.Integer)
    casper_y = db.Column('f_casper_y', db.String)
    casper_y_balance = db.Column('f_casper_y_balance', db.BigInteger)
    casper_n = db.Column('f_casper_n', db.String)
    casper_n_balance = db.Column('f_casper_n_balance', db.BigInteger)
    not_vote = db.Column('f_not_vote', db.String)
    not_vote_balance = db.Column('f_not_vote_balance', db.BigInteger)
    ghost_selection = db.Column('f_ghost_selection', db.String)


@app.route('/Overview')
def Overview():
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

    data2= Block.query.order_by(Block.slot).limit(32*225*100).all()
    print("data_loaded")
    canonical = []
    deposit = []
    dayData1 = []

    counter = 0
    prev = 0
    for i in data2:
        if math.floor((i.slot)/7200) != prev:
            canonical.append(counter)
            counter = 0
            prev = math.floor((i.slot)/7200)
        counter += 1
    canonical.append(counter)
    print("1")
    
    deposit = []
    for i in range(math.ceil((data2[-1].slot)/32)):
        deposit.append([])
    
    for i in data2:
        
        deposit[math.floor((i.slot)/32)].append(i.deposit)
    deposit1 = []
    for i in range(len(deposit)):
        deposit1.append([])
        deposit1[i] = sum(deposit[i])
    print('2')

    deposits = []
   
    for j in range(math.ceil(len(deposit1)/225)):
        deposits.append([])
        for i in deposit1[j*225:(j+1)*225]:
            deposits[j].append(i)

    print('3')
    for i in range(len(canonical)):
        s = {}
        add_day=datetime.timedelta(i)
        first_day = datetime.datetime(2020,12,1)
        s['day'] = datetime.datetime.strftime(first_day+add_day,'%Y-%m-%d')
        s['canonical'] =8160-canonical[i]
        s['deposits'] = deposits[i]
        dayData1.append(s)
    print('4')
    return json.dumps(dayData1)


@app.route('/EpochView')
def EpochView():
    data = Epoch.query.order_by(Epoch.epoch).limit(225)
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
    return json.dumps(epochs)


@app.route('/validator/<int:index>', methods=['GET'])
def validator(index):
    ats = Vote.query.filter(Vote.epoch == index).order_by(Vote.slot).all()
    val = []
    for a in ats:
        val = val + a.casper_n + a.not_vote
    
    val_error = []
    for v in val:
        tmp = {}
        tmp['validator_index'] = v
        tmp['vote'] = 1
        val_error.append(tmp)
    print(len(val_error))

    casper = []
    for s in range(index, index - 8 ,-1):
        print(s)
        cas = {}
        cas['epoch'] = s
        cas['validator'] = val_error
        temp = Vote.query.filter(Vote.epoch == s).all()
        aggregate_y = []
        aggregate_n = []
        aggregate_not_vote=[]
        for t in temp:
            aggregate_y += t.casper_y
            aggregate_n += t.casper_n
            aggregate_not_vote += t.not_vote
        print(1)
        for i in range(0, len(val_error)):
            v = cas['validator'][i]['validator_index']
            if v in aggregate_n:
                cas['validator'][i]['vote'] = 0
            else:
                if v in aggregate_not_vote:
                    cas['validator'][i]['vote'] = -1
                else:
                    if v in aggregate_y:
                        continue
                    else:
                        cas['validator'][i]['vote'] = -1
        casper.append(cas)
    return json.dumps(casper)


@app.route('/Vali/<int:index>',methods=['GET'])
def Vali(index):
    ats = Attestation.query.filter(Attestation.inclusion_slot.in_(range(index*32,(index+1)*32))).order_by(Attestation.inclusion_slot,Attestation.slot,Attestation.committee_index).all()
    
    # val为选定epoch中，投否定票或missed（没有投票）的参与者集合
    # print(list(set(ats[-16].committee()) - set(ats[-16].aggregation_indices)))
    com = ats[0].committee()
    val = com.committee
    for a in ats:
        if a.committee_index != com.index:
            com = a.committee()
            val = val + com.committee
        # print(list(set(a.committee()) - set(a.aggregation_indices)))
        j = 0
        val_correct = []
        while j < len(a.aggregation_indices):
            if a.bits()[j] == '1':
                val_correct.append(a.aggregation_indices[j])
            j += 1
        val = list(set(val)-set(val_correct))
    val = list(set(val))
    print(len(val))
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
        json.dump(records, open('epoch100.json', "w"))
    return render_template('exp.html', data = json.dumps(records), val_error = json.dumps(val))


@app.route('/slot/<int:index>',methods=['GET'])
def slot(index):
    slots = []
    links_temp = []
    for s in range(index*32,(index+1)*32):
        ats = Attestation.query.filter_by(inclusion_slot=s).order_by(Attestation.slot, Attestation.committee_index).all()
        print(len(ats))
        temp = {}
        temp['at_number'] = 0
        if len(ats) > 0:
            committee_prev = ats[0].committee_index
            ats_no = set()
            for a in ats:
                link = {}
                if a.slot < index*32 :
                    link['source'] = -1
                else:
                    link['source'] = a.slot%32
                link['target'] = a.inclusion_slot%32
                if committee_prev != a.committee_index:
                    temp['at_number'] += len(ats_no)
                    ats_no = set()
                    committee_prev = a.committee_index
                ats_no = ats_no|set(a.aggregation_indices)
                links_temp.append(link)
            temp['at_number'] += len(ats_no)

        votes = Vote.query.filter_by(slot = s).first()
        print(votes)
        temp['casper_balance'] = votes.casper_y_balance
        blocks = []
        if votes:
            blocks = votes.ghost_selection
        if len(blocks) > 0:
            blocks.sort(key=lambda x:(x['root']['data']))
            temp['block_header'] = 0
            temp['ex_blocks'] = []
            block_prev = blocks[0]['root']['data']
            balance = 0
            for b in blocks:
                if block_prev != b['root']['data']:
                    temp['ex_blocks'].append(balance)
                    block_prev = b['root']['data']
                    balance = 0
                balance += b['balance']
            temp['ex_blocks'].append(balance)
            temp['ex_blocks'].sort()
            if temp['at_number'] != 0:
                temp['block_header'] = temp['ex_blocks'].pop()

        if len(links_temp) > 0:
            l = {
                'source': links_temp[0]['source'],
                'target': links_temp[0]['target']
            }
            counter = 0
            links = []
            for li in links_temp:
                if li != l:
                    t = {}
                    t['source'] = l['source']
                    t['target'] = l['target']
                    t['value'] = counter
                    links.append(t)
                    counter = 1
                    l = li
                else:
                    counter += 1

        slots.append(temp)
    return render_template("slot.html", slots = json.dumps(slots), links = json.dumps(links))


@app.route('/block')
def block():
    s = 0
    temp = {} # 删除
    votes = Vote.query.filter_by(slot = s).first()
    # 以下tab
    if votes:
        blocks = votes.ghost_selection
    if len(blocks) > 0:
        blocks.sort(key=lambda x:(-x['canonical'],x['root']['data']))
        temp['block_header'] = 0
        temp['ex_blocks'] = []
        block_prev = blocks[0]['root']['data']
        balance = 0
        for b in blocks:
            if b['canonical'] == True:
                temp['block_header'] += b['balance']
            else:
                if block_prev != b['root']['data']:
                    if balance != 0:
                        temp['ex_blocks'].append(balance)
                    block_prev = b['root']['data']
                    balance = 0
                balance += b['balance']
    return ""
    
@app.route('/',methods=['GET'])
def index():
    return "Hello Vue"

@app.route('/get_filtered_list', methods=['GET','POST'])
def get_filtered_list():
    post_data = request.data.decode()
    index = 100
    if post_data != "":
        index = simplejson.loads(post_data)['epoch']
    ats = Attestation.query.filter_by(inclusion_slot=index*32).all()
    slots = []
    for a in ats:
        temp={}
        temp['inclusion_slot'] = a.inclusion_slot
        temp['slot'] = a.slot
        slots.append(temp)
    return json.dumps(slots)


if __name__ == '__main__':
    app.run(debug=True)
