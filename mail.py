import smtplib

gmail_user = 'nguyenanti01@gmail.com'
gmail_password = 'Nguyen2222'
sent_from = gmail_user
to = 'nt85272@gmail.com'
subject = 'Thong bao cham cong thanh cong'
id = 123
body = f'NV {id} cham cong thanh cong'

email_text = f"""\
From: {sent_from}
To: {to}
Subject: {subject}

{body}
"""
# email_text = """\
# From: %s
# To: %s
# Subject: %s
#
# %s
# """ % (sent_from, to, subject, body)


try:
    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    server.ehlo()
    server.login(gmail_user, gmail_password)
    server.sendmail(sent_from, to, email_text)
    server.close()

    print ('Email sent!')
except:
    print ('Something went wrong...')