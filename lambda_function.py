#coding:utf-8

from requests_oauthlib import OAuth1Session
from webscrape import webscrape
import datetime
import time
import urllib3
import os

CK = os.environ['CK']
CS = os.environ['CS']
AT = os.environ['AT']
AS = os.environ['AS']

URL = 'https://api.twitter.com/1.1/statuses/update.json'

def my_handler(event, context):
    hosts=webscrape()

    if hosts == "bartime":
        tweet = get_date() + "(" + get_day() + ")はバータイム営業です。"
    elif hosts == 'specialday':
        tweet = get_date() + "(" + get_day() + ")は特別営業の日です。\n詳しくはHPをご確認ください。\nhttps://www.cafecottonclub.com/jazz/"
    elif get_day() == '金':
        tweet = get_date() + "(" + get_day() + ")の深夜ジャムセッションホストは\n" + hosts + "です。"
    elif get_day() == '土':
        tweet = get_date() + "(" + get_day() + ")のオールナイトジャムセッションホストは\n" + hosts + "です。"
    elif get_day() == '水' or get_day() == '木':
        tweet = get_date() + "(" + get_day() + ")のオールナイトジャムセッションホストは\n" + "ゴッド井上as " + hosts + "です。"
    else:
        tweet = get_date() + "(" + get_day() + ")のジャムセッションホストは\n" + hosts + "です。"
    
    params = {"status": tweet }
    twitter = OAuth1Session(CK, CS, AT, AS)
    req = twitter.post(URL, params = params)

    if req.status_code == 200:
        return tweet
    else:
        return req.status_code

def get_day():
    w_n = datetime.datetime.today().weekday()
    w_list = ['月', '火', '水', '木', '金', '土', '日']
    return w_list[w_n]

def get_date():
    if datetime.datetime.today().strftime('%m')[0] == "0":
        month = datetime.datetime.today().strftime('%m')[1]
    else:
        month = datetime.datetime.today().strftime('%m')

    if datetime.datetime.today().strftime('%d')[0] == "0":
        days = datetime.datetime.today().strftime('%d')[1]
    else:
        days = datetime.datetime.today().strftime('%d')

    return month + "月" + days + "日"
    
print webscrape()