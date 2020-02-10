###############################################################################################################################################################
#####																SWL Library Complete 																  #####
###############################################################################################################################################################
"""
Exclusive Copyright (c) of Paul James Banahan, Sole Author and Sole Owner;
Paul James Banahan 2017-2019;
License:					None Allowable
Date of Origin:				8th March 2019;
Last Edited:				8th March 2019;
Purpose:					Library of the all complied and tested functions for the SparroWatch project
Project:					All python projects
"""

import numpy 																as np 
from termcolor 								import colored 					as co
from mvnc 									import mvncapi 					as mvnc 					
from datetime 								import datetime 				as dt
from datetime 								import time 					as TT
from datetime 								import timedelta
from os.path 								import basename 						
from email.mime.application 				import MIMEApplication
from email.mime.multipart 					import MIMEMultipart
from email.mime.text 						import MIMEText
from email.utils 							import COMMASPACE, formatdate
from threading 								import Thread, Event, Timer , Lock
from imutils.video 							import VideoStream
from imutils.video 							import FPS
import sqlite3
import time
import cv2   										
import os 											
#import sys 											
import imutils
import traceback
#import base64
import json
import re, commands 								
import httplib 										
#import subprocess 									
#import zipfile
import glob
import smtplib
#import uuid
import shutil				

#try:
#	import RPi.#GPIO as #GPIO
#	#GPIO.setmode(#GPIO.BCM)
#except RuntimeError:
#	print(co("Cant imort RPi.#GPIO", 'cyan'    , attrs=[ 'bold']))
#	pass


"""
Library of Functions developed, compiled and tested with while working at SparroWatch
"""

#######################################################
##  Examples of Running each of the below functions  ##
#######################################################
global term_color_error
term_color_error = 'cyan'
# 

#######################################
## The Main function for the program ##
#######################################
## STATUS: 	Complete
def main():
	print(co(" Library Compiled without Error ", 'cyan'))	## Prints output if build is successful


#############################################################
## CLASS FOR THE CAPTURING OF A BASELINE FRAME FROM CAMERA ##
#############################################################
## STATUS: 	Complete
####################################################
#########			DOCUMENTATION   		########
####################################################


####################################################
######## 		  IMPLEMENTATION 	 		########
####################################################
class Baseline():
	def __init__(self):
		pass
		#self.vs_b = VideoStream(usePiCamera=-1> 0).start()
		
	@staticmethod
	def Capture_Frame(self, Folder, DISPLAY_DIMS=(1280,720)):
		vs_b = VideoStream(usePiCamera=-1> 0).start()
		#Frame_Location = None
		if DISPLAY_DIMS == None:
			DISPLAY_DIMS = (1280,720)

		font 					= cv2.FONT_HERSHEY_DUPLEX
		bottomLeftCornerOfText	= (20,((DISPLAY_DIMS[1])-5))
		fontScale 				= 1
		fontColor 				= (255,255,255)
		lineType 				= 2
		x1 						= 0
		y1 						= (DISPLAY_DIMS[1] - 50)
		x2 						= DISPLAY_DIMS[0]
		y2						= DISPLAY_DIMS[1]
		alpha 					= 0.8

		try:
			print(co("[INFO] Taking a baseline photo of the area now", 'cyan', attrs=['bold']))
			Start_Up_Frame = vs_b.read()
			if Start_Up_Frame is None:
				print(co("[ERROR] Reading Frame in Baseline_Frame Function", 'cyan', attrs = ['bold']))
				quit()
			Start_Up_Frame = cv2.resize(Start_Up_Frame, DISPLAY_DIMS)
			Start_Time = dt.now()
			num = int(Start_Time.month)
			#Month_Name = str(self.Name_Of_Month(num))
			Start_Time_Now = ("{:02d}-{}-{:4d} --- {:02d}:{:02d}:{:02d}:{}" . format(Start_Time.day, Start_Time.month , Start_Time.year, Start_Time.hour, Start_Time.minute, Start_Time.second, Start_Time.microsecond))
			Start_Up_Frame = cv2.rectangle( Start_Up_Frame, (x1,y1), (x2,y2), (0,0,0), -1)
			Start_Up_Frame = cv2.putText( Start_Up_Frame, Start_Time_Now, bottomLeftCornerOfText, font, fontScale, fontColor, lineType)
			Start_Time_Now = str(time.strftime("%d %B %Y -- %H %M %S.{:4d}". format(Start_Time.microsecond)))
			Start_Up_Image_Name = ('Baseline_Image_From ' + Start_Time_Now + '.jpg')
			Frame_Name = str(Start_Up_Image_Name)
			#print(Folder)
			Frame_Location = str(Folder) + "/" + Frame_Name
			cv2.imwrite(Frame_Location, Start_Up_Frame)
			print(co(Frame_Location,'magenta',attrs=['reverse','bold']))
		except Exception as error:
			print(co("[FAILURE] Issue reading the frame -- Error Code {}". format(error),'cyan',attrs=['reverse','bold']))
			#GPIO.output(Red_LED,	 False) 
			#GPIO.output(Green_LED,	 False) 
			#GPIO.output(Yellow_LED,	 True) 
			time.sleep(0.5)
			quit()
		vs_b.stop()

		return Frame_Location

	def Name_Of_Month(self, number):
		if number == 1:
			month = "January"
		elif number == 2:
			month = "February"
		elif number == 3:
			month = "March"
		elif number == 4:
			month = "April"
		elif number == 5:
			month = "May"
		elif number == 6:
			month = "June"
		elif number == 7:
			month = "July"
		elif number == 8:
			month = "August"
		elif number == 9:
			month = "September"
		elif number == 10:
			month = "October"
		elif number == 11:
			month = "November"
		elif number == 12:
			month = "December"
		return month

