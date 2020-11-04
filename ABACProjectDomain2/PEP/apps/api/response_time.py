import datetime
import requests
 
url = ''
 
try:
    r = requests.get(url, timeout=6)
    r.raise_for_status()
    respTime = str(round(r.elapsed.total_seconds(),2))
    currDate = datetime.datetime.now()
    currDate = str(currDate.strftime("%d-%m-%Y %H:%M:%S"))
    print(currDate + " " + respTime)
except requests.exceptions.HTTPError as err01:
    print ("HTTP error: ", err01)
except requests.exceptions.ConnectionError as err02:
    print ("Error connecting: ", err02)
except requests.exceptions.Timeout as err03:
    print ("Timeout error:", err03)
except requests.exceptions.RequestException as err04:
    print ("Error: ", err04)