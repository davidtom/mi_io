"""TBD"""

import csv
import sqlite3
import sys

#Set default encoding as utf-8
reload(sys)
sys.setdefaultencoding('utf-8')

#Define files accessed in module
dbname = 'main_db.sqlite3'

#Connect to db
conn = sqlite3.connect(dbname)
cur = conn.cursor()

###Create functions to recategorize a specific or differently named condition
###into a broader condition 'bucket' (ie NSCLC rather than non-small cell lung cancer)
def bucket_conditions(condition):

    #Define lists to hold name of conditions in a bucket
    NSCLC_list = list()
    RCC_list = list()
    melanoma_list = list()
    prostate_cancer_list = list()

    #open conditions.csv and populate condition buckets
    with open('condition_buckets.csv', 'rU') as csv_file:
        f = csv.reader(csv_file, delimiter=',')

        for row in f:

            #Fill out NSCLC_list
            if row[1] == 'NSCLC':
                NSCLC_list.append(row[0])

            #Fill out RCC_list
            if row[1] == 'RCC':
                RCC_list.append(row[0])

            #Fill out RCC_list
            if row[1] == 'melanoma':
                melanoma_list.append(row[0])

            #Fill out prostate_cancer_list
            if row[1] == 'prostate Cancer':
                prostate_cancer_list.append(row[0])


    #Check if condition matches to NSCLC_list in cb module
    if condition in NSCLC_list:
        return 'NSCLC'

    #Check if condition matches to RCC_list in cb module
    elif condition in RCC_list:
        return 'Renal Cell Carcinoma'

    #Check if condition matches to melanoma_list in cb module
    elif condition in melanoma_list:
        return 'Melanoma'

    #Check if condition matches to melanoma_list in cb module
    elif condition in prostate_cancer_list:
        return 'Prostate Cancer'

    #Return original condition since condition matched to no buckets in cb module
    else:
        return condition


##Create function to read data from moa_list.csv and use it to assign
##interventions the appropriate MoAs. If data does not exist for one, it
##will add that information into moa_list.csv
def sync_moa_list():
    """TBD: higher level function - is not the one checking if a
    specific intervention is in  most_list.csv"""



##def
#########TO DO
#1) Clean up moa_list.csv. Use python to help clean the data! (ie splitting up rows, making sure no repeats)
#1.5) Recreate database and enter full data set into it
#2) Create function to query a 4 column table (or any dimension table, right?) based on the value of an
#### attribute (query_table(TABLENAME, COLUMNNAME, ATTRIBUTETOSEARCHFOR
#### or something))
#3) Use output of above, which returns the name of the attributes == ATTRIBUTETOSEARCHFOR
#### to add rows to moa_list.csv. Again make sure there are no duplicates
#4) Create a function that will update a table (id change Null to a value; dont use INSERT IGNORE)
#### perhaps make this dimension flexible too if possible, will be able to use this to update
#### all tables (either outright or as a template)

#Create a function that SELECTS all data from the Interventions Table, including
#intervention_type and moa. SELECT id is optional, not returned by default.
#Returns a list of tuples, each tuple being a unique row
def select_interventions_data(get_id = False):
    """TBD"""

    if get_id:
        script = """SELECT Interventions.id,
                                Interventions.intervention,
                                Intervention_Type.intervention_type,
                                Moa.moa

                        FROM Interventions
                        JOIN Intervention_Type
                        JOIN MoA
                        ON Interventions.intervention_type_id = Intervention_Type.id
                        AND Interventions.moa_id = Moa.id"""
    else:
        script = """SELECT Interventions.intervention,
                                Intervention_Type.intervention_type,
                                Moa.moa

                        FROM Interventions
                        JOIN Intervention_Type
                        JOIN MoA
                        ON Interventions.intervention_type_id = Intervention_Type.id
                        AND Interventions.moa_id = Moa.id"""

    #Run query
    cur.execute(script)

    #Put query_results into a stable list
    query_results = cur.fetchall()

    return query_results

    ###Drop relevant data into one file, all from db (dont overwrite)
    ###Upload data from a second file, whose name you must enter to update database
    ###Could I have a safegaurd in upload step? if there are less nulls in database, then request confirmation


###Creates a csv_file from query_results (should be a list of tuples, each tuple being a row)
###Default name of csv_file is: interventions_data.csv
###Items in csv file are sorted by first item in each row by defualt
def create_csv(query_results, csv_file = 'interventions_data.csv', sort_first_column = True):
    """TBD"""

    ##Sort query_results list by first value in each tuple:
    if sort_first_column:
        query_results.sort()


    with open(csv_file, 'a') as f:

        for row_tuple in query_results:
            row = ''
            for item in row_tuple:
                row = row + item +','
            row = row + '\n'
            f.write(row)

    return None

###Create a function that returns an intervention's MoA, or NULL if it is not available
###Data is read from moa_list.csv, which is assumed to have the structure:

###This should change as well!!

###Use this function one time to ready data from (cleaned) moa_list.csv, and add it to its own
##database. Then get_moa should query that database for an intervention, and return its MoA
###The intervention database will have more interventions than the Interventions table in my database
###Interventions with NULL MoAs in function above should then be added to the new database
def get_moa(intervention, data = 'moa_list.csv'):
    """TBD"""

    with open(data, 'rU+') as csv_file:

        f = csv.reader(csv_file, delimiter=',')

        for row in f:
            if intervention.lower().strip() == row[0].lower().strip():
                return row[1].lower().strip()
            else:
                pass

    return 'NULL'


###
