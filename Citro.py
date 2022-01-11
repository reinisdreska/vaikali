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
        shop_info["address"] = str(tags.text).replace("'", "").replace('"', '')
        tags = row.find('a')
        lat = tags.attrs['data-lat']
        shop_info["lat"] = str(lat)
        lng = tags.attrs['data-lng']
        shop_info["lng"] = str(lng)
        tags = row.find("div", class_="work-time")
        shop_info["work_time"] = str(tags.find("strong").text).replace("'", "").replace('"', '')
        tags = row.find("div", class_="contacts")
        shop_info["contacts"] = "+371 " + str(tags.find("strong").text).replace("'", "").replace('"', '')

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
            "link" : "https://citro.lv/musu-veikali/",
            "lat": float(row["lat"]),
            "lng": float(row["lng"]),
            "address": row["address"],
            "email": "None",
            "phone": row["contacts"],
            "working_hours": row["work_time"],
            "NOSAUKUMS": "Citro",
            "SAIS_NOS": "Citro",
            "GRUPA": "Pārtikas/mājsaimniecības preču tīklu veikali",
            "STIPS": 11,
            "TIPS": "tirdzniecibas centrs",
            "Layer": "tirdzniecibas centrs",
            "MEROGS": 0.0,
            "WMS": 0,
            "TELEFONS": row["contacts"],
            "PIEZIMES": row["work_time"],
            "X": float(row["lng"]),
            "Y": float(row["lat"]),
            "X1": "dms for lng",
            "Y1": "dms for lat"
        }
        data_json["features"].append({"type": "Feature", "geometry": {"type": "Point", "coordinates": [row["lng"], row["lat"]]}, "properties": properties})
    parsed = json.dumps(data_json, indent=6)
    open("Citro_tests1.json","w", encoding='UTF-8').write(parsed)

saglaba()