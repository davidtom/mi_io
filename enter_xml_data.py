"""TO BE COMPLETED - reads data from a folder containing xmls files and enters
it into a database (defined in module); for use with first data pull only(?).
"""

import sqlite3
import os
import re
import create_trial as CT

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

# def insert_from_xml(folderpath):
#     """TO BE COMPLETED - reads data from a folder containing xmls files and enters
#     it into a database (defined in module); for use with first data pull only(?).
#     """

#Iterate through all nct*.xml files in the folderpath
for xml in get_nct_list(folderpath):

    #Create an object of class Trial from current xml file
    active_trial = CT.Trial(folderpath + xml)

    #Create local variables for all attributes of the trial
    primary_completion_date = active_trial.get_primary_completion_date()

    status = active_trial.get_status()

    lead_sponsor_type = active_trial.get_lead_sponsor_type()

    start_date = active_trial.get_start_date()

    intervention = active_trial.get_intervention()

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

    #Input trial's lead_sponsor into Sponsor_Type table and store corresponding id
    sponsor_type_id = insert_2column_table('Sponsor_Type', 'sponsor_type', lead_sponsor_type)

    #Input trial's study_type into Study_Type table and store corresponding id
    study_type_id = insert_2column_table('Study_Type', 'study_type', study_type)

    #Input trial's study_design into Study_Design table and store corresponding id
    study_design_id = insert_2column_table('Study_Design', 'study_design', study_design)

    #Input trial's phase into Phases table and store corresponding id
    phase_id = insert_2column_table('Phases', 'phase', phase)

    #Iterate through tuple of countries in trial and input each into Country table
    #also store each corresponding id and enter it into Country_Link table, along with nct_id
    for item in country:
        country_id = insert_2column_table('Country', 'country', item)

        ##TO DO: Populate Country_Link table

    #Iterate through tuple of conditions in trial and input each into Conditions table
    #also store each corresponding id and enter it into Conditions_Link table, along with nct_id
    for item in condition:
        condition_id = insert_2column_table('Conditions', 'condition', item)

        ##TO DO: conditions like NSCLC and RCC are listed in multiple ways. Need to bucket these now
        ##TO DO: populate Conditions_Link table


    #Intervention dict info to enter: intervention_name, type, study_arm, and other_name
    ####

    conn.commit()


# if  __name__ == "__main__":
#     print insert_from_xml(folderpath)
