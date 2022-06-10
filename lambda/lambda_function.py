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

T_DELTA = datetime.timedelta(hours=9)
JST = datetime.timezone(T_DELTA, 'JST')
T_NOW = datetime.datetime.now(JST) #+ datetime.timedelta(days = 6)

def my_handler(event, context):
    musicians_name = webscrape()

    tweet_date_part = get_date() + "(" + get_day() + ")"

    #manenboushi_jam = "\n (まん延防止等重点措置中のため、15:00~21:00)"
    #manenboushi_bar = "\n (まん延防止等重点措置中のため、18:30~21:00)"

    if musicians_name == "bartime":
        tweet = tweet_date_part + "はバータイム営業です"
    elif musicians_name == 'sabbath':
        tweet = tweet_date_part + "はイントロとゴッド井上の安息日です。" 
    elif musicians_name == 'specialday':
        tweet = tweet_date_part + "は特別営業の日です。\n詳しくはHPをご確認ください。\nhttps://www.cafecottonclub.com/jazz/"
    elif get_day() == '金':
        tweet = tweet_date_part + "の深夜ジャムセッションホストは\n" + musicians_name + "です。"
    elif get_day() == '土':
        tweet = tweet_date_part + "のジャムセッションホストは\n" + musicians_name + "です。"
    elif get_day() == '水' or get_day() == '木':
        tweet = tweet_date_part + "のジャムセッションホストは\n" + "ゴッド井上as " + musicians_name + "です。"
    else:
        tweet = tweet_date_part + "のジャムセッションホストは\n" + "ゴッド井上as " + musicians_name + "です。"
    print("---TWEET---")
    print(tweet)
    params = {"status": tweet}
    twitter = OAuth1Session(CK, CS, AT, AS)
    req = twitter.post(URL, params=params)

    if req.status_code == 200:
        print(tweet)
        return tweet
    else:
        print(req.status_code)
        return req.status_code

def get_day():
    t_now = T_NOW
    w_n = t_now.weekday()
    w_list = ['月', '火', '水', '木', '金', '土', '日']
    return w_list[w_n]

def get_date():
    t_now = T_NOW
    
    if t_now.strftime('%m')[0] == "0":
        month = t_now.strftime('%m')[1]
    else:
        month = t_now.strftime('%m')

    if t_now.strftime('%d')[0] == "0":
        days = t_now.strftime('%d')[1]
    else:
        days = t_now.strftime('%d')

    return month + "月" + days + "日"