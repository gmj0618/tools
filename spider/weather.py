# -*- coding: utf-8 -*-
import sys

import json
import requests
import bs4
reload(sys)
sys.setdefaultencoding("utf-8")


def get_day_weather(city_code):
    day = None
    night = None
    resp = requests.get("http://www.weather.com.cn/weather1d/{}.shtml".format(city_code))
    html = bs4.BeautifulSoup(resp.content, 'html.parser')
    detail_info = html.find("input", attrs={"type": "hidden", "id": "hidden_title"}).attrs['value']
    attr = html.find("div", "t").ul.find_all("li")

    for tag in attr:
        block = tag.find("h1")
        if block:
            if "白天" in tag.find("h1").string:
                day = tag
            elif "夜间" in tag.find("h1").string:
                night = tag

    if day and night:
        day_weather = day_weather_collect(day)
        night_weather = day_weather_collect(night)
        return json.dumps([day_weather, night_weather, detail_info])
    return None, None


def day_weather_collect(tag):
    d = tag.find("h1").string
    wea = tag.find("p", "wea").string
    tem = "".join([tag.find("p", "tem").span.string, tag.find("p", "tem").em.string])
    win = tag.find("p", "win").span.string
    return " ".join([d, wea, tem, win])


def get_week_weather(city_code):
    resp = requests.get("http://www.weather.com.cn/weather/{}.shtml".format(city_code))
    html = bs4.BeautifulSoup(resp.content, 'html.parser')
    week_root = html.find("ul", "t clearfix").find_all("li")
    week_data = []
    for w in week_root:
        d = w.find("h1").string
        wea = w.find("p", "wea").string
        tem_attrs = w.find("p", "tem").attrs
        if "span" not in tem_attrs.keys():
            tem = w.find("p", "tem").i.string
        else:
            tem = "/".join([w.find("p", "tem").find("span").string, w.find("p", "tem").find("i").string])
        win = " ".join([w.find("p", "win").find("em").find("span").attrs['title'], w.find("p", "win").find("i").string])
        res = " ".join([d, wea, tem, win])
        week_data.append(res)
    return json.dumps(week_data)


def get_city_codes(city_name):
    resp = requests.get(
        "http://toy1.weather.com.cn/search?cityname={}&callback=success_jsonpCallback&_=1535016360549".format(
            city_name))
    html = bs4.BeautifulSoup(resp.content, 'html.parser')
    codes = html.contents[0]
    real_codes = json.loads(codes[22:-1])
    for rc in real_codes:
        info = rc['ref'].split("~")
        if info[2] == unicode(city_name):
            city_code = info[0]
            return city_code

city = sys.argv[1]
req_day = sys.argv[2]
code = get_city_codes(city)
if int(req_day) == 1:
    week_weather = get_day_weather(code)
else:
    week_weather = get_week_weather(code)
print week_weather

