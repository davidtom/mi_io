"""TO BE COMPLETED - reads data from a folder containing xmls files and enters
it into a database (defined in module); for use with first data pull only(?).
"""

import sqlite3
import os
import re
import csv
import create_trial as CT
import condition_buckets as cb


#Enter files accessed in module
dbname = 'main_db.sqlite3'
foldername = 'test_xml_folder'
folderpath = os.getcwd() + '/' + foldername +'/'


#Connect to db
conn = sqlite3.connect(dbname)
cur = conn.cursor()


#Define function that uses regex to give a list of file names in a folder that start with 'NCT'
def get_nct_list(folderpath):
    """Takes 1 argument: a folder path. Returns a list of file names in
    the folder that begin with 'NCT' and end with 'xml'."""

    nct_list = list()

    #iterate files in list returned by os.listdir() and extend only the ones
    #starting with 'NCT' and ending with '.xml'
    for filename in os.listdir(folderpath):
        nct_list.extend(re.findall('^NCT.*\.xml$', filename))

    return nct_list


#Define function to get methods from a class to make variable assignment easier
def get_methods():
    """Prints a string that can be used to assign all Trial variables using
    their associated .get_*() method"""

    method_list = list()

    #Iterate through a list of all methods in Trial class, keeping only those that start with 'get'
    for i in CT.Trial.__dict__:
        method_list.extend(re.findall('^get.*', i))

    #Print all get methods found above along with additional python syntax
    for i in method_list:
        print i + ' = ' + 'active_trial.' + i + '()'
        print '\n'


#Define function that inputs data into a table with 2 columns (id and a table-specific value),
#and returns a particular value's id (primary key)
def insert_2column_table(table_name, column_name, attribute):
    """Docstring TBD"""

    cur.execute("""
    INSERT OR IGNORE INTO {} ({})
    VALUES (?)""".format(table_name, column_name), (attribute, ))
    cur.execute('SELECT id FROM {} WHERE {} = ?'.format(table_name, column_name), (attribute, ))
    return cur.fetchone()[0]


def insert_3column_table(table_name, column_name1, attribute1, column_name2, attribute2):
    """Docstring TBD"""

    cur.execute("""
    INSERT OR IGNORE INTO {} ({}, {})
    VALUES (?, ?)""".format(table_name, column_name1, column_name2), (attribute1, attribute2))
    cur.execute('SELECT id FROM {} WHERE {} = ?'.format(table_name, column_name1), (attribute1, ))
    return cur.fetchone()[0]


def insert_4column_table(table_name, column_name1, attribute1,
    column_name2, attribute2, column_name3, attribute3):
    """Docstring TBD"""

    cur.execute("""
    INSERT OR IGNORE INTO {} ({}, {}, {})
    VALUES (?, ?, ?)""".format(table_name, column_name1, column_name2, column_name3), (attribute1, attribute2, attribute3))
    cur.execute('SELECT id FROM {} WHERE {} = ?'.format(table_name, column_name1), (attribute1, ))
    return cur.fetchone()[0]


#Define a function that inputs data into a link table. Utilizes a value's id (primary key)
#returned from a previous insert function
def insert_link_table(table_name, column1, column2, attribute1, attribute2):
        cur.execute('''INSERT OR REPLACE INTO {}
            ({}, {}) VALUES ( ?, ? )'''.format(table_name, column1, column2),
            (attribute1, attribute2))
        return None


