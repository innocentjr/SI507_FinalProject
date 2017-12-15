from set_up import *
from class_def import *
import copy
from states_abr import *
from db_setup import *
from time import sleep # this should go at the top of the file
from selenium import webdriver
from urllib.request import urlopen
from bs4 import BeautifulSoup
import re
import json
from viz import *

Project_instances = []
Legislation_instances = []
Opportunity_instances = []
conn, cur = None, None
dbname = "payforsuccessprojects"
IssueAreas = ["Mental Health", "Child Welfare", "Environment", "Criminal Justice", "Workforce", "Early Childhood", "Homelessness", "Recidivism", "Education", "Environment", "Health", "Maternal and Child Health"]

set_me_up()

with open('Master.json', 'r') as f:
    master = json.loads(f.read())
    f.close()

dic_keys = []
for key in master.keys():
    dic_keys.append(key)

randd = dic_keys[0]

try:
    attempt = master[randd]["filename"]
except:
    counter = 0
    for each in master:
        master[each]["filename"] = "project{}.html".format(counter)
        counter += 1

with open('Master.json', 'w') as f:
    dumping = json.dumps(master, indent = 4, sort_keys = True)
    f.write(dumping)
    f.close()

def connect_cache(dictionary):
    try:
        with open(dictionary['filename'], 'r', encoding='utf-8') as f:
            html = f.read()
            f.close()
        bsObj = BeautifulSoup(html, "html.parser")

    except:
        cache_link = dictionary["Link"]

        base_url = 'http://www.payforsuccess.org'
        #with open('test.html', 'r', encoding='utf-8') as f:
            #html = f.read()
            #f.close()

        driver = webdriver.Chrome()
        driver.get(base_url+cache_link);

        #page_source is a variable created by Selenium - it holds all the HTML
        html = driver.page_source
        #with open('test.html', 'r', encoding='utf-8') as f:
        #    html = f.read()
        #    f.close()

        bsObj = BeautifulSoup(html, "html.parser")
        bsObj2 = bsObj.prettify()


        with open(dictionary['filename'], 'w', encoding='utf-8') as f:
            f.write(bsObj2)
            f.close()

        driver.quit()

    return bsObj

dic_keys = []
for key in master.keys():
    dic_keys.append(key)

counter = 0

for key in dic_keys:
    if master[key]["Activity"] == "Legislation":
        legislation = connect_cache(master[key])
        main = legislation.find('div', {'class':"main"})
        status = legislation.find('a').get_text().strip()
        content = legislation.find('div', {'class':"content"})
        aside = legislation.find('aside', {'class':"sidebar"})
        interventions = aside.find('div', {'class':"facts__row"})
        content_sec = legislation.find('div', {'class':"facts__content"})
        l_object = Legislation(aside, content_sec)
        l_object.name = key
        l_object.address = master[key]["Address"]
        print(l_object)
        Legislation_instances.append(l_object)

    if master[key]["Activity"] == "Project":
        project = connect_cache(master[key])
        main = project.find('div', {'class':"main"})
        status = project.find('a').get_text().strip()
        content = project.find('div', {'class':"content"})
        teaser = main.find('div', {"class":"teasers"})
        aside = project.find('aside', {'class':"sidebar"})
        interventions = aside.find('div', {'class':"facts__row"})
        content_sec = project.find('div', {'class':"facts__content"})
        p_object = Project(aside, content, teaser, content_sec)
        p_object.name = key
        p_object.address = master[key]["Address"]
        print(p_object)
        Project_instances.append(p_object)

    if master[key]["Activity"] == "Opportunity":
        opportunity = connect_cache(master[key])
        main = opportunity.find('div', {'class':"main"})
        status = opportunity.find('a').get_text().strip()
        content = opportunity.find('div', {'class':"content"})
        aside = opportunity.find('aside', {'class':"sidebar"})
        interventions = aside.find('div', {'class':"facts__row"})
        content_sec = opportunity.find('div', {'class':"facts__content"})
        o_object = Opportunity(aside, content_sec)
        o_object.name = key
        o_object.address = master[key]["Address"]
        print(o_object)
        Opportunity_instances.append(o_object)

def sendInstances():
    return Project_instances

def insert_master(conn, cur, key, master):
    """Inserts an state and returns name, None if unsuccessful"""
    sql = """INSERT INTO Master(Name, Address, Activity, Link, Tag) VALUES(%s, %s, %s, %s, %s)"""
    cur.execute(sql, (key, master[key]["Address"], master[key]["Activity"], master[key]["Link"], master[key]["Tag"] ))
    conn.commit()
    print("Entry executed")

