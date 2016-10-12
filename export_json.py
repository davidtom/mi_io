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
nct_list = [1592370, 441337]
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

#Define function to merge multiple dictionaries
def merge_dicts(*dict_args):
    '''
    Given any number of dicts, shallow copy and merge into a new dict,
    precedence goes to key value pairs in latter dicts.
    '''
    result = {}
    for dictionary in dict_args:
        result.update(dictionary)
    return result

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

    #Store results of query in a variable as a list of tuples
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

    #Store results of query in a variable as a list of tuples
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

    #Store results of query in a variable as a list of tuples
    query_results = cur.fetchall()

    #list comprehension to iterate through results and add countries to list
    countries = [i[0] for i in query_results]

    #Create dict to store data
    nct_dict = dict()

    #Store list in nct_dict
    nct_dict['country'] = countries

    return nct_dict

#Define function that runs a sql query to find all information contained in
#Conditions table for a specific trial based on its nct
#Returns a dict with one k/v pair:
    #countries: list of conditions
def get_Conditions_data(nct):
    """TBD"""

    #Create sql query here, to be used below
    sql_script = """SELECT Conditions.condition

                    FROM Trials
                        JOIN Conditions_Link
                        JOIN Conditions
                    ON
                        Trials.nct = Conditions_Link.nct_id AND
                        Conditions_Link.condition_id = Conditions.id
                    WHERE Trials.nct = ?"""

    #Execute sql query script
    cur.execute(sql_script, (nct,))

    #Store results of query in a variable as a list of tuples
    query_results = cur.fetchall()

    #list comprehension to iterate through results and add conditions to list
    conditions = [i[0] for i in query_results]

    #Create dict to store data
    nct_dict = dict()

    #Store list in nct_dict
    nct_dict['condition'] = conditions

    return nct_dict


#Define function that runs a sql query to find all information contained in
#Study_Arms table for a specific trial basd on its nct
#Returns a list of dicts, each dict being the data for one study arm
def get_StudyArms_data(nct):
    """TBD"""

    #Create sql query here, to be used below
    sql_script = """SELECT Study_Arms.id, Study_Arms.arm_label

                    FROM Study_Arms
                        JOIN Trials
                    ON
                        Study_Arms.nct_id = Trials.nct
                    WHERE Trials.nct = ?"""

    #Execute sql query script
    cur.execute(sql_script, (nct,))

    #Store results of query in a variable as a list of tuples
    query_results = cur.fetchall()

    #Create a list to store data for each study arm (each arm will be its own dict)
    study_arms_list = list()

    #iterate through results and construct a dict for each study arm
    #dict contains: arm_label and interventions (another list of dicts)
    #append that dict to study_arms_list
    for row in query_results:

        #Store Study_Arms.id as a variable that can be passed to another fx/query
        study_arms_id = row[0]

        #Create a dict to hold information for one study arm
        study_arm_dict = dict()

        #Add 'label' key and value to study_arm_dict
        study_arm_dict['label'] = row[1]

        #Add 'interventions' key and value to study_arm_dict
        study_arm_dict['interventions'] = get_Interventions_data(study_arms_id)

        #Append study_arm_dict to study_arms_list
        study_arms_list.append(study_arm_dict)

    #Create dict to store data for all trial study_arms
    study_arms_dict = dict()

    #Store study_arms_list in study_arms_dict
    study_arms_dict['study_arms'] = study_arms_list

    return study_arms_dict

##Function that I will create below should do the same steps as above, except for interventions. This data
### should then be added to each individual study_arm_dict, with the key being set
#### equal to the output of the new function (will be a list of dicts). see shell code written on line 277

#Define function that runs a sql query to find all information contained in
#Interventions table for a specific study arm of a trial basd on its Study_Arms.id
#Returns a list of dicts, each dict being the data for one intervention of a study arm
def get_Interventions_data(study_arms_id):
    """TBD"""

