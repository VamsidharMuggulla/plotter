import datetime
import json
import os
import requests
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__, template_folder='Templates')
app.config.from_object(__name__)
app.secret_key = "super secret key"


@app.route("/")
def graph():
    return render_template('graph.html')


@app.route("/process/data/", methods=['POST'])
def process_data():
    data = json.loads(request.form.get('prices'))
    result = []
    for price in data:
        date = datetime.datetime.strptime(price[0], "%Y-%m-%d")
        respons = requests.get('http://api.fixer.io/' + price[0] + '?base=' + request.form.get('currencya'))
        respons = json.loads(respons.text)
        rate = respons.get('rates').get(request.form.get('currencyb'))
        result.append([date.strftime('%Y-%m-%d'), str(float(price[1]) * float(rate))])
    return json.dumps(result)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
