"""TBD"""

import csv

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




def get_moa(intervention, data = 'moa_list.csv'):
    """TBD"""

    with open(data, 'rU+') as csv_file:

        f = csv.reader(csv_file, delimiter=',')

        for row in f:
            if intervention.lower().strip() == row[0].lower().strip():
                return row[1].lower().strip()
            else:
                pass

    return None


###
