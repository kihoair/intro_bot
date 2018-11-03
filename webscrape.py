#coding:utf-8

from selenium import webdriver
from bs4 import BeautifulSoup
import datetime
import time
import re

def webscrape():
    # webdriver settings
    options = webdriver.ChromeOptions()
    options.binary_location = "./bin/headless-chromium"
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--single-process")

    driver = webdriver.Chrome(
        executable_path="./bin/chromedriver",
        chrome_options=options
    )

    # web scraping
    driver.get("https://www.cafecottonclub.com/jazz/")
    time.sleep(0.6)
    html = driver.page_source.encode('utf-8')

    return get_hosts(html)

def get_weekday(day):

    if day< 5:
        weekday = "no"
    elif day== 5:
        weekday = "sat"
    elif day== 6:
        weekday = "sun"

    return weekday

def get_tr_class_selector(day):

    if day.strftime("%m")[0] =="0":
        month = day.strftime("%m")[1]
    else:
        month = day.strftime("%m")

    if day.strftime("%d")[0] == "0":
        days = day.strftime("%d")[1]
    else:
        days = day.strftime("%d")

    date = month + "-" + days

    # odd and even are reversed, but the website is incorrect so this swapping is correct.
    if int(date[3:])%2 == 0:
        comment="odd"
    elif int(date[3:])%2 == 1:
        comment="even"
    tr_class_selector = 'day-' + date + '.' + comment

    return tr_class_selector

def get_god_exist(day):

    if day< 4:
        god_exist = False
    elif day == 4 or day == 5:
        god_exist = True
    elif day == 6:
        god_exist = False

    return god_exist

def get_hosts(html):

    soup = BeautifulSoup(html, "html.parser")
    aDate = datetime.datetime.today()

    tr_class_selector = get_tr_class_selector(aDate)
    weekday = get_weekday(aDate.weekday())
    god_exist = get_god_exist(aDate.weekday())

    # get selector
    selector = "#main-table > tbody > tr.{} > td.intro.{}"
    selector = selector.format(tr_class_selector,weekday)
    
    soup = soup.select_one(selector)

    for div in soup.find_all("span", {'class':'emp'}):
        if div.text.encode('utf-8') != get_jam():
            return "specialday"
        div.decompose()
    for div in soup.find_all("span", {'class':'red small'}):
        div.decompose()

    soup2 = soup.text.encode('utf-8')

    if aDate.weekday() == 0:
        hosts = "bartime"
    elif aDate.weekday() == 4:
        soup2 = re.search("(.*)：(.*)", soup2)
        results = re.search("(.*)と(.*)", soup2.group(2))
        hosts = results.group(1) + " " + results.group(2)[:-1]
    else:
        if god_exist == True:
            soup2 = re.search("(.*)：(.*)", soup2)
            results = re.search("(.*)と(.*)",soup2.group(2))
        elif god_exist == False:
            results = re.search("(.*)と(.*)",soup2)
        hosts = results.group(1)

    return hosts

def get_jam():
    w_n = datetime.datetime.today().weekday()
    w_list = ['Bar Time', '火曜練習ジャム', '水曜練習ジャム', '木曜練習ジャム', 'イントロ花金ミッドナイト・セッション23時〜翌3時', '毎週土曜12時間練習ジャム', '日曜練習ジャム']
    
    return w_list[w_n]