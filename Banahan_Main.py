#! python SWL_Final.py
term_color          = 'yellow'       # print(co("YELLOW is for General Information"     , 'yellow'   , attrs=[ 'bold'])
term_color_count    = 'blue'         # print(co("BLUE is for Development of Function"   , 'cyan'    , attrs=[ 'bold'])
from datetime 								import datetime 				as dt
from datetime 								import datetime 				as dt
from datetime 								import time 					as TT
from datetime 								import timedelta
from imutils.video 							import FPS
from imutils.video 							import VideoStream
from termcolor 								import colored 					as co
import Banahan as SWL
import cv2
import json
import time
import os

try:
	import RPi.GPIO as GPIO
	Red_LED 					= 9
	Green_LED 					= 11
	Yellow_LED 					= 10
	User_Switch_Shutdown		= 20
	User_Switch_Restart			= 22
	GPIO.setmode(GPIO.BCM)
	GPIO.setwarnings(False)
	GPIO.setup(Red_LED, GPIO.OUT)
	GPIO.setup(Green_LED, GPIO.OUT)
	GPIO.setup(Yellow_LED, GPIO.OUT)
	GPIO.setup(User_Switch_Shutdown, GPIO.IN, pull_up_down =GPIO.PUD_UP)
	GPIO.setup(User_Switch_Restart,  GPIO.IN, pull_up_down =GPIO.PUD_UP)
	GPIO.output(Red_LED, False) 	
	GPIO.output(Green_LED, False) 	
	GPIO.output(Yellow_LED, False) 	
	GPIO.output(Red_LED, True) 		
	GPIO.output(Green_LED, False) 	
	GPIO.output(Yellow_LED, False)
except RuntimeError:
	print(co("[ERROR] Cant imort RPi.GPIO", 'cyan'    , attrs=[ 'bold']))
	pass

cwd = str(os.getcwd())
print("CWD: {}". format(cwd))	

print(co("################################",                                term_color, attrs=[ 'bold']))
print(co("[STARTUP] Device Starting Up Now",                                term_color, attrs=[ 'bold']))
print(co("################################",                                term_color, attrs=[ 'bold']))

#############################
## Global Variable Calling ##
#############################
global Device_ID
text 						= True
files = folders 			= 0
event_countr				= 0
Person_countr				= 0
Person_countr_total			= 0
Frame_Count					= 0

#############################################
## Raspberry Pi Model 3 B+ File Extensions ##
#############################################
Evidence_Path	= "/media/pi/"
#conf_path 		= "/home/pi/SparroWatch/Configurations/conf.json"
conf_path 		= "./Configurations/conf.json"
graph_path 		= cwd+"/graphs"
graph_folder 	= os.path.join(graph_path)

############################################
## Ubuntu Machine TestBed File Extensions ##
############################################
# /home/paul/Desktop/SparroWatch_SBRI
# Evidence_Path		= "/home/paul/Desktop/Frames/"
# conf_path 			= "/home/paul/Desktop/SparroWatch_SBRI/Configurations/conf.json"
# graph_path 		= "/home/paul/Desktop/SparroWatch_SBRI/graphs"
# graph_folder 		= os.path.join(graph_path)

########################################
## SLW_Complete Variable Requirements ##
########################################
## Overall Database
database 				= "SparroWatch"		##	Location and name of the Database taht everything is stored into
table_name_event 		= "Event Log"	 	##	Name of the Event Log
Event_Trigger 			= "Person"			##  What Triggered the camera
Email_Info 				= "Startup"			##	Email Details
FOIC 					= 0					##	Frame Of Interest Count
Frame_Location			= ""				##	Location of the frame being logged
table_name_Heart		= "Heartbeat Log"	##  Name of the Heartbeat log
Repeat_Every_X_Seconds 	= 60				##	How often the heart should beat in Seconds

#############################################
#### SWL_Complete Function Calls and setup ##
#############################################
## Event Logging Function
Ev_DB = SWL.Event_DB(database, table_name_event)					# db, table 
Ev_DB.Create_Event(table_name_event)								# Table_name
## Heartbeat
Hb_DB = SWL.Heart_DB(database, table_name_Heart)					# db, table 
Hb_DB.Create_Heart(table_name_Heart)								# Table_name
Hb_DB.Heart_Logger()
## Neural Compute Stick
NCS = SWL.NCS(graph_folder)
predict = NCS.predict
## Labelling Class
Images = SWL.Images()
labelMaker = Images.LabelMaker

##########################################
## Naming Functions for this name space ##
##########################################
Time_Check 		 = SWL.Check_if_time_between
Internet_Check 	 = SWL.Check_Internet_Connection
Remover			 = SWL.FileRemover
String_Month	 = SWL.month
send_email		 = SWL.Send_Alert_Email
All_Folders 	 = SWL.List_All_Folders
Baseline		 = SWL.Baseline
motion_detect 	 = SWL.MotionDetect

