REDESIGN OF SOLARCALCULATOR IN PYTHON
Aiming to improve present version.
The major change is to use the library pytz contaaining tzinfo and datetime e.g. function timedelta instead of timezones saved in my data table directly.

Changes are tested using Libre Office Spreadsheet macOS version 26.2.2.2 (AARCH64)

1. Defining Julian Day Number (incl. the current date and time for any timezone)
First must be defined dateformat in spreadsheet. I'm using our national short format DD.MM.YY
e.g. 2026-04-10 is shown with format 10.04.26 .

more examples of date numbering of spreadsheet
Day number	Date
0	    30.12.1899
1	    31.12.1899
2   	01.01.1900
46023	01.01.2026
46122	10.04.2026

Julian date is calculated from the date as follows:
  JD = daynumber + 2415018
e.g. date 10.04.2026 resulting JD 2461140

Local time part hh:mm:ss is added to JD as fraction of day (24 hours):
JDN = JD + (hours + minutes/60 + seconds/3600 - timezoneHours)/24 + 0.5
It is converted to utc subtracting local timezone 3 h east from utc 3/24
e.g. local time 11:45:30 at timezone UTC + 3
JDN = 2461140 + (11 + 45/60 + 30/3600 - 3)/24 +0.5
As Julian date change is at 12:00 instead of usual 00:00 (or 24:00), 0.5 is added 
thus final JDN for utc time is 2461140.864931

Maybe shortest way to time conversions from local to utc or vice versa :
  print("UTC current time:", a.strftime('%Y-%m-%d %T %Z'))
  print("Same time other timezone:", b.strftime('%Y-%m-%d %T %Z'))

The time components can be retrieved easily to be used for Julian date.
  print("UTC", (a.year, a.month, a.day, a.hour, a.minute, a.second))
  print("Local", (b.year, b.month, b.day, b.hour, b.minute, b.second))

UTC current time: 2026-04-10 21:08:40 UTC
Same time other timezone: 2026-04-11 00:08:40 EEST
UTC (2026, 4, 10, 21, 8, 40)
Local (2026, 4, 11, 0, 8, 40)

How can we get the right datenumber of the current date?
We can calculate it using timedelta, the first date d0 1899-12-30 and the current date d2 2026-04-11.
>>> from datetime import datetime, timedelta
>>> date0 = datetime(1899,12,31)
>>> date2 = datetime(2026,4,11,0,0,0)
>>> d = date2 - date0
>>> d
datetime.timedelta(days=46123)
>>> d.days
46213
>>> jd = d.days + 2415018
>>> jd
2461141
>>>
Note, d is of type datetime.timedelta
>>> type(d)
<class 'datetime.timedelta'>
For local time 11:45:30 UTC+3
>>> jdn = 2461140 + (11 + 45/60 + 30/3600 - 3)/24 +0.5
>>> jdn
2461141.8649305557
Converting local time to utc before calculating jdn, you may just forget your local timezone:
>>> date2 = datetime(2026, 4, 11, 11, 45, 30)
>>> utcdate = date2.astimezone(pytz.utc)
>>> utcdate
datetime.datetime(2026, 4, 11, 8, 45, 30, tzinfo=<UTC>)
>>> 
thus, jdn may be calculated for converted utc time 08:45 on 2026-04-11
>>> jdn = 2461141 + (8 + 45/60 + 30/3600)/24 +0.5
>>> jdn
2461141.8649305557
Finally, we shall calculate the variable jcent, let's call it here Julian Century.
It has the min value 0.0 in the beginning of century and 1.0 at the end of century.
>>> jcent = (jdn - 2451545)/36525
>>> jcent
0.26274784204122353