#Create sql query here, to be used below
    sql_script = """SELECT Interventions.id,
                            Interventions.intervention,
                            Intervention_Type.intervention_type

                    FROM Study_Arms
                        JOIN Interventions_Link
                        JOIN Interventions
                        JOIN Intervention_Type
                    ON
                        Study_Arms.id = Interventions_Link.study_arm_id AND
                        Interventions_Link.intervention_id = Interventions.id AND
                        Interventions.intervention_type_id = Intervention_Type.id
                    WHERE Study_Arms.id = ?"""

    #Execute sql query script
    cur.execute(sql_script, (study_arms_id,))

    #Store results of query in a variable as a list of tuples
    query_results = cur.fetchall()

    #Create a list to store data for each intervention (each intervention will be its own dict)
    interventions_list = list()

    #iterate through results and construct a dict for each intervention
    #dict contains: name, type, other names (a list), and MoA
    #append that dict to interventions_list
    for row in query_results:

        #Store Interventions.id as a variable that can be passed to another fx/query
        interventions_id = row[0]

        #Create a dict to hold information for one study arm
        intervention_dict = dict()

        #Add key and value pairs to intervention_dict
        intervention_dict['intervention_name'] = row[1]
        intervention_dict['intervention_type'] = row[2]
        # intervention_dict['MoA'] = row[3] NEED TO CREATE MoA TABLE FIRST
        intervention_dict['intervention_other_names'] = get_InterventionOtherNames_data(interventions_id)

        #Append study_arm_dict to study_arms_list
        interventions_list.append(intervention_dict)

    return interventions_list


#Define function that runs a sql query to find all information contained in
#Intervention_Other_Names table for a specific intervention basd on its Interventions.id
#Returns a list of other names for the intervention
def get_InterventionOtherNames_data(interventions_id):
    """TBD"""

    #Create sql query here, to be used below
    sql_script = """SELECT Intervention_Other_Names.other_name

                    FROM Intervention_Other_Names
                        JOIN Interventions
                    ON
                        Intervention_Other_Names.intervention_id = Interventions.id
                    WHERE Interventions.id = ?"""

    #Execute sql query script
    cur.execute(sql_script, (interventions_id,))

    #Store results of query in a variable as a list of tuples
    query_results = cur.fetchall()

    #list comprehension to iterate through results and add conditions to list
    other_names = [i[0] for i in query_results]

    return other_names


#Define function that creates a single dictionary for all trial data stored
#in database
def create_trial_dict(nct):
    """TBD"""

    Trials_dict = get_Trials_data(nct)

    Endpoints_dict = get_Endpoints_data(nct)

    Country_dict = get_Country_data(nct)

    Conditions_dict = get_Conditions_data(nct)

    StudyArms_dict = get_StudyArms_data(nct)

    #Merge and return the individual dicts
    return merge_dicts(Trials_dict, Endpoints_dict, Country_dict, Conditions_dict, StudyArms_dict)

#Define a function that takes a list of trial ncts and returns a JSON file of
#all information contained within the database for that/those trials
###PARAMETER MUST BE A LIST!
def generate_json(nct_list):
    """TBD"""

    #Create list that will store all trial dicts, which will be converted to JSON
    trials_list = list()

    #Iterate through trials in nct_list and create a dictionary that contains
    #all data for each trial. append that dict to trials_list
    for nct in nct_list:

        trials_list.append(create_trial_dict(nct))

    return json.dumps(trials_list)

#####################################
###########    TESTING    ###########
#####################################

def run_test(command):
    if command == 1:
        for test_dict in test_dicts:
            for k, v in test_dict.iteritems():
                print '{}: {}'.format(k,v)
            print '---\n'
    else:
        return None

test_json = generate_json(nct_list)

parsed_json = json.loads(test_json)

print parsed_json[0]['nct']
print parsed_json[1]['study_arms'][1]['label']


# for i in test_dicts:
#     print i
#     print '-'*30, '\n'

run_test(0)

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
