#!/usr/bin/env python

import urllib
import json
import os

from flask import Flask
from flask import request
from flask import make_response

# Flask app should start in global layout
app = Flask(__name__)


@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json(silent=True, force=True)

    print("Request:")
    print(json.dumps(req, indent=4))

    res = processRequest(req)

    res = json.dumps(res, indent=4)
    # print(res)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r


def processRequest(req):
    if req.get("result").get("action") != "jackWebhook":
        return {}
    res = makeWebhookResult(req)
    return res

def listsum(numList):
    theSum = 0
    for i in numList:
        theSum = theSum + i
    return theSum

def makeWebhookResult(req):
    result = req.get("result")
    parameters = result.get("parameters")
    city = parameters.get("geo-city")
    number = parameters.get("number")
    mathop = parameters.get("math-operation")
    if mathop == "foo":
        speech = "Total value is "+str(listsum(number))
    print("Response:")
    print(speech)

    return {
        "speech": speech,
        "displayText": speech,
        "data": {},
        # "contextOut": [],
        "source": "apiai-weather-webhook-sample"
    }


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))

    print "Starting app on port %d" % port

    app.run(debug=False, port=port, host='0.0.0.0')