folders = len(All_Folders(Evidence_Path))

if folders == 0:
	print(co("[ERROR] USB DRIVE FAILED TO MOUNT CORRECTLY RESETTING NOW",	term_color_count, attrs = ['bold']))
	print(co("[ERROR] Rebooting now",										term_color_count, attrs = ['bold']))
	GPIO.output(Red_LED, False) 	
	GPIO.output(Green_LED, False) 
	GPIO.output(Yellow_LED, True) 	
	time.sleep(2.0)
	os.system(reboot)
if folders ==1 :
	Evidence_Path= ("/media/pi/SparroWatch/")
	
if folders > 1:
	Evidence_Path = ("/media/pi/SparroWatch"+(str(folders-1))+"/")
	
print(co("[INFO] Actionable Directory is: {}". format(Evidence_Path), term_color_count, attrs = ['bold']))


## Configurations for the User
with open(conf_path, mode="rb") as f:
	conf = json.load(f)
Person_Minimum 					= int		(conf["Person_Minimum"])
Device_ID 						= str		(conf["Device_ID"])
DISPLAY_DIMS 					= tuple		(conf["resolution"])
Email_Waiting_Time_minutes 		= float		(conf["Email_Waiting_Time_minutes"])
Email_To_Be_Notified			= str 		(conf["Email_To_Be_Notified"])
Operation_Start_Time_Conf 		= tuple		(conf["Operation_Start_Time"])
Notification_Start_Time_Conf	= tuple		(conf["Notification_Start_Time"])
Notification_Stop_Time_Conf 	= tuple		(conf["Notification_Stop_Time"])
Operation_Stop_Time_Conf		= tuple		(conf["Operation_Stop_Time"])
Heartrate						= float 	(conf["Heartrate"])

email = (str(Email_To_Be_Notified[0]),str(Email_To_Be_Notified[1]))
minimum_motion 					= 3			
Pred_Conf_Factor 				= 0.35

Email_Waiting_Time 				= Email_Waiting_Time_minutes * 60
Repeat_Every_X_Seconds 					= Heartrate * 60
## Perpetual Timer Function
t = SWL.perpetualTimer(Repeat_Every_X_Seconds, Hb_DB.Heart_Logger)
t.Start()


Operating_Lower_Limit_H 		= 	int(Operation_Start_Time_Conf[0])
Operating_Lower_Limit_M 		= 	int(Operation_Start_Time_Conf[1])
Operating_Lower_Limit_S			=	int(Operation_Start_Time_Conf[2])
Operate_Start_Time 				= 	TT(Operating_Lower_Limit_H,Operating_Lower_Limit_M,Operating_Lower_Limit_S)
Notification_Lower_Limit_H 		= 	int(Notification_Start_Time_Conf[0]) 	
Notification_Lower_Limit_M 		= 	int(Notification_Start_Time_Conf[1]) 	
Notification_Lower_Limit_S 		= 	int(Notification_Start_Time_Conf[2]) 	
Notify_Start_Time 				= 	TT(Notification_Lower_Limit_H, Notification_Lower_Limit_M, Notification_Lower_Limit_S)
Notification_Upper_Limit_H 		= 	int(Notification_Stop_Time_Conf[0]) 	
Notification_Upper_Limit_M 		= 	int(Notification_Stop_Time_Conf[1]) 	
Notification_Upper_Limit_S 		= 	int(Notification_Stop_Time_Conf[2]) 	
Notify_Stop_Time				= 	TT(Notification_Upper_Limit_H, Notification_Upper_Limit_M, Notification_Upper_Limit_S)
Operating_Upper_Limit_H 		= 	int(Operation_Stop_Time_Conf[0])	
Operating_Upper_Limit_M 		= 	int(Operation_Stop_Time_Conf[1])
Operating_Upper_Limit_S 		= 	int(Operation_Stop_Time_Conf[2])
Operate_Stop_Time 				= 	TT(Operating_Upper_Limit_H,Operating_Upper_Limit_M,Operating_Upper_Limit_S)

print("")
print(co("After Working with the Conf.json Tuple"								,'blue', attrs=['reverse','bold']))
print(co("Operate Start Time is:   {}"			. format(Operate_Start_Time)	,'blue', attrs=['reverse','bold']))
print(co("     Notify Start Time is:   {}"		. format(Notify_Start_Time)		,'blue', attrs=['reverse','bold']))
print(co("     Notify Stop Time is:    {}"		. format(Notify_Stop_Time)		,'blue', attrs=['reverse','bold']))
print(co("Operate Stop Time is:    {}"			. format(Operate_Stop_Time)		,'blue', attrs=['reverse','bold']))
print("")