######################################################################
## CLASS FOR THE EMAILLING OF NOTIFICATIONS AND ALERTS TO END USERS ##
######################################################################
## STATUS: 	Incomplete; Requires more time to write the internal function to check connection and send email
####################################################
#########			DOCUMENTATION   		########
####################################################

####################################################
######## 		  IMPLEMENTATION 	 		########
####################################################

class Emailling_Users():
	def __init__(self):
		pass

	def Detect_Internet_Connection(self):
		conn = httplib.HTTPConnection("www.google.ie", timeout=0.125)
		Error = None
		try:
			while True:
				conn.request("HEAD", "/")
				conn.close()
				Status = True
				Error = None
				break
		except Exception as error_1:
			print(co("Exception to Email!: {}" . format(error_1), term_color_error, attrs=['bold']))
			conn.close()
			Status = False
			Error = error_1
		return Status, Error

	def Email_User_Notification(self):
		pass		

	def Send_Alert_Email(self, End_User_Email, Frame_Path, Frame_Count, Person_Countr, Device_ID):
		gmail_user      = 'Sparrowatch.alert@gmail.com'
		gmail_password  = "Sparrow2017"
		to              = End_User_Email
		to              = ' , '.join(to)
		to              = str(to)
		subject         = 'Security Alert!!'
		body            = 'Something Detected by SparroWatch'
		email_text = ("""\
		Device ID:          %s
		Subject:            %s
		Information:        %s
		Total Frames Captured 		%s
		Person Estimated to be in the Space:	%s
		""" %(Device_ID, subject, body, str(Frame_Count), str(Person_Countr)))

		msg = MIMEMultipart()
		msg["From"] = gmail_user
		msg["To"] = to
		msg["Date"] = formatdate(localtime=True)
		msg["Subject"] = subject
		msg.attach(MIMEText(email_text))
		files = glob.glob(Frame_Path)
		for f in files:
			with open(f, "rb") as fil:
				part = MIMEApplication(        fil.read(),        Name=basename(f))
				part['Content-Disposition'] = 'attachment; filename="%s"' % basename(f)
				msg.attach(part)
		try:
			server = smtplib.SMTP_SSL('smtp.gmail.com',465)
			server.ehlo()
			server.login(gmail_user, gmail_password)
			server.sendmail(gmail_user, to, msg.as_string())
			server.quit()
		except Exception as error:
			print(co("[FAILURE] Could not send email -- Error Code {}". format(error),'cyan',attrs=['reverse','bold']))
		return

####################################################
## Class for the use of the Event Table in the DB ##
####################################################
## STATUS: 	Complete
####################################################
#########			DOCUMENTATION   		########
####################################################
##### __init__
# Input Value:		db:		The database that the function will utislses for data storage
#					table:	The table that the class will be associated and working  with
# Returned Value:	None
##### Create_Event
# Input Value:		TableName:			The name of the table data will be entered into ----- REDUNDANT, can be removed for self.table
# Returned Value:	None
##### Event_Logger

