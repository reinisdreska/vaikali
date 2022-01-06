import requests
import json
from bs4 import BeautifulSoup

url = 'https://citro.lv/musu-veikali/'


def saglaba():
    results = requests.get(url)
    open("citro.html",'w', encoding='UTF-8').write(results.text)
    info()

def info():
    data = []
    html = open("citro.html",'r', encoding='UTF-8').read()
    base = BeautifulSoup(html, "html.parser")
    main = base.find_all("div", class_="col-lg-6")

    for row in main:
        shop_info = {}
        tags = row.find("h2")
        shop_info["address"] = str(tags.text)
        tags = row.find('a')
        lat = tags.attrs['data-lat']
        shop_info["lat"] = float(lat)
        lng = tags.attrs['data-lng']
        shop_info["lng"] = float(lng)
        tags = row.find("div", class_="work-time")
        shop_info["work_time"] = str(tags.find("strong").text)
        tags = row.find("div", class_="contacts")
        shop_info["contacts"] = "+371" + str(tags.find("strong").text)

        data.append({"address":shop_info["address"], "lat":shop_info["lat"],"lng":shop_info["lng"],"work_time":shop_info["work_time"],"contacts":shop_info["contacts"]})
    print(data)

saglaba()