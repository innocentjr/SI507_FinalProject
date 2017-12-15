import csv

def state_abr():
    states_abr = []
    states_dict = {}
    with open('states.csv', 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            states_abr.append(row)
            #print (row[0]
    states_abr.pop(0)
    for each in states_abr:
        states_dict[each[0]] = each[1]
    return states_dict

def abr():
    states_abr = []
    states_dict = {}
    with open('states.csv', 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            states_abr.append(row[1])
    states_abr.pop(0)
    return states_abr
    #return states_abr
