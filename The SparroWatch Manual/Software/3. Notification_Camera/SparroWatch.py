#! python '1. Notification_Camera/SparroWatch.py'
from datetime 								import datetime 				as dt
from datetime 								import datetime 				as dt
from datetime 								import time 					as TT
from datetime 								import timedelta
from imutils.video 							import FPS
from imutils.video 							import VideoStream
from termcolor 								import colored 					as co
import SWL
import cv2
import json
import time
import os
try:
	import RPi.GPIO as GPIO
	Red_LED = 9
	Green_LED = 10
	Yellow_LED 	= 11
	Shutdown_GPIO = 20
	GPIO.setmode(GPIO.BCM)
	GPIO.setwarnings(False)
	GPIO.setup(Red_LED, GPIO.OUT)
	GPIO.setup(Green_LED, GPIO.OUT)
	GPIO.setup(Yellow_LED, GPIO.OUT)
	GPIO.setup(Shutdown_GPIO, GPIO.IN, pull_up_down=GPIO.PUD_UP)
	GPIO.output(Red_LED, False) 	
	GPIO.output(Green_LED, False) 	
	GPIO.output(Yellow_LED, False) 	
	GPIO.output(Red_LED, True) 		
	GPIO.output(Green_LED, False) 	
	GPIO.output(Yellow_LED, False)
	print(co("Red_Led: {}; Yellow_LED: {}; Green_LED: {}; Shutdown_GPIO: {};". format(Red_LED, Yellow_LED, Green_LED, Shutdown_GPIO), 'blue', attrs=['bold']))
except RuntimeError as RunError:
	print(co("[ERROR] RuntimeError occured when loading GPIO library: {}". format(RunError),'cyan',attrs=['reverse','bold']))
	os.system("sudo reboot now")
print(co("################################", 	'yellow', attrs=[ 'bold']))
print(co("[STARTUP] Device Starting Up Now", 	'yellow', attrs=[ 'bold']))
print(co("################################",	'yellow', attrs=[ 'bold']))
global Device_ID
files = folders = 0
Frame_Count	= 0
Evidence_Path = "/media/pi/"
graph_path 	= "/home/pi/SparroWatch/graphs"
graph_folder = os.path.join(graph_path)
table_name_event = "Event Log"	
Email_Info ="Startup"			
FOIC = 0				
table_name_Heart= "Heartbeat Log"	
NCS = SWL.NCS(graph_folder)
predict = NCS.predict
Images = SWL.Images()
labelMaker = Images.LabelMaker
Time_Check = SWL.Check_if_time_between
Internet_Check = SWL.Check_Internet_Connection
Remover	= SWL.FileRemover
String_Month = SWL.month
send_email = SWL.Send_Alert_Email
Baseline = SWL.Baseline
motion_detect = SWL.MotionDetect
Check = SWL.Shutdown_User_Button
All_Folders = SWL.List_All_Folders
folders = len(All_Folders(Evidence_Path))
if folders == 0:
	print(co("[ERROR] Failed to mount USB storage correctly",	'blue', attrs = ['bold']))
	GPIO.output(Red_LED, False) 	
	GPIO.output(Green_LED, False) 
	GPIO.output(Yellow_LED, True) 	
	time.sleep(2.0)
	os.system("sudo reboot now")
if folders == 1:
	Evidence_Path= ("/media/pi/Sparrowatch/")
if folders > 1:
	Evidence_Path = ("/media/pi/Sparrowatch"+(str(folders-1))+"/")
conf_path = Evidence_Path+"/User_Configurations.json"
print(co("[INFO] Actionable Directory is: {}". format(Evidence_Path), 'blue', attrs = ['bold']))
database = Evidence_Path+"/SparroWatch Log"	
Ev_DB = SWL.Event_DB(database, table_name_event)
Ev_DB.Create_Event(table_name_event)
Hb_DB = SWL.Heart_DB(database, table_name_Heart)
Hb_DB.Create_Heart(table_name_Heart)
Hb_DB.Heart_Logger()
with open(conf_path, mode="rb") as f:
	conf = json.load(f)
