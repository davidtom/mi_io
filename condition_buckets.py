"""TBD"""

import csv

NSCLC_list = list()
RCC_list = list()
melanoma_list = list()
prostate_cancer_list = list()

with open('conditions.csv', 'rb') as csv_file:
    f = csv.reader(csv_file, delimiter=',')

    for row in f:

        #Fill out NSCLC_list
        if row[1] == 'NSCLC':
            NSCLC_list.append(row[0])

        #Fill out RCC_list
        if row[1] == 'RCC':
            RCC_list.append(row[0])

        #Fill out RCC_list
        if row[1] == 'Melanoma':
            melanoma_list.append(row[0])

        #Fill out prostate_cancer_list
        if row[1] == 'Prostate Cancer':
            prostate_cancer_list.append(row[0])

def bucket_condition(condition):
    """TBD"""

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
