#importing libraries
import requests
from tzlocal import get_localzone
import requests
import json
from datetime import datetime, timedelta


interviewer_data =  {
    "mail" : 'sumeet.kumar@thinsil.com',
    "from_time" : datetime.now(),
    "to_time" : datetime.now() + timedelta(days=7),
    "timeInterval" : 60
}
url = f'https://graph.microsoft.com/v1.0/users/{interviewer_data['mail']}/calendar/getschedule'

#Getting token
def get_access_token(client_id='310ebdea-e9b8-4fc5-854a-508e88926264',
                     client_secret='3PF8Q~rnFlpJevaeae.zsL666YlHzQ3e_VpTWdnE',
                     tenant_id='5b17af8c-0eb5-4a44-a2d7-559439dfaeba'):
    token_url = f'https://login.microsoftonline.com/{tenant_id}/oauth2/v2.0/token'
    token_data = {
        'grant_type': 'client_credentials',
        'client_id': client_id,
        'client_secret': client_secret,
        'scope': 'https://graph.microsoft.com/.default'
    }

    token_response = requests.post(token_url, data=token_data)
    if token_response.status_code == 200:
        access_token = token_response.json().get('access_token')
        print("Token Accessed successfully")
        return access_token
    else:
        print("Failed to obtain access token:", token_response.text)
        return None

# Usage:
token = get_access_token()


#timezone
def get_timezone():

    timezone_name = get_localzone()

    timezone_abbreviations = {
        'Asia/Calcutta': 'India Standard Time',   # Indian Standard Time
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
    url = f'https://graph.microsoft.com/v1.0/users/{interviewer_data["mail"]}/calendar/getschedule'
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

        if len(day) == 5:

            return free_timings
        else:
            current_date = datetime.now() + timedelta(days=7)
            return self.check_schedule(day, current_date)

    def proposeInterviewData(self):
        
        vacant_timing = self.check_schedule()
        start = vacant_timing[0] + timedelta(days=1)
        end= timedelta(hours=1)
        end = start + end
        timezone = get_timezone()
        
        url = f'https://graph.microsoft.com/v1.0/users/{interviewer_data["mail"]}/events'

        headers = {
            'Authorization': f'Bearer  {token}',  # Replace 'YOUR_ACCESS_TOKEN' with your actual access token
            'Prefer': f'outlook.timezone= "{timezone}"',
            'Content-type': 'application/json'
        }

        data = {
            "subject": "Next Round Interview",
            "body": {
                "contentType": "HTML",
                "content": "This is the proposed time"
            },
            "start": {
                "dateTime": f"{start.strftime('%Y-%m-%dT%H:%M:%S')}",
                "timeZone": f"{timezone}"
            },
            "end": {
                "dateTime": f"{end.strftime("%Y-%m-%dT%H:%M:%S")}",
                "timeZone": f"{timezone}"
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


interview_response =  calender_data_func(mail= interviewer_data['mail'],
                                        timezone=get_timezone(),
                                        from_time=interviewer_data['from_time'],
                                        to_time=interviewer_data['to_time'],
                                        timeinterval=interviewer_data['timeInterval'], 
                                        token=token
                                        )
data = interview_response.json()


if interview_response.status_code == 200:
    try: 
        meetingcreate = MeetingScheduler(data)
        event = meetingcreate.proposeInterviewData()
        if event.status_code == 201:
            print('Meeting Created')
        else:
            print("Meeting creation error...")
            
    except Exception as e:
        print("Internal Error: ", e)
else:
    print('External error')
