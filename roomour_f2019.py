#Testing New Room App Functions


def all_considered_rooms(biglist):
    '''
    Gives a list of all rooms SFU offers classes at
    '''
    room_dict={}
    lrooms=[]
    for dic in biglist:
        if 'buildingCode' in dic:
            if dic['buildingCode'] not in room_dict:
                room_dict[dic['buildingCode']]=[]
        if 'roomNumber' in dic:
            if dic['roomNumber'] not in room_dict[dic['buildingCode']]:
                room_dict[dic['buildingCode']].append(dic['roomNumber'])
    
    for key in room_dict:
        for room in room_dict[key]:
            lrooms.append(key+" "+room)
    return lrooms

    

def bookings_by_day(two_letter_weekday, biglist):
    '''
    Based on your choice of day, shows what rooms are occupied by half-hour time slots
    '''
    lstarttimes=['8:30', '9:00', '9:30', '10:00', '10:30', '11:00', '11:30', '12:00', '12:30', '13:00', '13:30', '14:00',
            '14:30', '15:00', '15:30', '16:00', '16:30', '17:00', '17:30', '18:00', '18:30', '19:00', '19:30', '20:00', '20:30']
    lendtimes=['8:20', '8:50', '9:20', '9:50', '10:20', '10:50', '11:20', '11:50', '12:20', '12:50', '13:20', '13:50', '14:20',
               '14:50', '15:20', '15:50', '16:20', '16:50', '17:20', '17:50', '18:20', '18:50', '19:20', '19:50', '20:20']
    dfull_by_time={'8:30':[], '9:00': [], '9:30': [], '10:00': [], '10:30': [], '11:00': [], '11:30': [], '12:00': [],
                   '12:30': [], '13:00': [], '13:30': [], '14:00': [], '14:30': [], '15:00': [], '15:30': [], '16:00': [],
                   '16:30': [], '17:00': [], '17:30': [], '18:00': [], '18:30': [], '19:00': [], '19:30': [], '20:00': [], '20:30': []}
    for dic in biglist:
        if 'buildingCode' in dic:
            if two_letter_weekday in dic['days']:
                startfound="nah"
                endfound="nope"
                check=0
                startTimeThere = "yes"
                while startfound=="nah" and check<len(lstarttimes) and startTimeThere == "yes":
                    if 'startTime' in dic:
                    #seems like it's not there for at least one case
                        if dic['startTime']==lstarttimes[check]:
                            startfound=lstarttimes[check]
                        else: check+=1
                    else:
                        startTimeThere = "no"
                checkend=0
                endTimeThere = "yes"
                while endfound=="nope" and checkend<len(lendtimes) and endTimeThere == "yes":
                    if 'endTime' in dic:
                        if dic['endTime']==lendtimes[checkend]:
                            endfound=lendtimes[checkend]
                            for index in range(check, checkend):
                                dfull_by_time[lstarttimes[index]].append(dic['buildingCode']+" "+dic['roomNumber'])
                    else:
                        endTimeThere = "no"
                    checkend+=1
    return dfull_by_time


def empty_by_day(two_letter_weekday, biglist):
    #The information we want!!!
    '''
    Based on your choice of day, shows which rooms are free by half-hour timeslots
    Builds on previous functions
    Grouped by building code, but otherwise not organized yet
    Need to separate by campus as well
    '''
    free_room_dict={'8:30':[], '9:00': [], '9:30': [], '10:00': [], '10:30': [], '11:00': [], '11:30': [], '12:00': [],
                   '12:30': [], '13:00': [], '13:30': [], '14:00': [], '14:30': [], '15:00': [], '15:30': [], '16:00': [],
                   '16:30': [], '17:00': [], '17:30': [], '18:00': [], '18:30': [], '19:00': [], '19:30': [], '20:00': [], '20:30': []}
    timelist=['8:30', '9:00', '9:30', '10:00', '10:30', '11:00', '11:30', '12:00', '12:30', '13:00', '13:30', '14:00',
            '14:30', '15:00', '15:30', '16:00', '16:30', '17:00', '17:30', '18:00', '18:30', '19:00', '19:30', '20:00', '20:30']
    dfull_by_time=bookings_by_day(two_letter_weekday, biglist)
    lrooms=all_considered_rooms(biglist)
    for room in lrooms:
        for time in timelist:
            if room not in dfull_by_time[time]:
                free_room_dict[time].append(room)
    return free_room_dict

