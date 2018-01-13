import paho.mqtt.client as mqtt
from multiprocessing import Process
import time;
import datetime 
import runpy
from random import randint
from flask import Flask, request, render_template
#from flask_socketio import SocketIO, emit

app = Flask(__name__)
#socketio = SocketIO(app)
S_mqtt = ""
def on_connect(client, userdata,flags , rc):
	print("Connected with result code "+str(rc))    # Subscribing in on_connect() means that if we lose the$
        client.subscribe("/esp/pot")
	client.subscribe("/esp/hum_1") # remember this topic to put inside ESP code later
	client.subscribe("/esp/temp_1")
	client.subscribe("/esp/hum_2") # remember this topic to put inside ESP c$
        client.subscribe("/esp/temp_2")
# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, ms):
	if ms.topic == "/esp/pot":
#        	socketio.emit('Smqtt', {'data' :ms.payload})
		Smqtt=str(ms.payload)
	if ms.topic == "/esp/hum_1":
#               socketio.emit('Smqtt', {'data' :ms.payload})
                hum1=str(ms.payload)
	if ms.topic == "/esp/temp_1":
#               socketio.emit('Smqtt', {'data' :ms.payload})
                temp1=str(ms.payload)
	if ms.topic == "/esp/hum_2":
#               socketio.emit('Smqtt', {'data' :ms.payload})
                hum2=str(ms.payload)
	if ms.topic == "/esp/temp_2":
#               socketio.emit('Smqtt', {'data' :ms.payload})
                temp2=str(ms.payload)
	global Smqtt
	global hum1
	global temp1
	global hum2
        global temp2


mqttc=mqtt.Client()
mqttc.loop_start()
mqttc.on_connect = on_connect
mqttc.on_message = on_message
mqttc.connect("localhost",1883,60)


time_H=int(time.strftime("%H"))
time_M=int(time.strftime("%M"))
vak =[[400,18,1],[350,18,1],[600,18,2]] 

@app.route('/select_mode')
def mode():
	    if 'mode' in request.args:
		mode = request.args.get('mode')
		#runpy.run_path("test.py")
		auto(vak[int(mode)][0],vak[mode][1],vak[mode][2])
		return render_template('index.html')
   	    else:
		return "EXIT"

@app.route('/select_vak')
def vak_mode():
            if 'vak_mode' in request.args:
                vak_mode = request.args.get('vak_mode')
#		if vak_mode = "1":
#			if S_mqtt
		auto(vak[int(vak_mode)][0],vak[int(vak_mode)][1],vak[int(vak_mode)][2])
                return render_template('index.html')
            else:
                return "EXIT"

def auto(Soil,Time_ST,Time_Sum):
	print Soil
	print Time_ST
	print Time_Sum
	St_water = 1
	mqttc.publish("water",1)
#	while True:
	print Smqtt
	print Soil
	if Soil > int(Smqtt)+100 and St_water == 0:
		print St_water
		print Soil,">",int(Smqtt)
		St_water = 1
		mqttc.publish("water",1)
		print "++++++++ ON 1 +++++++"
	elif Soil < int(Smqtt) and St_water == 1:
		St_water = 0
		mqttc.publish("water",0)
		print "--------- OFF 1 ---------"
	elif Time_ST <= int(time.strftime("%H")) < Time_ST+Time_Sum and St_water == 0:
		print St_water
		st_water = 1
		mqttc.publish("water",1)
		print "+++++ ON 2 +++++"
	else:
		mqttc.publish("water",1)
		print "else caes"
#def setTime():
#def user():

#WEB
@app.route('/')
def index():
    return render_template('index.html')

#PRINT VL ON NEWPAGE
@app.route('/Time_Set')
def testGetStringQuery():
    if 'Time_Start' in request.args:
        Time_Start = request.args.get('Time_Start')
     	Time_End = request.args.get('Time_End')
        print Time_Start
	while True :
		TimeInt_Hs = int(Time_Start[0]+Time_Start[1])
		TimeInt_Ms = int(Time_Start[3]+Time_Start[4])
		TimeInt_He = int(Time_End[0]+Time_End[1])
        	TimeInt_Me = int(Time_End[3]+Time_End[4])
		TimeH_Set = int(time.strftime("%H"))
		TimeM_Set = int(time.strftime("%M"))
		print 'Time',TimeInt_Hs,':',TimeInt_Ms,TimeInt_He,':',TimeInt_Me
		print 'Time Now',TimeH_Set,':',TimeM_Set	
#		mqttc.publish("water",1)
#		mqttc.publish("water",0)
 		if TimeInt_Hs <= TimeInt_He:
    			if TimeInt_Hs == TimeInt_He:
        			if TimeInt_Ms < TimeInt_Me:
            				if TimeInt_Ms < TimeM_Set and TimeInt_Me > TimeM_Set:
                				mqttc.publish("water",1)
						print "++++++ON1+++++++"
            				else:
						mqttc.publish("water",0)
               	 				print "-----OFF1-----"
        			else:
            				if TimeInt_Me <= TimeM_Set and TimeInt_Ms >= TimeM_Set:
                				mqttc.publish("water",0)
						print "+++++++++OFF2 ++++++++"
            				else:
                    				mqttc.publish("water",1)
						print "--------ON2--------"
    			elif TimeInt_Hs < TimeInt_He:
        			if TimeInt_Hs == TimeH_Set:
            				if TimeInt_Ms < TimeM_Set:
						mqttc.publish("water",1)
                				print "++++++ ON3 +++++"
            				else:
						mqttc.publish("water",0)
              					print "------ OFF3 ------"
        			elif TimeInt_Hs < TimeH_Set and TimeH_Set < TimeInt_He:
              				mqttc.publish("water",1)
					print "++++++++ ON4 ++++++++"
        			else:
					mqttc.publish("water",0)
              				print "------- OFF4 --------"
    			else:
       	 			printf("last")
		else:
    			print "Burn"
#		return render_template('index.html')
    else:
        return "No username argument found."
S_tus = "Burn"

@app.route('/manual_Set')
def man_mode():
            if 'water1_ON' in request.args:
                water1 = request.args.get('water1_ON')
		water2 = request.args.get('water1_OFF')
                #runpy.run_path("test.py")
                mqttc.publish("water",1)
		S_tus = water1
		print water1
                return render_template('index.html')
	    elif 'water1_OFF' in request.args:
		water1 = request.args.get('water1_ON')
		water2 = request.args.get('water1_OFF')
		mqttc.publish("water",0)
		print water2
		S_tus = water2
		return render_template('index.html')
            else:
                return "EXIT"

#SHOW ON WEB
@app.route('/status')
def status():
    return S_tus

@app.route('/show')
def test():
    return Smqtt

@app.route('/hum_1')
def dht_hum1():
	return hum1

@app.route('/temp_1')
def dht_temp1():
        return temp1

@app.route('/hum_2')
def dht_hum2():
        return hum2

@app.route('/temp_2')
def dht_temp2():
        return temp2



@app.route('/time')
def timeTest():
        return str(time.strftime("%H:%M:%S"))

if __name__ == '__main__':
	print S_mqtt,"BUrn"
#	print datetime.datetime.now()
	app.run(debug=True, host='0.0.0.0', port=8181)

mqttc.loop_forever()
 
