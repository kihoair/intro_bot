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
    musicians_name = webscrape()


    tweet_date_part = get_date() + "(" + get_day() + ")"

    if musicians_name == "bartime":
        tweet = tweet_date_part + "はバータイム営業です。"
    elif musicians_name == 'specialday':
        tweet = tweet_date_part + "は特別営業の日です。\n詳しくはHPをご確認ください。\nhttps://www.cafecottonclub.com/jazz/"
    elif get_day() == '金':
        tweet = tweet_date_part + "の深夜ジャムセッションホストは\n" + musicians_name + "です。"
    elif get_day() == '土':
        tweet = tweet_date_part + "のオールナイトジャムセッションホストは\n" + musicians_name + "です。"
    elif get_day() == '水' or get_day() == '木':
        tweet = tweet_date_part + "のジャムセッションホストは\n" + "ゴッド井上as " + musicians_name + "です。"
    else:
        tweet = tweet_date_part + "のジャムセッションホストは\n" + musicians_name + "です。"

    params = {"status": tweet}
    twitter = OAuth1Session(CK, CS, AT, AS)
    req = twitter.post(URL, params=params)

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