def empty_by_time(two_letter_weekday, start_time, biglist):
    day_room_dict = empty_by_day(two_letter_weekday, biglist)
    if start_time in day_room_dict:
        return day_room_dict[start_time]

def empty_by_window(two_letter_weekday, start_time, end_time, biglist):
    ltimes = ['8:30', '9:00', '9:30', '10:00', '10:30', '11:00', '11:30', '12:00', '12:30', '13:00', '13:30', '14:00',
            '14:30', '15:00', '15:30', '16:00', '16:30', '17:00', '17:30', '18:00', '18:30', '19:00', '19:30', '20:00', '20:30']
    day_room_dict = empty_by_day(two_letter_weekday, biglist)
    oldlist = empty_by_time(two_letter_weekday, start_time, biglist)
    start_index=0
    end_index=0
    start_temp=0
    end_temp=0
    newlist = []
    for time in ltimes:
        if time == start_time:
            start_index=start_temp
        if time == end_time:
            end_index=end_temp
          
        start_temp += 1
        end_temp += 1
    index = start_index
    while (index < end_index):
        templist=empty_by_time(two_letter_weekday, ltimes[index], biglist)
        newlist=[]
        for room in templist:
            if room in oldlist:
                newlist.append(room)
        oldlist=newlist
        index+=1
    print("\n\nRooms available from", start_time, "to", end_time, "on", two_letter_weekday+":\n")
    return newlist

def room_info(room, two_letter_weekday, biglist):

	timelist = ['8:30', '9:00', '9:30', '10:00', '10:30', '11:00', '11:30', '12:00', '12:30', '13:00', '13:30', '14:00',
            '14:30', '15:00', '15:30', '16:00', '16:30', '17:00', '17:30', '18:00', '18:30', '19:00', '19:30', '20:00', '20:30']
	room_use_dict = {'8:30': 'in use', '9:00': 'in use', '9:30': 'in use', '10:00': 'in use', '10:30': 'in use', '11:00': 'in use', '11:30': 'in use', '12:00': 'in use', 
                   '12:30': 'in use', '13:00': 'in use', '13:30': 'in use', '14:00': 'in use', '14:30': 'in use', '15:00': 'in use', '15:30': 'in use', '16:00': 'in use', 
                   '16:30': 'in use', '17:00': 'in use', '17:30': 'in use', '18:00': 'in use', '18:30': 'in use', '19:00': 'in use', '19:30': 'in use', '20:00': 'in use',                                 '20:30': 'in use'}
    
	for time in timelist:
		if room in empty_by_time(two_letter_weekday, time, biglist):
			room_use_dict[time] = 'free'
	return room_use_dict
            
        