##### Measure_Temperature_Event
## Input Value:		None
## Returned Value:	temperature:	The temperature value of the CPU of the Raspberry Pi
#####Name_Of_Month
# Input Value:		number:		Integer passed in taken from the dt.now.month() function
# Returned Value:	STRING:		The Name of the Month corresponding to the value passed in
##### Update_Event
# Input Value:		TableName:				
#					Time_Of_Event:			The time the event occured at
#					Event_Trigger_Type:		The Type of Event that triggered the recording
#					CPU_Temperature:		The CPU Temperature of the raspberry Pi at the time of the event
#					Email_Details:			The details around the device sending emails to the end user
#					FOIC:					The Frame Of Interest Count, how many frames have been captured thus far
#					Frame_Location:			The location of the frame captured for the given event
# Returned Value:	None
####################################################
######## 		  IMPLEMENTATION 	 		########
####################################################
# Ev_DB = Event_DB(database, table_name)								 # db, table 
# Ev_DB.Create_Event(table_name)										 # Table_name
# Ev_DB.Event_Logger('Person', 'Email Details', 33, 'Somewhere') # Event_Trigger_Type, Email_Details, FOIC, Frame_Location,CPU_Temperature
class Event_DB():

	def __init__(self, db, table ):
		self.db 			= db
		self.table 			= table
		self.connection 	= sqlite3.connect(db + '.db', check_same_thread = False)
		self.cursor 		= self.connection.cursor()

	def Create_Event(self, Table_name):
		dbcommand = ('    CREATE TABLE IF NOT EXISTS "{tn}"( DB_Index INTEGER PRIMARY KEY, Time_Of_Event VARCHAR(100), Event_Trigger_Type VARCHAR(50), CPU_Temperature CHAR(10), Email_Details VARCHAR(100), FOIC INTEGER , Frame_Location VARCHAR(50) );'. format(tn=Table_name))
		try:
			self.cursor.execute(dbcommand)
		except OperationalError as DB_Error:
			print(co("Database OperationalError -- Event_DB: {}" . format(DB_Error), 'red', attrs=['bold', 'reverse']))
			self.connection.rollback()
		except Exception as Gen_Error:
			print(co("Database Exception -- Event_DB: {}" . format(Gen_Error), 'red', attrs=['bold', 'reverse']))
			self.connection.rollback()

	def Close(self):
		self.connection.close()

	def Event_Logger(self, Event_Trigger_Type, Email_Details, FOIC, Frame_Location):
		try:
			CPU_Temperature  = self.Measure_Temperature_Event()
			E_N = dt.now()
			Month_Name = self.Name_Of_Month(E_N.month)
			Event_Time = ("{:2d}-{}-{:4d} --- {:2d}:{:2d}:{:2d}:{}" .format(E_N.day, Month_Name, E_N.year, E_N.hour, E_N.minute, E_N.second, E_N.microsecond))
			self.Update_Event(self.table, Event_Time, Event_Trigger_Type, CPU_Temperature, Email_Details, FOIC, Frame_Location)
		except Exception as error:
			print(co("Exception to Event_DB Logger!: {}" . format(error)	,'cyan',attrs=['reverse','bold']))
			print(co(traceback.print_exc()									,'cyan', attrs=['reverse','bold']))
			print(co(""))

	def Measure_Temperature_Event(self):
		temperature = None
		err, msg = commands.getstatusoutput('vcgencmd measure_temp')
		if not err:
			m = re.search(r'-?\d\.?\d*', msg)
			try:
				temperature = float(m.group())
			except:
				pass
		return temperature

	def Name_Of_Month(self, number):
		if number == 1:
			return "January"
		elif number == 2:
			return "February"
		elif number == 3:
			return "March"
		elif number == 4:
			return "April"
		elif number == 5:
			return "May"
		elif number == 6:
			return "June"
		elif number == 7:
			return "July"
		elif number == 8:
			return "August"
		elif number == 9:
			return "September"
		elif number == 10:
			return "October"
		elif number == 11:
			return "November"
		elif number == 12:
			return "December"

	def Update_Event(self, TableName, Time_Of_Event, Event_Trigger_Type, CPU_Temperature, Email_Details, FOIC, Frame_Location):
		information =( Time_Of_Event, Event_Trigger_Type, CPU_Temperature, Email_Details, FOIC, Frame_Location)
		dbcommand = ('INSERT INTO "{tn}" VALUES (NULL, ?, ?, ?, ?, ?, ? );' . format(tn=TableName))
		try:
			self.cursor.execute(dbcommand, information)
			self.connection.commit()
		except Exception as Gen_Error:
			print(co("Database Exception -- Update_Event: {}" . format(Gen_Error), 'red', attrs=['bold', 'reverse']))
			self.connection.rollback()

