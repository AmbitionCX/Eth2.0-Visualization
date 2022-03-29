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
import random
import pandas as pd
import numpy as np
import csv

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:ChenXuan46@10.192.9.11'
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
    head_correct = db.Column('f_head_correct', db.String)
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

class Vote1(db.Model):
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

class Vote2(db.Model):
    __tablename__ = 'c_main_table_2'
    slot = db.Column('f_slot', db.Integer, primary_key = True)
    epoch = db.Column('f_epoch', db.Integer)
    casper_y = db.Column('f_casper_y', db.String)
    casper_y_balance = db.Column('f_casper_y_balance', db.BigInteger)
    casper_n = db.Column('f_casper_n', db.String)
    casper_n_balance = db.Column('f_casper_n_balance', db.BigInteger)
    not_vote = db.Column('f_not_vote', db.String)
    not_vote_balance = db.Column('f_not_vote_balance', db.BigInteger)
    ghost_selection = db.Column('f_ghost_selection', db.String)

class Vote3(db.Model):
    __tablename__ = 'c_main_table_3'
    slot = db.Column('f_slot', db.Integer, primary_key = True)
    epoch = db.Column('f_epoch', db.Integer)
    casper_y = db.Column('f_casper_y', db.String)
    casper_y_balance = db.Column('f_casper_y_balance', db.BigInteger)
    casper_n = db.Column('f_casper_n', db.String)
    casper_n_balance = db.Column('f_casper_n_balance', db.BigInteger)
    not_vote = db.Column('f_not_vote', db.String)
    not_vote_balance = db.Column('f_not_vote_balance', db.BigInteger)
    ghost_selection = db.Column('f_ghost_selection', db.String)

class Vote4(db.Model):
    __tablename__ = 'c_main_table_4'
    slot = db.Column('f_slot', db.Integer, primary_key = True)
    epoch = db.Column('f_epoch', db.Integer)
    casper_y = db.Column('f_casper_y', db.String)
    casper_y_balance = db.Column('f_casper_y_balance', db.BigInteger)
    casper_n = db.Column('f_casper_n', db.String)
    casper_n_balance = db.Column('f_casper_n_balance', db.BigInteger)
    not_vote = db.Column('f_not_vote', db.String)
    not_vote_balance = db.Column('f_not_vote_balance', db.BigInteger)
    ghost_selection = db.Column('f_ghost_selection', db.String)

def Attestation_a():
    with open(r"E:\Eth-Vis\Eth2.0-Vis\Backend\ats.csv") as f:
        row = csv.reader(f,delimiter = ',')
        next(row)
        Ats = []
        for r in row:
            s = {}
            s['inclusion_slot'] = eval(r[0])
            s['inclusion_index'] = eval(r[2])
            s['slot'] = eval(r[3])
            s['committee_index'] = eval(r[4])
            s['aggregation_bits'] = r[5]
            s['aggregation_indices'] = list(eval(r[6]))
            s['beacon_block_root'] = r[7]
            s['source_epoch'] = eval(r[8])
            s['target_epoch'] = eval(r[10])
            if r[13] == 't':
                s['target_correct'] = True
            else:
                s['target_correct'] = False
            if r[14] == 't':
                s['head_correct'] = True
            else:
                s['head_correct'] = False
            Ats.append(s)
    Ats.sort(key = lambda x:(x['inclusion_slot'], x['slot'], x['committee_index']))
    return Ats


def Vote_a():
    with open(r"E:\Eth-Vis\Eth2.0-Vis\Backend\mtb.csv") as f:
        row = csv.reader(f,delimiter = ',')
        next(row)
        Votes = []
        for r in row:
            s = {}
            s['slot'] = eval(r[1])
            s['epoch'] = eval(r[0])
            s['casper_y'] = list(eval(r[2]))
            s['casper_y_balance'] = eval(r[3])
            s['casper_n'] = list(eval(r[4]))
            s['casper_n_balance'] = eval(r[5])
            s['not_vote'] = list(eval(r[6]))
            s['not_vote_balance'] = eval(r[7])
            s['ghost_selection'] = eval((r[8].replace('true','True')).replace('false','False'))
            
            Votes.append(s)
    Votes.sort(key = lambda x:(x['slot']))
    return Votes

def filter(votes0, s):
    for i in range(len(votes0)):
        if votes0[i]['epoch'] >= s:
            break
    votes1 = votes0[i:]
    for k in range(len(votes1)):
        if votes1[k]['epoch'] >= s + 1:
            break

    if k == len(votes1) - 1:
        k += 1
    votes = votes1[:k]

    return votes


