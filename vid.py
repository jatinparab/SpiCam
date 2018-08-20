#!/usr/bin/env python
# encoding: utf-8
"""
python_3_email_with_attachment.py
Created by Robert Dempsey on 12/6/14.
Copyright (c) 2014 Robert Dempsey. Use at your own peril.

This script works with Python 3.x

NOTE: replace values in ALL CAPS with your own values
"""

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
    sender = 'email'
    gmail_password = 'password'
    recipients = ['parabcamera@gmail.com']
    f_time = datetime.datetime.now().strftime('%a %d %b @ %H:%M')
    subject = 'Video @' + f_time
    # Create the enclosing (outer) message
    outer = MIMEMultipart()
    outer['Subject'] = subject
    outer['To'] = COMMASPACE.join(recipients)
    outer['From'] = sender
    outer.preamble = 'You will not see this in a MIME-aware mail reader.\n'

    # List of attachments
    filejatin = '/mnt/motionvideos/' + datetime.datetime.now().strftime('%Y%m%d%H%M.avi')
    filejatin2 = '/mnt/motionvideos/' + ((datetime.datetime.now() - datetime.timedelta(minutes = 1)).strftime('%Y%m%d%H%M.avi'))
    filejatin3 = '/mnt/motionvideos/' + ((datetime.datetime.now() - datetime.timedelta(minutes = 2)).strftime('%Y%m%d%H%M.avi'))
    attachments = [filejatin, filejatin2, filejatin3]
    deletepath = 'sudo rm -r ' + filejatin
    deletepath2 = 'sudo rm -r ' + filejatin2
    deletepath3 = 'sudo rm -r ' + filejatin3

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
	        
    try:
       os.remove(filejatin)
    except:
       try:
          os.remove(filejatin2)
       except:   
          os.remove(filejatin3)

if __name__ == '__main__':
    main()
