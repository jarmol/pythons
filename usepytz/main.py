#!/usr/local/bin/python3

import time, datetime
from math import pi 
from citydata import *
from solarfuncs import *
import pytz
utc = pytz.utc
datetime = datetime.datetime
strfmt = "%A, %Y-%m-%d %T %Z"
print('tzname',)

black_bg = "\033[40m"
white_text = "\033[97m"
cyan_text = "\033[96m"
green_text = "\033[92m"
yellow_text = "\033[93m"
clear_screen = "\033[2J"
print(black_bg, white_text, clear_screen + "Welcome to the Python Solar Calculator!")
#runmode = input("Use mode d for debuging: ") or 'r'
runmode = 'd'
t=''

for j in range(0, len(suncities)):
    t += suncities[j]['cityNumber'] + '. ' + suncities[j]['cityName']
    if j == 5 or j == 9: t += '\n'
    else: t += ', '

t += "99. Enter values of your own"

print(t)
cNr =  input(f"City number (1 - {len(suncities)}): ") or "1"
cNr = int(cNr)
if (len(suncities) < cNr < 99): cNr = 1 # Invalid index forced to 1 
cNr = cNr - 1

if -1 < cNr < len(suncities):
        latitude = suncities[cNr]['latitude']
        longitude = suncities[cNr]['longitude']
        longitude = float(longitude)
        latitude = float(latitude)
        tz_info = suncities[cNr]['tz_info']
        cityName = suncities[cNr]['cityName']
        cityNumber = cNr + 1
elif cNr == 98:
        longitude = input("Enter your longitude in degrees (east +, west -): ") or 24.9
        longitude = float(longitude)
        latitude = input("Enter your latitude in degrees (north +, south -): ") or 60.2
        latitude = float(latitude)
        tz_info = input("Enter Timezone info e.g. Europe/Berlin ): ") or "Europe/Berlin"
        cityName = "No name"

d = datetime.now() # local
dutc = d.astimezone(pytz.utc) # utc
print("UTC time now", dutc.strftime('%T %Z'))

localTime_str = d.astimezone(pytz.timezone('Europe/Helsinki')).strftime(strfmt) 
tz_id = localTime_str[-4:]
if tz_id in ['EEST', 'CEST']:
    summer = 1
else: summer = 0

print(f" Local time:   {localTime_str} (summer = {summer})")

y, m, d_ = d.year, d.month, d.day
hr,mn,sc = d.hour, d.minute, d.second
uthr,utmn,utsc = dutc.hour, dutc.minute, dutc.second

def jdn_from_date(yr, mnt, day) :
    result = 367*yr - 7*(yr + (mnt + 9)//12)//4 \
    - 3*((yr + (mnt - 9)//7)//100 + 1)//4 \
    + 275*mnt//9 + day + 1721029
    return(result)

jdn = jdn_from_date(dutc.year, dutc.month, dutc.day)

# *** Now Finland, Sweden and Paris is Ok, tested 2026-04-14 ***
# New York, Chicago and Tokyo tested 2026-04-14: Ok
utc_time = datetime.now(pytz.utc) # UTC time
summer = 0 # Day Light Saving in local time 
jd_morning = jdn - 1.5 + uthr / 24 + utmn / 60 / 24 + utsc / 3600 / 24
jd_morning += 1.0 
jd_afternoon =   jdn - 0.5 + uthr / 24 + utmn / 60 / 24 + utsc / 3600 / 24

def rad(x): # converting degrees to radians
    return(pi * x / 180.0)

def deg(x): # converting radians to degrees
    return(180.0 * x / pi)

def julian_century(jd):
# Calculate Julian Century from Julian Day
    jc = (jd - 2451545.0) / 36525.0
    return jc
jd_selected = jd_morning 
if (uthr >= 12): jd_selected = jd_afternoon
print('***',cityName,'***')
print('jd_morning',jd_morning)
print('jd_afternoon', jd_afternoon)
jc = julian_century(jd_selected) 

sd = sun_declination(jc)
localTime_str = utc_time.astimezone(pytz.timezone('Europe/Helsinki')).strftime(strfmt) 
tz_id = localTime_str[-4:]
if tz_id in ['EEST', 'CEST', 'EDT']:
    summer = 1
else: summer = 0

print(clear_screen + "Current times:")
print(f" Local time:  {localTime_str} (summer = {summer})")
print(" GMT time:   ", utc_time.astimezone(pytz.timezone('GMT')).strftime(strfmt))
print(" UTC time:   ", utc_time.strftime(strfmt))
try:
    print(" " + tz_info, utc_time.astimezone(pytz.timezone(tz_info)).strftime(strfmt))
except pytz.UnknownTimeZoneError as err: print('Wrong timezone:', err)

print(cyan_text)
print(f"{cityName}: Latitude {latitude}°, Longitude {longitude}°")

try:
    if type(latitude) == float:    
        haSunR = haSunrise(latitude, sd)
except ValueError as err: print("Latitude near to northern or southern pole", err)

try:
#   tst = true_solar_time(longitude, hr, mn, sc, tz_offset, jc)
#   if 'Tornio' in cityName or 'Helsinki' in cityName or 'Stockholm' in cityName or 'Paris' in cityName:
    tst = true_solar_time(longitude, hr - summer, mn, sc, tz_offset, jc)
except NameError as err: print("Exception:", err)

if runmode == 'd': print("True Solar Time (minutes)", round(tst,6))

try:
    hourAngle = hour_angle(tst)
except NameError as e:
     print('Exception:', e)

if runmode == 'd': print("hourAngle=", round(hourAngle,6))

try:
    if tz_info in tzinfos:
        solarNoon = solar_noon(longitude, jc, tz_info)
        print(yellow_text)
        print(' |    Noon time        ', solarNoon[0])

        sunrise_str = sun_time(solarNoon[1], haSunR, tz_info)
        print(" |    Sunrise time     ", sunrise_str)
        sunset_str = sun_time(solarNoon[1], -haSunR, tz_info)
        print(" |    Sunset time      ", sunset_str)
except NameError as e: print('Exception:', e)

try:
    dayLength = 2 * haSunR / 15 # in decimal hours
    dlhr = int(dayLength)
    dlmn = int((dayLength - dlhr) * 60)
    dlsc = (dayLength - dlhr - dlmn / 60) * 3600
    print(f" |    Daylength         {dlhr} h {dlmn} min {round(dlsc)} sec")
except NameError as e: print('Exception:', e)

try:
    sza = solar_zenith_angle(hourAngle, latitude, sd)

    saz = solar_azimuth(hourAngle, sza, sd, latitude)

    print(f" |    Sun Altitude without refraction corr.   {round(90.0 - sza, 3)}°")

    refract = atmosRefract(90.0 - sza)
    cor_elev = 90.0 - sza + refract
    print(f" |    Sun Altitude with refraction correction {round(cor_elev,3)}°")
    print(f" |    Solar Azimuth (clockwise from north)   {round(saz, 3)}°")
except NameError as e: print('Exception:', e)
print(green_text)
print(f" Julian Date (JD) for current time and date (summer = {summer}), {round(jd_selected,6)}")
print(" Julian Century JC", round(jc,8))
print(f" Sun declination   {round(sd,6)}°")
print(" Local time offset", tz_offset, 'h')
print(" Equation of Time", round(equation_of_time(jc), 6), "minutes")
print(" True Solar Time (minutes)", round(tst,6))
print(f" Approx. atmospheric refraction {round(refract,5)}°")
# 03.04.26 Tested Helsinki, Tornio and Stockholm Ok