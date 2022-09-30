#THIS CODE ALLOWS THE USER TO CREATE AN ALLOCATED TAG DATABASE TO BE USED AS A LOOKUP TABLE 
#SCAN THE TAG
#ENTER THE ALLOCATED ID
#EG A RACE PLATE NUMBER OR A ASSET ID OR WHATEVER

import serial
import os
import sys
import time
import string
import datetime
import csv

serial_port = '/dev/ttyUSB0' #this should be correct, but if not working use $ python -m serial.tools.miniterm
ser = serial.Serial(port=serial_port,baudrate = 38400,parity=serial.PARITY_NONE,stopbits=serial.STOPBITS_ONE,bytesize=serial.EIGHTBITS,timeout=1)

#start set_up_the_reader()
def set_up_the_reader():
	#set the power level and report back the value
	power_level = '02'			 #Reader power level from -2 ~ 25dB
	ser.write(b'\nN1,{power_level}\r')

	#set up the region - this is the frequency of operation - uncomment correct line
	#ser.write(b'\nN5,03\r')                 #Region 01: US  902~928MHz
	#ser.write(b'\nN5,03\r')                 #Region 02: TW  922~928MHz
	ser.write(b'\nN5,03\r')                  #Region 03: CN  920~925MHz
	#ser.write(b'\nN5,03\r')                 #Region 04: CN2 840~845MHz
	#ser.write(b'\nN5,03\r')                 #Region 05: EU  865~868MHz
	#ser.write(b'\nN5,03\r')                 #Region 06: JP  916~921MH
#end set_up_the_reader()

#start write_to_csv()
def write_to_csv(RFID_Tag,Allocated_ID):
	data = [RFID_Tag[1:64], Allocated_ID]
	with open('tag_table.csv', 'a+') as read_file:
		writer = csv.writer(read_file)
		read_file.seek(0)
		writer.writerow(data)
#end write_to_csv()

#start send_command()
def send_command():
	#reader_command = '\nU\r'                   #uncomment if you want to only see EPC
	reader_command = '\nU2,R2,0,6\r'            #uncomment if you want to see the full EPC and TID
	ser.write(reader_command.encode())
	time.sleep(0.1)
#end send_command()

#start read_buffer()
def read_buffer():
	RFID_Tag = ser.read(ser.inWaiting())   #read the buffer (ser.read) for specific byte length (inWaiting)
	return RFID_Tag
#end read_buffer()

#main()
set_up_the_reader()
send_command()
read_buffer()


while True:
	ser.reset_input_buffer()
	ser.reset_output_buffer()
	input ('Place tag on reader surface and <ENTER> to continue...')
	send_command()
	RFID_Tag = read_buffer()
	print (f'Tag EPC is {RFID_Tag[1:64]}')
	good_read = input ('Confirm EPC is good?   Y/N:')
	if good_read == 'Y' or good_read == 'y':
		Allocated_ID = input  ('Please enter the allocated tag id: ')
		write_to_csv(RFID_Tag,Allocated_ID)
		print ('\n')
		Allocated_ID = 'NaN'
