import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from flask_cors import CORS

from flask import Flask, request
import smtplib
import configparser
import os
import logging
app = Flask(__name__)
CORS(app)
import sys


@app.route('/')
def send_emails():
    return 'hi test!'


@app.route('/v1/customemail', methods=['GET','POST'])
def customemail():
    app.logger.addHandler(logging.StreamHandler(sys.stdout))
    app.logger.setLevel(logging.ERROR)
    data = request.get_json()
    app.logger(data)
    print(data)
    email = os.getenv('username')
    val = os.getenv('pw')
    print(email)
    print(val)
    gmail_user = email
    gmail_password = val
    sent_from = gmail_user
    app.logger("logger username: "+gmail_user)
    to = ['amahmood561@gmail.com']
    subject = data.get('subject')
    body = data.get('message')

    message = MIMEMultipart()
    message['From'] = sent_from
    message['To'] = sent_from
    message['Subject'] = subject  # The subject line
    message.attach(MIMEText(body, 'plain'))
    mime_test = message.as_string()

    try:
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.ehlo()
        server.login(gmail_user, gmail_password)
        server.sendmail(sent_from, to, mime_test)
        server.close()
        app.logger("sent emial")
        print('Email sent!')
    except :
        print('Something went wrong...')
    return 'OK!'



if __name__ == '__main__':
    print("Running in debug mode")
    CORS = CORS(app)
    PORT = int(os.environ.get('PORT', 5000))
    #app.run()
    app.run(host='0.0.0.0', port=PORT, debug=True)
