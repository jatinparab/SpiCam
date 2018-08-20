#!/usr/bin/env python
# encoding: utf-8


import os
import time
import datetime 
from datetime import timedelta
import smtplib
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart

COMMASPACE = ', '

def main():
    sender = 'youremail'
    gmail_password = 'pass'
    recipients = ['cameraemail']
    f_time = (datetime.datetime.now() - datetime.timedelta(days=1)).strftime('%a %d %b')
    subject = 'Timelapse @' + f_time
    # Create the enclosing (outer) message
    outer = MIMEMultipart()
    outer['Subject'] = subject
    outer['To'] = COMMASPACE.join(recipients)
    outer['From'] = sender
    outer.preamble = 'Timelapse' + f_time

    # List of attachments
    #filejatin = '/mnt/motionvideos/' + datetime.datetime.now().strftime('%Y%m%d-timelapse.avi')
    filejatin2 = '/mnt/motionvideos/' + ((datetime.datetime.now() - datetime.timedelta(days = 1)).strftime('%Y%m%d-timelapse.avi'))
    #filejatin3 = '/mnt/motionvideos/201703030015.avi'
    attachments = [filejatin2]
    
    deletepath2 = 'sudo rm -r ' + filejatin2
    

    # Add the attachments to the message
    for file in attachments:
        try:
            with open(file, 'rb') as fp:
                msg = MIMEBase('application', "octet-stream")
                msg.set_payload(fp.read())
            encoders.encode_base64(msg)
            msg.add_header('Content-Disposition', 'attachment', filename=os.path.basename(file))
            outer.attach(msg)
        except:      
            continue
            
    composed = outer.as_string()

    # Send the email
    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as s:
            s.ehlo()
            s.starttls()
            s.ehlo()
            s.login(sender, gmail_password)
            s.sendmail(sender, recipients, composed)
            s.close()
        print("Email sent!")
    except:
        print("not mail" + file)	        
    
  
    

if __name__ == '__main__':
    main()
