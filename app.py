import os
import json
import twilio
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



@app.route('/voice', methods=['POST'])
def voice():
    fro = cleanup(request.form.get('From', None))
    SMS = "Yo, %s is at the door." % (fro)

    if fro in data:
        SMS += " (%s)" % (data[fro])

    for number in local_settings.team_numbers:
        send_text(number, SMS)
    return render_template("root.xml", **{})


@app.route('/sms', methods=['POST'])
def sms():
    pass


if __name__ == '__main__':
    app.run(debug=True)
