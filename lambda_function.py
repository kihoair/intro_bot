#coding:utf-8

from requests_oauthlib import OAuth1Session
from webscrape import webscrape
import datetime
import time
import urllib3

CK = process.env['CK']
CS = process.env['CS']
AT = process.env['AT']
AS = process.env['AS']

URL = 'https://api.twitter.com/1.1/statuses/update.json'

def my_handler(event, context):

    hosts=webscrape()

    if hosts == 'bartime':
        tweet = get_date() + "(" + get_day() + ")はバータイム営業です。"
    if hosts == 'specialday':
        tweet = get_date() + "(" + get_day() + ")は特別営業の日です。\n詳しくはHPをご確認ください。\nhttps://www.cafecottonclub.com/jazz/"
    else:
        tweet = get_date() + "(" + get_day() + ")のジャムセッションホストは\n" + hosts + "です。"

    session = OAuth1Session(CK, CS, AT, AS)

    params = {"status": tweet }
    session.post(URL, params = params)

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