#Iterate through all nct*.xml files in the folderpath
for xml in get_nct_list(folderpath):

    #Create an object of class Trial from current xml file
    active_trial = CT.Trial(folderpath + xml)

    #Create local variables for all attributes of the trial
    primary_completion_date = active_trial.get_primary_completion_date()

    status = active_trial.get_status()

    lead_sponsor_type = active_trial.get_lead_sponsor_type()

    start_date = active_trial.get_start_date()

    intervention_details = active_trial.get_intervention_details()

    file_name = active_trial.get_file_name()

    completion_date = active_trial.get_completion_date()

    primary_endpoint = active_trial.get_primary_endpoint()

    nct = active_trial.get_nct()

    phase = active_trial.get_phase()

    study_type = active_trial.get_study_type()

    condition = active_trial.get_condition()

    lead_sponsor = active_trial.get_lead_sponsor()

    first_received_date = active_trial.get_first_received_date()

    verification_date = active_trial.get_verification_date()

    last_changed_date = active_trial.get_last_changed_date()

    study_design = active_trial.get_study_design()

    secondary_endpoint = active_trial.get_secondary_endpoint()

    study_arm = active_trial.get_study_arm()

    country = active_trial.get_country()

    #Insert trial's lead_sponsor_type into Sponsor_Type table and store corresponding id
    sponsor_type_id = insert_2column_table('Sponsor_Type', 'sponsor_type', lead_sponsor_type)

    #Insert trial's lead_sponsor and sponsor_type_id into Sponsor table
    #(sponsor_name and sponsor_type_id repsectively)
    sponsor_id = insert_3column_table('Sponsor',
                                        'sponsor_name', lead_sponsor,
                                        'sponsor_type_id', sponsor_type_id)

    #Insert trial's study_type into Study_Type table and store corresponding id
    study_type_id = insert_2column_table('Study_Type', 'study_type', study_type)

    #Insert trial's study_design into Study_Design table and store corresponding id
    study_design_id = insert_2column_table('Study_Design', 'study_design', study_design)

    #Insert trial's phase into Phases table and store corresponding id
    phase_id = insert_2column_table('Phases', 'phase', phase)

    #Iterate through tuple of countries in trial and insert each into Country table
    #also store each corresponding id and enter it into Country_Link table, along with nct_id
    for item in country:
        country_id = insert_2column_table('Country', 'country', item)
        insert_link_table('Country_Link', 'country_id', 'nct_id', country_id, nct)


    #Iterate through tuple of conditions in trial and insert each into Conditions table
    #also store each corresponding id and enter it into Conditions_Link table, along with nct_id
    for item in condition:
        condition_id = insert_2column_table('Conditions', 'condition', cb.bucket_condition(item))
        insert_link_table('Conditions_Link', 'condition_id', 'nct_id', condition_id, nct)


    ###Debug code, delete later
    # print 'nct number::', nct
    # print 'intervention:\n', intervention_details

    #Iterate through dicts contained within intervention_details (1 dict per intervention)
    for item in intervention_details:

        #Insert intervention's type into Intervention_Type table and store intervention_type_id
        intervention_type_id = insert_2column_table('Intervention_Type',
        'intervention_type', item['type'])

        #Insert intervention's name, intervention_type_id and MoA_id
        #(placeholder for now) into Interventions table
        intervention_id = insert_4column_table('Interventions',
        'intervention', item['intervention'],
        'intervention_type_id', intervention_type_id,
        'moa_id', 999)

        #Iterate through items contained within other_name tuple and insert
        #them into Intervention_Other_Names table, along with the corresponding
        #intervention_id
        for name in item['other_name']:
            insert_3column_table('Intervention_Other_Names',
            'other_name', name,
            'intervention_id', intervention_id)

    # Input data into Trials table
    cur.execute("""INSERT OR IGNORE INTO Trials (nct_id,
                                                phase_id,
                                                status,
                                                study_type_id,
                                                study_design_id,
                                                start_date,
                                                completion_date,
                                                primary_completion_date,
                                                verification_date,
                                                last_changed_date,
                                                sponsor_id)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""", (nct,
                                                    phase_id,
                                                    status,
                                                    study_type_id,
                                                    study_design_id,
                                                    start_date,
                                                    completion_date,
                                                    primary_completion_date,
                                                    verification_date,
                                                    last_changed_date,
                                                    sponsor_id))

    ###Debug code, delete later
    #print '---'


    #Tuple of dicts, each dict represents the info for one intervention in the trial (strings AND tuples are values)


    #Intervention dict info to enter: intervention_name, type, study_arm, and other_name
    ####

    conn.commit()
