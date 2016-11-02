"""
TBD

Functions to manage moa_db.sqlite3

Includes:
    *adding data from original csv
    *adding interventions and moas from trial_db.sqlite3
    *updating interventions with NULL moa
    *insert moa data into trial_db.sqlite3

    """

#Import modules
import sqlite3
import os
import csv
import sys
import enter_xml_data as exd ###CHANGE THIS ONCE A MODULE HAS BEEN CREATED FOR THESE FUNCTIONS

#Set default encoding as utf-8 (to read moa_list.csv)
reload(sys)
sys.setdefaultencoding('utf-8')

#Connect to database
dbname = 'moa_db.sqlite3'
conn = sqlite3.connect(dbname)
cur = conn.cursor()


#Create function that reads data from a csv (moa_list.csv by default)
#and enters all its data into the database
#Note:
#   *assumes structure of: agent,moa, moa_bucket,source
#   *INSERT OR IGNORE - cannot overwrite data with this function
def enter_csv_data(csv_file = 'moa_list.csv', headers = True):

    #Open csv_file
    with open(csv_file, 'rU+') as csv_f:

        #Read contents of csv_file
        f = csv.reader(csv_f, delimiter=',')

        #Strip/store headers from csv_file if they exist
        headers_str = None
        if headers:
            headers_str = f.next()

        #Iterate through rows of csv_file and insert data into
        #appropriate Tables

        for row in f:

            agent = row[0].lower().strip()
            moa = row[1].lower().strip()
            macro_moa = row[2].lower().strip()
            source = row[3].lower().strip()

            ##Debugging Code
            # print 'agent: {}'.format(agent)
            # print 'moa: {}'.format(moa)
            # print 'macro_moa: {}'.format(macro_moa)
            # print 'source: {}'.format(source)
            # print '---'

            #Insert data into Macro_MoA table and get associated id
            macro_moa_id = exd.insert_2column_table('Macro_MoA',
                                                    'macro_moa', macro_moa, cur)

            #Insert data into MoA table and get associated id
            moa_id = exd.insert_3column_table('MoA',
                                            'moa', moa,
                                            'macro_moa_id', macro_moa_id, cur)

            #Insert data into Agent table
            cur.execute("""INSERT OR IGNORE INTO Agent (agent,
                                                        moa_id,
                                                        source)
                            VALUES (?, ?, ?)""", (agent,
                                                    moa_id,
                                                    source))

            conn.commit()

    return None


if __name__ == '__main__':
    enter_csv_data()
