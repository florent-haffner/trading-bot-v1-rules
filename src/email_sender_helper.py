import smtplib
from email import encoders
from email.mime.application import MIMEApplication
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from CONSTANT import __EMAIL_USER, __EMAIL_PASSWORD

__DESTINATION = 'neltharak@gmail.com'


def get_cowsay_asci(text):
    return """
         _____________ 
        < """ + text + """">
        \   ^__^
         \  (oo)\_______
            (__)\       )\/
                ||----w |
                ||     ||
    """


def send_email(subject, body, attachments):
    __SENDER = __EMAIL_USER

    msg = MIMEMultipart()
    msg['From'] = __EMAIL_USER
    msg['To'] = __DESTINATION
    msg['Subject'] = subject

    msgText = MIMEText('<b>%s</b>' % (body), 'html')
    msg.attach(msgText)

    for file in attachments:
        with open(file, 'rb') as fp:
            img = MIMEImage(fp.read())
            img.add_header('Content-Disposition', 'attachment', filename=file)
            msg.attach(img)

    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as smtpObj:
            smtpObj.ehlo()
            smtpObj.starttls()
            smtpObj.login(__EMAIL_USER, __EMAIL_PASSWORD)
            smtpObj.sendmail(__SENDER, __DESTINATION, msg.as_string())
    except Exception as e:
        print(e)


if __name__ == '__main__':
    send_email('no files', '', [])
    attachments = ['/tmp/2021-04-05 16:47:11.089790-macds.png', '/tmp/2021-04-05 16:47:11.296193-close_12_ema.png']
    send_email('files', 'wsh', attachments)
