#!/usr/bin/env python
# Written by Andy PITCHER

import time
import os
import sys
import random
import pymysql
import getpass

def clear_screen():
    os.system("clear")

def get_login_credentials():
    print("Enter your credentials to start!")
    retry_nb = 0
    while retry_nb <= 3:
        login = input("Login: ")
        password = getpass.getpass("Password: ")
        try:
            conn = pymysql.connect(host="localhost", user=login, passwd=password)
            clear_screen()
            return conn, login
        except pymysql.Error as e:
            retry_nb += 1
            print("\nBad Login or Password! Retry!")
    
    print("You have reached the maximum connection retries.\n\nEXITING THE PROGRAM...")
    sys.exit()

def create_database(conn, cursor, db_name, db_user, db_user_pw):
    try:
        cursor.execute("CREATE DATABASE {}".format(db_name))
        conn.commit()
        time.sleep(2)
        
        create_user_query = "CREATE USER %s IDENTIFIED BY %s"
        cursor.execute(create_user_query, (db_user, db_user_pw))
        conn.commit()
        time.sleep(2)
        
        grant_user_query = "GRANT ALL PRIVILEGES ON {}.* TO %s".format(db_name)
        cursor.execute(grant_user_query, db_user)
        conn.commit()
        
        print("\nDatabase '{}' has been created!\n\nYou can configure Owncloud for accessing the database as below:\nDatabase user: {}\nDatabase password: {}\nDatabase name: {}".format(db_name, db_user, db_user_pw, db_name))
        sys.exit()
    
    except pymysql.Error as e:
        print("[Error] Database '{}' already exists!\n\nEXITING THE PROGRAM...".format(db_name))
        sys.exit()
    
def generate_random_password(length=16):
    alphabet = "abcdefghijklmnopqrstuvwxyz0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    return ''.join(random.choice(alphabet) for _ in range(length))

def generate_random_user_id(length=3):
    number = "1234567890"
    return ''.join(random.choice(number) for _ in range(length))

def validate_site_name(site_name):
    site_name_length = len(site_name)
    return 0 < site_name_length <= 8

def validate_decision(decision):
    return decision.lower() in ["y", "n"]

def main():
    clear_screen()
    
    conn, login = get_login_credentials()
    cursor = conn.cursor()
    
    print("Logged as:", login)
    print("Welcome to Owncloud Database Creation!\nWritten by Andy PITCHER\n\n")
    
    site_name_full = input("Enter the cloud name (full URL: cloud.example.com): ")
    
    while True:
        site_name = input("Write a shortcut for the database name (client name): ")
        if validate_site_name(site_name):
            break
        else:
            print("Shortcut length must be between 1 and 8 characters. Retry!")
    
    site_type = "cloud"
    db_name = "{}_db_{}".format(site_type, site_name)
    db_user = "{}_{}_{}".format(site_type, site_name, generate_random_user_id())
    db_user_full = "'{}'@'localhost'".format(db_user)
    db_user_pw = generate_random_password()
    
    # Summary before creation
    print("\nInformation before Creation:\n")
    print("Site Name:", site_name_full)
    print("Database Name:", db_name)
    print("Database User:", db_user)
    print("Database Password:", db_user_pw)
    
    while True:
        decision = input("\nAre these information correct? [Y/n] ")
        if validate_decision(decision):
            break
        else:
            print("Please enter Y or n!\n")
    
    if decision.lower() == "n":
        print("\nOK, start over for database creation!\nEXITING...\n")
        sys.exit()
    
    print("\n\nProceeding to database creation...\n")
    time.sleep(2)
    
    create_database(conn, cursor, db_name, db_user_full, db_user_pw)

if __name__ == "__main__":
    main()
