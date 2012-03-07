import smtplib
import os
from email.MIMEMultipart import MIMEMultipart
from email.MIMEBase import MIMEBase
from email.MIMEText import MIMEText
from email.Utils import COMMASPACE, formatdate
from email import Encoders
from email.header import Header
import urllib2

from django.conf import settings


def send_mail(send_to, subject, text, send_from="admin@mitnk.com", files=[], fail_silently=False):
    assert (type(send_to) == list or type(send_to) == tuple)
    assert (type(files) == list or type(files) == tuple)

    msg = MIMEMultipart()
    msg['From'] = send_from
    msg['To'] = COMMASPACE.join(send_to)
    msg['Date'] = formatdate(localtime=True)
    msg['Subject'] = Header(subject, "utf-8")
  
    msg.attach( MIMEText(text) )

    for f in files:
        basename = str(Header(os.path.basename(f), 'utf8'))
        part = MIMEBase('application', "octet-stream", charset="utf8")
        part.set_payload( open(f, "rb").read() )
        Encoders.encode_base64(part)
        part.add_header('Content-Disposition', 'attachment; filename="%s"' % basename)
        msg.attach(part)

    try:
        smtp = smtplib.SMTP("smtp.gmail.com", 587)
        smtpserver = 'smtp.gmail.com'
        smtpuser = send_from
        smtppass = settings.EMAIL_HOST_PASSWORD
        smtp.ehlo()
        smtp.starttls()
        smtp.ehlo()
        smtp.login(smtpuser, smtppass)
        smtp.sendmail(send_from, send_to, msg.as_string())
        smtp.close()
    except:
        if not fail_silently:
            raise
