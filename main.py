#importing libraries
import requests
from tzlocal import get_localzone
import requests
import json
from datetime import datetime, timedelta

#Authorization data 
token = 'eyJ0eXAiOiJKV1QiLCJub25jZSI6Ilo0VjllWDlnaWRVT3hiTVhaZDJqdFMzQUZvU0g2aThJN3pMMVRJcEZ2WWMiLCJhbGciOiJSUzI1NiIsIng1dCI6IlQxU3QtZExUdnlXUmd4Ql82NzZ1OGtyWFMtSSIsImtpZCI6IlQxU3QtZExUdnlXUmd4Ql82NzZ1OGtyWFMtSSJ9.eyJhdWQiOiJodHRwczovL2dyYXBoLm1pY3Jvc29mdC5jb20iLCJpc3MiOiJodHRwczovL3N0cy53aW5kb3dzLm5ldC81YjE3YWY4Yy0wZWI1LTRhNDQtYTJkNy01NTk0MzlkZmFlYmEvIiwiaWF0IjoxNzAyNTYyODYxLCJuYmYiOjE3MDI1NjI4NjEsImV4cCI6MTcwMjU2Njc2MSwiYWlvIjoiRTJWZ1lOaGpMc29rbWpiUi90blJMVXNVOXhaRUFRQT0iLCJhcHBfZGlzcGxheW5hbWUiOiJNZWV0aW5nIFNjaGVkdWxlciIsImFwcGlkIjoiMzEwZWJkZWEtZTliOC00ZmM1LTg1NGEtNTA4ZTg4OTI2MjY0IiwiYXBwaWRhY3IiOiIxIiwiaWRwIjoiaHR0cHM6Ly9zdHMud2luZG93cy5uZXQvNWIxN2FmOGMtMGViNS00YTQ0LWEyZDctNTU5NDM5ZGZhZWJhLyIsImlkdHlwIjoiYXBwIiwib2lkIjoiOTZhNWFlZWQtZDc2ZC00ZTcwLWE3ZmEtOGM5Njg1ZTU4OTUwIiwicmgiOiIwLkFUMEFqSzhYVzdVT1JFcWkxMVdVT2QtdXVnTUFBQUFBQUFBQXdBQUFBQUFBQUFDaEFBQS4iLCJzdWIiOiI5NmE1YWVlZC1kNzZkLTRlNzAtYTdmYS04Yzk2ODVlNTg5NTAiLCJ0ZW5hbnRfcmVnaW9uX3Njb3BlIjoiQVMiLCJ0aWQiOiI1YjE3YWY4Yy0wZWI1LTRhNDQtYTJkNy01NTk0MzlkZmFlYmEiLCJ1dGkiOiI4ZFZGd1k4M2trNnNGRGEwSlVwT0FBIiwidmVyIjoiMS4wIiwid2lkcyI6WyIwOTk3YTFkMC0wZDFkLTRhY2ItYjQwOC1kNWNhNzMxMjFlOTAiXSwieG1zX3RjZHQiOjE2OTk4NDk5NzB9.HBDDtqERbczbTS6-CiQ8IlB4VZyPq5iZMnkOQC27vNf1pjEXP0bag4MULHQzYpDNkt5nZ3llinF8NfwQJL3MHZ4LOArulk7LvZboV33jraWS8S7PxmR_6NQgzRrfMj3zwI-S-Awo5RqCuBFwAgTBU-9tF6xB-nF-bpF_jsX3wTlYLCIzbwg4qUCT4C9cbs30VwVVNhlcp90qm1zowW-E4gbRWr-YiBelkJ5V5O0hDmPUmhS-zV8EQ1a9JATgzXmFgL6vuzUNGkBD2OhTYT-PkAKvHaqB21elXI07kSPOE9fu23t8EepKZZQi6vrfi-ZLFHdN7Ys8Jf3roPMP2O0ZPw'

interviewer_data =  {
    "mail" : 'sumeet.kumar@thinsil.com',
    "from_time" : datetime.now(),
    "to_time" : datetime.now() + timedelta(days=7),
    "timeInterval" : 15
}
url = f'https://graph.microsoft.com/v1.0/users/{interviewer_data['mail']}/calendar/getschedule'


#timezone
def get_timezone():

    timezone_name = get_localzone()

    timezone_abbreviations = {
        'Asia/Calcutta': 'Indian Standard Time',  # Indian Standard Time
        'America/New_York': 'Eastern Standard Time',  # Eastern Standard Time (USA)
        'America/Los_Angeles': 'Pacific Standard Time',  # Pacific Standard Time (USA)
        'Europe/London': 'Greenwich Mean Time',  # Greenwich Mean Time
        'Australia/Sydney': 'Australian Eastern Daylight Time',  # Australian Eastern Daylight Time
        # Add more mappings as needed   
    }

    timezone = timezone_abbreviations[f'{timezone_name}']
    return timezone

timezone = get_timezone()

