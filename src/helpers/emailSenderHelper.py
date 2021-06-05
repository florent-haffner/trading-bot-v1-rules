from src.helpers.dateHelper import SIMPLE_DATE_STR
from src.secret.keys import __EMAIL_USER, __EMAIL_PASSWORD

import smtplib
from datetime import datetime
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


__DESTINATION: str = 'neltharak@gmail.com'


def send_email(subject, body, attachments):
    __SENDER: str = __EMAIL_USER

    msg = MIMEMultipart()
    msg['From'] = __EMAIL_USER
    msg['To'] = __DESTINATION
    msg['Subject'] = '[' + datetime.now().strftime(SIMPLE_DATE_STR) + '] ' + subject

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

        # TODO -> check if still useful
        # if attachments:
        #     for file in attachments:
        #         remove_tmp_pics(file)
    except Exception as e:
        print(e)
    print('Sended email to', __DESTINATION, 'from', __EMAIL_USER, ', length msg', len(msg), 'and', len(attachments),
          'attachments')


if __name__ == '__main__':
    send_email('no files', '', [])
    # attachments = ['/tmp/2021-04-05 16:47:11.089790-macds.png', '/tmp/2021-04-05 16:47:11.296193-close_12_ema.png']
    # send_email('files', 'wsh', attachments)
