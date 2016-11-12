"""TBD Class that creates a database object"""

class DB(object):
    """TBD"""

#import modules
import sqlite3
import os
import re
import csv
import create_trial as ct
import csv_data
import sys

#Set default encoding as utf-8
reload(sys)
sys.setdefaultencoding('utf-8')


#


class DB(object):
    """TBD"""

    def __init__(self, db_name):
        """TBD. db_name MUST be a string AND END IN sqlite3
        Connects to databases that exists; creates DB objects, but not databases
        for those that don't exist. Use create(type_str) to create a database
        of either type trial or moa"""

        self.db_name = db_name

        #Define a base directory, based on where db_class.py module is located
        self.base_dir = os.path.dirname(os.path.abspath(__file__))

        #Define a path for the database to connect to, within the base directory
        self.db_path = os.path.join(self.base_dir, db_name)

        #check to see if file exists or not, and ????????
        if os.path.isfile(db_name):
            self.conn = sqlite3.connect('{}'.format(db_name))
            self.cur = self.conn.cursor()
            print 'Successfully connected to existing database: {}'.format(db_name)
        else:
            print "DB Object created, but no database of specified name exists in current folder.\nRun create_db() to create a database."


    def get_db_name(self):
        return self.db_name

    def get_base_dir(self):
        return self.base_dir

    def get_db_path(self):
        return self.db_path

    def create_db(self, type_str, xml_folder = 'XML_folder', csv_file = 'moa_list.csv', headers = True):
        """TBD - creates a db if it does not exist AND enters data into it"""

        if not os.path.isfile(self.db_name):
            self.conn = sqlite3.connect('{}'.format(self.db_name))
            self.cur = self.conn.cursor()

            if type_str == 'trial':

                #Sql script to create tables
                self.cur.executescript('''
                CREATE TABLE IF NOT EXISTS Trials (
                    nct INTEGER NOT NULL PRIMARY KEY UNIQUE,
                    brief_title TEXT,
                    official_title TEXT,
                    phase_id INTEGER,
                    status TEXT,
                    enrollment INTEGER,
                    study_type_id INTEGER,
                    study_design_id INTEGER,
                    start_date TEXT,
                    completion_date TEXT,
                    primary_completion_date TEXT,
                    verification_date TEXT,
                    last_changed_date TEXT,
                    sponsor_id INTEGER,
                    index_date TEXT
                );

                CREATE TABLE IF NOT EXISTS Study_Type (
                id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
                study_type TEXT UNIQUE
                );

                CREATE TABLE IF NOT EXISTS Study_Design (
                id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
                study_design TEXT UNIQUE
                );

                CREATE TABLE IF NOT EXISTS Sponsor (
                id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
                sponsor_name TEXT UNIQUE,
                sponsor_type_id INTEGER
                );

                CREATE TABLE IF NOT EXISTS Phases (
                id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
                phase TEXT UNIQUE
                );

                CREATE TABLE IF NOT EXISTS Sponsor_Type (
                id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
                sponsor_type TEXT UNIQUE
                );

                CREATE TABLE IF NOT EXISTS Country (
                id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
                country TEXT UNIQUE
                );

                CREATE TABLE IF NOT EXISTS Country_Link (
                country_id INTEGER,
                nct_id INTEGER,
                PRIMARY KEY (country_id, nct_id)
                );

                CREATE TABLE IF NOT EXISTS Conditions (
                id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
                condition TEXT UNIQUE
                );

                CREATE TABLE IF NOT EXISTS Conditions_Link (
                condition_id INTEGER,
                nct_id INTEGER,
                PRIMARY KEY (condition_id, nct_id)
                );

                CREATE TABLE IF NOT EXISTS Interventions (
                id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
                intervention TEXT UNIQUE,
                intervention_type_id INTEGER,
                moa_id INTEGER
                );

                CREATE TABLE IF NOT EXISTS Interventions_Link (
                intervention_id INTEGER,
                study_arm_id INTEGER,
                PRIMARY KEY (intervention_id, study_arm_id)
                );

                CREATE TABLE IF NOT EXISTS Intervention_Type (
                id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
                intervention_type TEXT UNIQUE
                );

                CREATE TABLE IF NOT EXISTS MoA (
                id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
                moa TEXT UNIQUE
                );

                CREATE TABLE IF NOT EXISTS Intervention_Other_Names (
                id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
                other_name TEXT UNIQUE,
                intervention_id INTEGER
                );

                CREATE TABLE IF NOT EXISTS Study_Arms (
                id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
                nct_id INTEGER,
                arm_label TEXT,
                CONSTRAINT trial_arm UNIQUE (nct_id, arm_label)
                );

                CREATE TABLE IF NOT EXISTS Endpoints (
                id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
                endpoint_type INTEGER,
                endpoint TEXT,
                CONSTRAINT endpoint_tier UNIQUE (endpoint_type, endpoint)
                );

                CREATE TABLE IF NOT EXISTS Endpoint_Link (
                endpoint_id INTEGER,
                nct_id INTEGER,
                PRIMARY KEY (endpoint_id, nct_id)
                );

                ''')

                #Get a list of file names xml_folder that begin with
                #'NCT' and end with 'xml'.
                nct_list = list()

                #set up path for xml_folder
                xml_folder_path = os.path.join(self.base_dir, xml_folder)

                #iterate files in list returned by os.listdir() and extend only the ones
                #starting with 'NCT' and ending with '.xml'
                for filename in os.listdir(xml_folder_path):
                    nct_list.extend(re.findall('^NCT.*\.xml$', filename))

                #Create a reference dictionary for reference/bucket conditions
                #used when inserting data into condition table to try to clean
                #data a bit upfront
                ref_dict = test.create_reference_condition_dict()

                ##Iterate through all nct*.xml files in xml_folder and add data to db
                for xml in nct_list:

                    #Create an object of class Trial from current xml file
                    t = ct.Trial(os.path.join(xml_folder_path, xml))

                    #Create local variable for nct attribute of trial
                            ##need to change once I update trial primary key

                    nct = t.get_nct()

                    #Insert trial's lead_sponsor_type into Sponsor_Type table and store corresponding id
                    sponsor_type_id = self.insert_2column_table('Sponsor_Type', 'sponsor_type', t.get_lead_sponsor_type())

                    #Insert trial's lead_sponsor and sponsor_type_id into Sponsor table
                    #(sponsor_name and sponsor_type_id repsectively)
                    sponsor_id = self.insert_3column_table('Sponsor',
                                                        'sponsor_name', t.get_lead_sponsor(),
                                                        'sponsor_type_id', sponsor_type_id)

                    #Insert trial's study_type into Study_Type table and store corresponding id
                    study_type_id = self.insert_2column_table('Study_Type', 'study_type', t.get_study_type())

                    #Insert trial's study_design into Study_Design table and store corresponding id
                    study_design_id = self.insert_2column_table('Study_Design', 'study_design', t.get_study_design())

                    #Insert trial's phase into Phases table and store corresponding id
                    phase_id = self.insert_2column_table('Phases', 'phase', t.get_phase())

                    #Iterate through tuple of countries in trial and insert each into Country table
                    #also store each corresponding id and enter it into Country_Link table, along with nct_id
                    for item in t.get_country():
                        country_id = self.insert_2column_table('Country', 'country', item)
                        self.insert_link_table('Country_Link', 'country_id', country_id, 'nct_id', nct)


                    #Iterate through tuple of conditions in trial and insert each into Conditions table
                    #also store each corresponding id and enter it into Conditions_Link table, along with nct_id
                    for item in t.get_condition():
                        condition_id = self.insert_2column_table('Conditions', 'condition', self.return_reference_condition(item, ref_dict))
                        self.insert_link_table('Conditions_Link', 'condition_id', condition_id, 'nct_id', nct)


                    #Iterate through trials' primary_endpoint tuple and insert each into Endpoints table
                    #also store each corresponding id and enter it Endpoint_Link table, along with nct_id
                    for item in t.get_primary_endpoint():
                        endpoint_id = self.insert_3column_table('Endpoints',
                                                            'endpoint', item,
                                                            'endpoint_type', 1)
                        self.insert_link_table('Endpoint_Link',
                                            'endpoint_id', endpoint_id, 'nct_id', nct)


                    #Iterate through trials' secondary_endpoint tuple and insert each into Endpoints table
                    #also store each corresponding id and enter it Endpoint_Link table, along with nct_id
                    for item in t.get_secondary_endpoint():
                        endpoint_id = self.insert_3column_table('Endpoints',
                                                            'endpoint', item,
                                                            'endpoint_type', 2)
                        self.insert_link_table('Endpoint_Link',
                                            'endpoint_id', endpoint_id, 'nct_id', nct)


                    #Iterate through dicts contained within intervention_details (1 dict per intervention)
                    for item in t.get_intervention_details():

                        #Insert intervention's type into Intervention_Type table and store intervention_type_id
                        intervention_type_id = self.insert_2column_table('Intervention_Type',
                        'intervention_type', item['type'])

                        moa_id = self.insert_2column_table('MoA',
                        'moa', csv_data.get_moa(item['intervention']))

                        #Insert intervention's name, intervention_type_id and MoA_id
                        #(placeholder for now) into Interventions table
                        intervention_id = self.insert_4column_table('Interventions',
                        'intervention', item['intervention'],
                        'intervention_type_id', intervention_type_id,
                        'moa_id', moa_id)

                        #Iterate through items contained within other_name tuple and insert
                        #them into Intervention_Other_Names table, along with the corresponding
                        #intervention_id
                        for name in item['other_name']:
                            self.insert_3column_table('Intervention_Other_Names',
                            'other_name', name,
                            'intervention_id', intervention_id)

                        # Iterate through items contained within arm_group tuple and insert
                        # them into Intervention_Other_Names table, along with the corresponding
                        # intervention_id
                        for arm in item['arm_group']:
                            study_arm_id = self.insert_constrained3column_table('Study_Arms',
                                                            'nct_id', nct,
                                                            'arm_label', arm)
                            self.insert_link_table('Interventions_Link',
                                                            'intervention_id', intervention_id,
                                                            'study_arm_id', study_arm_id)


                    #Insert data into Trials table
                    self.cur.execute("""INSERT OR IGNORE INTO Trials (nct,
                                                                brief_title,
                                                                official_title,
                                                                phase_id,
                                                                status,
                                                                enrollment,
                                                                study_type_id,
                                                                study_design_id,
                                                                start_date,
                                                                completion_date,
                                                                primary_completion_date,
                                                                verification_date,
                                                                last_changed_date,
                                                                sponsor_id)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""", (nct,
                                                                    t.get_brief_title(),
                                                                    t.get_official_title(),
                                                                    phase_id,
                                                                    t.get_status(),
                                                                    t.get_enrollment(),
                                                                    study_type_id,
                                                                    study_design_id,
                                                                    t.get_start_date(),
                                                                    t.get_completion_date(),
                                                                    t.get_primary_completion_date(),
                                                                    t.get_verification_date(),
                                                                    t.get_last_changed_date(),
                                                                    sponsor_id))


                    self.conn.commit()

                #Provide confirmation that db was created
                if os.path.isfile(self.db_name):
                    print '{} created successfully.'.format(self.db_name)
                else:
                    print 'Error creating Database'


            elif type_str == 'moa':

                self.cur.executescript('''
                CREATE TABLE IF NOT EXISTS Agent (
                    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
                    agent TEXT UNIQUE,
                    moa_id INTEGER,
                    source TEXT
                );

                CREATE TABLE IF NOT EXISTS MoA (
                id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
                moa TEXT UNIQUE,
                macro_moa_id INTEGER
                );

                CREATE TABLE IF NOT EXISTS Macro_MoA (
                id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
                macro_moa TEXT UNIQUE
                );

                ''')

                #Read data from csv file (moa_list.csv by default)
                #and enter all its data into the database
                #Note:
                #   *assumes structure of: agent,moa, moa_bucket,source
                #   *assumes Headers exist
                #   *INSERT OR IGNORE - cannot overwrite data with this function

                csv_file = 'moa_list.csv'
                headers = True

                #set up path for csv_file
                csv_file_path = os.path.join(self.base_dir, csv_file)

                #Open csv_file
                with open(csv_file_path, 'rU+') as csv_f:

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
                        macro_moa_id = self.insert_2column_table('Macro_MoA',
                                                                'macro_moa', macro_moa)

                        #Insert data into MoA table and get associated id
                        moa_id = self.insert_3column_table('MoA',
                                                        'moa', moa,
                                                        'macro_moa_id', macro_moa_id)

                        #Insert data into Agent table
                        self.cur.execute("""INSERT OR IGNORE INTO Agent (agent,
                                                                    moa_id,
                                                                    source)
                                        VALUES (?, ?, ?)""", (agent,
                                                                moa_id,
                                                                source))

                        self.conn.commit()

                #Provide confirmation that db was created
                if os.path.isfile(self.db_name):
                    print '{} created successfully.'.format(self.db_name)
                else:
                    print 'Error creating Database'

            else:
                raise ValueError('Unrecognized database type string')

        else:
            raise ValueError('Database {} already exists in current folder'.format(self.db_name))


    #Define function that inputs data into a table with 2 columns (id and a table-specific value),
    #and returns a particular value's id (primary key)
    def insert_2column_table(self, table_name, column_name, attribute, cur = None):
        """Docstring TBD"""

        #http://stackoverflow.com/questions/1802971/nameerror-name-self-is-not-defined
        if cur is None:
            cur = self.cur

        cur.execute("""
        INSERT OR IGNORE INTO {} ({})
        VALUES (?)""".format(table_name, column_name), (attribute, ))
        cur.execute('SELECT id FROM {} WHERE {} = ?'.format(table_name, column_name), (attribute, ))
        return cur.fetchone()[0]


    def insert_3column_table(self, table_name, column_name1, attribute1, column_name2, attribute2, cur = None):
        """Docstring TBD - ATTRIBUTE SEARCHED FOR TO FIND THE CORRESPONDING ID SHOULD BE COLUMN_NAME1/ATTRIBUTE1"""

        #http://stackoverflow.com/questions/1802971/nameerror-name-self-is-not-defined
        if cur is None:
            cur = self.cur

        cur.execute("""
        INSERT OR IGNORE INTO {} ({}, {})
        VALUES (?, ?)""".format(table_name, column_name1, column_name2), (attribute1, attribute2))
        cur.execute('SELECT id FROM {} WHERE {} = ?'.format(table_name, column_name1), (attribute1, ))
        return cur.fetchone()[0]

    def insert_constrained3column_table(self, table_name, column_name1, attribute1, column_name2, attribute2, cur = None):
        """Docstring TBD - USES BOTH ATTRIBUTES TO SEARCH FOR THE CORRESPONDING ID"""

        #http://stackoverflow.com/questions/1802971/nameerror-name-self-is-not-defined
        if cur is None:
            cur = self.cur

        cur.execute("""
        INSERT OR IGNORE INTO {} ({}, {})
        VALUES (?, ?)""".format(table_name, column_name1, column_name2), (attribute1, attribute2))
        cur.execute('SELECT id FROM {} WHERE {} = ? AND {} = ?'.format(table_name, column_name1, column_name2), (attribute1, attribute2))
        return cur.fetchone()[0]

    def insert_4column_table(self, table_name, column_name1, attribute1,
        column_name2, attribute2, column_name3, attribute3, cur = None):
        """Docstring TBD - ATTRIBUTE SEARCHED FOR TO FIND THE CORRESPONDING ID SHOULD BE COLUMN_NAME1/ATTRIBUTE1"""

        #http://stackoverflow.com/questions/1802971/nameerror-name-self-is-not-defined
        if cur is None:
            cur = self.cur

        cur.execute("""
        INSERT OR IGNORE INTO {} ({}, {}, {})
        VALUES (?, ?, ?)""".format(table_name, column_name1, column_name2, column_name3), (attribute1, attribute2, attribute3))
        cur.execute('SELECT id FROM {} WHERE {} = ?'.format(table_name, column_name1), (attribute1, ))
        return cur.fetchone()[0]

    #Define a function that inputs data into a link table. Utilizes a value's id (primary key)
    #returned from a previous insert function
    def insert_link_table(self, table_name, column_name1, attribute1, column_name2, attribute2, cur = None):

            #http://stackoverflow.com/questions/1802971/nameerror-name-self-is-not-defined
            if cur is None:
                cur = self.cur

            cur.execute('''INSERT OR REPLACE INTO {}
                ({}, {}) VALUES ( ?, ? )'''.format(table_name, column_name1, column_name2),
                (attribute1, attribute2))
            return None

    #Create function that reads a csv file containing conditions and their
    #reference condition/condition bucket and creates a dictionary to store data
    def create_reference_condition_dict(self, csv_file = 'condition_buckets.csv'):

        #set up path for file
        csv_file_path = os.path.join(self.base_dir, csv_file)

        #Open file as a csv reader
        with open(csv_file_path, 'rU+') as csv_f:
            f = csv.reader(csv_f, delimiter=',')

            #remove and save headers from reader object
            headers = f.next()

            #iterate through reader object and create reference condition dictionary
            reference_condition_dict = dict()

            for row in f:
                reference_condition_dict[row[0].lower()] = row[1]

            return reference_condition_dict

    #Create file that checks a condition against a reference dict and returns
    #reference condition/condition bucket. If condition is not in reference dict
    #returns condition
    def return_reference_condition(self, condition, reference_dict):
        return reference_dict.get(condition.lower(), condition)




test = DB('trial_db.sqlite3')