testlist=[{'department': 'ACMA', 'course': '210', 'section': 'D100', 'schedule': [{'startTime': '10:30', 'startDate': 'Tue Sep 04 00:00:00 PDT 2018', 'roomNumber': '1014', 'days': 'Tu', 'endDate': 'Mon Dec 03 00:00:00 PST 2018', 'sectionCode': 'LEC', 'endTime': '11:20', 'isExam': False, 'buildingCode': 'SECB', 'campus': 'Burnaby'}, {'startTime': '9:30', 'startDate': 'Tue Sep 04 00:00:00 PDT 2018', 'roomNumber': '1012', 'days': 'Th', 'endDate': 'Mon Dec 03 00:00:00 PST 2018', 'sectionCode': 'LEC', 'endTime': '11:20', 'isExam': False, 'buildingCode': 'SECB', 'campus': 'Burnaby'}]}, {'department': 'ACMA', 'course': '210', 'section': 'D101', 'schedule': [{'startTime': '9:30', 'startDate': 'Tue Sep 04 00:00:00 PDT 2018', 'roomNumber': '8500', 'days': 'Fr', 'endDate': 'Mon Dec 03 00:00:00 PST 2018', 'sectionCode': 'TUT', 'endTime': '10:20', 'isExam': False, 'buildingCode': 'TASC2', 'campus': 'Burnaby'}]}, {'department': 'ACMA', 'course': '210', 'section': 'D102', 'schedule': [{'startTime': '10:30', 'startDate': 'Tue Sep 04 00:00:00 PDT 2018', 'roomNumber': '7100', 'days': 'Fr', 'endDate': 'Mon Dec 03 00:00:00 PST 2018', 'sectionCode': 'TUT', 'endTime': '11:20', 'isExam': False, 'buildingCode': 'RCB', 'campus': 'Burnaby'}]}, {'department': 'ACMA', 'course': '336', 'section': 'D100', 'schedule': [{'startDate': 'Tue Sep 04 00:00:00 PDT 2018', 'days': '', 'endDate': 'Mon Dec 03 00:00:00 PST 2018', 'sectionCode': 'PRA', 'isExam': False}]}, {'department': 'ACMA', 'course': '336', 'section': 'D200', 'schedule': [{'startDate': 'Tue Sep 04 00:00:00 PDT 2018', 'days': '', 'endDate': 'Mon Dec 03 00:00:00 PST 2018', 'sectionCode': 'PRA', 'isExam': False}]}, {'department': 'ACMA', 'course': '336', 'section': 'I100', 'schedule': [{'startDate': 'Tue Sep 04 00:00:00 PDT 2018', 'days': '', 'endDate': 'Mon Dec 03 00:00:00 PST 2018', 'sectionCode': 'PRA', 'isExam': False}]}, {'department': 'ACMA', 'course': '337', 'section': 'D100', 'schedule': [{'startDate': 'Tue Sep 04 00:00:00 PDT 2018', 'days': '', 'endDate': 'Mon Dec 03 00:00:00 PST 2018', 'sectionCode': 'PRA', 'isExam': False}]}, {'department': 'ACMA', 'course': '337', 'section': 'D200', 'schedule': [{'startDate': 'Tue Sep 04 00:00:00 PDT 2018', 'days': '', 'endDate': 'Mon Dec 03 00:00:00 PST 2018', 'sectionCode': 'PRA', 'isExam': False}]}, {'department': 'ACMA', 'course': '337', 'section': 'I100', 'schedule': [{'startDate': 'Tue Sep 04 00:00:00 PDT 2018', 'days': '', 'endDate': 'Mon Dec 03 00:00:00 PST 2018', 'sectionCode': 'PRA', 'isExam': False}]}, {'department': 'ACMA', 'course': '355', 'section': 'D100', 'schedule': [{'startTime': '14:30', 'startDate': 'Tue Sep 04 00:00:00 PDT 2018', 'roomNumber': '3531', 'days': 'Mo', 'endDate': 'Mon Dec 03 00:00:00 PST 2018', 'sectionCode': 'LEC', 'endTime': '16:20', 'isExam': False, 'buildingCode': 'WMC', 'campus': 'Burnaby'}, {'startTime': '14:30', 'startDate': 'Tue Sep 04 00:00:00 PDT 2018', 'roomNumber': '2268', 'days': 'We', 'endDate': 'Mon Dec 03 00:00:00 PST 2018', 'sectionCode': 'LEC', 'endTime': '15:20', 'isExam': False, 'buildingCode': 'WMC', 'campus': 'Burnaby'}]}, {'department': 'ACMA', 'course': '355', 'section': 'D101', 'schedule': [{'startTime': '9:30', 'startDate': 'Tue Sep 04 00:00:00 PDT 2018', 'roomNumber': '2122', 'days': 'Fr', 'endDate': 'Mon Dec 03 00:00:00 PST 2018', 'sectionCode': 'TUT', 'endTime': '10:20', 'isExam': False, 'buildingCode': 'AQ', 'campus': 'Burnaby'}]}, {'department': 'ACMA', 'course': '425', 'section': 'D100', 'schedule': [{'startTime': '11:30', 'startDate': 'Tue Sep 04 00:00:00 PDT 2018', 'roomNumber': '5009', 'days': 'We', 'endDate': 'Mon Dec 03 00:00:00 PST 2018', 'sectionCode': 'LEC', 'endTime': '12:20', 'isExam': False, 'buildingCode': 'AQ', 'campus': 'Burnaby'}, {'startTime': '10:30', 'startDate': 'Tue Sep 04 00:00:00 PDT 2018', 'roomNumber': '5009', 'days': 'Fr', 'endDate': 'Mon Dec 03 00:00:00 PST 2018', 'sectionCode': 'LEC', 'endTime': '12:20', 'isExam': False, 'buildingCode': 'AQ', 'campus': 'Burnaby'}]}, {'department': 'ACMA', 'course': '425', 'section': 'D101', 'schedule': [{'startTime': '12:30', 'startDate': 'Tue Sep 04 00:00:00 PDT 2018', 'roomNumber': '2122', 'days': 'Mo', 'endDate': 'Mon Dec 03 00:00:00 PST 2018', 'sectionCode': 'TUT', 'endTime': '13:20', 'isExam': False, 'buildingCode': 'AQ', 'campus': 'Burnaby'}]}, {'department': 'ACMA', 'course': '436', 'section': 'D100', 'schedule': [{'startDate': 'Tue Sep 04 00:00:00 PDT 2018', 'days': '', 'endDate': 'Mon Dec 03 00:00:00 PST 2018', 'sectionCode': 'PRA', 'isExam': False}]}, {'department': 'ACMA', 'course': '436', 'section': 'D200', 'schedule': [{'startDate': 'Tue Sep 04 00:00:00 PDT 2018', 'days': '', 'endDate': 'Mon Dec 03 00:00:00 PST 2018', 'sectionCode': 'PRA', 'isExam': False}]}, {'department': 'ACMA', 'course': '436', 'section': 'I100', 'schedule': [{'startDate': 'Tue Sep 04 00:00:00 PDT 2018', 'days': '', 'endDate': 'Mon Dec 03 00:00:00 PST 2018', 'sectionCode': 'PRA', 'isExam': False}]}, {'department': 'ACMA', 'course': '437', 'section': 'D100', 'schedule': [{'startDate': 'Tue Sep 04 00:00:00 PDT 2018', 'days': '', 'endDate': 'Mon Dec 03 00:00:00 PST 2018', 'sectionCode': 'PRA', 'isExam': False}]}]

