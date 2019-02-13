# SpiCam
A Raspberry Pi based, Spy Camera, with Motion Detection, Android Notifications, Intruder Alerts, Snapshots, E-Mails and NAS system for storage of video snippets. 

## Synopsis

SpiCam is a prebuilt Raspberry Pi based Spy Camera. It detects motion and starts recording video and sends you a notification at the same time. It also emails you the video of the entire 'motion' event and send you one image of the best frame. It also records timelapse video by taking snapshot at every 5 seconds and renders a video at 3 am everyday, and mails it at the same time.

## Motivation

My house recently had a break-in, and due to no CCTV arrangements in our housing complex it was impossible for us to do or prove anything, so I decided to make a Spy Camera of my own.

## Installation

### Prerequisites
1. A Raspberry Pi (with Internet Connectivity)
2. Pi Camera (or a similar usb camera, although I'll be considering steps to enable Pi camera only)
3. A Computer or HDMI Cable + Mouse + Keyboard (to control and write to the Pi)
###

You can either use the HDMI cable to control the Pi or directly control it via SSH, doesn't matter because all the commands are to executed in the Terminal itself.

So I am assuming that you have set up the Pi to run, and already have a way to control and execute commands from the terminal too.

First off, we need to enable the Pi Camera. Connect the Pi Camera to board in the Camera Slot, make sure that it is tight enough.

Open up a terminal and enter the following commands.

```
sudo apt-get update
sudo apt-get upgrade
sudo raspi-config

```

You should now see a grey background screen with many options.

Select Camera and enable it. Now reboot your Pi with this command.

```
sudo reboot

```

Now try clicking an image

```
raspistill -o image.jpg

```

If it does not give any error you have enabled the camera.

Navigate to you Desktop 

```
cd home/pi/Desktop

```

Clone my git repository here.

```
git clone https://www.github.com/sulphurgfx/SpiCam

```

A service called as motion is needed. 

But first we need to remove services that might interfere with Motion.

```
sudo apt-get remove libavcodec-extra-56 libavformat56 libavresample2 libavutil54

```

Install these packages.

```

wget https://github.com/ccrisan/motioneye/wiki/precompiled/ffmpeg_3.1.1-1_armhf.deb
sudo dpkg -i ffmpeg_3.1.1-1_armhf.deb

```

Install other depending packages

```

sudo apt-get install curl libssl-dev libcurl4-openssl-dev libjpeg-dev libx264-142 libavcodec56 libavformat56 libmysqlclient18 libswscale3 libpq5

```

Install Motion

```

wget https://github.com/Motion-Project/motion/releases/download/release-4.0.1/pi_jessie_motion_4.0.1-1_armhf.deb
sudo dpkg -i pi_jessie_motion_4.0.1-1_armhf.deb

```

Make a directory to save videos, images and scripts.

```

sudo mkdir /mnt/motionvideos

```

Copy all the scripts from my repo to this folder.

```

sudo cp -R /home/pi/Desktop/SpiCam/*.py /mnt/motionvideos

```

Delete the existing motion.conf file and replace it with my motion.conf

```

sudo rm -r /etc/motion/motion.conf
sudo cp -R /home/pi/Desktop/SpiCam/motion.conf /etc/motion/

```

Edit ___image.py___ 

```

sudo nano /mnt/motionvideos/image.py

```
replace MAIL with your Gmail account PASSWORD with your password and CAMERA_ACCOUNT with the recipient email address.

```python

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
    sender = 'MAIL'
    gmail_password = 'PASSWORD'
    recipients = ['CAMERA_ACCOUNT']
    f_time = datetime.datetime.now().strftime('%a %d %b %H:%M')
    subject = 'Photo @' + f_time
    # Create the enclosing (outer) message
    outer = MIMEMultipart()
    outer['Subject'] = subject
    outer['To'] = COMMASPACE.join(recipients)
    outer['From'] = sender
    outer.preamble = 'Photo' + f_time

    # List of attachments
    filejatin = '/mnt/motionvideos/' + datetime.datetime.now().strftime('%Y%m%d%H%M.jpg')
    filejatin2 = '/mnt/motionvideos/' + ((datetime.datetime.now() - datetime.timedelta(minutes = 1)).strftime('%Y%m%d%H%M.jpg'))
    attachments = [filejatin, filejatin2]
    deletepath = 'sudo rm -r ' + filejatin
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
   

    try:
        os.remove(filejatin)
    except:
        os.remove(filejatin2)
    

if __name__ == '__main__':
    main()
    
```

Edit ___timelapse.py___ similarly.

```

sudo nano /mnt/motionvideos/timelapse.py


```
Replace youremail, pass, cameraemail.

```python
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


```

Edit ___vid.py___

```
sudo nano /mnt/motionvideos/vid.py

```
Replace the pass, cameraemail and email

```python

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
    sender = 'email'
    gmail_password = 'pass'
    recipients = ['cameraemail']
    f_time = datetime.datetime.now().strftime('%a %d %b @ %H:%M')
    subject = 'Video @' + f_time
    # Create the enclosing (outer) message
    outer = MIMEMultipart()
    outer['Subject'] = subject
    outer['To'] = COMMASPACE.join(recipients)
    outer['From'] = sender
    outer.preamble = ''

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


```

You need to make use of an API called as Pushetta to send you notifications to your mobile
Go to <https://www.pushetta.com> and make your Account, and Channel.

Make sure to Copy the Api Key in a safe place, and also remember your channel name.

Now install Pushetta on your Pi.

```

pip install pushetta


```

Edit ___notif.py___

```

sudo nano /mnt/motionvideos/notif.py


```

Replace apikey with your API KEY and channel with your Channel name.

```

import os
from pushetta import Pushetta
API_KEY="apikey"
CHANNEL_NAME="channel"
p=Pushetta(API_KEY)
p.pushMessage(CHANNEL_NAME, "Someone is at your DOOR !")

```

You are all setup now!

Fire up the camera by entering the following command.


```

sudo motion /etc/motion/motion.conf

```

Stop the camera by entering the following command.


```

sudo service motion stop

```

Enter the ip-address of your Pi followed by :8081 to see a live stream of your camera.

If you are not able to see a preview edit the modules file

```

sudo nano /etc/modules

```

Add this file to the end of the modules file.

```

bcm2835-v4l2


```

Now reboot your Pi

```

sudo reboot

```

Repeat the above steps with and you should be able to see a live stream.

Now test the camera by pointing it at a stable location, and walk in front of it.

It should send you an email and a notification.


## Tests

Edit ___motion.conf___ file to suit your needs if you want. The file is quite large but everything is well documented so you should have no problem to understand any of the properties.

```

sudo nano /etc/motion/motion.conf

```



