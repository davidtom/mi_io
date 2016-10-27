"""TBD"""

import csv
import sqlite3

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

#Create a function that searches a column in a table to find values equal to
# a specified value. Returns the value of a specified row in that column ('id' by default)
#Returns the value(s) as a list of tuples
def get_value(table_name, column_name, search_value, column ='id'):
    """TBD"""

    #Run query
    cur.execute("""SELECT {} FROM {} WHERE {} = ?""".format(column, table_name, column_name), (search_value,))

    #Check to make sure only one id is returned, otherwise data assumptions are wrong
    query_results = cur.fetchall()

    if len(query_results) == 1:
        #return the first value (and only value), of the first tuple (and only tuple)
        return query_results[0][0]
    if len(query_results) > 1:
        return query_results
    else:
        raise ValueError('query_results has len(value) == 0; it is an empty list')

    return None

###Per above to do list, now I need to enter the interventions with no MoA id into csv file
def add_to_csv(): ##VARIABLES TBD
    """TBD"""

    ##Need to manipulate this list:
    values = get_value('Interventions', 'moa_id', get_value('MoA', 'moa', 'NULL'), 'intervention')
    print values
    print len(values)


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