def search_id(search, conn, cur):
    sql = """SELECT ID FROM Master where name = %s"""
    cur.execute(sql, (search,))
    data = ''.join(map(str,cur.fetchone()))
    return data

def search_project(search, conn, cur):
    sql = """SELECT ID FROM Project where name = %s"""
    cur.execute(sql, (search,))
    data = ''.join(map(str,cur.fetchone()))
    return data

def insert_legislation(legis, conn, cur):
    """Returns True if succcessful, False if not"""
    legis_id = search_id(legis.name, conn, cur)
    sql = """INSERT INTO Legislation(Name, Project_ID, "Document Type", "Source Link", Download) VALUES(%s, %s, %s, %s, %s)"""
    cur.execute(sql,(legis.name, legis_id, legis.document_type, legis.source_link, legis.download_link ))
    conn.commit()
    print("Entry executed")

def insert_opportunity(opportunity, conn, cur):
    """Returns True if succcessful, False if not"""
    opportunity_id = search_id(opportunity.name, conn, cur)
    sql = """INSERT INTO Opportunity(Name, Project_ID, Status, "Available Funding", Stakeholders, Interventions, "Issue Areas", Download) VALUES(%s, %s, %s, %s, %s, %s, %s, %s)"""
    cur.execute(sql,(opportunity.name, opportunity_id, opportunity.opportunity_status, opportunity.avail_funding, opportunity.stakeholder, opportunity.interventions, opportunity.np_issue_areas, opportunity.download_link ))
    conn.commit()
    print("Entry executed")

def insert_project(project, conn, cur):
    """Inserts an state and returns name, None if unsuccessful"""
    project_id = search_id(project.name, conn, cur)
    sql = """INSERT INTO Project(Name, Project_ID, Level, "Level Name", State, Phase, Motivation, Objective, "Population Served", Geography, "Issue Area") VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
    cur.execute(sql,(project.name, project_id, project.level, project.level_name, project.level_state, project.phase, project.motivation, project.objective, project.population_served, project.geography, project.p_issue_areas
 ))
    conn.commit()
    print("Entry executed")

def insert_financing(project, conn, cur):
    """Inserts an state and returns name, None if unsuccessful"""
    project_id = search_project(project.name, conn, cur)
    sql = """INSERT INTO Project_Financing(Project_ID, "Senior Debt", "Junior Debt", "Deferred Fee", "Recoverable Grant", "Non-recoverable Grant", Guarantor, "Initial Investment", "Max Repayment by Payor", "Service Term", "Repayment Period", "Interim Outomces", Recycling) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
    cur.execute(sql,(project_id, project.senior_debt, project.junior_debt, project.deferred_fee, project.recoverable_grant, project.non_recoverable, project.guarantor, project.initial_inv, project.max_repayment_by_payor, project.service_term, project.repayment_period, project.interim_outcomes, project.recycling
 ))
    conn.commit()
    print("Entry executed")

def insert_project_partners(project, conn, cur):
    """Inserts an state and returns name, None if unsuccessful"""
    project_id = search_project(project.name, conn, cur)
    sql = """INSERT INTO Project_Partners(Project_ID, "Service Provider", Payor, "Transaction Coordinator", Evaluator, Validator, "Project Manager", "External Counsel", "Technical Assistance") VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s)"""
    cur.execute(sql,(project_id, project.service_provider, project.payor, project.transaction_coordinator, project.evaluator, project.validator, project.project_manager, project.external_counsel, project.technical_assist_provider ))
    conn.commit()
    print("Entry executed")


def get_connect_and_cursor():
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

def get_state(conn, cur, IssueAreas):
    states = abr()
    data = []

    for each in IssueAreas:
        sql = """SELECT state FROM Project WHERE "Issue Area" LIKE '%{}%'""".format(each)
        cur.execute(sql)
        states_request = cur.fetchall()
        for y in states_request:
            if len(y) > 1:
                for x in temp:
                    x = x.strip()
                    lx = [each, x]
                    data.append(lx)
            else:
                x = y[0].strip()
                lx = [each, x]
                data.append(lx)

    twist = copy.deepcopy(data)
    master_list = []

    for i in range(len(data)):
        x = i+1
        count = 1
        while x < len(twist):
            if twist[i] == twist[x]:
                #print(len(twist))
                #print("{} and {} match".format(twist[i], twist[x]))
                #print("Below")
                #print(twist[x])
                twist.pop(x)
                count += 1
            else:
                if x >= len(twist):
                    break
                else:
                    x += 1
                #print(x)
        try:
            #print(twist[i])
            temp = copy.deepcopy(twist[i])
            temp.append(count)
            master_list.append(temp)
        except:
            #print(i)
            pass
    return master_list