########################################################
## Class for the use of the Heartbeat Table in the DB ##
########################################################
## STATUS: 	Complete
## Implementation:	
# Hb_DB = Heart_DB(database, table_name_Heart)						 # db, table 
# Hb_DB.Create_Heart(table_name_Heart)								 # Table_name
# HEARTBEAT = Hb_DB.Heart_Logger()
####################################################
#########			DOCUMENTATION   		########
####################################################
##### __init__
# Input Value:		db:		The database that the function will utislses for data storage
#					table:	The table that the class will be associated and working  with
# Returned Value:	None
##### Create_Heart
# Input Value:		TableName:			The name of the table data will be entered into ----- REDUNDANT, can be removed for self.table
# Returned Value:	None
##### Measure_Temperature_Heartbeat
# Input Value:		None
# Returned Value:	temperature:	The temperature value of the CPU of the Raspberry Pi
##### Name_Of_Month
# Input Value:		number:		Integer passed in taken from the dt.now.month() function
# Returned Value:	STRING:		The Name of the Month corresponding to the value passed in
##### Update_Heart
# Input Value:		TableName:			The name of the table data will be entered into ----- REDUNDANT, can be removed for self.table
#					Heartbeat_Time:		The UTC time of the heartbeat
#					CPU_Temperature:	The core temperature of the CPU of the Raspberry Pi, will be null on other platforms
#					Message:			JSONified packet of data. Contents above
# Returned Value:	None
####################################################
######## 		  IMPLEMENTATION 	 		########
####################################################
# Hb_DB = Heart_DB(database, table_name_Heart)						 # db, table 
# Hb_DB.Create_Heart(table_name_Heart)								 # Table_name
# Hb_DB.Heart_Logger()
# Hb_DB.Close_HB_DB()
class Heart_DB():

	def __init__(self, db, table ):
		self.db 			= db
		self.table 			= table
		self.connection 	= sqlite3.connect(db + '.db', check_same_thread = False)
		self.cursor 		= self.connection.cursor()

	def Create_Heart(self, Table_name):
		dbcommand = ('  CREATE TABLE IF NOT EXISTS "{tn}"( DB_Index INTEGER PRIMARY KEY, HeartbeatTime VARCHAR(20), CPU_Temperature CHAR(15), Message CHAR(30));'. format(tn=Table_name))
		try:
			self.cursor.execute(dbcommand)
		except OperationalError as DB_Error:
			print(co("Database OperationalError -- Heart_DB: {}" . format(DB_Error), 'red', attrs=['bold', 'reverse']))
			self.connection.rollback()
		except Exception as Gen_Error:
			print(co("Database Exception Create_Heart -- Heart_DB: {}" . format(Gen_Error), 'red', attrs=['bold', 'reverse']))
			self.connection.rollback()

	def Close(self):
		self.connection.close()

	def Heart_Logger(self):
		try:
			Hb_T = dt.today()
			Month_Name = self.Name_Of_Month(Hb_T.month)
			Heartbeat_Time = ("{:02d}-{:02d}-{:02d}---{:02d}:{}:{}" . format(Hb_T.hour, Hb_T.minute, Hb_T.second, Hb_T.day, Month_Name, Hb_T.year ))
			CPU_Temperature = self.Measure_Temperature_Heartbeat()
			Message_1   = {'HeartbeatData':[{"TimeOfBeat":Heartbeat_Time, "DeviceCoreTemperature":CPU_Temperature, }]}
			Message     = json.dumps(Message_1, indent = 3)
			event_name  = 'Heartbeat Data'
			event_data  = Message
			self.Update_Heart(self.table, Heartbeat_Time, CPU_Temperature, Message)
		except Exception as error:
			print(co("Exception to Heart_Logger -- Heart_DB: {}".format(error)		,'cyan',attrs=['reverse','bold']))
			print(co("																							"))
			print(co(traceback.print_exc()))

	def Measure_Temperature_Heartbeat(self):
		temperature = None
		err, msg = commands.getstatusoutput('vcgencmd measure_temp')
		if not err:
			m = re.search(r'-?\d\.?\d*', msg)
			try:
				temperature = float(m.group())
			except:
				pass
		return temperature

	def Name_Of_Month(self, number):
		if number == 1:
			return "January"
		elif number == 2:
			return "February"
		elif number == 3:
			return "March"
		elif number == 4:
			return "April"
		elif number == 5:
			return "May"
		elif number == 6:
			return "June"
		elif number == 7:
			return "July"
		elif number == 8:
			return "August"
		elif number == 9:
			return "September"
		elif number == 10:
			return "October"
		elif number == 11:
			return "November"
		elif number == 12:
			return "December"

	def Update_Heart(self, TableName, Heartbeat_Time, CPU_Temperature, Message):
		information =( Heartbeat_Time, CPU_Temperature, Message)
		dbcommand = ('INSERT INTO "{tn}"  VALUES (NULL, ?, ?, ?);' . format(tn=TableName))
		try:
			self.cursor.execute(dbcommand, information)
			self.connection.commit()
		except Exception as Gen_Error:
			print(co("Database Exception Update_Heart -- Heart_DB: {}" . format(Gen_Error), 'red', attrs=['bold', 'reverse']))
			self.connection.rollback()

