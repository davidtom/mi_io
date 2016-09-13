"""TO BE COMPLETED - reads data from a folder containing xmls files and enters
it into a database (defined in module); for use with first data pull only(?).
"""

import sqlite3
import os
import re
import create_trial as CT

#Enter files accessed in module
dbname = 'maindb.sqlite3'
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

    print lead_sponsor

# if  __name__ == "__main__":
#     print insert_from_xml(folderpath)
