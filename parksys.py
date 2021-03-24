""" Main App for Omni Comunnication Assistant (OCA)
    @author     putrinawang42@gmail.com
    @created    2021-03-23
    test coding """

from flask import Flask, request, jsonify
import datetime, json

app = Flask(__name__)

@app.route('/registration', methods=["POST"])
def car_regist():

    if "tipe" in request.json :
        tipe = request.json["tipe"]
    if "warna" in request.json:
        warna = request.json["warna"]
    if "plat_nomor" in request.json:
        plat_nomor = request.json["plat_nomor"]
        plat_nomor = plat_nomor.replace(" ", "")
        print (plat_nomor)

    checkin = datetime.datetime.now()

    carDict = {
        "tipe": tipe,
        "plat_nomor": plat_nomor,
        "warna": warna,
        "parking_lot": "A1",
        "tanggal_masuk": str(checkin),
        "tanggal_keluar": ""
    }

    filename = 'DataParkir.json'
    with open(filename) as f:
        data = json.load(f)

    with open(filename, 'w') as f:
        data.append(carDict)
        json.dump(data, f)

    response = {
        "plat_nomor": plat_nomor,
        "parking_lot": "A1",
        "tanggal_masuk": str(checkin)
    }

    return jsonify(response)

@app.route('/checkout', methods=["GET"])
def car_checkout():
    
    filename = 'DataParkir.json'
    with open(filename, 'r') as f:
        json_data = json.load(f)
    
    if "plat_nomor" in request.json :
        plat_nomor = request.json["plat_nomor"]
        plat_nomor = plat_nomor.replace(" ", "")
    
    for i in json_data:
        if plat_nomor.lower() == i["plat_nomor"].lower():
            checkin = i["tanggal_masuk"]
            checkin = datetime.datetime.strptime(checkin, '%Y-%m-%d %H:%M:%S.%f')
            
            checkout = datetime.datetime.now()
            i['tanggal_keluar'] = str(checkout)
            td = (checkout - checkin).seconds / 3600
            
            if i['tipe'] == "SUV":
                tariff = 25000 + round(td)*5000
            elif i['tipe'] == "MPV":
                tariff = 35000 + round(td)*7000
            
    with open(filename, 'w') as f:
        json.dump(json_data, f, indent=2)
    
    response = {
        "plat_nomor": i["plat_nomor"],
        "tanggal_masuk": i["tanggal_masuk"],
        "tanggal_keluar": str(checkout),
        "jumlah_bayar": tariff
    }
    
    return jsonify(response)

@app.route('/count', methods=["GET"])
def car_count():
    filename = 'DataParkir.json'
    with open(filename, 'r') as f:
        json_data = json.load(f)
    
    if "tipe" in request.json :
        tipe = request.json["tipe"]
    
    jumlah = []
    count = 0
    for i in json_data:
        if tipe.lower() == i["tipe"].lower():
            jumlah.append(i['plat_nomor'])
            count = len(jumlah)

    response = {
        'jumlah_kendaraan': count
    }

    return jsonify(response)

@app.route('/listplat', methods=["GET"])
def plat_list():
    
    filename = 'DataParkir.json'
    with open(filename, 'r') as f:
        json_data = json.load(f)

    if "warna" in request.json :
        warna = request.json["warna"]
    
    plat = []
    for i in json_data:
        if warna.lower() == i["warna"].lower():
            plat.append(i['plat_nomor'])
    
    response = {
        'plat_nomer': plat
    }

    return jsonify(response)

app.run()