Device_ID = str		(conf["Device_ID"])
DISPLAY_DIMS  = tuple		(conf["resolution"])
Email_Waiting_Time_minutes = float		(conf["Email_Waiting_Time_minutes"])
Email_To_Be_Notified = tuple 	(conf["Email_To_Be_Notified"])
email = Email_To_Be_Notified
Operation_Start_Time_Conf = tuple	(conf["Operation_Start_Time"])
Notification_Start_Time_Conf = tuple	(conf["Notification_Start_Time"])
Notification_Stop_Time_Conf = tuple	(conf["Notification_Stop_Time"])
Operation_Stop_Time_Conf = tuple	(conf["Operation_Stop_Time"])
Heartrate = float (conf["Heartrate"])
Data_Retention_Duration = int (conf["Data_Retention_Duration"])
minimum_motion = 3			
Pred_Conf_Factor = 0.35
Email_Waiting_Time 	= Email_Waiting_Time_minutes * 60
Repeat_Every_X_Seconds = Heartrate * 60
t = SWL.perpetualTimer(Repeat_Every_X_Seconds, Hb_DB.Heart_Logger)
t.Start()
Operating_Lower_Limit_H = int(Operation_Start_Time_Conf[0])
Notification_Lower_Limit_H = int(Notification_Start_Time_Conf[0]) 	
Notification_Upper_Limit_H = int(Notification_Stop_Time_Conf[0])
Operating_Upper_Limit_H = int(Operation_Stop_Time_Conf[0])
Operating_Lower_Limit_M = int(Operation_Start_Time_Conf[1])
Notification_Lower_Limit_M = int(Notification_Start_Time_Conf[1]) 
Notification_Upper_Limit_M = int(Notification_Stop_Time_Conf[1]) 	
Operating_Upper_Limit_M = int(Operation_Stop_Time_Conf[1])
Operating_Upper_Limit_S = int(Operation_Stop_Time_Conf[2])
Notification_Upper_Limit_S = int(Notification_Stop_Time_Conf[2])
Notification_Lower_Limit_S = int(Notification_Start_Time_Conf[2]) 
Operating_Lower_Limit_S	= int(Operation_Start_Time_Conf[2])
Operate_Start_Time = TT(Operating_Lower_Limit_H,Operating_Lower_Limit_M,Operating_Lower_Limit_S)
Notify_Start_Time = TT(Notification_Lower_Limit_H, Notification_Lower_Limit_M, Notification_Lower_Limit_S)
Notify_Stop_Time= TT(Notification_Upper_Limit_H, Notification_Upper_Limit_M, Notification_Upper_Limit_S)
Operate_Stop_Time = TT(Operating_Upper_Limit_H,Operating_Upper_Limit_M,Operating_Upper_Limit_S)
CLASSES = ("Background", "Aeroplane", "Bicycle", "Bird",	"Boat", "Bottle", "Bus", "Car", "Cat", "Chair", "Cow",
	"Diningtable", "Dog", "Horse", "Motorbike", "Person",	"Pottedplant", "Sheep", "Sofa", "Train", "TVmonitor")
COLOURS = ((255, 117, 0),(255, 0, 138),(255, 0, 250),(0, 255, 250),	(0, 255, 0), (0, 1, 255),(139,0,139), (127,255,212),(0,206,209),(0,128,128), (240,255,255),
	(255,255,240), (255,222,173),(255,105,180), (138,43,226), (42,211,42),	(30,144,255), (123,104,238), (0,191,255), (230,230,250), (240,248,255))
todaysDate = time.strftime("%d-%B-%Y")
evidencePath_Today = todaysDate
evidenceDirectory = Evidence_Path + evidencePath_Today
TodaysFolder = evidenceDirectory
if not os.path.exists(evidenceDirectory):
	Remover(Evidence_Path,Data_Retention_Duration)
	os.makedirs(evidenceDirectory, 0777)
	os.chmod(evidenceDirectory, 0777)  	
Email_Details = "Email Function not enabled on Device"
Baseline_Capture = Baseline.Capture_Frame
a = None
Frame_Location = Baseline_Capture(a, TodaysFolder, DISPLAY_DIMS)
Frame_Count += 1
len_email = len(email)
Connection_Status, _ = Internet_Check()
if Connection_Status == True:
	Email_Details = "Alert Email Sent - Internet Connection Status is True"
	if len_email == 0:
		pass
	if len_email == 1:
		send_email(email, Frame_Location, Frame_Count, 00, Device_ID)
	if len_email > 1:
		for i in range(len(email)):
			send_email(email[i], Frame_Location, Frame_Count, 00, Device_ID)
if Connection_Status == False:
	Email_Details = "Alert Email Not Sent - Internet Connection Status is False"