######################################################
## CLASS FOR THE DRAWING AND MANIPLUATION OF FRAMES ##
######################################################
## STATUS: 	Complete
####################################################
#########			DOCUMENTATION   		########
####################################################
##### labelMaker
# Input Value:		frame:				The frame that all operations will be performed on
#					DISPLAY_DIMS:		The dimensions of the frame
# Returned Value:	image_with_Details	The frame with the details and operations completed
##### Name_Of_Month
# Input Value:		number:		Integer passed in taken from the dt.now.month() function
# Returned Value:	STRING:		The Name of the Month corresponding to the value passed in
####################################################
######## 		  IMPLEMENTATION 	 		########
####################################################
class Images():
	def __init__(self):
		pass

	def LabelMaker(self,frame, DISPLAY_DIMS=(1280,720)):
		## Values are set for images of size: [1280,720]
		font 					= cv2.FONT_HERSHEY_DUPLEX
		bottomLeftCornerOfText	= (20,((DISPLAY_DIMS[1])-5))
		fontScale 				= 1
		fontColor 				= (255,255,255)
		lineType 				= 2
	
		x1 						= 0
		x2 						= DISPLAY_DIMS[0]
		
		y1 						= (DISPLAY_DIMS[1] - 50)
		y2						= DISPLAY_DIMS[1]
		alpha 					= 0.75

		PT 						= dt.now() 
		Named_Month 			= self.Name_Of_Month(int(PT.month))
		Time_Now 				= ("{:02d}-{}-{} --- {:02d}:{:02d}:{:02d}" . format(PT.day, Named_Month, PT.year, PT.hour, PT.minute, PT.second))
		overlay 				= frame.copy()
		output  				= frame.copy()
		cv2.rectangle(overlay, (x1,y1), (x2,y2),	(0,0,0), -1)
		frame_NEW 				= cv2.addWeighted(overlay, alpha, output, (1 - alpha),		0, output)
		image_with_Details 		= cv2.putText( frame_NEW, Time_Now, bottomLeftCornerOfText, font, fontScale, fontColor, lineType)
		return image_with_Details  

	def Name_Of_Month(self, number):
		if number == 1:
			return "January"
		elif number == 2:
			return "February"
		elif number == 3:
			return "March"
		elif number == 4:
			return "April"
		elif number == 5:
			return "May"
		elif number == 6:
			return "June"
		elif number == 7:
			return "July"
		elif number == 8:
			return "August"
		elif number == 9:
			return "September"
		elif number == 10:
			return "October"
		elif number == 11:
			return "November"
		elif number == 12:
			return "December"

