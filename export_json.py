"""
Module Purpose: Generates a json file containing all information stored in
the database for one or more trials.

input:
output:
"""

import sqlite3
import json

#Enter files accessed in module
dbname = 'main_db.sqlite3'

#Connect to db
conn = sqlite3.connect(dbname)
cur = conn.cursor()

# #Specify nct of trial to display (not sure how useful this will be in future,
# #but good for QC role now)
# specific_nct = raw_input('Enter nct to export: ')
# if len(specific_nct) < 1:
#     nct = 441337
# else:
#     nct = specific_nct

###PLACEHOLDER: nct(s) to export - update to make it more useable later
nct_list = [441337]
nct = 441337

#Define function to format the printing of an item with a list (ie study_design)
def print_comma_list(comma_string):
    print '\tStudy Design:'
    for i in comma_string.split(','):
        print '\t\t', i.lstrip()
    return None

#Define function that returns an 8 digit string from an int (for NCT id)
def int_to_str8(number):
    str_number = str(number)
    return str_number.zfill(8)

#Define function that runs a sql query to find all information contained in
#Trials table for a specific trial based on its nct
#Returns a dictionary containing this data
def get_Trials_data(nct):
    """TBD"""

    #Create sql query here, to be used below
    sql_script = """SELECT Trials.nct,
                            Trials.brief_title,
                            Trials.officiaL_title,
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
                            Sponsor_Type.sponsor_type,
                            Phases.phase
                    FROM Trials
                        JOIN Study_Type
                        JOIN Study_Design
                        JOIN Sponsor
                        JOIN Sponsor_Type
                        JOIN Phases
                    ON
                        Trials.study_type_id = Study_Type.id AND
                        Trials.study_design_id = Study_Design.id AND
                        Trials.sponsor_id = Sponsor.id AND
                        Sponsor.sponsor_type_id = Sponsor_Type.id AND
                        Trials.phase_id = Phases.id
                    WHERE Trials.nct = ?"""

    #Execute sql query script
    cur.execute(sql_script, (nct,))

    #Store results of query in a variable
    query_results = cur.fetchall()

    #Check to make sure that only one row was returned in query, and raise a
    #ValueError if there was more than one returned
    if len(query_results) > 1:
        raise ValueError('More than one row was returned in get_Trials_info query')

    #Create dict to store data
    nct_dict = dict()

    #Iterate through query_results and store items in nct_dict
    for i in query_results:

        nct_dict['nct'] = int_to_str8(i[0])
        nct_dict['brief_title'] = i[1]
        nct_dict['official_title'] = i[2]
        nct_dict['status'] = i[3]
        nct_dict['enrollment'] = i[4]
        nct_dict['start_date'] = i[5]
        nct_dict['completion_date'] = i[6]
        nct_dict['primary_completion_date'] = i[7]
        nct_dict['verification_date'] = i[8]
        nct_dict['last_changed_date'] = i[9]
        nct_dict['index_date'] = i[10]
        nct_dict['study_type'] = i[11]
        nct_dict['study_design'] = i[12]
        nct_dict['sponsor'] = i[13]
        nct_dict['sponsor_type'] = i[14]
        nct_dict['phase'] = i[15]

    return nct_dict


#Define function that runs a sql query to find all information contained in
#Endpoints table for a specific trial basd on its nct
#Returns a dict with the following k/v pairs:
    #primary_endpoints: list of primary endpoints
    #secondary_endpoints: list of secondary endpoints
def get_Endpoints_data(nct):
    """TBD"""

    #Create sql query here, to be used below
    sql_script = """SELECT Endpoints.endpoint_type,
                            Endpoints.endpoint
                    FROM Trials
                        JOIN Endpoint_Link
                        JOIN Endpoints
                    ON
                        Trials.nct = Endpoint_Link.nct_id AND
                        Endpoint_Link.endpoint_id = Endpoints.id
                    WHERE Trials.nct = ?"""

    #Execute sql query script
    cur.execute(sql_script, (nct,))

    #Store results of query in a variable
    query_results = cur.fetchall()

    #Create lists to store primary and secondary endpoints found in db
    primary_endpoints = list()
    secondary_endpoints = list()

    #iterate through results and add endpoints to their respective lists
    for row in query_results:
        if row[0] == 1:
            primary_endpoints.append(row[1])

        if row[0] == 2:
            secondary_endpoints.append(row[1])

    #Create dict to store data
    nct_dict = dict()

    #Store both lists in nct_dict
    nct_dict['primary_endpoints'] = primary_endpoints
    nct_dict['secondary_endpoints'] = secondary_endpoints

    return nct_dict


#Define function that runs a sql query to find all information contained in
#Country table for a specific trial basd on its nct
#Returns a dict with one k/v pair:
    #countries: list of study countries