Ev_DB.Event_Logger('Startup Procedure', Email_Details, (int(Frame_Count)), (str(Frame_Location)))
def main():
	GPIO.output(Red_LED, False) 	
	GPIO.output(Green_LED, True)
	GPIO.output(Yellow_LED, False)
	Frame_Count					= 0
	Shutdown_GPIO				= 20
	motionCounter 				= 0
	t1 							= dt.now()
	t3 							= t1
	Seconds_Since_Last_Email 	= 0
	event_countr				= 0
	Frame_Count					= 1
	avg 						= None
	len_email 					= len(email)
	vs 							= VideoStream(usePiCamera=-1> 0).start()
	fps 						= FPS().start()
	while True:
		try: 
			todaysDate = time.strftime("%d-%B-%Y")
			evidencePath_Today = todaysDate
			evidenceDirectory = Evidence_Path + evidencePath_Today
			TodaysFolder = evidenceDirectory
			if not os.path.exists(evidenceDirectory):
				Remover(Evidence_Path,Data_Retention_Duration)
				os.makedirs(evidenceDirectory, 0777)   
				os.chmod(evidenceDirectory, 0777)  	
			frame = vs.read()
			t2 = dt.now()
			if frame is None:
				print(co("[ERROR] Reading Frame from Camera"  , 'cyan', attrs = ['bold']))
				os.system("sudo reboot now")
				break
			if not Check(Shutdown_GPIO):
				print(co("[SHUTDOWN] User Shutdown called", 'white', attrs = ['bold']))
				break
			image_for_result = frame.copy()    
			image_for_result = cv2.resize(frame, DISPLAY_DIMS)
			motion, avg = motion_detect(frame, avg)
			if motion == True:
				motionCounter += 1
				if motionCounter >= minimum_motion:
					predictions = predict(frame)
					Event_Now = True
					for (i, pred) in enumerate(predictions):
						(pred_class, pred_conf, pred_boxpts) = pred
						if pred_class == 15:
							if pred_conf >= Pred_Conf_Factor:
								event_Type = CLASSES[pred_class]
								Frame_Count += 1
								if Event_Now == True:
									event_countr = event_countr + 1
									Event_Now = False
								image_for_result = labelMaker(image_for_result)
								Time_now = dt.now()
								Frame_Name = str(time.strftime("%d %B %Y -- %H.%M.%S.{}.jpg". format(Time_now.microsecond)))
								Frame_Location = TodaysFolder + "/" + Frame_Name
								cv2.imwrite(Frame_Location, image_for_result)
								print("[EVENT] {}". format(Frame_Location))
								Email_Details = "Not Email Time yet"
								if Seconds_Since_Last_Email >= Email_Waiting_Time:                                           
									Connection_Status, _ = Internet_Check()
									number = int(Time_now.month)
									Named_Month = String_Month(number)
									Frame_now = ("{:02d}-{}-{:4d}---{:02d}:{:02d}:{:02d}.{}" . format(Time_now.day, Named_Month, Time_now.year, Time_now.hour, Time_now.minute, Time_now.second, Time_now.microsecond))
									if Connection_Status == True:
										Email_Details = "Alert Email Sent - Internet Connection Status is True"
										t1 = t2
										if len_email == 0:
											pass
										if len_email == 1:
											send_email(email, Frame_Location, Frame_Count, 0, Device_ID)
										if len_email > 1:
											for i in range(len(email)):
												send_email(email[i], Frame_Location, Frame_Count, 0, Device_ID)
									if Connection_Status == False:
										Email_Details = "Alert Email Not Sent - Internet Connection Status is False"
								Ev_DB.Event_Logger(CLASSES[pred_class],Email_Details, Frame_Count, str(Frame_Location))
					avg 				= None	
					motionCounter		= 0
			else:
				motionCounter 			= 0
			fps.update()
		except AttributeError as AttributeProblem:
			print("		")
			print("[AttributeProblem]")
			print(AttributeProblem)	
			print("		")
			time.sleep(5.0)
			break
		except KeyboardInterrupt:
			print(co("[SHUTDOWN] User pressed Ctrl+C to exit the program"        ,'red', attrs=[ 'bold']))
			break
		except Exception as Error:
			print("		")
			print("[General Error]")
			print(Error)
			print("		")
			time.sleep(5.0)
			break
		fps.update()
	fps.stop()
	vs.stop()
	print(co("  *****   *****   *****   *****   *****   ", 'red', attrs = ['reverse']))
print(co("  *****   *****   *****   *****   *****   ", 'green', attrs = ['reverse']))

if __name__ == "__main__":
	main()
	wait_time = (0.030625)
	time.sleep(wait_time*2)
	Frame_Location = Baseline_Capture(a, TodaysFolder, DISPLAY_DIMS)
	Connection_Status, _ = Internet_Check()
	if Connection_Status == True:
		Email_Details = "Alert Email Sent - Internet Connection Status is True"
		if len_email == 0:
			pass
		if len_email == 1:
			send_email(email, Frame_Location, Frame_Count, 00, Device_ID)
		if len_email > 1:
			for i in range(len(email)):
				send_email(email[i], Frame_Location, Frame_Count, 00, Device_ID)
	if Connection_Status == False:
		Email_Details = "Alert Email Not Sent - Internet Connection Status is False"
	print(co("###################################",	'yellow', attrs=[ 'bold']))
	print(co("[SHUTDOWN] Device shuting down Now ", 'yellow', attrs=[ 'bold']))
	print(co("###################################",	'yellow', attrs=[ 'bold']))
	Ev_DB.Event_Logger('Shutdown Procedure', Email_Details, (int(Frame_Count)), (str(Frame_Location)))
	cv2.destroyAllWindows()
	Ev_DB.Close()
	t.Cancel()
	Hb_DB.Close()
	time.sleep(1.0)
	os.system("sudo shutdown now")