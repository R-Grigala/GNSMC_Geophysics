from flask import Flask, render_template, url_for, jsonify

app = Flask(__name__)
data_list = [
    {
        "tStStatuse": "1",
        "tStCode": "BTNK",
        "tStNetworkCode": "GO",
        "tStLocation": "Botanical Garden (Tbilisi)",
        "tStLatitude": "41.6832",
        "tStLongitude": "40.7988",
        "tStElevation": "570",
        "tStOpenDate": "2011-12-27",
        "tStCloseDate": "0000-00-00",
        "tStType": "Permanent",
        "tStShow": "0",
        "tStLastEditor": "roma grigalashvili",
        "tStLastEditTime": "2019-02-22 11:00:28",
    },
    {
        "tStStatuse": "1",
        "tStCode": "BTNK",
        "tStNetworkCode": "GO",
        "tStLocation": "Botanical Garden (Tbilisi)",
        "tStLatitude": "41.6832",
        "tStLongitude": "44.7988",
        "tStElevation": "570",
        "tStOpenDate": "2011-12-27",
        "tStCloseDate": "0000-00-00",
        "tStType": "Permanent",
        "tStShow": "0",
        "tStLastEditor": "roma grigalashvili",
        "tStLastEditTime": "2019-02-22 11:00:28",
    },
    {
        "tStStatuse": "1",
        "tStCode": "BTNK",
        "tStNetworkCode": "GO",
        "tStLocation": "Botanical Garden (Tbilisi)",
        "tStLatitude": "40.6832",
        "tStLongitude": "44.7988",
        "tStElevation": "570",
        "tStOpenDate": "2011-12-27",
        "tStCloseDate": "0000-00-00",
        "tStType": "Permanent",
        "tStShow": "0",
        "tStLastEditor": "roma grigalashvili",
        "tStLastEditTime": "2019-02-22 11:00:28",
    },
        {
        "tStStatuse": "1",
        "tStCode": "BTNK",
        "tStNetworkCode": "GO",
        "tStLocation": "Botanical Garden (Tbilisi)",
        "tStLatitude": "41.6832",
        "tStLongitude": "40.7988",
        "tStElevation": "570",
        "tStOpenDate": "2011-12-27",
        "tStCloseDate": "0000-00-00",
        "tStType": "Permanent",
        "tStShow": "0",
        "tStLastEditor": "roma grigalashvili",
        "tStLastEditTime": "2019-02-22 11:00:28",
    },
    {
        "tStStatuse": "1",
        "tStCode": "BTNK",
        "tStNetworkCode": "GO",
        "tStLocation": "Botanical Garden (Tbilisi)",
        "tStLatitude": "41.6832",
        "tStLongitude": "44.7988",
        "tStElevation": "570",
        "tStOpenDate": "2011-12-27",
        "tStCloseDate": "0000-00-00",
        "tStType": "Permanent",
        "tStShow": "0",
        "tStLastEditor": "roma grigalashvili",
        "tStLastEditTime": "2019-02-22 11:00:28",
    },
    {
        "tStStatuse": "1",
        "tStCode": "BTNK",
        "tStNetworkCode": "GO",
        "tStLocation": "Botanical Garden (Tbilisi)",
        "tStLatitude": "40.6832",
        "tStLongitude": "44.7988",
        "tStElevation": "570",
        "tStOpenDate": "2011-12-27",
        "tStCloseDate": "0000-00-00",
        "tStType": "Permanent",
        "tStShow": "0",
        "tStLastEditor": "roma grigalashvili",
        "tStLastEditTime": "2019-02-22 11:00:28",
    }
]

@app.route("/")
def index():
    return render_template("index.html", data_list=data_list)

@app.route('/api/data')
def get_data():
    return jsonify(data_list)

if __name__ == '__main__':
    app.run(debug=True)
