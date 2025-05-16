from draftkingsV4 import DraftKingsDataExtractor
from betMGM import MGMDataExtractor
from bovada import BovadaDataExtractor
from caesarsV1 import CaesarsDataExtractor
from espn import ESPNDataExtractor


import smtplib
from email.message import EmailMessage
import getpass

HOST = "smtp-mail.outlook.com"
PORT = 587


FROM_EMAIL = "sports_arbing@outlook.com"
TO_EMAIL = "ayushp802@gmail.com"
PASSWORD = "$portsBets123"

MESAGE = """Subject: Script Test

Hi this is a test
"""


smtp = smtplib.SMTP(HOST, PORT)

status_code, response = smtp.ehlo()

print("echoing server", status_code, response)
status_code, response = smtp.starttls()
print("start tls", status_code, response)

status_code, response = smtp.login(FROM_EMAIL, PASSWORD)
print("loggin in", status_code, response)
smtp.sendmail(FROM_EMAIL, TO_EMAIL, MESAGE)
smtp.quit()

