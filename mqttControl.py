import paho.mqtt.client as mqtt
import trackingLogic as logic
import json
import time
import subprocess
import os
import signal
import sys
import argparse
process_str='raspivid -t 0 -cd MJPEG -w 640 -h 480'
process_str+=' -fps 40 -b 8000000 -o - | gst-launch-1.0 fdsrc !'
process_str+=' "image/jpeg,framerate=40/1" ! jpegparse ! rtpjpegpay !'
process_str+=' udpsink ' #host=192.168.41.3 port=4001'

topic='rpi/#'
ip='172.20.5.22'
port='1883'
gport='4001'
logic=logic.Logic()
def parse_args():
	parser = argparse.ArgumentParser()
	parser.add_argument('-H', dest="host",help="ip adress")
	parser.add_argument('-mp', dest="mp",help="mqtt port")
	parser.add_argument('-gp', dest="gp",help="gstreamer port")
	results=parser.parse_args()
	global process_str,ip,port,gport
	if results.host:
		ip=results.host
	if results.mp:
		port=results.mp
	if results.gp:
		gport=results.gp
	process_str+='host={} port={}'.format(ip,gport)
	
def on_connect(client, userdata, flags, rc):
	print("Connected with result code "+str(rc))
	client.subscribe(topic)
def on_message(client, userdata, msg):
	if msg.topic=='rpi/motors':
		handleMotors(str(msg.payload))
	elif msg.topic=='rpi/camera':
		handleCamera(str(msg.payload))
	elif msg.topic=='rpi/object_tracking':
		handleObjectTracking(str(msg.payload))
	else:
	    	print(msg.topic+" "+str(msg.payload))
def handleMotors(msg):
	if msg=='forward':
		logic.robot.goForward()
	elif msg=='backward':
		logic.robot.goBackward()
	elif msg=='left':
		logic.robot.goLeft()
	elif msg=='right':
		logic.robot.goRight()
	else:
		logic.robot.stop()
		
def handleCamera(msg):
	if msg=='up':
                logic.robot.servoUD.move(20)
        elif msg=='down':
                logic.robot.servoUD.move(-20)
        elif msg=='left':
                logic.robot.servoLR.move(-20)
        elif msg=='right':
                logic.robot.servoLR.move(20)
        else:
                logic.robot.servoUD.stop()
		logic.robot.servoLR.stop()
def handleObjectTracking(msg):
#	time.sleep(0.01)
	data=json.loads(msg.decode())
        x_offset=data.get("xoff")
	radius=data.get("radius")
        y_offset=data.get("yoff")
        print(x_offset,y_offset,radius)
        logic.handleV2(x_offset,y_offset,radius)

if __name__=='__main__':	
	parse_args()
	sp=subprocess.Popen(process_str,shell=True, preexec_fn=os.setsid)
	client=mqtt.Client("rpi_control")
	client.on_connect = on_connect
	client.on_message = on_message
	print('Trying to connect to mqtt broker')
	print(ip)
	client.connect(ip,port,3600)
	client.loop_start()
	print("Done")
	try:
		while True:
			pass
	except KeyboardInterrupt:
        	os.killpg(sp.pid, signal.SIGTERM)
        	print("Camera killed")
		client.loop_stop()
        	sys.exit()