def get_levels(conn, cur, IssueAreas):
    states = abr()
    levels = []

    for each in IssueAreas:
        sql = """SELECT level FROM Project WHERE "Issue Area" LIKE '%{}%'""".format(each)
        cur.execute(sql)
        level_results = cur.fetchall()
        for y in level_results:
            if len(y) > 1:
                for x in temp:
                    x = x.strip()
                    lx = [each, x]
                    levels.append(lx)
            else:
                x = y[0].strip()
                lx = [each, x]
                levels.append(lx)

    sweet = copy.deepcopy(levels)
    master_list_levels = []

    for i in range(len(levels)):
        x = i+1
        count = 1
        while x < len(sweet):
            if sweet[i] == sweet[x]:
                #print(len(twist))
                #print(x)
                #print("{} and {} match".format(sweet[i], sweet[x]))
                #print("Below")
                #print(twist[x])
                sweet.pop(x)
                count += 1
            else:
                if x >= len(sweet):
                    break
                else:
                    x += 1
                #print(x)
        try:
            #print(sweet[i])
            temp = copy.deepcopy(sweet[i])
            temp.append(count)
            master_list_levels.append(temp)
        except:
            #print(i)
            pass
    return master_list_levels

if __name__ == '__main__':

    db_user = str(input("Please enter user name: "))
    db_password = str(input("Please enter password: "))

    conn, cur = get_connect_and_cursor()
    setup_database(conn, cur)

    with open('Master.json', 'r') as f:
        master = json.loads(f.read())
        f.close()

    dic_keys = []
    for key in master.keys():
        dic_keys.append(key)

    for key in dic_keys:
        #print(key)
        insert_master(conn, cur, key, master)

    for each in Legislation_instances:
        insert_legislation(each, conn, cur)
        print("Entry completed!")

    for each in Opportunity_instances:
        insert_opportunity(each, conn, cur)
        print("{} has been entered into the database.".format(each.name))

    for each in Project_instances:
        split = each.address.split(";")
        temp = []
        for x in split:
            x = x.strip()
            temp.append(x)
        split = temp
        address = ','.join(map(str, split))
        split = address.split(",")
        if len(split) == 3:
            if 'county' in '**{}**'.format(split[0].lower()):
                each.level = "County"
                each.level_name = split[0]
                each.level_state = split[1]
            else:
                each.level = "City"
                each.level_name = split[0]
                each.level_state = split[1]
        elif len(split) == 2:
            each.level = "State"
            each.level_name = split[0]
            dic = state_abr()
            entry = dic[split[0]]
            each.level_state = entry
        elif len(split) == 6:
            if 'county' in '**{}**'.format(split[0].lower()):
                each.level = "County"
            else:
                each.level = "City"
            level_names = [split[0], split[3]]
            each.level_name = ', '.join(map(str, level_names))
            dic = state_abr()
            if split[1] == split[4]:
                each.level_state = split[1]
            else:
                states_names = [split[1], split[4]]
                each.level_state = ', '.join(map(str, states_names))
        elif len(split) == 4:
            each.level = "State"
            level_names = [split[0], split[2]]
            each.level_name = ', '.join(map(str, level_names))
            dic = state_abr()
            split[0] = dic[split[0]]
            split[2] = dic[split[2]]
            if split[0] == split[2]:
                each.level_state = split[0]
            else:
                states_names = [split[0], split[2]]
                each.level_state = ', '.join(map(str, states_names))
        else:
            each.level = "Multiple"
            each.level_name = "Multiple"
            each.level_state = "Multiple"
        insert_project(each, conn, cur)

        #print(split)
        print("{} has been entered into the database.".format(each.name))

    for each in Project_instances:
        insert_project_partners(each, conn, cur)
        print("{} has been entered into the database.".format(each.name))

    for each in Project_instances:
        insert_financing(each, conn, cur)
        print("{} has been entered into the database.".format(each.name))

    states = get_state(conn, cur, IssueAreas)
    lev = get_levels(conn, cur, IssueAreas)
    dicti = {}
    dicti['states'] = states
    dicti['levels'] = lev

    with open('viz_data.json', 'w') as f:
        dumping = json.dumps(dicti, indent = 4, sort_keys = True)
        f.write(dumping)
        f.close()
#comment
    app.run(host='127.0.0.1', port=5000)