def calender_data_func(from_time, timezone, to_time, timeinterval, mail, token):
    url = f'https://graph.microsoft.com/v1.0/users/sumeet.kumar@thinsil.com/calendar/getschedule'
    print(timezone, to_time, from_time, mail)
    if token:
        print("True")
    calender_data = {        
        "Schedules": [f"{mail}"],
        "StartTime": {
            "dateTime": f"{from_time}",
            "timeZone": f"{timezone}"
        },
        "EndTime": {
            "dateTime": f"{to_time}",
            "timeZone": f"{timezone}"
        },
        "availabilityViewInterval": f"{timeinterval}"
    }

    header = {
        'Prefer' :f'outlook.timezone="{timezone}"',
        'Authorization': f'Bearer {token}',  
        'Content-Type' : 'application/json'
        }

    # data = calender_data

    response = requests.post(url, headers=header, data=json.dumps(calender_data))
    return response


class MeetingScheduler:

    def __init__(self, interviewer_respose):
        self.Intresponse = interviewer_respose
        self.Intend, self.Intstart = self.getTimings()

    def getTimings(self):
        schedule = self.Intresponse["value"][0]['scheduleItems']
        startdt = []
        enddt = []
        
        cleaned_start = []
        cleaned_end = []

        for item in schedule:
            startdt.append(item['start']['dateTime'])
            enddt.append(item['end']['dateTime'])

        for dt in startdt:
            cleaned_dt = dt.replace('-', '').replace('T', '').replace(':', '').replace('.', '')
            cleaned_start.append(cleaned_dt)
        
        for dt in enddt:
            cleaned_dt = dt.replace('-', '').replace('T', '').replace(':', '').replace('.', '')
            cleaned_end.append(cleaned_dt)
        
        end_time = [datetime.strptime(ts, '%Y-%m-%d %H:%M:%S') for ts in self.extract_busy_duration(cleaned_end)]
        start_time = [datetime.strptime(ts, '%Y-%m-%d %H:%M:%S') for ts in self.extract_busy_duration(cleaned_start)]

        return end_time, start_time

    def extract_busy_duration(self, times):
        timings = []
        for start in times:
            time = datetime.strptime(start[:14], '%Y%m%d%H%M%S')
            time = str(time)
            timings.append(time)
        return timings
    
    def check_schedule(self, day = None, current_date = None):
        
        if current_date is None:
            current_date = datetime.now()

        free_timings = []  # List to store free timings
        if day is None:
            day = []

        # Loop through the next 7 days
        for _ in range(7):
            if current_date.weekday() in (5, 6):  # Skip weekends
                current_date += timedelta(days=1)
                continue
        
            # Check for free times between 10 and 18 hours
            for hour in range(10, 19):
                check_time = current_date.replace(hour=hour, minute=0, second=0)

                # Check if the hour falls outside of any busy slot
                Int_busy = False

                for busy_start, busy_end in zip(self.Intstart, self.Intend):  # Assuming these are sorted lists
                    if busy_start <= check_time < busy_end:
                        Int_busy = True
                        break
                if not Int_busy:
                    free_timings.append(check_time)
                    day.append(check_time.weekday())

        
        
            current_date += timedelta(days=1)
        day = list(sorted(set(day)))
        print(day)

        if len(day) == 5:

            return free_timings
        else:
            current_date = timedelta(days=7)
            self.check_schedule(day, current_date)

    def proposeInterviewData(self):
        
        vacant_timing = self.check_schedule()
        start = vacant_timing[0]
        end= timedelta(hours=1)
        end = start + end
        timezone = get_timezone()
        
        url = 'https://graph.microsoft.com/v1.0/me/events'

        headers = {
            'Authorization': f'Bearer  {token}',  # Replace 'YOUR_ACCESS_TOKEN' with your actual access token
            'Prefer': f'outlook.timezone= "{timezone}"',
            'Content-type': 'application/json'
        }

        data = {
            "subject": "Next Round Interview",
            "body": {
                "contentType": "HTML",
                "content": "This is the propoed time"
            },
            "start": {
                "dateTime": f"{start.strftime('%Y-%m-%dT%H:%M:%S')}",
                "timeZone": "Pacific Standard Time"
            },
            "end": {
                "dateTime": f"{end.strftime("%Y-%m-%dT%H:%M:%S")}",
                "timeZone": "Pacific Standard Time"
            },
            "location": {
                "displayName": "Online"
            },
            "attendees": [
                {
                    "emailAddress": {
                        "address": "snkatke9874@gmail.com",
                        "name": "Sumeet Katke"
                    },
                    "type": "required"
                }
            ],
            "allowNewTimeProposals": True,
            "isOnlineMeeting": True,
            "onlineMeetingProvider": "teamsForBusiness"
        }

        response = requests.post(url=url, json= data, headers=headers)
        return response




print(interviewer_data['to_time'].strftime("%Y-%m-%dT%H:%M:%S"))

interview_response =  calender_data_func(mail= interviewer_data['mail'],
                                        timezone=get_timezone(),
                                        from_time=interviewer_data['from_time'],
                                        to_time=interviewer_data['to_time'],
                                        timeinterval=interviewer_data['timeInterval'], 
                                        token=token
                                        )

"""
if interview_response.status_code == 200:
    try: 
        meetingcreate = MeetingScheduler(interview_response)
        event = meetingcreate.proposeInterviewData()
        if event.status_code == 201:
            print('Meeting Created')
        else:
            print("Meeting creation error...")
    except Exception as e:
        print("Internal Error: ", e)
else:
    print('External error')

# inst = MeetingScheduler(interview_response)
# inst.check_schedule()
"""
print(interview_response.status_code) 
print(interview_response.text)