import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from flask_cors import CORS

from flask import Flask, request
import smtplib
import configparser
import os

app = Flask(__name__)
CORS(app)


@app.route('/')
def send_emails():
    return 'hi test!'


@app.route('/v1/customemail', methods=['GET','POST'])
def customemail():
    data = request.get_json(silent=True)
    # data is empty
    config = configparser.ConfigParser()
    config.read('config.cfg')
    print(config)
    #email = config.get('DEFAULT', 'email')
    #val = config.get('DEFAULT', 'info')
    email = os.getenv('username')
    val = os.getenv('pw')
    email = email[1:-1]
    val = val[1:-1]
    gmail_user = email
    gmail_password = val

    sent_from = gmail_user

    to = ['amahmood561@gmail.com']
    subject = data.get('subject')
    body = data.get('message')
    #subject = 'OMG Super Important Message'
    #body = "Hey, what's sup?\n\n - You"

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

        print('Email sent!')
    except :
        print('Something went wrong...')
    return 'OK!'



if __name__ == '__main__':
    app.run()
