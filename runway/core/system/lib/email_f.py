import smtplib
from collections import namedtuple
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from . import site_settings_f
import os

template = """
<html>
      <head>
        <style type="text/css" media="screen">
        body
        {{
            font-family:            "Calibri", "Helvetica", "Arial", "Verdana", "sans-serif";
            font-size:              11pt;
            line-height:            1.3em;
        }}
        </style>
    </head>
    <body>
        {}
    </body>
</html>
"""

# http://stackoverflow.com/questions/882712/sending-html-email-in-python
def send_email(to, subject, text_message="", html_message="", email_from=None, test_mode=False):
    if text_message == "" and html_message == "":
        raise Exception("Cannot send an empty message")
    
    if email_from is None:
        domain = site_settings_f.get_setting("runway.system.domain")
        email_from = "{0} <no-reply@{0}>".format(domain)
    
    # Create message container - the correct MIME type is multipart/alternative.
    msg = MIMEMultipart('alternative')
    msg['Subject'] = subject
    msg['From'] = email_from
    
    if type(to) == str:
        msg['To'] = to
    else:
        msg['To'] = ", ".join(to)
    
    if html_message == "" and text_message != "":
        html_message = text_message.replace("\n", "<br />")
    
    # Create the body of the message (a plain-text and an HTML version).
    html_message = template.format(html_message)
    
    html_message = html_message.replace("£", "")
    text_message = text_message.replace("£", "")
    
    # Record the MIME types of both parts - text/plain and text/html.
    part1 = MIMEText(text_message, 'plain')
    part2 = MIMEText(html_message, 'html')
    
    # Attach parts into message container.
    # According to RFC 2046, the last part of a multipart message, in this case
    # the HTML message, is best and preferred.
    msg.attach(part1)
    msg.attach(part2)
    
    if not test_mode:
        _send(email_from, to, msg.as_string())
    else:
        return (email_from, to, msg.as_string())

def _send(from_email_address, to, msg):
    # My local dev doesn't send emails, to prevent tests erroring I've added this line
    if __file__[:14] == "/home/teifion/":
        return
    
    s = smtplib.SMTP('localhost')
    # sendmail function takes 3 arguments: sender's address, recipient's address
    # and message to send - here it is sent as one string.
    s.sendmail(from_email_address, to, msg)
    s.quit()

# http://stackoverflow.com/questions/3362600/how-to-send-email-attachments-with-python
def send_email_attatchment(to, subject, message, files, email_from=None, server="localhost"):
    assert type(files)==list
    
    raise Exception("Not implemented")

    msg = MIMEMultipart()
    msg['From'] = email_from
    if type(to) == str:
        to = [to]
    msg['To'] = ", ".join(to)
    
    msg['Subject'] = subject
    msg.attach(MIMEText(message))

    for f in files:
        part = MIMEBase('application', "octet-stream")
        part.set_payload(open(f,"rb").read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', 'attachment; filename="%s"' % os.path.basename(f))
        msg.attach(part)

    smtp = smtplib.SMTP(server)
    smtp.sendmail(email_from, to, msg.as_string())
    smtp.close()