def get_Country_data(nct):
    """TBD"""

    #Create sql query here, to be used below
    sql_script = """SELECT Country.country

                    FROM Trials
                        JOIN Country_Link
                        JOIN Country
                    ON
                        Trials.nct = Country_Link.nct_id AND
                        Country_Link.country_id = Country.id
                    WHERE Trials.nct = ?"""

    #Execute sql query script
    cur.execute(sql_script, (nct,))

    #Store results of query in a variable
    query_results = cur.fetchall()

    #list comprehension to iterate through results and add countries to list
    countries = [i[0] for i in query_results]

    #Create dict to store data
    nct_dict = dict()

    #Store both lists in nct_dict
    nct_dict['country'] = countries

    return nct_dict


#Define main function of module: reads a list of trials' ncts and returns
#a JSON file of all information contained within the database for those trials
def generate_json(nct_list):
    """TBD"""

    #Create list that will store all trial dicts, which will be converted to JSON
    trials_list = list()

    #Iterate through trials in nct_list and create dictionaries that contain
    #all data for each trial
    for nct in nct_list:

        Trials_dict = get_Trials_data(nct)

        Endpoints_dict = get_Endpoints_data(nct)

        Country_dict = get_Country_data(nct)

        #Merge dictionaries into one dictionary
        #### TO BE COMPLETED

    #CHANGE THIS ONCE I HAVE COMPLETED THE FUNCTION: RETURN ONE DICT
    return (Trials_dict, Endpoints_dict, Country_dict)




#####################################
###########    TESTING    ###########
#####################################

test_dicts = generate_json(nct_list)

for test_dict in test_dicts:
    for k, v in test_dict.iteritems():
        print '{}: {}'.format(k,v)
    print '---\n'


###########################################################################
###########################################################################
###########################################################################

# Have all of these functions create one big dict (heh), which can the be encoded to json!!
# Data within a k/v pair that has more levels should probably be saved as a dict of dicts if possible
# Check how to best do this though BEFORE YOU START!!
#
# USE JSON CREATED HERE TO CREATE THE 'NEW' TRIAL CLASS TYPE - MAKES THE MOST SENSE!!!!!
# THIS JSON CAN THEREFORE BE EXPORTED TO ANY PROGRAM, INCLUDING MY FIDELITY CHECK PROGRAM (OR A BETTER NAME...)
# see this page for reference: http://stackoverflow.com/questions/23110383/how-to-dynamically-build-a-json-object-with-python
#
# Everything below should be moved to the functions above to assign k/v's.
# Can just manipulate the dict to print in whatever format I want.

###########################################################################
###########################################################################
###########################################################################







####Legacy code below, for reference and in case its useful later


#Define function that returns a tuple of all data stored in the Trial table of a trial
    #Used nct_param to make this function iterable and to reduce naming confusion
def get_Trials_info(nct_param):
    """TBD"""

    sql_script = """SELECT Trials.nct,
                            Trials.brief_title,
                            Trials.officiaL_title,
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
                            Sponsor_Type.sponsor_type,
                            Phases.phase
                    FROM Trials
                        JOIN Study_Type
                        JOIN Study_Design
                        JOIN Sponsor
                        JOIN Sponsor_Type
                        JOIN Phases
                    ON
                        Trials.study_type_id = Study_Type.id AND
                        Trials.study_design_id = Study_Design.id AND
                        Trials.sponsor_id = Sponsor.id AND
                        Sponsor.sponsor_type_id = Sponsor_Type.id AND
                        Trials.phase_id = Phases.id
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


def print_Trials_info(Trials_info):
    """TBD"""

    for i in Trials_info:
        print 'Tracking Information:'
        print '\tNCT: {}'.format(int_to_str8(i[0]))
        print '\tLast Changed Date: {}'.format(i[9])
        print '\tStart Date: {}'.format(i[5])
        print '\tPrimary Completion Date: {}'.format(i[7])


        print 'Currently Uncategorized Information:'
        print '\tBrief Title: {}'.format(i[1])
        print '\tOfficial Title: {}'.format(i[2])
        print '\tStatus: {}'.format(i[3])
        print '\tPhase: {}'.format(i[15])
        print '\tEnrollment: {}'.format(i[4])
        print '\tCompletion Date: {}'.format(i[6])
        print '\tVerification Date: {}'.format(i[8])
        print '\tIndex Date: {}'.format(i[10])
        print '\tStudy Type: {}'.format(i[11])
        print_comma_list(i[12])
        print '\tSponsor: {}'.format(i[13])
        print '\tSponsor Type: {}'.format(i[14])

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


# Trials_info = get_Trials_info2(nct)
# Endpoints_info = get_Endpoints_info(nct)
#
# print_Trials_info(Trials_info)
# print_Endpoints_info(Endpoints_info)

# print '\n\n\n\n\n'
# print Endpoints_info['primary_endpoints']