##############################################################################
##  CLASS FOR THE GATHERING OF PREDICTIOS FROM THE NSC1 THROUGH THE NCSDKv1 ##
##############################################################################
## STATUS: 	Complete, untested with NCSDKv1
####################################################
#########			DOCUMENTATION   		########
####################################################
##### predict
# Input Value:		image:			The image to be anaysised by the neural network
#					graph: 			The network that the image will be passed through
# Returned Value:	predictions:	Tuple with the predictions gathered
##### preprocessed_image
# Input Value:		input_image:		The image to be processed by the function
#					PREPROCESS_DIMS:	The dimensions the image is to be resized to; Default (300,300)
# Returned Value:	preprocessed:		The preocessed image
####################################################
######## 		  IMPLEMENTATION 	 		########
####################################################
class NCS():
	def __init__(self, graph_folder):
		### INIT of NCS may need to go here: will have to see
		# self.graph = 
		# 
		devices = mvnc.EnumerateDevices()
		if len(devices) == 0:
			print(co("[WARNING] No Neural devices found!",'cyan', attrs=[ 'bold']))
			#GPIO.output(Red_LED, False)
			#GPIO.output(Green_LED, False)
			#GPIO.output(Yellow_LED, True)
			time.sleep(2.5)
			#quit()
		device = mvnc.Device(devices[0])
		device.OpenDevice()
		with open(graph_folder + "/mobilenetgraph", mode="rb") as f:
			graph_in_memory = f.read()
		self.graph = device.AllocateGraph(graph_in_memory)

		pass

	def predict(self, image):
		## *** NO PRINT STATEMENTS IN THIS FUNCTION *** ##
		image = self.preprocess_image(image)
		self.graph.LoadTensor(image, None)
		(output, _) = self.graph.GetResult()
		num_valid_boxes = output[0]
		predictions = []
		for box_index in range(num_valid_boxes):
			base_index = 7 + box_index * 7
			if (not np.isfinite(output[base_index]) or
				not np.isfinite(output[base_index + 1]) or
				not np.isfinite(output[base_index + 2]) or
				not np.isfinite(output[base_index + 3]) or
				not np.isfinite(output[base_index + 4]) or
				not np.isfinite(output[base_index + 5]) or
				not np.isfinite(output[base_index + 6])):
				continue
			(h, w) = image.shape[:2]
			x1 = max(0, int(output[base_index + 3] * w))
			y1 = max(0, int(output[base_index + 4] * h))
			x2 = min(w, int(output[base_index + 5] * w))
			y2 = min(h, int(output[base_index + 6] * h))
			pred_class = int(output[base_index + 1])
			pred_conf = output[base_index + 2]
			pred_boxpts = ((x1, y1), (x2, y2))
			prediction = (pred_class, pred_conf, pred_boxpts)
			predictions.append(prediction)
		return predictions

	def preprocess_image(self, input_image, PREPROCESS_DIMS=(300,300)):
		## *** NO PRINT STATEMENTS IN THIS FUNCTION *** ##
		preprocessed = cv2.resize(input_image, PREPROCESS_DIMS)
		preprocessed = preprocessed - 127.5
		preprocessed = preprocessed * 0.007843
		preprocessed = preprocessed.astype(np.float16)
		return preprocessed

	def Close_NCS(self):
		self.graph.DeallocateGraph()
		self.device.CloseDevice()
###################################################################
## Threaded Timer Class for the Heartbeat function of the device ##
###################################################################
## STATUS: 	Complete
####################################################
#########			DOCUMENTATION   		########
####################################################

# Input Value:		None
# Returned Value:	Non
####################################################
######## 		  IMPLEMENTATION 	 		########
####################################################
# Repeat_Every_X_Seconds = 15
# t = perpetualTimer(Repeat_Every_X_Seconds, Hb_DB.Heart_Logger)
# t.start()
# print("[SLEEP] Proving the Timer Class works with the Heart_DB Class")
# time.sleep(15)
# print("[AWAKE] Proving the Timer Class works with the Heart_DB Class")
# t.Cancel()
class perpetualTimer():
	def __init__(self, t, hFunction):
		self.t = t
		self.hFunction = hFunction
		self.thread = Timer(self.t, self.handle_function)

	def Cancel(self):

		self.thread.cancel()

	def handle_function(self):
		self.hFunction()
		self.thread = Timer(self.t, self.handle_function)
		self.thread.start()

	def Start(self):

		self.thread.start()


###################################################################################################################################################################
################################################################## GENERAL FUNTION DEFINES ########################################################################
###################################################################################################################################################################

# A B C D E F G H I J K L M N O P Q R S T U V W X Y Z

##########################################################################
##  Checking if the current or declared time is between two other times ##
##########################################################################
## STATUS: 	Complete
####################################################
#########			DOCUMENTATION   		########
####################################################
# Input Value:		begin_time: 	The start of the time window to be checked
#					end_time:		The end of the time window to be checked
#					check_time: 	The time to check if it is inside or outside of the time window
# Returned Value:	check_time:		Boolean value of the time check; True = between the times; False = Outside of the two times
####################################################
######## 		  IMPLEMENTATION 	 		########
####################################################
# Time_Check = Check_if_time_between( TT(17,00,00), TT(08,00,00), dt.now())
def Check_if_time_between(begin_time, end_time, check_time=None):
	# If check time is not given, default to current UTC time
	check_time = check_time or dt.utcnow().time()
	if begin_time < end_time:
		return check_time >= begin_time and check_time <= end_time
	else: # crosses midnight
		return check_time >= begin_time or check_time <= end_time

