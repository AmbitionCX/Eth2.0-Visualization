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
import copy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:password@10.192.9.11'
db = SQLAlchemy(app)
CORS(app)

class c_overview(db.Model):
    __tablename__ = 'c_overview'
    days = db.Column('f_days',db.Integer,primary_key = True)
    blocks = db.Column('f_blocks',db.Integer)
    deposits = db.Column('f_deposits',db.Integer)

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

class Proposer(db.Model):
    __tablename__ = 't_proposer_duties'
    slot = db.Column('f_slot', db.Integer, primary_key = True)
    proposer = db.Column('f_validator_index', db.Integer)

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
    data= c_overview.query.order_by(c_overview.days).limit(230).all()
    dayData = []
    for i in data:
        s = {}
        add_day=datetime.timedelta(i.days)
        first_day = datetime.datetime(2020,12,1)
        s['day'] = datetime.datetime.strftime(first_day+add_day,'%Y-%m-%d')
        s['canonical']= sum(i.blocks)
        s['deposits']= i.deposits
        dayData.append(s)
    return json.dumps(dayData)


@app.route('/EpochView/<int:index>')
def EpochView(index):
    data = Epoch.query.filter(Epoch.epoch.in_(range(index,index+225))).order_by(-Epoch.epoch).all()
    epochs = []
    for d in data[::-1]:
        s = {}
        s['epoch'] = d.epoch
        s['active_balance'] = d.active_balance
        s['attesting_balance'] = d.attesting_balance
        s['target_correct_balance'] = d.target_correct_balance
        s['head_correct_balance'] = d.head_correct_balance
        epochs.append(s)
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
    val_error.sort(key=lambda x:x['validator_index'])

    #print(len(val_error))

    casper = []
    for s in range(index, index - 8 ,-1):
        #print(s)
        cas = {}
        cas['epoch'] = s
        cas['validator'] =copy.deepcopy(val_error)
        temp = Vote.query.filter(Vote.epoch == s).all()
        aggregate_y = []
        aggregate_n = []
        aggregate_not_vote=[]
        for t in temp:
            aggregate_y += t.casper_y
            aggregate_n += t.casper_n
            aggregate_not_vote += t.not_vote

        for i in range(0, len(val_error)):
            v = cas['validator'][i]['validator_index']

            if v in aggregate_n:
                cas['validator'][i]['vote'] = 0

            else:
                if v in aggregate_not_vote:
                    cas['validator'][i]['vote'] = -1

                else:
                    if v in aggregate_y:
                        cas['validator'][i]['vote']=1
                    else:
                        cas['validator'][i]['vote'] = -2
        casper.append(cas)
    
    proposer = []
    for i in range(index, index-8, -1):
        p = []
        for s in range(i*32, (i+1)*32):
            data = Proposer.query.filter_by(slot=s).first()
            p.append(data.proposer)
        proposer.append(p)
    return json.dumps([casper] + [proposer])


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
            t = {}
            t['source'] = l['source']
            t['target'] = l['target']
            t['value'] = counter
            links.append(t)

        slots.append(temp)
    return json.dumps([slots] + [links])



@app.route('/',methods=['GET'])
def index():
    return "Hello Vue"


if __name__ == '__main__':
    app.run(debug=True)