daylist = ["Mo", "Tu", "We", "Th", "Fr"]
timelist = ['8:30', '9:00', '9:30', '10:00', '10:30', '11:00', '11:30', '12:00', '12:30', '13:00', '13:30', '14:00', '14:30', '15:00', '15:30', '16:00', '16:30', '17:00', '17:30', '18:00', '18:30', '19:00', '19:30', '20:00', '20:30']
two_letter_weekday = "init"
start_time = "urmom"
end_time = "macaroni"
while (two_letter_weekday not in daylist):
	two_letter_weekday = raw_input("Enter desired 2-letter weekday (Mo, Tu, We, Th or Fr):  ")
    #using raw_input so it can work on all machines without quotations
print("\n")

answer=0
while (answer != "1" and answer != "2"):
	print("Are you looking for a list of empty rooms for a given time frame, or do you want to know which times a certain room is free?\n") 
	answer = raw_input('Type "1" for the former or "2" for the latter:  ')

print("\nThank you, Roomour will take that into consideration")

if (answer == "1"):

	while (start_time not in timelist):
		start_time = raw_input("Enter desired start time between 8:30 and 20:30 (on the half hour or hour mark only):  ")
	print("\n")
	while (end_time not in timelist):
		end_time = raw_input("Now please enter desired end time between 8:30 and 20:30 (on the half hour or hour mark only):  ")
	print("\n")

	free_rooms=empty_by_window(two_letter_weekday, start_time, end_time, biglist)
	print(free_rooms)

else:
	lrooms = all_considered_rooms(biglist)
	selected_room = "roominate"
	while (selected_room not in lrooms):
		selected_room = raw_input('Please input a valid SFU classroom. For example, "AQ 5020":  ')
	print("\nSchedule for", selected_room, "on", two_letter_weekday, "\n")
	print (room_info(selected_room, two_letter_weekday, biglist))
	