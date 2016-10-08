"""
Module Purpose: Generate a dashboard showing all relevant information for
a trial and its interventions

input: sqlite3 database(main_db)
output: Dashboard of information on a trial and its interventions
"""

import sqlite3

#Enter files accessed in module
dbname = 'main_db.sqlite3'

#Connect to db
conn = sqlite3.connect(dbname)
cur = conn.cursor()

#Specify nct of trial to display (not sure how useful this will be in future,
#but good for QC role now)
specific_nct = raw_input('Enter nct to display: ')
if len(specific_nct) < 1:
    nct = 441337
else:
    nct = specific_nct

#SQL Script that will select all information about a trial from all tables in db
sql_script = """SELECT Trials.nct,
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
                        Sponsor_Type.sponsor_type
                FROM Trials
                    JOIN Study_Type
                    JOIN Study_Design
                    JOIN Sponsor
                    JOIN Sponsor_Type
                ON
                    Trials.study_type_id = Study_Type.id AND
                    Trials.study_design_id = Study_Design.id AND
                    Trials.sponsor_id = Sponsor.id AND
                    Sponsor.sponsor_type_id = Sponsor_Type.id
                WHERE Trials.nct = ?"""

cur.execute(sql_script, (nct,))

for i in cur.fetchall():
    print i
    print 'Trial Table:'
    print '\tNCT: {}'.format(i[0])
    print '\tStatus: {}'.format(i[1])
    print '\tEnrollment: {}'.format(i[2])
    print '\tStart Date: {}'.format(i[3])
    print '\tCompletion Date: {}'.format(i[4])
    print '\tPrimary Completion Date: {}'.format(i[5])
    print '\tVerification Date: {}'.format(i[6])
    print '\tLast Changed Date: {}'.format(i[7])
    print '\tIndex Date: {}'.format(i[8])
