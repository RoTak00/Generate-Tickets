import smtplib, ssl
import random
import base64

from pathlib import Path
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.utils import COMMASPACE, formatdate
from email import encoders

scope = str(input("g / l:\n"))

smtp_server = "smtp.gmail.com"
port = 587  # For starttls
filename = "img1.png"

marker = "MARKERUNIQUE"

fo = open(filename, "rb")
filecontent = fo.read()
encodedcontent = base64.b64encode(filecontent)

msgbody = """
Salut! Aici este biletul tau! Nu il transmite nimanui si prezinta-l la intrarea la film.
Nu uita sa iti aduci snacks-uri, papuci de casa si o paturica. De asemenea, nu uita ca taxa de intrare este de 5 lei!
Te asteptam!
"""

msg1 = """From: De la CSE CNLR Bistrita <cse@cnlr.ro>
To: Pentru """
msg3 = """>
Subject: Vizionare de Film CNLR Atasament
MIME-Version: 1.0
Content-type: multipart/mixed; boundary = %s
--%s
""" % (marker, marker)

msg4 = """Content-Type: text/plain
Content-Transfer-Encoding:8bit

%s
--%s
""" %(msgbody, marker)

msg5 = """Content-Type: multipart/mixed; name =\"%s\"
Content-Transfer-Encoding:base64
Content-Disposition: attachment; filename = %s

%s
--%s--
""" %(filename, filename, encodedcontent, marker)



sender_email = "cse@cnlr.ro"
password = input("Type your password and press enter: \n")

if scope == "l":
    f_list = open("listL.txt", "r", encoding = "utf-8");
else:
    f_list = open("listG.txt", "r", encoding = "utf-8");
    
v_list = []
while True:
    temp_el = f_list.readline().rstrip("\n").rstrip(" ")
    #print(temp_el)
    if temp_el == "":
        break
    v_list.append([x.strip(" ") for x in temp_el.split(",")])

input("Se vor trimite " + str(len(v_list)) + " mail-uri OK? \n")

# Create a secure SSL context
context = ssl.create_default_context()

# Try to log in to server and send email
try:
    server = smtplib.SMTP(smtp_server,port)
    server.ehlo() # Can be omitted
    server.starttls(context=context) # Secure the connection
    server.ehlo() # Can be omitted
    server.login(sender_email, password)

    for i in range(len(v_list)):
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = v_list[i][0]
        msg['Date'] = formatdate(localtime=True)
        msg['Subject'] = "Movie Night CNLR"
        msg.attach(MIMEText("""Salut! Aici este biletul tau pentru Movie Night-ul de Marti, 21 Decembrie 2021, ora 17:30!
Te rugam sa ajungi cu aproximativ 10 minute inainte de ora 17:30, pentru a se asigura intrarea facila a tuturor participantilor!
Nu il transmite nimanui si prezinta-l la intrarea la film.
Nu uita sa iti aduci snacks-uri, papuci de casa si o paturica. De asemenea, nu uita ca taxa de intrare este de 5 lei!
Te asteptam cu drag si iti uram o seara foarte frumoasa!"""))

        part = MIMEBase('application', "octet-stream")
        filename = ""
        if scope == "l":
            filename = "imgL/bilet"+str(v_list[i][1])+".png"
        else:
            filename = "imgG/bilet"+str(v_list[i][1])+".png"
        with open(filename, 'rb') as file:
            part.set_payload(file.read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition','attachment; filename = {}'.format(Path(filename).name))
        msg.attach(part)

        print(str(i) + " Se trimite la " + str(v_list[i][0]), end = "")
        server.sendmail(sender_email, v_list[i][0], msg.as_string())
        print (" OK")
except Exception as e:
    # Print any error messages to stdout
    print(e)
finally:
    server.quit() 
