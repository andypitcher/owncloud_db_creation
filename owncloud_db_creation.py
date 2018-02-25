#!/usr/bin/env python
#Written by Andy PITCHER
import time
import os
import sys
import random
import MySQLdb as prog
import getpass

os.system("clear")
#variable
cond=0
retry_nb=0

#Start of program

print ("Enter your credentials to start!")
while True:
        if retry_nb > 3:
                print("You have reached the maximum connexion retries\n\nEXITING THE PROGRAM...")
                sys.exit()
        else:
                try:
                        login = raw_input("Login: ")
			password = getpass.getpass("Password: ")
			conn = prog.connect(host="localhost",user=login,passwd=password)
                        cursor = conn.cursor()
			print("Login succeeded!")
			os.system("clear")
                        break
		except prog.Error as e:
                        retry_nb= retry_nb +1
			print ("\nBad Login or Password! Retry!")
                        
os.system("date")
print("Logged as: "+login)
print("Welcome to Owncloud Database Creation!\nWritten by Andy PITCHER\n\n")
site_name_full = raw_input("Enter the cloud name (full URL: cloud.example.com) : ")
while cond == 0:
        site_name = raw_input("Write a shortcut for database name (client name): ")
        site_name_lg=len(site_name)
	
	if site_name_lg>0 and site_name_lg < 8:
                cond = 1
                break
	elif site_name_lg == 0:
		print("Please provide a name!")
		cond = 0
        else:
                print("Shortcut lenght must be 8 max! Retry!")
                cond=0
site_type="cloud" 
db_name = site_type+"_db_"+site_name

#Generate password for db_user
alphabet = "abcdefghijklmnopqrstuvwxyz0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
pw_length = 16
db_user_pw = ""

for i in range(pw_length):
    next_index = random.randrange(len(alphabet))
    db_user_pw = db_user_pw + alphabet[next_index]

#generate user_id for db_user
number = "1234567890"
id_lenght = 3
user_id = ""

for i in range(id_lenght):
    next_index = random.randrange(len(number))
    user_id = user_id + number[next_index]

db_user=site_type+"_"+site_name+"_"+user_id
db_user_full="\'"+db_user+"\'"+"@"+"\'localhost\'"

#Summary before creation
print "\nInformation before Creation:\n"
print "Site Name: "+site_name_full
print "Database Name: "+db_name
print "Database User: "+db_user
print "Database Password: "+db_user_pw

while True:
	decision = raw_input("\nAre those information correct? [Y/n] ")
	if decision == "Y" or decision == "y":
		print("\n\nProceeding to database creation...\n")
		time.sleep(2)
		
		#Create database db_name
		while True:
			try:
            			create_db="CREATE DATABASE "+db_name
                		cursor.execute(create_db)
                		time.sleep(2)
				#create db_user from site_name and user_id
				while True:
					try:
            					create_user="CREATE USER "+db_user_full+" IDENTIFIED BY \'"+db_user_pw+"\'"
                				cursor.execute(create_user)
						time.sleep(2)
						#Grant db_user on db_name
						while True:
							try:
            							grant_user="GRANT ALL PRIVILEGES ON "+db_name+".* TO "+db_user_full
                						cursor.execute(grant_user)
								print "\nDatabase '"+db_name+"' has been created!\n\nYou can configure the Owncloud for accessing the database as below:\nDatabase user: "\
								+db_user+"\nDatabase password: "+db_user_pw+"\nDatabase name: "+db_name
                						sys.exit()
        						except prog.Error as e:
                						print("[Error Grant]",e)
                						sys.exit()
        				except prog.Error as e:
                				sys.exit()
        		except prog.Error as e:
                		print("[Error] Database "+db_name+ " already exists!\n\nEXITING THE PROGRAM...")
                		sys.exit()
				

	elif decision == "N" or decision == "n":
		print("\nOK, start over for database creation!\nEXITING...\n")
		sys.exit()
	else:
		print("Please enter Y or n !\n")
