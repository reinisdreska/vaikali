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
    data_json = {
        "type": "FeatureCollection",
        "features": []
    }
    for row in data:
        properties = {
            "id" : len(str(row)),
            "link" : "https://www.latts.lv/lats-veikali",
            "lat": row["lat"],
            "lng": row["lng"],
            "address": row["address"],
            "email": "None",
            "phone": row["contacts"],
            "working_hours": row["work_time"],
            "NOSAUKUMS": "Lats",
            "SAIS_NOS": "Lats",
            "GRUPA": "Pārtikas/mājsaimniecības preču tīklu veikali",
            "STIPS": 11,
            "TIPS": "tirdzniecibas centrs",
            "Layer": "tirdzniecibas centrs",
            "MEROGS": 0.0,
            "WMS": 0,
            "TELEFONS": row["contacts"],
            "PIEZIMES": row["work_time"],
            "X": row["lng"],
            "Y": row["lat"],
            "X1": "dms for lng",
            "Y1": "dms for lat"
        }
        data_json["features"].append({"type": "Feature", "geometry": {"type": "Point", "coordinates": [row["lng"], row["lat"]]}, "properties": properties})
    parsed = json.dumps(data_json, indent=6)
    open("Lats.json","w", encoding='UTF-8').write(parsed)

saglaba()