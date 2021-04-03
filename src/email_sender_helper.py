import os
import smtplib
from CONSTANT import __EMAIL_USER, __EMAIL_PASSWORD


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


def send_email(destination, subject, text):
    SMTPServer = smtplib.SMTP("smtp.gmail.com", 587)
    SMTPServer.ehlo()
    SMTPServer.starttls()
    SMTPServer.ehlo()
    SMTPServer.login(__EMAIL_USER, __EMAIL_PASSWORD)

    header = 'To:' + destination + '\n' +\
             'From: ' + __EMAIL_USER + '\n' +\
             'Subject:' + subject + '\n'

    msg = header + '\n' + get_cowsay_asci(text)
    print(header)

    SMTPServer.sendmail(__EMAIL_USER, destination, msg)
    print('Sended a ', len(text), ' characers email')
    SMTPServer.close()


if __name__ == '__main__':
    destination = 'neltharak@gmail.com'
    send_email(destination, 'Hello world!', 'Incoming news :D')
