"""Program to allow easier executing of program actions/modules"""

from create_trial import Trial
import create_db
import enter_xml_data
import test_script
import csv_data

def run_controlpanel():

    instructions = '''Commands:
    'trialdb' = create_db.create_trial_database()
    'moadb' = create_db.create_moa_database()
    'xmldata' = enter_data.py
    'test' = python test_script.py
    'c' = print commands
    'q' = exit
    '''

    print instructions

    while True:

        command = raw_input('Enter command:')

        if command == 'trialdb':
            create_db.create_trial_database()

        elif command == 'moadb':
            create_db.create_moa_database()

        elif command == 'xmldata':
            enter_xml_data.enter_xml_data()

        elif command == 'test':
            test_script.main()

        elif command == 'c':
            print instructions

        elif command == 'q':
            break

        else:
            print 'Command not recognized\n'


if __name__ == '__main__':
    run_controlpanel()