@app.route('/SlotView_Attack/<int:index>')
def SlotView_Attack(index):
    temp0 = {}
    temp0['at_number'] = 0
    votes0 = Vote_a()
    slots = [temp0]*32
    links_temp = []
    links = []
    delays = []
    delay_temp = []
    ats = Attestation_a()
    temp = {}
    temp['at_number'] = 0
    ats_no = set()

    for i in range(len(ats)):
        if ats[i]['inclusion_slot'] >= index*32:
            break

    slt = ats[i]['inclusion_slot']
    committee_prev = ats[i]['committee_index']
    for a in ats[i:]:
        if committee_prev != a['committee_index']:
            temp['at_number'] += len(ats_no)
            ats_no = set()
            committee_prev = a['committee_index']
        if a['inclusion_slot'] != slt:
            # slots.append(temp)
            slots[slt%32] = temp
            slt = a['inclusion_slot']
            temp = {}
            temp['at_number'] = 0
        if a['inclusion_slot'] >= (index+1)*32:
            break

        ats_no = ats_no|set(a['aggregation_indices'])
        
        link = {}
        if a['slot'] < index * 32:
            link['source'] = -1
        else:
            link['source'] = a['slot']%32
        link['target'] = a['inclusion_slot']%32
        link['correct'] = a['target_correct'] and a['head_correct']
        links_temp.append(link)

        delay_temp.append(a['target_epoch'] - a['source_epoch'])

    temp['at_number'] += len(ats_no)
    # slots.append(temp)
    slots[slt%32] = temp

    for i in range(len(votes0)):
        if votes0[i]['slot'] >= index*32:
            break
    votes1 = votes0[i:]
    for k in range(len(votes1)):
        if votes1[k]['slot'] >= (index + 1)*32:
            break
    if k == len(votes1) - 1:
        k += 1
    votes = votes1[:k]

    j = 0
    for v in votes:
        slots[j]['casper_balance'] = 0
        slots[j]['block_header'] = 0
        slots[j]['ex_blocks'] = []
        blocks = []
        if v['slot'] != j + index*32:
            j += 1
            continue

    
        slots[j]['casper_balance'] = v['casper_y_balance']
        blocks = v['ghost_selection']
        if len(blocks) > 0:
            blocks.sort(key=lambda x:(x['root']['data']))
            block_prev = blocks[0]['root']['data']
            balance = 0
            for b in blocks:
                if block_prev != b['root']['data']:
                    slots[j]['ex_blocks'].append(balance)
                    block_prev = b['root']['data']
                    balance = 0
                balance += b['balance']
            slots[j]['ex_blocks'].append(balance)
            slots[j]['ex_blocks'].sort()
            if slots[j]['at_number'] != 0:
                slots[j]['block_header'] = slots[j]['ex_blocks'].pop()
        j += 1

    if len(links_temp) > 0:
        l = {
            'source': links_temp[0]['source'],
            'target': links_temp[0]['target'],
            'correct': links_temp[0]['correct']
        }
    
        counter = 0
        links = []
        for li in links_temp:
            # print(li['target'])
            if li != l:
                t = {}
                t['source'] = l['source']
                t['target'] = l['target']
                t['correct'] = l['correct']
                t['value'] = counter
                links.append(t)
                counter = 1
                l = li
            else:
                counter += 1

        t = {}
        t['source'] = li['source']
        t['target'] = li['target']
        t['correct'] = li['correct']
        t['value'] = counter
        links.append(t)

    for b in set(delay_temp):
        gap = {}
        gap['gap'] = b
        gap['count'] = delay_temp.count(b)
        delays.append(gap)

    return json.dumps([slots]+[links]+[delays])


@app.route('/Validator_Attack/<int:index>')
def Validator_Attack(index):
    votes0 = Vote_a()

    ats = filter(votes0,index)
    
    val = []
    for a in ats:
        val = val + a['casper_n'] + a['not_vote']
    print(val)
    val_error = []
    for v in val:
        if v:
            tmp = {}
            tmp['validator_index'] = v
            tmp['vote'] = 1
            val_error.append(tmp)
    val_error.sort(key=lambda x:x['validator_index'])

    #print(len(val_error))

    casper = []
    for s in range(index, index - 7 ,-1):
        #print(s)
        cas = {}
        cas['epoch'] = s
        cas['validator'] =copy.deepcopy(val_error)
        temp = filter(votes0,s)
        aggregate_y = []
        aggregate_n = []
        aggregate_not_vote=[]
        for t in temp:
            aggregate_y += t['casper_y']
            aggregate_n += t['casper_n']
            aggregate_not_vote += t['not_vote']

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
    for i in range(index, index-7, -1):
        p = []
        for s in range(i*32, (i+1)*32):
            data = Proposer.query.filter_by(slot=s).first()
            p.append(data.proposer)
        p.sort()
        proposer.append(p)
    return json.dumps([casper]+[proposer])


