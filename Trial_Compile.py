#Import modules
import urllib
import bs4
import zipfile
import xml.etree.ElementTree as ET
import pandas as pd
import os
import re
import natsort

#Define function to take an xml file and convert it into an ET root element
def xml_to_root(xml_file):
    return ET.parse(xml_file).getroot()

#Define function that reads through arm_labels of a study and adds them to a dictionary
def get_arm_labels(root_element, row_dict):
    count = 0
    for i in root_element.findall('arm_group'):
        count += 1
        row_dict['arm_group'+ str(count)] = i.find('arm_group_label').text
    return row_dict

#Define function that reads through endpoints (primary or secondary) of a study and adds them to a dictionary
def get_endpoints(root_element, endpoint_level, row_dict):
    count = 0
    for i in root_element.findall(endpoint_level + '_outcome'):
        count += 1
        row_dict[endpoint_level + '_outcome' + str(count)] = i.find('measure').text
    return row_dict
#Define a function that reads dates in 'month y(####)' format and converts them to yyyy/mm



#Define a function that reads dates in 'month, dd y(####) format and converts them to yyyy/mm/dd'

#Define a function to read an ET root element into a pandas series
def root_to_series(root_element):

    #Create an empty dict to populate with info from root element
    row_dict = {}

    #Read through root element and populate row_dict
    try:
        row_dict['nct_id'] = root_element.find('id_info/nct_id').text
    except AttributeError:
        pass

    try:
        row_dict['lead_sponsor'] = root_element.find('sponsors/lead_sponsor/agency').text
    except AttributeError:
        pass

    try:
        row_dict['lead_sponsor_class'] = root_element.find('sponsors/lead_sponsor/agency_class').text
    except AttributeError:
        pass

    try:
        row_dict['overall_status'] = root_element.find('overall_status').text
    except AttributeError:
        pass

    try:
        row_dict['start_date'] = root_element.find('start_date').text
    except AttributeError:
        pass

    try:
        row_dict['completion_date'] = root_element.find('completion_date').text
    except AttributeError:
        pass

    try:
        row_dict['primary_completion_date'] = root_element.find('primary_completion_date').text
    except AttributeError:
        pass

    try:
        row_dict['phase'] = root_element.find('phase').text
    except AttributeError:
        pass

    try:
        row_dict['study_type'] = root_element.find('study_type').text
    except AttributeError:
        pass

    try:
        row_dict['study_design'] = root_element.find('study_design').text
    except AttributeError:
        pass

    try:
        row_dict['verification_date'] = root_element.find('verification_date').text
    except AttributeError:
        pass

    try:
        row_dict['lastchanged_date'] = root_element.find('lastchanged_date').text
    except AttributeError:
        pass

    try:
        row_dict['firstreceived_date'] = root_element.find('firstreceived_date').text
    except AttributeError:
        pass

    try:
        row_dict['condition'] = root_element.find('condition').text
    except AttributeError:
        pass

    try:
        row_dict['firstreceived_results_date'] = root_element.find('firstreceived_results_date').text
    except AttributeError:
        pass

    #Use get_arm_labels function to pull all arm label groups and put them into row_dict
    get_arm_labels(root_element, row_dict)

    #Use get_endpoints function to pull all primary endpoints and put them into row_dict
    get_endpoints(root_element, 'primary', row_dict)

    #Use get_endpoints function to pull all secondary endpoints and put them into row_dict
    get_endpoints(root_element, 'secondary', row_dict)

    #Convert row_dict to a pandas series and return it
    return pd.Series(row_dict)

#Define function that uses regex to give a list of file names that start with 'NCT'
def get_NCT_list(folder_name):
    #Make a doc string: folder_name has to be a folder within the current working directory

    NCT_list = list()

    for file in os.listdir(folder_name):
        NCT_list.extend(re.findall('^NCT.*', file))

    return NCT_list

#Define function to create series from all files in a folder and append them to a dataframe
def build_df(folder_name):

    #Create empty dataframe to add rows to
    df = pd.DataFrame()

    #Create string to find folder
    path = os.getcwd() + '/' + folder_name +'/'

    #Go through xml files in the folder, appending them to the df
    for file in get_NCT_list(folder_name):
        df = df.append(root_to_series(xml_to_root(path+file)), True)

    return df

#Define function that finds and reorders a grouped variable
def order_group_variables(col_list, group_root):

    regex_group_root = group_root + '.*'

    group_list = list()

    for item in col_list:
        group_list.extend(re.findall(regex_group_root, item))

    group_list = natsort.natsorted(group_list)

    return group_list

#Define function that reorders all the columns in the dataframe in specified order
def reorder_all_columns(df):

    reordered_columns_head = ['nct_id',
                              'condition',
                              'phase',
                              'overall_status',
                              'start_date',
                              'primary_completion_date',
                              'completion_date',
                              'firstreceived_date',
                              'firstreceived_results_date',
                              'study_type', 'study_design']
    reordered_columns_tail = ['verification_date',
                              'lastchanged_date',
                              'lead_sponsor',
                              'lead_sponsor_class']

    reordered_columns_head.extend(order_group_variables(df.columns, 'arm_group'))
    reordered_columns_head.extend(order_group_variables(df.columns, 'primary_outcome'))
    reordered_columns_head.extend(order_group_variables(df.columns, 'secondary_outcome'))
    reordered_columns_head.extend(reordered_columns_tail)

    return df.reindex(columns=reordered_columns_head)

#Define function that exports dataframe to excel
#Export to excel (make this a function)
def export_to_excel(df, file_name):
    writer = pd.ExcelWriter(file_name)
    df.to_excel(writer, index = False)
    writer.save()
    return None