#####################################################################
##  Ensuring whether the device can connect to the Internet or not ##
#####################################################################
## STATUS: 	Complete
####################################################
#########			DOCUMENTATION   		########
####################################################
# Input Value:		None
# Returned Value:	Status: The status of the interent connection 
#					Error:	An Error that occured, will be None if no error occured
####################################################
######## 		  IMPLEMENTATION 	 		########
####################################################	
# Connect_Status, Err = Check_Internet_Connection()
def Check_Internet_Connection():
		conn = httplib.HTTPConnection("www.google.ie", timeout=0.125)
		Err = None
		try:
			while True:
				conn.request("HEAD", "/")
				conn.close()
				Status = True
				Error = None
				break
		except Exception as Err:
			print(co("Exception to Email!: {}" . format(Err), term_color_error, attrs=['bold']))
			conn.close()
			Status = False
		return Status, Err

###################################################################################################
##  Removing Folders and their data should the folder be older then the specified number of days ##
###################################################################################################
## STATUS: 	Complete
####################################################
#########			DOCUMENTATION   		########
####################################################
# Input Value:		folderpath: 	Path to the folder being checked
#					Day_Cutoff:		Maximum age of the folders allowed; Baseline set to 30 days
# Returned Value:	None
####################################################
######## 		  IMPLEMENTATION 	 		########
####################################################
# FileRemover("/media/pi/", 30)
def FileRemover(folderpath, Day_Cutoff=30):
	Now = time.time()
	Day_Cutoff_in_Seconds = (Day_Cutoff*86400)
	directory=os.path.join(folderpath," ")
	for r,d,f in os.walk(folderpath):
		for dir in d:
			timestamp = os.path.getmtime(os.path.join(r,dir))
			if (Now - Day_Cutoff_in_Seconds) > timestamp:
				try:
					shutil.rmtree(os.path.join(r,dir))
				except Exception as Err:
					print(co("Exception to Email!: {}" . format(Err), term_color_error, attrs=['bold']))
					pass

########################################################################################
##  Converting the Integer value of the given month into the String name of the month ##
########################################################################################
## STATUS: 	Complete
####################################################
#########			DOCUMENTATION   		########
####################################################
# Input Value:		number:		Integer passed in taken from the dt.now.month() function
# Returned Value:	STRING:		The Name of the Month corresponding to the value passed in
####################################################
######## 		  IMPLEMENTATION 	 		########
####################################################	
# value = month(int)
def month(number):
	if number == 1:
		return "January"
	elif number == 2:
		return "February"
	elif number == 3:
		return "March"
	elif number == 4:
		return "April"
	elif number == 5:
		return "May"
	elif number == 6:
		return "June"
	elif number == 7:
		return "July"
	elif number == 8:
		return "August"
	elif number == 9:
		return "September"
	elif number == 10:
		return "October"
	elif number == 11:
		return "November"
	elif number == 12:
		return "December"

#########################################################
##  Reboot Light Configuration is set through the GPIO ##
#########################################################
## STATUS: Complete, but not used, alternative method used instead
####################################################
#########			DOCUMENTATION   		########
####################################################
# Input Value:		None
# Returned Value:	None
####################################################
######## 		  IMPLEMENTATION 	 		########
####################################################	
#GPIO.add_event_detect(User_Switch_Restart , #GPIO.FALLING, callback=Reboot_UserButton , bouncetime=2000)
def Reboot_UserButton():
	#GPIO.output(Red_LED, True)
	#GPIO.output(Green_LED, False)
	#GPIO.output(Yellow_LED, False) 	
	Operating_Loop_Flag = False	