@app.route('/Epoch_Attack/<int:index>')
def Epoch_Attack(index):
    votes0 = Vote_a()
    votes = filter(votes0, 32533)
    all_balance = 0
    ghost_correct_balance = 0
    casper_correct_balance = 0
    for d in votes:
        all_balance += d['casper_y_balance'] + d['casper_n_balance'] + d['not_vote_balance']
        casper_correct_balance += d['casper_y_balance']
        for g in d['ghost_selection']:
            if g['canonical']:
                ghost_correct_balance += g['balance']

    st = {}
    st['epoch'] = 32533
    st['active_balance'] = all_balance
    st['head_correct_balance'] = ghost_correct_balance
    st['target_correct_balance'] = casper_correct_balance
        
    epochs = []
    if index >= 93750:
        Vote = Vote4
    else:
        if index >= 62500:
            Vote = Vote3
        else:
            if index >= 31250:
                Vote = Vote2
            else:
                Vote = Vote1
    data = Vote.query.filter(Vote.slot.in_(range(index*32,(index+225)*32))).all()
    print(len(data))

    prev_epoch = index
    all_balance = 0
    casper_correct_balance = 0
    ghost_correct_balance = 0
    for d in data:
        print(d.epoch)
        if d.epoch != prev_epoch:
            s = {}
            s['epoch'] = prev_epoch
            s['active_balance'] = all_balance
            s['head_correct_balance'] = ghost_correct_balance
            s['target_correct_balance'] = casper_correct_balance
            epochs.append(s)
            prev_epoch = d.epoch
            all_balance = 0
            casper_correct_balance = 0
            ghost_correct_balance = 0
        all_balance += d.casper_y_balance + d.casper_n_balance + d.not_vote_balance
        casper_correct_balance += d.casper_y_balance
        for g in d.ghost_selection:
            if g['canonical']:
                ghost_correct_balance += g['balance']
    s = {}
    s['epoch'] = prev_epoch
    s['active_balance'] = all_balance
    s['head_correct_balance'] = ghost_correct_balance
    s['target_correct_balance'] = casper_correct_balance
    epochs.append(s)

    print(len(epochs))

    if index > 32527 and index + 224 <= 32533:
        for e in epochs:
            if e['epoch'] == 32533:
                e = st
                break
            
    return json.dumps(epochs)

@app.route('/Overview')
def Overview():
    data= c_overview.query.order_by(c_overview.days).all()
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
    epochs = []
    # if index < 54225:
    #     data = Epoch.query.filter(Epoch.epoch.in_(range(index,index+225))).order_by(-Epoch.epoch).all()
    #     for d in data[::-1]:
    #         s = {}
    #         s['epoch'] = d.epoch
    #         s['active_balance'] = d.active_balance
    #         s['attesting_balance'] = d.attesting_balance
    #         s['target_correct_balance'] = d.target_correct_balance
    #         s['head_correct_balance'] = d.head_correct_balance
    #         epochs.append(s)
    # else:
        # if index >= 93750:
        #     print(4)
        #     Vote = Vote4
        # else:
        #     if index >= 62500:
        #         Vote = Vote3
        #         print(3)
        #     else:
        #         if index >= 54225:
        #             Vote = Vote2
        #             print(2)
    if index >= 93750:
        Vote = Vote4
    else:
        if index >= 62500:
            Vote = Vote3
        else:
            if index >= 31250:
                Vote = Vote2
            else:
                Vote = Vote1
    data = Vote.query.filter(Vote.slot.in_(range(index*32,(index+225)*32))).all()
    print(len(data))

    prev_epoch = index
    all_balance = 0
    al_balance = 0
    casper_correct_balance = 0
    ghost_correct_balance = 0
    for d in data:
        print(d.epoch)
        if d.epoch != prev_epoch:
            s = {}
            s['epoch'] = prev_epoch
            s['active_balance'] = all_balance
            s['active_balance_g'] = al_balance
            s['head_correct_balance'] = ghost_correct_balance
            s['target_correct_balance'] = casper_correct_balance
            epochs.append(s)
            prev_epoch = d.epoch
            all_balance = 0
            al_balance = 0
            casper_correct_balance = 0
            ghost_correct_balance = 0
        all_balance += d.casper_y_balance + d.casper_n_balance + d.not_vote_balance
        casper_correct_balance += d.casper_y_balance
        for g in d.ghost_selection:
            al_balance += g['balance']
            if g['canonical']:
                ghost_correct_balance += g['balance']
    s = {}
    s['epoch'] = prev_epoch
    s['active_balance'] = all_balance
    s['active_balance_g'] = al_balance
    s['head_correct_balance'] = ghost_correct_balance
    s['target_correct_balance'] = casper_correct_balance
    epochs.append(s)

    print(len(epochs))
    return json.dumps(epochs)


