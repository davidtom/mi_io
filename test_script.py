### enter_data


### Trials
from create_trial import Trial
test = Trial('NCT01454102.xml')
print test.get_intervention()
# print len(test.get_study_arm())
# for i in test.get_intervention():
#     print i['intervention']
#     print '-----'

##############
##To do list
##############

##INTERVENTION FUNCTION NEED TO BE DEFINED WITHIN A NEW CLASS
    #Functions to store and retrieve: intervention(s)/drug(s) used in trial
    ##Need to have: intervention other name, intervention type,

    #-add doc strings for all get_functions at least (indicating what type of data you will get back,
    #for example, a typle of all conditions for a trial, or a tuple of dates, or a datetime object)