CLASSES = ("Background", "Aeroplane", "Bicycle", "Bird",	"Boat", "Bottle", "Bus", "Car", "Cat", "Chair", "Cow",
	"Diningtable", "Dog", "Horse", "Motorbike", "Person",	"Pottedplant", "Sheep", "Sofa", "Train", "TVmonitor")
COLOURS = ((255, 117, 0),(255, 0, 138),(255, 0, 250),(0, 255, 250),	(0, 255, 0), (0, 1, 255),(139,0,139), (127,255,212),(0,206,209),(0,128,128), (240,255,255),
	(255,255,240), (255,222,173),(255,105,180), (138,43,226), (42,211,42),	(30,144,255), (123,104,238), (0,191,255), (230,230,250), (240,248,255))

todaysDate = time.strftime("%d-%B-%Y")
evidencePath_Today = todaysDate
evidenceDirectory = Evidence_Path + evidencePath_Today
TodaysFolder = evidenceDirectory
if not os.path.exists(evidenceDirectory):
	Remover(Evidence_Path)
	os.makedirs(evidenceDirectory, 777)
	os.chmod(evidenceDirectory, 0777)  	

Email_Details = "Email Function not enabled on Device"
Baseline_Capture = Baseline.Capture_Frame
a = None
Frame_Location = Baseline_Capture(a, TodaysFolder, DISPLAY_DIMS)

Connection_Status, _ = Internet_Check()
if Connection_Status == True:
	Email_Details = "Alert Email Sent - Internet Connection Status is True"
	for i in range(len(email)):
		gg = time.time()
		print(co("[EMAIL] Sending Email to {}. Time is {} in UNIX Epoch". format(email[i], gg),'white', attrs=['bold']))
		#send_email(email[i], Frame_Location, Frame_Count,Person_countr,Device_ID)
		print(time.time())
		print(" ")

if Connection_Status == False:
	Email_Details = "Alert Email Not Sent - Internet Connection Status is False"

Ev_DB.Event_Logger('Startup Procedure', Email_Details, (int(Frame_Count)), (str(Frame_Location)))

GPIO.output(Red_LED, False) 	
GPIO.output(Green_LED, True)
GPIO.output(Yellow_LED, False)

Delta_Thresh	= 5
Minimum_Area	= 250
blur_size		= (21,21)



