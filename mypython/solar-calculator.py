# We are building a new version of solar calculator using Python
# First we need to convert the current local time to Julian Day (JD)
# The JD calculation is based on the algorithm from
# "Astronomical Algorithms" by Jean Meeus, 1991
# Chapter 7, page 61, formula 7.1
# However, I don't use libraries like astropy to do the conversion
# to keep the code self-contained and easy to understand
# I have i fact studied the solar functions presented in the spreadsheet of 
# NOAA solar calculator in libreoffice format and translated them to Python functions
# The algorithm should work for all Gregorian dates after 1582-10-15
# The JD starts at noon UTC, so we need to adjust the time accordingly
# We also calculate the timezone offset from UTC

import time, datetime
d = datetime.datetime.now()
print("Current local time", d.strftime("%Y-%m-%d %H:%M:%S"))
y, m, d_ = d.year, d.month, d.day
hr,mn,sc = d.hour, d.minute, d.second

def jdn_from_date(yr, mnt, day) :
    result = 367*yr - 7*(yr + (mnt + 9)//12)//4 \
    - 3*((yr + (mnt - 9)//7)//100 + 1)//4 \
    + 275*mnt//9 + day + 1721029
    return(result)


jdn = jdn_from_date(y, m, d_)

print("Julian Day Number JDN", jdn)
print("year",y,"month",m,"day",d_)

tposix = time.mktime(d.timetuple())
print("Epoch seconds", tposix)
tday = 24*3600
seconds = tposix % 60
print("Current time seconds part", seconds)

days = tposix // tday
print("Epoch (1970-01-01) posix daynumber", days)

dsecs = tposix % tday
print(f"remaining of today {dsecs} sec")

utc_hours = dsecs // 3600
print("Hours of current UTC time", utc_hours)

tz_offset = utc_hours - d.hour
# Needs correction as utc offset cannot be less than -12 h or more than +12 h
# If local time is 00:00:00 to 01:00:00 an timezone +2h, offset should be -2 h
# Correction: if tz_offset > 12 then tz_offset = tz_offset - 24
# respectively for positive offset (west from Greenwich) 
# If local time is tz_offset < -12 then tz_offset = tz_offset + 24
# Combined both conditions results:
if tz_offset > 12:
    tz_offset -= 12

if tz_offset < -12:
    tz_offset += 12

# NOTE Also the date must be corrected: keep yesterday for for east from Greenwich (tz_offset < 0)
# Not corrected in this version!

print(f"Timezone Offset {tz_offset} hours from UTC")

# Local time 
x = datetime.datetime(y, m, d_, hr, mn, sc)
print("Local time:", x.strftime("%A, %Y-%m-%d %H:%M:%S"), f"UTC {-tz_offset} h")

# UTC Time
ut = datetime.datetime(y, m, d_, hr + int(tz_offset), mn, sc) # UTC time
print("UTC time:  ", ut.strftime("%A, %Y-%m-%d %H:%M:%S"))

jd_afternoon = jdn + (hr + tz_offset - 12) / 24 + mn / 60 / 24 + sc / 3600 / 24
jd_morning = jdn - 0.5 + (hr + tz_offset) / 24 + mn / 60 / 24 + sc / 3600 / 24

jd_selected = jd_morning if (utc_hours < 12) else jd_afternoon

print("Selected JD", round(jd_selected,6))
# You can check the calculation with online JD calculators
# Example : https://www.aavso.org/jd-calculator
# https://ssd.jpl.nasa.gov/tools/jdc/#/jd_calculator
# We can also use astropy to verify the result
# from astropy.time import Time
# t = Time(x, scale='utc')
# print("Astropy JD", round(t.jd,6))

# Next we continue with defining the functions for calculating the solar position for given location and time
# using NOAA solar model, see https://gml.noaa.gov/grad/solcalc/solareqns.PDF
# The required functions are translated manually from the NOAA's spreadsheet
# and attached in the file noaa-solar.py

# We shall define first the function 'Julian Century' which is used
# frequently as argument of many further functions.
# As the latest epoch is J2000.0 at JD 2451545.0, it is the starting point for
# solar functions depending on time.
def julian_century(jd):
    """Calculate Julian Century from Julian Day"""
    jc = (jd - 2451545.0) / 36525.0
    return jc

jc = julian_century(jd_selected)
print("Julian Century JC", round(jc,8))

# NOTE: INCORRECT TIMEZONE OFFSET AS LOCAL TIME IS OVER 24:00
# NEEDS TO ADJUST THE DATE AND JD ACCORDINGLY
# THIS WILL BE FIXED IN THE NEXT VERSION
# Output was following when local time was 2024-06-30 25:15:30
"""
Current local time 2026-01-20 01:08:15
Julian Day Number JDN 2461061
year 2026 month 1 day 20
Epoch seconds 1768864095.0
Current time seconds part 15.0
Epoch (1970-01-01) posix daynumber 20472.0
remaining of today 83295.0 sec
Hours of current UTC time 23.0
Timezone Offset 22.0 hours from UTC
# INCORRECT: (utc - local) = (23 - 01) h = 22 h, should be -2h
Local time: Tuesday, 2026-01-20 01:08:15 UTC -22.0 h 
# INCORRECT timezone offset +22 h, needs to be -2 h
UTC time:   Tuesday, 2026-01-20 23:08:15 " 
# Correct utc-hour 23, INCORRECT day 01-20 and weekday 'Tuesday',
# needs to be 'Monday 19th' because UTC-hour is still less than 24
"""

# Selected JD 2461061.464063   
# NOTE correct value inspite of incorrect utc-offset
# Julian Century JC 0.26054659
