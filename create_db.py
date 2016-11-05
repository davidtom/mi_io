"""
Module Purpose: Creates databases, tables, and constraints that will contain
all data pulled from clinicaltrials.gov using sqlite3

input: none
output:
    trial_db.sqlite3
    moa_db.sqlite3
"""

import sqlite3

def create_trial_database(dbname = "trial_db.sqlite3"):
    conn = sqlite3.connect(dbname)
    curr = conn.cursor()


    curr.executescript('''
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

    /*CREATE TABLE IF NOT EXISTS Study_Arms_Link (
    study_arm_id INTEGER,
    nct_id INTEGER,
    PRIMARY KEY (study_arm_id, nct_id)
    );*/

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


def create_moa_database(dbname = "moa_db.sqlite3"):
    conn = sqlite3.connect(dbname)
    cur = conn.cursor()

    cur.executescript('''
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


##If this module is run as the main program (not imported into another module)
## this code will run (because __name__  is set to "__main__"). If the file is
## being imported from another module __name__ will be set to the modeules's
## name (and code below does not run)
if __name__ == "__main__":
    create_trial_database()
    create_moa_database()
