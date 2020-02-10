


# **Paul Banahan**
## Chief Technology Officer SparroWatch Limited
### 27th March 2019

## Description of the Software
__File Name__: 1. Standard_Camera/SparroWatch.py

The program will start up, initialise the various variables and define the necessary functions to operate.
The program requires that there be a USB of the name "Sparrowatch" plugged into the Raspberry Pi 3Model B+. Failure to read the USB or absence of the 
drive all-together will result in the system resetting until the device is able to locate the drive. On the drive is the "User_Configuration.json" file. This file holds the various configuration options avialable for the user to alter. The USB will also be the sole storing location for the Frames collected by the unit. The program will automatically create a Database called "SparroWatch Log.db" on the USB drive. Should the USB drive already have the file on the device, then the device will use the existing database to log data.

The "User_Configuration.json" file must contain all of the data that is in the sample verion of the file provided. Should it not have this file or some of the contents in the file, the system will fail and shutdown.

Prior to beginning the main functionality of the program, the device will capture a Baseline image of the site. Giving the user the ability to view the area prior to the operation of the system.

The device will generate a folder of today's date for the collection of the Frames gathered during that 24 hour period. This function is repeated every day at 12 midnight. Aslo at midnight, the device will check the age of the files in the Evidence Path. Should any of the files be older then the specified "Data_Retention_Duration" then the device will remove it perminately.

The Main Function:
This function will operate forever, provided there is power and that the device's shutdown button is not pressed.
The device reads a frame from the attached USB camera, makes a copy and resizes the copy to the user's configured size. The device the detects motion between the current frame that it just read from the camera and the background average frame that it has in memory. Should there be significant motion detected in the image the function will return a Boolean True, otherwise it returns a Boolean False. When motion is detected the background model is updated with to the current frame from the old basline frame. With motion detected the program will then attempt to quantify the cause of the motion, through the use of the Neural Compute Stick and the applied Neural Network; "mobilenetgraph". The predictions are unpacked and read. If the prediction indicates a person(s) triggered the camera, the device will perform a check on the confidence of the prediction. If the confidence is above the preset value the program will assume that the event occured as a direct result of a person in the Area of Interest // Field of View. The device then saves the Frame associated with the event to the USB Drive with the name of the frame being the date and time of the incident. The program will then log the details of the device and the event into the "SparroWatch Log.db" file in the "Events Log" Table. The program then resets the loop and awaits the next incident in the monitering region.

If the user calls for a shutdown the device will close all of the opened resources and enter an entry in the "Event Log" table in the "SparroWatch Log.db" database. Should an error be discovered in the device's setup during the operation of the main function, the device will print the error to the attached screen, wait 5 seconds and then completely shutdown, after entering the shutdown procedure


