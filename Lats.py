import requests
import json
from bs4 import BeautifulSoup
import re

url = 'https://www.latts.lv/lats-veikali'

def saglaba():
    results = requests.get(url)
    open("lats.html",'w', encoding='UTF-8').write(results.text)
    info()

def info():
    data = []
    html = open("lats.html",'r', encoding='UTF-8').read()
    base = BeautifulSoup(html, "html.parser")
    main = base.find_all("tr")

    for row in main:
        shop_info = {}
        tags = row.find("h4")
        if str(tags) != "None":
            shop_info["address"] = str(tags.text).replace("'", "").replace('"', '')
        else:
            continue
        tags = row.find(class_="draw-ride")
        if tags:
            lat = tags.attrs['data-lat']
            shop_info["lat"] = str(lat)
            lng = tags.attrs['data-long']
            shop_info["lng"] = str(lng)
        else:
            shop_info["lat"] = "None"
            shop_info["lng"] = "None"
        tags = row.find("div", class_="HiddenTimeWork")
        shop_info["work_time"] = re.sub("\s+", " ", str(tags.text).replace("\n\n", "").replace("\n", "; ").replace(" : ", " ").replace("a:", "a")).replace("'", "").replace('"', '')
        tags = row.find(class_="Phone")
        if tags:
            shop_info["contacts"] = re.sub("\n+", "", "+371 " + str(tags.text).replace("'", "").replace('"', ''))
        else:
            shop_info["contacts"] = "None"
        
        data.append({"address":shop_info["address"], "lat":shop_info["lat"],"lng":shop_info["lng"],"work_time":shop_info["work_time"],"contacts":shop_info["contacts"]})
    get_json(data)

def get_json(data):
    data_str = "[\n"
    for row in data:
        data_string = str(row).replace("'", '"').replace(r'\xa0', " ")
        data_str += "\t" + data_string + ","
        data_str = data_str + "\n"
    data_str = data_str[:-2] + "\n" + "]"
    open("lats.json","w", encoding='UTF-8').write(data_str)

saglaba()