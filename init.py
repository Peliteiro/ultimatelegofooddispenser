import smtplib
import os
import zipfile
import time
import RPi.GPIO as GPIO
import picamera

from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.MIMEBase import MIMEBase
from email import encoders
from pathlib import Path
from datetime import datetime
from picamera import PiCamera




def main():
	now= datetime.now()
	currentHour = now.hour
	currentMinute = now.minute
	print "The time is "+str(currentHour)+ ":"+str(currentMinute)

	while True:
		
		led_verde()
		
		now = datetime.now()
		minute = now.minute
		hour = now.hour
		
		print "Alarme a Tocar."
		os.system("beep -f 555 -l 460")
		print "Alarme Tocou."
		
		ligar_motor()
		
		time.sleep(2)
		
		num_fotos=take_photos()
	
		make_video()
	
		send_email('/home/pi/Desktop/animation.mp4')
		
		led_vermelho()
			
        
def take_photos():
	print "A tirar Fotos."
	x = 0
	cycle= True
	camera = PiCamera()
	camera.rotation = 0
	camera.start_preview()

	
	while cycle:
		x += 1
		path= "/home/pi/Desktop/Fotos/NovaImg" + str(x) +".jpg"
		camera.capture(path)
		if x == 120:
			break
		camera.stop_preview()

	return x
	
	
	
def send_email(filename):
	
	print "A enviar email..."
	
	fromaddr = "unijunior182@gmail.com"
	toaddr = "unijunior182@gmail.com"

	msg =MIMEMultipart()

	msg['From'] = fromaddr
	msg['To'] = toaddr
	msg['Subject'] = "Video stop motion"

	body = "VIDEO ANIMAL"

	msg.attach(MIMEText(body,'plain'))

	attachment = open("/home/pi/Desktop/animation.mp4", "rb")

	part = MIMEBase('application', 'octet-stream')
	part.set_payload((attachment).read())
	encoders.encode_base64(part)
	part.add_header('Content-Disposition', "attachment; filename= %s" % filename)

	msg.attach(part)

	server = smtplib.SMTP_SSL('smtp.gmail.com',465)

	server.login(fromaddr, "182unijunior")
	text = msg.as_string()
	server.sendmail(fromaddr, toaddr, text)
	server.quit()
	
	print "Email enviado."



with picamera.PiCamera() as camera:
	 camera.resolution = (1280,720)
	 camera.capture("/home/pi/Desktop/Fotos/NovaImg.jpg")




def make_video():
	print "A fazer video."
	my_path = Path("/home/pi/Desktop/animation.mp4")
	if my_path.exists():
		os.remove("/home/pi/Desktop/animation.mp4")
	
	os.system("avconv -r 4 -i Fotos/NovaImg%d.jpg -qscale 5  animation.mp4")
	return "Video criado."
	print "Video criado."



def ligar_motor():
    print "O motor ligou."
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(7,GPIO.OUT)
    p=GPIO.PWM(7,50)
    p.start(7.5)
    try:

            p.ChangeDutyCycle(12.5)
            time.sleep(1)
            p.ChangeDutyCycle(2.5)
            time.sleep(1)
    except KeyboardInterrupt:
            p.stop()
            GPIO.cleanup()
	
	
    
def led_vermelho():
	GPIO.setmode(GPIO.BOARD)
	GPIO.setwarnings(False)
	GPIO.setup(11,GPIO.OUT)
	print "LED VERMELHO ON"
	GPIO.output(11,GPIO.HIGH)
	time.sleep(10)
	GPIO.output(11,GPIO.LOW)
	
	

def led_verde():
	GPIO.setmode(GPIO.BOARD)
	GPIO.setwarnings(False)
	GPIO.setup(13,GPIO.OUT)
	print "LED VERDE ON"
	GPIO.output(13,GPIO.HIGH)
	time.sleep(3)
	GPIO.output(13,GPIO.LOW)


if __name__ == '__main__':
    main()
    

    
    


       








