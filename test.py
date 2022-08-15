from beautiful_date import Aug, hours
from gcsa.event import Event
from gcsa.google_calendar import GoogleCalendar
from decouple import config

cal_id = config('CAL_ID')

calender = GoogleCalendar(
'primary', credentials_path='new_credentials.json', token_path='token.pickle'
)

start = (16/Aug/2022)[12:00]
end = start + 2 * hours
event = Event('Meeting',
              start=start,
              end=end)

calender.add_event(event)
