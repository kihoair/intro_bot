from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time
import datetime
import re

T_DELTA = datetime.timedelta(hours=9)
JST = datetime.timezone(T_DELTA, 'JST')
T_NOW = datetime.datetime.now(JST) # + datetime.timedelta(days = 6)

def webscrape():
    options = Options()
    options.binary_location = '/opt/headless-chromium'
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--single-process')
    options.add_argument('--disable-dev-shm-usage')

    driver = webdriver.Chrome('/opt/chromedriver', chrome_options=options)

    driver.get('https://www.cafecottonclub.com/jazz/')
    time.sleep(0.8)
    html = driver.page_source

    driver.close();
    driver.quit();

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
    if int(days)%2 == 0:
        comment="odd"
    elif int(days)%2 == 1:
        comment="even"
    tr_class_selector = 'day-' + date + '.' + comment

    return tr_class_selector

def is_got_exist(day):

    if day< 4:
        god_exist = False
    elif day == 4 or day == 5:
        god_exist = True
    elif day == 6:
        god_exist = False

    return god_exist

def get_selector(tr_class_selector, td_class_selector):
    selector = "#main-table > tbody > tr.{} > td.intro.{}"
    formated_selector = selector.format(tr_class_selector, td_class_selector)
    
    return formated_selector

def get_jam(weekday_number):
    w_list = [
        ['Bar Time'],
        ['火曜練習ジャム','火曜練習ジャム15：00〜21：00'],
        ['水曜練習ジャム','水曜練習ジャム15：00〜21：00'],
        ['木曜練習ジャム','木曜練習ジャム15：00〜21：00'], 
        ['イントロ花金ミッドナイト・セッション23時〜翌3時'], 
        ['毎週土曜練習会','毎週土曜練習会15：00〜21：00'], 
        ['日曜練習ジャム','日曜練習ジャム15：00〜21：00']
        ]

    return w_list[weekday_number]

def extract_jam_desc_text(intro_one_day_html, weekday_number):
    # remove today's jam session title
    for div in intro_one_day_html.find_all("span", {'class':'emp'}):
        if div.text == "イントロとゴッド井上の安息日です。":
            return "sabbath"
        if div.text == "ジャズの隠れた名盤を聴くバータイム(18：30〜21：00)":
            return "bartime"
        if div.text not in get_jam(weekday_number):
            return "specialday"
        div.decompose()
    for div in intro_one_day_html.find_all("span", {'class':'red small'}):
        div.decompose()

    return intro_one_day_html.text

def format_hosts_name(jam_desc_text, weekday_number, god_exist):
    if weekday_number == 0:
        hosts = "bartime"
    elif weekday_number == 4:
        jam_desc_text = re.search("(.*)：(.*)", jam_desc_text)
        friday_host = re.search("ゴッド井上asと(.*)／", jam_desc_text.group(2))
        hosts = "ゴッド井上as " + friday_host.group(1)
    else:
        if god_exist == True:
            jam_desc_text = re.search("(.*)：(.*)", jam_desc_text)
            results = re.search("(.*)と(.*)",jam_desc_text.group(2))
        elif god_exist == False:
            results = re.search("(.*)と(.*)",jam_desc_text)
        hosts = results.group(1)
    
    return hosts

def get_hosts(html):
    parsed_html = BeautifulSoup(html, "html.parser")
    aDate = T_NOW
    weekday_number = aDate.weekday()

    tr_class_selector = get_tr_class_selector(aDate)
    td_class_selector = get_weekday(weekday_number)
    god_exist = is_got_exist(weekday_number)

    selector = get_selector(tr_class_selector, td_class_selector)
    intro_one_day_html = parsed_html.select_one(selector)
    jam_desc_text = extract_jam_desc_text(intro_one_day_html, weekday_number)
    

    if jam_desc_text == "bartime":
        return "bartime"
    if jam_desc_text == "sabbath":
        return "sabbath"
    if jam_desc_text == "specialday":
        return "specialday"
    
    formated_hosts = format_hosts_name(jam_desc_text, weekday_number, god_exist)

    return formated_hosts

