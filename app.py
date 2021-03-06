import os
import json
import twilio
import requests
import local_settings
from twilio.rest import TwilioRestClient
from flask import Flask, render_template, request

app = Flask(__name__)

data = json.load(open(os.path.join(
    os.path.abspath(os.path.dirname(__file__)),
    "numbers.json"
)))


def cleanup(thing):
    if thing is None:
        return None

    thing = thing.replace(" ", "")
    thing = thing.replace(".", "")
    thing = thing.replace("(", "")
    thing = thing.replace(")", "")
    thing = thing.replace("-", "")
    thing = thing.replace("+", "")
    thing = thing[-10:]
    return thing


def send_text(whom, message):
    client = TwilioRestClient(
        local_settings.account_sid,
        local_settings.auth_token,
    )
    client.messages.create(to=whom, from_=local_settings.from_number,
                           body=message)


def send_yo():
    requests.post(
        "http://api.justyo.co/yoall/",
        data={"api_token": local_settings.yoapp_token}
    )


@app.route('/voice', methods=['POST'])
def voice():
    send_yo()

    fro = cleanup(request.form.get('From', None))
    SMS = "Yo, %s is at the door." % (fro)

    if fro in data:
        SMS += " (%s)" % (data[fro])

    for number in local_settings.team_numbers:
        send_text(number, SMS)
    return render_template("voice.xml", **{})


@app.route('/sms', methods=['POST'])
def sms():
    fro = cleanup(request.form.get('From', None))
    msg = request.form.get('Body', None)

    SMS = "From %s" % (fro)
    if fro in data:
        SMS += " (%s)" % (data[fro])
    SMS += " %s" % (msg)

    for number in local_settings.team_numbers:
        send_text(number, SMS)
    return render_template("sms.xml", **{})


@app.route('/yo', methods=['POST'])
def yo():
    pass


if __name__ == '__main__':
    app.run(debug=True)
