"""
Module Purpose: Generate a dashboard showing all relevant information for
a trial and its interventions

input: sqlite3 database(main_db)
output: Dashboard of information on a trial and its interventions
"""

import sqlite3
import json

#Enter files accessed in module
dbname = 'main_db.sqlite3'

#Connect to db
conn = sqlite3.connect(dbname)
cur = conn.cursor()

#Specify nct of trial to display (not sure how useful this will be in future,
#but good for QC role now)
specific_nct = raw_input('Enter nct to display: ')
if len(specific_nct) < 1:
    nct = 441337
else:
    nct = specific_nct

#Define function to format the printing of an item with a list
def print_comma_list(comma_string):
    print '\tStudy Design:'
    for i in comma_string.split(','):
        print '\t\t', i.lstrip()
    return None

#Define function that returns an 8 digit string from an int (for NCT id)
def int_to_str8(number):
    str_number = str(number)
    return str_number.zfill(8)

#Define function that returns a tuple of all data stored in the Trial table of a trial
    #Used nct_param to make this function iterable and to reduce naming confusion
def get_Trials_info(nct_param):
    """TBD"""

    sql_script = """SELECT Trials.nct,
                            Trials.status,
                            Trials.enrollment,
                            Trials.start_date,
                            Trials.completion_date,
                            Trials.primary_completion_date,
                            Trials.verification_date,
                            Trials.last_changed_date,
                            Trials.index_date,
                            Study_Type.study_type,
                            Study_Design.study_design,
                            Sponsor.sponsor_name,
                            Sponsor_Type.sponsor_type
                    FROM Trials
                        JOIN Study_Type
                        JOIN Study_Design
                        JOIN Sponsor
                        JOIN Sponsor_Type
                    ON
                        Trials.study_type_id = Study_Type.id AND
                        Trials.study_design_id = Study_Design.id AND
                        Trials.sponsor_id = Sponsor.id AND
                        Sponsor.sponsor_type_id = Sponsor_Type.id
                    WHERE Trials.nct = ?"""

    cur.execute(sql_script, (nct_param,))

    return cur.fetchall()


#Define function that returns a dictionary, which contains two keys:
    #primary_endpoints and secondar_endpoints. Values are tuples of the
        #respective endpoints
    #Used nct_param to make this function iterable and to reduce naming confusion
def get_Endpoints_info(nct_param):
    """TBD"""

    sql_script = """SELECT Endpoints.endpoint_type,
                            Endpoints.endpoint
                    FROM Trials
                        JOIN Endpoint_Link
                        JOIN Endpoints
                    ON
                        Trials.nct = Endpoint_Link.nct_id AND
                        Endpoint_Link.endpoint_id = Endpoints.id
                    WHERE Trials.nct = ?"""

    cur.execute(sql_script, (nct_param,))

    endpoints_dict = dict()
    primary_endpoints = list()
    secondary_endpoints = list()

    for row in cur.fetchall():
        if row[0] == 1:
            primary_endpoints.append(row[1])

        if row[0] == 2:
            secondary_endpoints.append(row[1])

    endpoints_dict['primary_endpoints'] = primary_endpoints
    endpoints_dict['secondary_endpoints'] = secondary_endpoints

    return endpoints_dict

###########################################################################
###########################################################################
###########################################################################

Have all of these functions create one big dict (heh), which can the be encoded to json!!
Data within a k/v pair that has more levels should probably be saved as a dict of dicts if possible
Check how to best do this though BEFORE YOU START!!

USE JSON CREATED HERE TO CREATE THE 'NEW' TRIAL CLASS TYPE - MAKES THE MOST SENSE!!!!!
THIS JSON CAN THEREFORE BE EXPORTED TO ANY PROGRAM, INCLUDING MY FIDELITY CHECK PROGRAM (OR A BETTER NAME...)
see this page for reference: http://stackoverflow.com/questions/23110383/how-to-dynamically-build-a-json-object-with-python

Everything below should be moved to the functions above to assign k/v's.
Can just manipulate the dict to print in whatever format I want.

###########################################################################
###########################################################################
###########################################################################

def print_Trials_info(Trials_info):
    """TBD"""

    for i in Trials_info:
        print 'Tracking Information:'
        print '\tNCT: {}'.format(int_to_str8(i[0]))
        print '\tLast Changed Date: {}'.format(i[7])
        print '\tStart Date: {}'.format(i[3])
        print '\tPrimary Completion Date: {}'.format(i[5])


        print 'Currently Uncategorized Information:'
        print '\tStatus: {}'.format(i[1])
        print '\tEnrollment: {}'.format(i[2])
        print '\tCompletion Date: {}'.format(i[4])
        print '\tVerification Date: {}'.format(i[6])
        print '\tIndex Date: {}'.format(i[8])
        print '\tStudy Type: {}'.format(i[9])
        print_comma_list(i[10])
        print '\tSponsor: {}'.format(i[11])
        print '\tSponsor Type: {}'.format(i[12])

    return None


def print_Endpoints_info(Endpoints_info):
    """TBD"""

    print "Primary Endpoints:"
    for row in Endpoints_info['primary_endpoints']:
        print '\t*: {}'.format(row)

    print "Secondary Endpoints:"
    for row in Endpoints_info['secondary_endpoints']:
        print '\t*: {}'.format(row)

    return None


Trials_info = get_Trials_info(nct)
Endpoints_info = get_Endpoints_info(nct)

print_Trials_info(Trials_info)
print_Endpoints_info(Endpoints_info)

print '\n\n\n\n\n'
print Endpoints_info['primary_endpoints']