@app.route('/validator/<int:index>', methods=['GET'])
def validator(index):
    if index >= 93750:
        Vote = Vote4
    else:
        if index >= 62500:
            Vote = Vote3
        else:
            if index >= 31250:
                Vote = Vote2
            else:
                Vote = Vote1

    ats = Vote.query.filter(Vote.epoch == index).order_by(Vote.slot).all()
    val = []
    for a in ats:
        val = val + a.casper_n + a.not_vote
    print(val)
    val_error = []
    for v in val:
        if v:
            tmp = {}
            tmp['validator_index'] = v
            tmp['vote'] = 1
            val_error.append(tmp)
    val_error.sort(key=lambda x:x['validator_index'])

    #print(len(val_error))

    casper = []
    for s in range(index, index - 7 ,-1):
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
    for i in range(index, index-7, -1):
        p = []
        for s in range(i*32, (i+1)*32):
            data = Proposer.query.filter_by(slot=s).first()
            p.append(data.proposer)
        p.sort()
        proposer.append(p)
    return json.dumps([casper]+[proposer])


@app.route('/slot/<int:index>',methods=['GET'])
def slot(index):
    if index >= 93750:
        Vote = Vote4
    else:
        if index >= 62500:
            Vote = Vote3
        else:
            if index >= 31250:
                Vote = Vote2
            else:
                Vote = Vote1
    slots = []
    links_temp = []
    links = []
    delays = []
    delay_temp = []
    for s in range(index*32,(index+1)*32):
        ats = Attestation.query.filter_by(inclusion_slot=s).order_by(Attestation.slot, Attestation.committee_index).all()

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
                link['correct'] = a.target_correct and a.head_correct
                if committee_prev != a.committee_index:
                    temp['at_number'] += len(ats_no)
                    ats_no = set()
                    committee_prev = a.committee_index
                ats_no = ats_no|set(a.aggregation_indices)
                links_temp.append(link)

                delay_temp.append(a.target_epoch - a.source_epoch)
            temp['at_number'] += len(ats_no)

        votes = Vote.query.filter_by(slot = s).first()
        temp['casper_balance'] = 0
        temp['block_header'] = 0
        temp['ex_blocks'] = []
        blocks = []
        if votes:
            blocks = votes.ghost_selection
            temp['casper_balance'] = votes.casper_y_balance
        if len(blocks) > 0:
            blocks.sort(key=lambda x:(x['root']['data']))
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
        
        slots.append(temp)
        if temp['casper_balance'] == 0:
            continue

    if len(links_temp) > 0:
        l = {
            'source': links_temp[0]['source'],
            'target': links_temp[0]['target'],
            'correct': links_temp[0]['correct']
        }
    
        counter = 0
        links = []
        for li in links_temp:
            # print(li['target'])
            if li != l:
                t = {}
                t['source'] = l['source']
                t['target'] = l['target']
                t['correct'] = l['correct']
                t['value'] = counter
                links.append(t)
                counter = 1
                l = li
            else:
                counter += 1

        t = {}
        t['source'] = li['source']
        t['target'] = li['target']
        t['correct'] = li['correct']
        t['value'] = counter
        links.append(t)

    # delay_temp.append(2)
    for b in set(delay_temp):
        gap = {}
        gap['gap'] = b
        gap['count'] = delay_temp.count(b)
        delays.append(gap)
    # slots[20]['at_number'] *= 200
    # slots[20]['ex_blocks'] = []
    # slots[20]['ex_blocks'].append(slots[20]['block_header'])
    # slots[20]['ex_blocks'].append(slots[20]['block_header'])
    # slots[20]['ex_blocks'].append(slots[20]['block_header'])
    # for l in links:
    #     if l['source'] < 15 and l['target'] == 20 and not l['correct']:
    #         l['value'] *= 200
    #         break

    return json.dumps([slots] + [links] + [delays])



@app.route('/',methods=['GET'])
def index():
    return "Hello Vue"


if __name__ == '__main__':
    app.run(debug=True)