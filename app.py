import twilio
import local_settings
from twilio.rest import TwilioRestClient
from flask import Flask, render_template

app = Flask(__name__)


def send_text(whom, message):
    client = TwilioRestClient(
        local_settings.account_sid,
        local_settings.auth_token,
    )
    client.messages.create(to=whom, from_=local_settings.from_number,
                           body=message)



@app.route('/')
def index():
    for number in local_settings.team_numbers:
        send_text(number, 'test')
    return render_template("root.xml", **{})


if __name__ == '__main__':
    app.run(debug=True)
