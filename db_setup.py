# Import statements
import psycopg2
from states_abr import *
import csv
#from config import *
import json
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import sys
import psycopg2.extras

conn, cur = None, None
db_name = "payforsuccessprojects"
# Write code / functions to set up database connection and cursor here.
#comment

def get_connection_and_cursor():
    global conn, cur, db_name
    try:
        conn = psycopg2.connect("dbname='{}' user='{}' password='{}'".format(db_name, db_user, db_password)) # No password on the databases yet -- wouldn't want to save that in plain text, anyway
# Remember: need to, at command prompt or in postgres GUI: createdb test507_music (or whatever db name is in line ^)
        print("Success connecting to database")

    except:
        try:
            conn = psycopg2.connect("dbname='postgres' user='{}' password='{}'".format(db_user, db_password)) # No password on the databases yet -- wouldn't want to save that in plain text, anyway
            conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
            cur = conn.cursor()
            sql = """CREATE DATABASE """
            cur.execute(sql + db_name)
            cur.close()
            conn.close()
            conn = psycopg2.connect("dbname='{}' user='{}' password='{}'".format(db_name, db_user, db_password)) # No password on the databases yet -- wouldn't want to save that in plain text, anyway
            #Remember: need to, at command prompt or in postgres GUI: createdb test507_music (or whatever db name is in line ^)
            print("Success connecting to database")

        except:
            print("Unable to connect to the database. Check server and credentials.")
            sys.exit(1) # Stop running program if there's no db connection.

## SETUP FOR CREATING DATABASE AND INTERACTING IN PYTHON
# cur = conn.cursor()
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor) # So you can insert by column name, instead of position, which makes the Python code even easier to write!
    return conn, cur

# Write code / functions to create tables with the columns you want and all database setup here.
def setup_database(conn, cur):
## Code to DROP TABLES IF EXIST IN DATABASE (so no repeats
## We'll address this idea in more depth later.
    cur.execute("DROP TABLE IF EXISTS Master, Project, Legislation, Project_Partners, Opportunity, Project_Financing CASCADE")
    conn.commit()

    cur.execute("""CREATE TABLE Master(
            ID SERIAL PRIMARY KEY,
            Name VARCHAR(255) UNIQUE,
            Address VARCHAR(255),
            Level VARCHAR(255),
            Activity VARCHAR(40),
            Link TEXT,
            Tag VARCHAR(120))
            """)
    conn.commit()

    cur.execute("""CREATE TABLE Project(
        ID SERIAL PRIMARY KEY,
        Name VARCHAR(255) UNIQUE,
        Project_ID INTEGER REFERENCES Master(ID) NOT NULL,
        Phase VARCHAR(128),
        Level VARCHAR(255),
        "Level Name" VARCHAR(255),
        State VARCHAR(255),
        Motivation TEXT,
        Objective TEXT,
        "Population Served" VARCHAR(255),
        Geography VARCHAR(255),
        "Issue Area" VARCHAR(255)
        )""")
    conn.commit()

    cur.execute("""CREATE TABLE Project_Partners(
        ID SERIAL PRIMARY KEY,
        Project_ID INTEGER REFERENCES Project(ID) NOT NULL,
        "Service Provider" VARCHAR(255),
        Payor VARCHAR(255),
        "Transaction Coordinator" VARCHAR(255),
        Evaluator VARCHAR(255),
        Validator VARCHAR(255),
        "Project Manager" VARCHAR(255),
        "External Counsel" VARCHAR(255),
        "Technical Assistance" VARCHAR(255)
        )""")
    conn.commit()

    cur.execute("""CREATE TABLE Legislation(
        ID SERIAL PRIMARY KEY,
        Name VARCHAR(255) UNIQUE,
        Project_ID INTEGER REFERENCES Master(ID) NOT NULL,
        "Document Type" VARCHAR(40),
        "Source Link" VARCHAR(255),
        Download VARCHAR(255)
        )""")
    conn.commit()

    cur.execute("""CREATE TABLE Opportunity(
        ID SERIAL PRIMARY KEY,
        Name VARCHAR(255) UNIQUE,
        Project_ID INTEGER REFERENCES Master(ID) NOT NULL,
        Download VARCHAR(255),
        Status VARCHAR(40),
        "Available Funding" VARCHAR(40),
        Stakeholders TEXT,
        Interventions VARCHAR(255),
        "Issue Areas" VARCHAR(255)
        )""")
    conn.commit()

    cur.execute("""CREATE TABLE Project_Financing(
        ID SERIAL PRIMARY KEY,
        Project_ID INTEGER REFERENCES Project(ID) NOT NULL,
        "Senior Debt" TEXT,
        "Junior Debt" TEXT,
        "Deferred Fee" VARCHAR(255),
        "Recoverable Grant" VARCHAR(255),
        "Non-recoverable Grant" VARCHAR(255),
        Guarantor VARCHAR(255),
        "Initial Investment" VARCHAR(128),
        "Max Repayment by Payor" VARCHAR(255),
        "Service Term" VARCHAR(128),
        "Repayment Period" VARCHAR(255),
        "Interim Outomces" TEXT,
        Recycling TEXT
        )""")
    conn.commit()

# Write code / functions to deal with CSV files and insert data into the database here.

#def insert_master(conn, cur, key, master):
    #"""Inserts an state and returns name, None if unsuccessful"""
    #sql = """INSERT INTO Master(Name, Address, Activity, Link, Tag) VALUES(%s, %s, %s, %s, %s)"""
    #cur.execute(sql, (key, master[key]["Address"], master[key]["Activity"], master[key]["Link"], master[key]["Tag"] ))
    #conn.commit()
    #print("Entry executed")

#def search_id(search, conn, cur):
        #sql = """SELECT ID FROM Master where name = %s"""
        #cur.execute(sql, (search,))
        #data = ''.join(map(str,cur.fetchone()))
        #return data

#def insert_legislation(legis, conn, cur):
    #"""Returns True if succcessful, False if not"""
    #legis_id = search_id(legis.name, conn, cur)
    #sql = """INSERT INTO Legislation(Name, Project_ID, "Document Type", "Source Link", Download) VALUES(%s, %s, %s, %s, %s)"""
    #cur.execute(sql,(legis.name, legis_id, legis.document_type, legis.source_link, legis.download_link ))
    #conn.commit()
    #return True


# Write code to be invoked here (e.g. invoking any functions you wrote above)

#if __name__ == '__main__':

#    db_user = str(input("Please enter user name: "))
#    db_password = str(input("Please enter password: "))

#    conn, cur = get_connection_and_cursor()
#    setup_database(conn, cur)