################################################
##  Sending Emails to the Specified End Users ##
################################################
## STATUS: 	Complete; Requires testing for rolling email account in function call
####################################################
#########			DOCUMENTATION   		########
####################################################
# Input Value:		End_User:		The email that the alert will be sent to
#					Frame_Path:		The Path to the frame being sent in the email
#					Frame_Count:	The Number of frames captured so far
#					Person_Count:	The Number of People detected in the area
# Returned Value:	None
####################################################
######## 		  IMPLEMENTATION 	 		########
####################################################	
def Send_Alert_Email(End_User_Email, Frame_Path, Frame_Count, Person_Countr, Device_ID):
	gmail_user      = 'Sparrowatch.alert@gmail.com'
	gmail_password  = "Sparrow2017"
	to              = End_User_Email
	#to              = ' , '.join(to)
	to              = str(to)
	subject         = 'SparroWatch Security Alert'
	body            = 'Something Detected by SparroWatch'
	email_text = ("""\
		Device ID:          %s
		Subject:            %s
		Information:        %s
		Total Frames Captured 		%s
		Person Estimated to be in the Space:	%s
	""" %(Device_ID, subject, body, str(Frame_Count), str(Person_Countr)))

	msg = MIMEMultipart()
	msg["From"] = gmail_user
	msg["To"] = to
	msg["Date"] = formatdate(localtime=True)
	msg["Subject"] = subject
	msg.attach(MIMEText(email_text))
	files = glob.glob(Frame_Path)
	for f in files:
		with open(f, "rb") as fil:
			part = MIMEApplication(        fil.read(),        Name=basename(f))
			part['Content-Disposition'] = 'attachment; filename="%s"' % basename(f)
			msg.attach(part)
	try:
		server = smtplib.SMTP_SSL('smtp.gmail.com',465)
		server.ehlo()
		server.login(gmail_user, gmail_password)
		server.sendmail(gmail_user, to, msg.as_string())
		server.quit()
	except Exception as error:
		print(co("[FAILURE] Could not send email -- Error Code {}". format(error),'cyan',attrs=['reverse','bold']))
		pass
	return

###########################################################
##  Shutdown Light Configuration is set through the GPIO ##
###########################################################
## STATUS: Complete, but not used, alternative method used instead
####################################################
#########			DOCUMENTATION   		########
####################################################
# Input Value:		None
# Returned Value:	None
####################################################
######## 		  IMPLEMENTATION 	 		########
####################################################	
#GPIO.add_event_detect(User_Switch_Shutdown, #GPIO.FALLING, callback=Shutdown_UserButton, bouncetime=2000)
def Shutdown_UserButton():
	#GPIO.output(Red_LED, True)
	#GPIO.output(Green_LED, False)
	#GPIO.output(Yellow_LED, False) 	
	Operating_Loop_Flag = False		

###############################################################################
##  Listing all the folders including hidden folders in the given directtory ##
###############################################################################
## STATUS: Complete
####################################################
#########			DOCUMENTATION   		########
####################################################
# Input Value:		Path: 		The location that will be examined by the function
# Returned Value:	List: 	A list of all the folders that are in the folder
####################################################
######## 		  IMPLEMENTATION 	 		########
####################################################
# var = List_All_Folders(path)	
def List_All_Folders(path):
	List = glob.glob(os.path.join(path, '*'))
	return List

###############################################################################
##  Detecting motion in the images provided ##
###############################################################################
## STATUS: Complete
####################################################
#########			DOCUMENTATION   		########
####################################################
# Input Value:		Frame:	The newest frame from the image pipeline
#					AVG:	The most recent averaged//baseline of the location
# Returned Value:	motion: Boolean object that determines if the area has movement in it
####################################################
######## 		  IMPLEMENTATION 	 		########
####################################################
# motion = MotionDetect(Frame, blur_size, avg, Delta_Thresh,Minimum_Area)
def MotionDetect(Frame, avg):
	Delta_Thresh	= 5
	Minimum_Area	= 250
	blur_size		= (21,21)
	motion = False	 #"Unchanged"
	#print("[DEBUG] 1")
	a = True
	while a == True:
		try:
			gray = cv2.cvtColor(Frame, cv2.COLOR_BGR2GRAY)
			gray = cv2.GaussianBlur(gray, blur_size, 0)
			if avg is None:
				avg = gray.copy().astype("float")
	#			print("[DEBUG] 2")
				continue
	#		print("[DEBUG] 3")
			frameDelta = cv2.absdiff(gray, cv2.convertScaleAbs(avg))
			cv2.accumulateWeighted(gray, avg, 0.5)
			thresh = cv2.threshold(frameDelta, Delta_Thresh, 255,    cv2.THRESH_BINARY)[1]
			thresh = cv2.dilate(thresh, None, iterations=2)
			im2 ,cnts, _ = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
	#		print("[DEBUG] 4")
			for c in cnts:    
				#if cv2.contourArea(c) < Minimum_Area:
				if cv2.contourArea(c) > Minimum_Area:
	#				print("[DEBUG] 5")
					motion = True
					continue
				#motion = True
	#		print("[DEBUG] 6")
			a = False
		except Exception as error:
			print("Motion Detection Function: {}". format(error))
			a = False
	return motion, avg


#####	BEST PRACTICE -- REMOVES FLOATING GLOBAL VALUES 	#####
#if __name__ == "__main__":
#	main()
