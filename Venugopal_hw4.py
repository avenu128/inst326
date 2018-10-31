#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Name: Anant Venugopal
# Directory ID: avenu128
# Date: 2018-10-24
# Assignment: Homework 4

import csv
import sqlite3
import sys

db = sqlite3.connect('db1.sqlite')#writes to a file
cursor = db.cursor()

INPUTFILE = sys.argv[1]
INPUTFILE2 = sys.argv[2]
INPUTFILE3 = sys.argv[3]
splitInput = INPUTFILE.split(".")
splitInput2 = INPUTFILE2.split(".")
splitInput3 = INPUTFILE3.split(".")

#stores filenames from command line arguments into variables


def main():
    cursor.execute('''CREATE TABLE IF NOT EXISTS assets (
                        id integer PRIMARY KEY AUTOINCREMENT NOT NULL UNIQUE,
                        md5 text,
                        bytes integer,
                        sha1 text,
                        sha256 text)'''
                   )
    cursor.execute('''CREATE TABLE IF NOT EXISTS files (
                          id integer PRIMARY KEY AUTOINCREMENT NOT NULL UNIQUE,
                          path text,
                          directory text,
                          filename text,
                          extension text,
                          mtime text,
                          moddate text,
                          asset_id integer)'''
                   )
    #creates tables with necessary columns
    insert_assets_query = '''INSERT INTO assets (md5,bytes,sha1,sha256)
    VALUES (?,?,?,?)'''
    insert_files_query = '''INSERT INTO files (path, directory, filename, extension, mtime, moddate,asset_id)
    VALUES (?,?,?,?,?,?,?)'''
    #create queries to insert data into tables
    try:
        arg1 = sys.argv[1]
    except IndexError:
        print("Argument error, closing the program")
        sys.exit()
    try:
        arg2 = sys.argv[2]
    except IndexError:
        print("Argument error, closing the program")
        sys.exit()
    try:
        arg3 = sys.argv[3]
    except IndexError:
        print("Argument error, closing the program")
        sys.exit()
    #Look to see if user failed to enter an argument
    if (splitInput[1]!= "csv" or splitInput2[1] != "csv" or splitInput3[1] != "csv"):
        exit()
    with open(INPUTFILE, 'r', encoding='utf-8', errors='ignore') as inhandle:
        reader = csv.DictReader(inhandle)
        data = []
        for row in reader:
            data.append(row)
    #Move all data from the file into an ordered list of dictionaries
    for val in data:
        md5 = val['MD5']
        bytes = val['BYTES']
        assetData = (md5, val['BYTES'], val['SHA1'], val['SHA256'])
        cursor.execute("SELECT id from assets WHERE md5 = ? AND bytes = "+bytes,(md5,))
        results = cursor.fetchone()
        #check to see if id is already in the table by comparing md5 values
        if (results is None):
            cursor.execute(insert_assets_query, assetData)
            cursor.execute("SELECT id from assets WHERE md5 = ? AND bytes = " + bytes, (md5,))
            id = cursor.fetchone()[0]
            #if it isn't in the table creates a new id and adds data to assets table, sets id to new value
        else:
            id = cursor.fetchone()[0]
            #if id does exist doesn't add new data just sets id to the value
        filesData = (val['PATH'], val['DIRECTORY'], val['FILENAME'], val['EXTENSION'], val['MTIME'], val['MODDATE'],id)
        cursor.execute(insert_files_query, filesData)
        #adds data to the files table
    with open(INPUTFILE2, 'r', encoding='utf-8', errors='ignore') as inhandle:
        reader = csv.DictReader(inhandle)
        data = []
        for row in reader:
            data.append(row)
    for val in data:
        md5 = val['MD5']
        bytes = val['BYTES']
        assetData = (md5, val['BYTES'], val['SHA1'], val['SHA256'])
        cursor.execute("SELECT id from assets WHERE md5 = ? AND bytes = "+bytes,(md5,))
        results = cursor.fetchone()
        if (results is None):
            cursor.execute(insert_assets_query, assetData)
            cursor.execute("SELECT id from assets WHERE md5 = ? AND bytes = " + bytes, (md5,))
            id = cursor.fetchone()[0]
        elif (results is not None):
            id = results[0]
        filesData = (val['PATH'], val['DIRECTORY'], val['FILENAME'], val['EXTENSION'], val['MTIME'], val['MODDATE'],id)
        cursor.execute(insert_files_query, filesData)
    with open(INPUTFILE3, 'r', encoding='utf-8', errors='ignore') as inhandle:
        reader = csv.DictReader(inhandle)
        data = []
        for row in reader:
            data.append(row)
    for val in data:
        md5 = val['MD5']
        bytes = val['BYTES']
        assetData = (md5, val['BYTES'], val['SHA1'], val['SHA256'])
        cursor.execute("SELECT id from assets WHERE md5 = ? AND bytes = "+bytes,(md5,))
        results = cursor.fetchone()
        if (results is None):
            cursor.execute(insert_assets_query, assetData)
            cursor.execute("SELECT id from assets WHERE md5 = ? AND bytes = " + bytes, (md5,))
            id = cursor.fetchone()[0]
        elif (results is not None):
            id = results[0]
        filesData = (val['PATH'], val['DIRECTORY'], val['FILENAME'], val['EXTENSION'], val['MTIME'], val['MODDATE'],id)
        cursor.execute(insert_files_query, filesData)




    db.commit()
    db.close()

if __name__ == '__main__':
    main()
