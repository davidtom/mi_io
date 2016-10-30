"""
Module Purpose: Creates a class, Trial, which takes as an argument an xml file
for a clinical trial downloaded from clinicaltrials.gov and parses it into
attributes of the Trial object (i.e. nct, phase, sponsor, intervention, etc.)
"""

#Import modules
import xml.etree.ElementTree as ET
import re
import datetime
import calendar



#Define trial class, which contains all information from a clinical trial
class Trial(object):
    """Class docstring - TO BE COMPLETED
    """

    #Create dictionary of k:v = month:# (using list comprehension) in order
    # to create date tuples (year#, month#) to store date variables
    months_dict = dict((v,k) for k,v in enumerate(calendar.month_name))

    ##Convert values (integers) in months_dict to be double digit
    for i in months_dict.keys():
        if len(str(months_dict[i])) < 2:
            months_dict[i] = int('%02d'%months_dict[i])

    ##Define class functions
    def parse_xml(self, xml_file):
        return ET.parse(xml_file).getroot()

    #Function to retrieve a trial's filename:
    def get_file_name(self):
        return self.file_name

    #Functions to store and retrieve: NCT Number
    def find_nct(self, root):
        try:
            nct_id = root.find('id_info/nct_id').text

            nct_number = re.findall('[0-9]+', nct_id)[0]
            return nct_number

        except AttributeError:
            return None

    def get_nct(self):
        return self.nct_number

    #Functions to store and retrieve: Trial's brief title
    def find_brief_title(self, root):
        try:
            brief_title = root.find('brief_title').text
            return brief_title.lower().strip()

        except AttributeError:
            return None

    def get_brief_title(self):
        return self.brief_title

    #Functions to store and retrieve: Trial's official title
    def find_official_title(self, root):
        try:
            official_title = root.find('official_title').text
            return official_title.lower().strip()

        except AttributeError:
            return None

    def get_official_title(self):
        return self.official_title

    #Functions to store and retrieve: trial's phase
    def find_phase(self, root):
        try:
            return root.find('phase').text.lower().strip()
        except AttributeError:
            return None

    def get_phase(self):
        return self.phase

    #Functions to store and retrieve: lead sponsor
    def find_lead_sponsor(self, root):
        try:
            return root.find('sponsors/lead_sponsor/agency').text.lower().strip()
        except AttributeError:
            return None

    def get_lead_sponsor(self):
        return self.lead_sponsor

    #Functions to store and retrieve: lead sponsor type
    def find_lead_sponsor_type(self, root):
        try:
            return root.find('sponsors/lead_sponsor/agency_class').text.lower().strip()
        except AttributeError:
            return None

    def get_lead_sponsor_type(self):
        return self.lead_sponsor_type

    #Functions to store and retrieve: trial status
    def find_status(self, root):
        try:
            return root.find('overall_status').text.lower().strip()
        except AttributeError:
            return None

    def get_status(self):
        return self.status

    #Functions to store and retrieve: trial enrollment
    def find_enrollment(self, root):
        try:
            return int(root.find('enrollment').text)
        except AttributeError:
            return None

    def get_enrollment(self):
        return self.enrollment

    #Functions to store and retrieve: trial start date
    def find_start_date(self, root):
        """Initially as YYYY-MM format, but assumes DD is 01 to allow
        creation as a datetime object"""
        try:
            raw_date = root.find('start_date').text.split()
            return datetime.date(int(raw_date[1]), self.months_dict[raw_date[0]], 01)
        except AttributeError:
            return None

    def get_start_date(self):
        return self.start_date

    #Functions to store and retrieve: trial completion date
    def find_completion_date(self, root):
        try:
            raw_date = root.find('completion_date').text.split()
            return datetime.date(int(raw_date[1]), self.months_dict[raw_date[0]], 01)
        except AttributeError:
            return None

            #completion_date,
            #                                             primary_completion_date,
            #                                             verification_date

    def get_completion_date(self):
        return self.completion_date

    #Functions to store and retrieve: trial's primary endpoint completion date
    def find_primary_completion_date(self, root):
        try:
            raw_date = root.find('primary_completion_date').text.split()
            return datetime.date(int(raw_date[1]), self.months_dict[raw_date[0]], 01)
        except AttributeError:
            return None

    def get_primary_completion_date(self):
        return self.primary_completion_date

    #Functions to store and retrieve: study type (interventional, observational, etc.)
    def find_study_type(self, root):
        try:
            return root.find('study_type').text.lower().strip()
        except AttributeError:
            return None

    def get_study_type(self):
        return self.study_type

    #Functions to store and retrieve: study design (allocation, arms, etc.)
    def find_study_design(self, root):
        try:
            return root.find('study_design').text.lower().strip()
        except AttributeError:
            return None

    def get_study_design(self):
        return self.study_design

    #Functions to store and retrieve: trial's verification date
    def find_verification_date(self, root):
        try:
            raw_date = root.find('verification_date').text.split()
            return datetime.date(int(raw_date[1]), self.months_dict[raw_date[0]], 01)
        except AttributeError:
            return None

    def get_verification_date(self):
        return self.verification_date

    #Functions to store and retrieve: date trial was last changed on CT.gov
    def find_last_changed_date(self, root):
        try:
            date_list = root.find('lastchanged_date').text.split()
            return datetime.date(int(date_list[2]),
                int(self.months_dict[date_list[0]]),
                int(re.findall('[0-9]+', date_list[1])[0]))
        except AttributeError:
            return None

    def get_last_changed_date(self):
        return self.last_changed_date

    #Functions to store and retrieve: date trial was first received on CT.gov
    def find_first_received_date(self, root):
        try:
            date_list = root.find('firstreceived_date').text.split()
            return datetime.date(int(date_list[2]),
                int(self.months_dict[date_list[0]]),
                int(re.findall('[0-9]+', date_list[1])[0]))
        except AttributeError:
            return None

    def get_first_received_date(self):
        return self.first_received_date

    #Functions to store and retrieve: condition(s) being studied
    def find_condition(self, root):
        #Use list comprehension to unpack all conditions :)
        try:
            return tuple([i.text.lower().strip() for i in root.findall('condition')])
        except AttributeError:
            return None

    def get_condition(self):
        return self.condition

    #Functions to store and retrieve: countries trial is being conducted in
    def find_country(self, root):
        try:
            return tuple([i.text.lower().strip() for i in root.findall('location_countries/country')])
        except AttributeError:
            return None

    def get_country(self):
        return self.country

    #Functions to store and retrieve: trial's study arm(s)
    def find_study_arm(self, root):
        try:
            return tuple([i.text.lower().strip() for i in root.findall('arm_group/arm_group_label')])
        except AttributeError:
            return None

    def get_study_arm(self):
        return self.study_arm

    #Functions to store and retrieve: trial's primary endpoint(s)
    def find_primary_endpoint(self, root):
        """Returns a tuple that is a set of all <primary_outcome>/<measure>
        strings contained in xml file. Repeated endpoints, which may vary by
        timeframe or safety issue (yes/no) will be condensed into a
        single item"""

        try:
            return set(tuple([i.text.lower().strip() for i in root.findall('primary_outcome/measure')]))
        except AttributeError:
            return None

    def get_primary_endpoint(self):
        """Returns a tuple that is a set of all <primary_outcome>/<measure>
        strings contained in xml file. Repeated endpoints, which may vary by
        timeframe or safety issue (yes/no) will be condensed into a
        single item"""
        return self.primary_endpoint

    #Functions to store and retrieve: trial's secondary endpoint(s)
    def find_secondary_endpoint(self, root):
        """Returns a tuple that is a set of all <secondary_outcome>/<measure>
        strings contained in xml file. Repeated endpoints, which may vary by
        timeframe or safety issue (yes/no) will be condensed into a
        single item"""

        try:
            return set(tuple([i.text.lower().strip() for i in root.findall('secondary_outcome/measure')]))
        except AttributeError:
            return None

    def get_secondary_endpoint(self):
        """Returns a tuple that is a set of all <secondary_outcome>/<measure>
        strings contained in xml file. Repeated endpoints, which may vary by
        timeframe or safety issue (yes/no) will be condensed into a
        single item"""
        return self.secondary_endpoint


    #Functions to store and retrieve: all relevant information on
        #intervention(s) in a trial
    def find_intervention_details(self, root):
        """Returns a tuple of dictionaries. Each dictionary contains the
        following information on a single, unique intervention:
        intervention_name, type, study_arm, and other_name"""

        #Create function to try to clean an intervention_name
        #in order to make it as singular as possible (nivo + ipi = (nivo, ipi))
        ###Returns a tuple of string(s)
        def clean_intervention(intervention_name):
            """TBD"""

        #Break apart the '+' and 'and' items for now - can only get this so clean
        #using large patterns (for fear of compromising the data). Rest of data
        #cleaning will have to be done at analysis phase (good opportunity to learn python pandas!)

        #make all of these lower case to allow 'stacking'
        #also replace commas with semicolons, to avoid issues with creating csv files later

            #Replace commas in intervention_name with semicolons, make all lower case
            clean_intervention_name = intervention_name.replace(',', ';').lower()

            #Create 'flag' variables to denote if 'placebo' or 'and/+' exists anywhere in intervention
            placebo_flag = False

            concatentation_flag = False

            #define a string variable to store concatentation pattern to look for
            concat_pat = "\+|and|plus"

            #If placebo is anywhere in intervention name, flag it to be corrected
            if len(re.findall('placebo', clean_intervention_name)) > 0:
                placebo_flag = True

            #If a string in concat_pat is in the intervention name, flag that there is a concatenation
            if len(re.findall(concat_pat, clean_intervention_name)) > 0:
                concatentation_flag = True


            #If a placebo is in string, return placebo
            if placebo_flag and not concatentation_flag:
                return ('placebo',)
            #If a concatentation item is in string, return a list of split items
            elif concatentation_flag:
                return tuple(re.split(concat_pat, clean_intervention_name))
            #If neither flags are triggered (ie nivo, placebo, ipi, etc.)
            #return intervention_name as is
            else:
                return (clean_intervention_name,)


        #Create list that will store intervention dicts (will be returned as a tuple)
        intervention_details_list = list()

        #Parse xml and pull all groups that start with <intervention>
        intervention_blocks = root.findall('intervention')

        #Parse blocks of <intervention> data and assign them to intervention_dict
        for block in intervention_blocks:

            #Identify intervention(s) included in the intervention block using clean_intervention()
            try:
                intervention_name = clean_intervention(block.find('intervention_name').text)
            except AttributeError:
                pass

            #Iterate across the one or more interventions, storing the relevant details
            #For split interventions, the information will be duplicated, except for 'intervention'
            #This will have to be dealt with later, and is the cost of cleaning the data at this step
            for intervention in intervention_name:

                #Create dict that will store information for a unique intervention
                intervention_dict = dict()

                #Store relevant details for the intervention
                intervention_dict['intervention'] = intervention.strip()

                try:
                    intervention_dict['type'] = block.find('intervention_type').text.lower().strip()
                except AttributeError:
                    pass

                try:
                    other_name_list = list()
                    for i in block.findall('other_name'):
                        other_name_list.append(i.text.lower().strip())
                    intervention_dict['other_name'] = tuple(other_name_list)
                except AttributeError:
                    pass

                try:
                    arm_group_list = list()
                    for i in block.findall('arm_group_label'):
                        arm_group_list.append(i.text.lower().strip())
                    intervention_dict['arm_group'] = tuple(arm_group_list)
                except AttributeError:
                    pass

                #append current intervention_dict to the intervention_details_list
                intervention_details_list.append(intervention_dict)

        return tuple(intervention_details_list)

    def get_intervention_details(self):
        return self.intervention_details


    #Function to instantiate a trial, assigning it all relevant info from XML
    def __init__(self, xml_file):

        self.file_name = xml_file

        self.root = self.parse_xml(xml_file)

        self.nct_number = self.find_nct(self.root)

        self.brief_title = self.find_brief_title(self.root)

        self.official_title = self.find_official_title(self.root)

        self.phase = self.find_phase(self.root)

        self.lead_sponsor = self.find_lead_sponsor(self.root)

        self.lead_sponsor_type = self.find_lead_sponsor_type(self.root)

        self.status = self.find_status(self.root)

        self.enrollment = self.find_enrollment(self.root)

        self.start_date = self.find_start_date(self.root)

        self.completion_date = self.find_completion_date(self.root)

        self.primary_completion_date = self.find_primary_completion_date(self.root)

        self.study_type = self.find_study_type(self.root)

        self.study_design = self.find_study_design(self.root)

        self.verification_date = self.find_verification_date(self.root)

        self.condition = self.find_condition(self.root)

        self.country = self.find_country(self.root)

        self.last_changed_date = self.find_last_changed_date(self.root)

        self.first_received_date = self.find_first_received_date(self.root)

        self.study_arm = self.find_study_arm(self.root)

        self.primary_endpoint = self.find_primary_endpoint(self.root)

        self.secondary_endpoint = self.find_secondary_endpoint(self.root)

        self.intervention_details = self.find_intervention_details(self.root)
