__author__ = 'Jorge'

import smtplib

from email.MIMEText import MIMEText

def senMail():
    _from = "jorge.guerra881215@gmail.com"
    _to = _from

    message = MIMEText("This is a python mail")
    message["From"] = _from
    message["To"] = _to
    message["Subject"] = "Hello"

    serverSMTP = smtplib.SMTP("smtp.gmail.com",578)
    serverSMTP.ehlo()
    serverSMTP.strttls()
    serverSMTP.ehlo()
    serverSMTP.login(_from,"JLGTelnene1")

    serverSMTP.sendmail(_from,_to,message.as_string())

    serverSMTP.close()
