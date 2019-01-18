def get_data_from_url(url):
    '''
    Gets json from url, decodes json, and returns data
    '''
    with urllib.request.urlopen(url) as url:
        data = json.loads(url.read().decode())
    return data

def url_is_alive(url):
   """
   Checks that a given URL is reachable.
   """
   request = urllib.request.Request(url)
   request.get_method = lambda: 'HEAD'

   try:
       urllib.request.urlopen(request)
       return True
   except urllib.request.HTTPError:
       return False
   
def create_new_ldict(old_ldict, old_key, new_key):
    '''
    Function to build upon existing list of dictionary (eg. adds course numbers to ldict_dept, adds sections to ldict_dept_course)
    Note: does not work for coure schedule because json from these sites are not lists of dictionaries
    @param old_ldict - current list of dictionary to be built upon
    @param old_key - key in SFU's json corresponding to value of interest
    @param new_key - key name chosen to correspond with value in new dictionaries
    '''
    new_ldict = []
    for dictionary in old_ldict:
        webname = SFU_DATA_WEBSITE
        for key in dictionary:
            webname += dictionary[key] +'/'
        if url_is_alive(webname):
            unrefined_ldict = get_data_from_url(webname)
            for item in unrefined_ldict:
                new_dict = {}
                new_dict.update(dictionary)
                new_dict[new_key] = item[old_key]
                new_ldict.append(new_dict)
    return new_ldict

import urllib.request
import json

def all_considered_rooms(biglist):
    room_dict={}
    for dic in biglist:
        for indict in dic['schedule']:
            if 'buildingCode' in indict:
                if indict['buildingCode'] not in room_dict:
                    room_dict[indict['buildingCode']]=[]
            if 'roomNumber' in indict:
                if indict['roomNumber'] not in room_dict[indict['buildingCode']]:
                    room_dict[indict['buildingCode']].append(indict['roomNumber'])
    return room_dict
                
    

def bookings_by_day(two_letter_weekday, biglist):
    lstarttimes=['8:30', '9:00', '9:30', '10:00', '10:30', '11:00', '11:30', '12:00', '12:30', '13:00', '13:30', '14:00',
            '14:30', '15:00', '15:30', '16:00', '16:30', '17:00', '17:30', '18:00', '18:30', '19:00', '19:30', '20:00', '20:30']
    lendtimes=['8:20', '8:50', '9:20', '9:50', '10:20', '10:50', '11:20', '11:50', '12:20', '12:50', '13:20', '13:50', '14:20',
               '14:50', '15:20', '15:50', '16:20', '16:50', '17:20', '17:50', '18:20', '18:50', '19:20', '19:50', '20:20']
    dfull_by_time={'8:30':[], '9:00': [], '9:30': [], '10:00': [], '10:30': [], '11:00': [], '11:30': [], '12:00': [],
                   '12:30': [], '13:00': [], '13:30': [], '14:00': [], '14:30': [], '15:00': [], '15:30': [], '16:00': [],
                   '16:30': [], '17:00': [], '17:30': [], '18:00': [], '18:30': [], '19:00': [], '19:30': [], '20:00': []}
    for dic in biglist:
        for indict in dic['schedule']:
            if indict['days']==two_letter_weekday:
                startfound="nah"
                endfound="nope"
                check=0
                while startfound=="nah" and check<len(lstarttimes):
                    if indict['startTime']==lstarttimes[check]:
                        startfound=lstarttimes[check]
                    else: check+=1
                checkend=0
                while endfound=="nope" and checkend<len(lendtimes):
                    if indict['endTime']==lendtimes[checkend]:
                        endfound=lendtimes[checkend]
                        for index in range(check, checkend):
                             dfull_by_time[lstarttimes[index]].append(indict['buildingCode']+" "+indict['roomNumber'])
                    checkend+=1
    return dfull_by_time 

#Top Level Variables
CURRENT_YEAR = "2018"
CURRENT_SEASON = "fall"
SFU_DATA_WEBSITE = "http://www.sfu.ca/bin/wcm/course-outlines?"+CURRENT_YEAR+"/"+CURRENT_SEASON+"/"

ldict_dept = create_new_ldict([{}], 'text', 'department')

ldict_dept_course = create_new_ldict(ldict_dept, 'text', 'course')

ldict_dept_course_sect = create_new_ldict(ldict_dept_course, 'text', 'section')

ldict_sched = []
for dictionary in ldict_dept_course_sect:
    webname = SFU_DATA_WEBSITE
    for key in dictionary:
        webname += dictionary[key] +'/'
    if url_is_alive(webname):
        unrefined_dict = get_data_from_url(webname)
        ldict_sched += unrefined_dict['courseSchedule']