def main():
	motionCounter 				= 0
	t1 							= dt.now()
	t3 							= t1
	Seconds_Since_Last_Email 	= 0
	event_countr				= 0
	Person_countr				= 0
	Person_countr_total			= 0
	Frame_Count					= 1
	avg = None
	vs = VideoStream(usePiCamera=-1> 0).start()
	fps = FPS().start()
	while True:
		try: 
			Oppy_Time = Time_Check(Operate_Start_Time, Operate_Stop_Time)
			if Oppy_Time == True:   
				
				todaysDate = time.strftime("%d-%B-%Y")
				evidencePath_Today = todaysDate
				evidenceDirectory = Evidence_Path + evidencePath_Today
				TodaysFolder = evidenceDirectory
				if not os.path.exists(evidenceDirectory):
					Remover(Evidence_Path)
					os.makedirs(evidenceDirectory, 0777)   
					os.chmod(evidenceDirectory, 0777)  	
					
				frame = vs.read()
				t2 = dt.now()
				if frame is None:
					print(co("[ERROR] Reading Frame", 'cyan', attrs = ['bold']))
					break
				image_for_result = frame.copy()    
				image_for_result = cv2.resize(frame, DISPLAY_DIMS)

				text, avg = motion_detect(image_for_result, avg)
				
				cv2.imshow('Frame', frame)
				avg_1 = cv2.resize(frame, (300,300))
				cv2.imshow('AVG', avg_1)
				
				if cv2.waitKey(1) == ord('q'):
					print("Escaping now")
					break
				if text == True:
					motionCounter += 1
					if motionCounter >= minimum_motion:
						predictions = predict(frame)
						Event_Now = True
						for (i, pred) in enumerate(predictions):
							(pred_class, pred_conf, pred_boxpts) = pred
							if pred_class == 15:
								if pred_conf >= Pred_Conf_Factor:
									event_Type = 'Person'
									Frame_Count += 1
									if Event_Now == True:
										event_countr = event_countr + 1
										Event_Now = False
									Person_countr += 1
									image_for_result = labelMaker(image_for_result)
									Time_now = dt.now()
									Frame_Name = str(time.strftime("%d %B %Y -- %H.%M.%S.{}.jpg". format(Time_now.microsecond)))
									Frame_Location = TodaysFolder + "/" + Frame_Name
									cv2.imwrite(Frame_Location, image_for_result)
									Email_Details = "Not in the Notifcation Time Window yet"
									Noty_User = Time_Check(Notify_Start_Time, Notify_Stop_Time)
									if Noty_User == True:
										delta_T = t2 - t1    
										Seconds_Since_Last_Email = delta_T.total_seconds()
										Email_Details = 'Notify Time Window but Email Time not reached yet'
										if Seconds_Since_Last_Email >= Email_Waiting_Time:                                           
											Connection_Status, _ = Internet_Check()
											number = int(Time_now.month)
											Named_Month = String_Month(number)
											Frame_now = ("{:02d}-{}-{:4d}---{:02d}:{:02d}:{:02d}.{}" . format(Time_now.day, Named_Month, Time_now.year, Time_now.hour, Time_now.minute, Time_now.second, Time_now.microsecond))
											if Connection_Status == True:
												Email_Details = "Alert Email Sent - Internet Connection Status is True"
												t1 = t2
												for i in range(len(email)):
													pass
													#send_email(email[i], Frame_Location, Frame_Count,Person_countr,Device_ID)
											if Connection_Status == False:
												Email_Details = "Alert Email Not Sent - Internet Connection Status is False"
									if Noty_User == False:
										Email_Details = "Not in the Notifcation Time Window yet"
										pass
									Ev_DB.Event_Logger(CLASSES[pred_class],Email_Details, Frame_Count, str(Frame_Location))
									print(co("[EVENT] Email Details: {};	Email Wait Time: {:.01f};	Seconds_Since_Last_Email is: {:.02f};	Person Count: {}" . format(Email_Details, Email_Waiting_Time,Seconds_Since_Last_Email,Person_countr),'magenta', attrs=['reverse','bold']))		### DEBUGGING ONLY
						avg 				= None	
						motionCounter		= 0
						Person_countr_total = Person_countr + Person_countr_total
						Person_countr 		= 0
				else:
					motionCounter 			= 0
				fps.update()
			if Oppy_Time == False:
				x = dt.now()
				number = int(x.month)
				Named_Month = String_Month(number)
				XX = ("{:02d}-{}-{:4d} --- {:02d}:{:02d}:{:02d}  " . format(x.day, Named_Month, x.year, x.hour, x.minute, x.second, x.microsecond))
				#print(co("Op Loop = OFF. Noty Loop = OFF. A = {}; B = {}; Time is {}". format(Oppy_Time, Noty_User, XX) ,'white', attrs=['reverse','bold']))
				time.sleep(1)			## Sleep for a second, then check the time
		except AttributeError as AttributeProblem:
			print("		")
			print("AttributeProblem")
			print(AttributeProblem)	
			print("		")
			break
		except KeyboardInterrupt:
			print(co("[SHUTDOWN] User pressed Ctrl+C to exit the program"        ,'red', attrs=[ 'bold']))
			break
		except Exception as Error:
			print("		")
			print("General Error")
			print(Error)
			print("		")
			break
		fps.update()
	fps.stop()
	vs.stop()
	print(co("  *****   *****   *****   *****   *****   ", 'green', attrs = ['reverse']))
	print(co("  *****   *****   *****   *****   *****   ", 'white', attrs = ['reverse']))
	print(co("  *****   *****   *****   *****   *****   ", 'yellow', attrs = ['reverse']))

print(co("  *****   *****   *****   *****   *****   ", 'white', attrs = ['reverse']))
print(co("  *****   *****   *****   *****   *****   ", 'white', attrs = ['reverse']))
print(co("  *****   *****   *****   *****   *****   ", 'yellow', attrs = ['reverse']))

if __name__ == "__main__":
	main()
	
	wait_time = (0.030625)
	time.sleep(wait_time)
	Frame_Location = Baseline_Capture(a, TodaysFolder, DISPLAY_DIMS)
	Connection_Status, _ = Internet_Check()
	print(co("MAIN: {}". format(Frame_Location), 'red'))
	if Connection_Status == True:
		Email_Details = "Alert Email Sent - Internet Connection Status is True"
		for i in range(len(email)):
			print(co("[EMAIL] Sending Email to {}". format(email[i]),'white'))
			#send_email(email[i], Frame_Location, Frame_Count,Person_countr,Device_ID)
			print(" ")
	if Connection_Status == False:
		Email_Details = "Alert Email Not Sent - Internet Connection Status is False"
	Ev_DB.Event_Logger('Startup Procedure', Email_Details, (int(Frame_Count)), (str(Frame_Location)))
	cv2.destroyAllWindows()
	## Closing down the classes ##
	Ev_DB.Close()
	t.Cancel()
	Hb_DB.Close()
	NCS.Close_NCS()