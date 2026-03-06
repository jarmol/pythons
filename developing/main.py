import time, datetime
from math import pi 
from citydata import *
from solarfuncs import *

black_bg = "\033[40m"
white_text = "\033[97m"
green_text = "\033[92m"
yellow_text = "\033[93m"
clear_screen = "\033[2J"
print(black_bg, white_text, clear_screen + "Welcome to the Python Solar Calculator!")
#runmode = input("Use mode d for debuging: ") or 'r'
runmode = 'r'
t=''

for j in range(0,8):
    t += suncities[j]['cityNumber'] + '. ' + suncities[j]['cityName']
    t+= ', '
    if j == 6: t += '\n'


print(t)


cNr =  input("City number (1 - 8): ") or "1"
cNr = int(cNr) - 1

if -1 < cNr < 8:
    latitude = suncities[cNr]['latitude']
    longitude = suncities[cNr]['longitude']
    longitude = float(longitude)
    latitude = float(latitude)
    tz_city = suncities[cNr]['tz_city']
    cityName = suncities[cNr]['cityName']
    cityNumber = cNr + 1
elif cNr == 8:
    longitude = input("Enter your longitude in degrees (east +, west -): ") or 24.9
    longitude = float(longitude)
    latitude = input("Enter your latitude in degrees (north +, south -): ") or 60.2
    latitude = float(latitude)
    tz_city = input("Enter your time zone (west neg., east pos. ): ") or 2.0
    tz_city = float(tz_city)
    cityName = "No name"
else:
    print("Index out of range!")
    print("Nr", cNr )
    cNr = 0
    print("Using location", suncities[0]['cityName'])


d = datetime.datetime.now()
if runmode == 'd': print("Current local time", d.strftime("%Y-%m-%d %H:%M:%S"))
y, m, d_ = d.year, d.month, d.day
hr,mn,sc = d.hour, d.minute, d.second


def jdn_from_date(yr, mnt, day) :
    result = 367*yr - 7*(yr + (mnt + 9)//12)//4 \
    - 3*((yr + (mnt - 9)//7)//100 + 1)//4 \
    + 275*mnt//9 + day + 1721029
    return(result)

jdn = jdn_from_date(y, m, d_)

if runmode == 'd':
    print("Julian Day Number JDN", jdn)
    print("year",y,"month",m,"day",d_)

tposix = time.mktime(d.timetuple())
if runmode == 'd': print("Epoch seconds", tposix)

tday = 24*3600
seconds = tposix % 60
if runmode == 'd': print("Current time seconds part", seconds)

days = tposix // tday
if runmode == 'd': print("Epoch (1970-01-01) posix daynumber", days)

day_seconds = tposix % tday
if runmode == 'd': print(f"remaining of today {day_seconds} sec")

utc_hours = int(day_seconds // 3600)
if runmode == 'd': print("Hours of current UTC time", utc_hours)

cet_hours = utc_hours + 1
tz_offset = time.timezone / 3600
# NEW: Show the sign (+/-) of timezone offset correctly
# Note, the sign is inverted when showing UTC offset
tz_sign = ''

if tz_offset > 0:
    tz_sign = '-'
elif tz_offset == 0: tz_sign = ' '
else :
    tz_sign = '+'


if runmode == 'd': print(f"Timezone Offset {tz_offset} hours from UTC")

# Local time 
x = datetime.datetime(y, m, d_, hr, mn, sc)
tloc = hr + mn / 60 + sc / 3600 # Local time in hours decimal

# UTC Time
print("debug utc_hours",utc_hours)

if utc_hours >=  22:
    d_ -= 1
    
# CET time
#if cet_hours > 24 + tz_offset:
#    d_ -= 1

if cet_hours > 23:
    cet_hours -= 24
    d_ += 1

print('debug cet_hours =',cet_hours)
ut = datetime.datetime(y, m, d_, utc_hours, mn, sc) # UTC time
et = datetime.datetime(y, m, d_, cet_hours, mn, sc) # CET time

jd_morning = jdn - 1.5 + (hr + tz_offset) / 24 + mn / 60 / 24 + sc / 3600 / 24
jd_morning += 1.0 
jd_afternoon =   jdn - 0.5 + (hr + tz_offset) / 24 + mn / 60 / 24 + sc / 3600 / 24

def rad(x): # converting degrees to radians
    return(pi * x / 180.0)

def deg(x): # converting radians to degrees
    return(180.0 * x / pi)

def julian_century(jd):
# Calculate Julian Century from Julian Day
    jc = (jd - 2451545.0) / 36525.0
    return jc

jd_selected = jd_morning if (utc_hours < 12) else jd_afternoon
jc = julian_century(jd_selected) 

sd = sun_declination(jc)
cet_offset = -1
print(" Local time:", x.strftime("%A, %Y-%m-%d %H:%M:%S"), f"Timezone UTC {tz_sign}{abs(tz_offset)} h")
print(" CET time:  ", et.strftime("%A, %Y-%m-%d %H:%M:%S"), f"Timezone UTC {tz_sign}{abs(cet_offset)} h")
print(" UTC time:  ", ut.strftime("%A, %Y-%m-%d %H:%M:%S"))

if 0 <= cNr < 9:
    print("index",cNr)
    print(f"{cityName}: Latitude {latitude}°, Longitude {longitude}°")
else: print("index out of range!", cNr)

haSunR = haSunrise(latitude, sd)
if runmode == 'd': print("haSunrise", round(haSunR,6))


tst = true_solar_time(longitude, hr, mn, sc, tz_offset, jc)
if runmode == 'd': print("True Solar Time (minutes)", round(tst,6))

hourAngle = hour_angle(tst)
if runmode == 'd': print("hourAngle=", round(hourAngle,6))

if tz_city == 2:
    solarNoon = solar_noon(longitude, jc, tz_offset)
    print(yellow_text, "|    Eastern European normal time UTC + 2 h")
    print(' |    Noon time        ', solarNoon[0])

if tz_city == 1:
    cet_offset = -1
    print(yellow_text, "|    Central European normal time UTC + 1 h")
    cetNoon   = solar_noon(longitude, jc, cet_offset)
    print(' |    Noon time        ', cetNoon[0])

if tz_city == 0:
    utc_offset =  0
    utNoon    = solar_noon(longitude, jc, utc_offset)
    print(yellow_text, "|    Western European time UTC + 00:00")
    print(' |    Noon time        ', utNoon[0])

if tz_city == 2:
    sunrise_str = sun_time(solarNoon[1], haSunR, tz_offset)
    print(" |    Sunrise time     ", sunrise_str)
    sunset_str = sun_time(solarNoon[1], -haSunR, tz_offset)
    print(" |    Sunset time      ", sunset_str)

if tz_city == 1:
    sunrise_cet = sun_time(cetNoon[1], haSunR, cet_offset)
    print(" |    Sunrise time     ", sunrise_cet)
    sunset_cet = sun_time(cetNoon[1], -haSunR, cet_offset)
    print(" |    Sunset time      ", sunset_cet)


if tz_city == 0:
    sunrise_utc = sun_time(utNoon[1], haSunR, utc_offset)
    print(" |    Sunrise time     ", sunrise_utc)
    sunset_utc = sun_time(utNoon[1], -haSunR, utc_offset)
    print(" |    Sunset time      ", sunset_utc) 


dayLength = 2 * haSunR / 15 # in decimal hours
if runmode == 'd': print("Daylength (hours)     ", round(dayLength,4))
dlhr = int(dayLength)
dlmn = int((dayLength - dlhr) * 60)
dlsc = (dayLength - dlhr - dlmn / 60) * 3600
print(f" |    Daylength         {dlhr} h {dlmn} min {round(dlsc)} sec")

sza = solar_zenith_angle(hourAngle, latitude, sd)
if runmode == 'd': print("Solar Zenith Angle (degrees)", round(sza,6))

saz = solar_azimuth(hourAngle, sza, sd, latitude)

print(f" |    Solar elevation w/o refraction          {round(90.0 - sza, 3)}°")

refract = atmosRefract(90.0 - sza)
cor_elev = 90.0 - sza + refract
print(f" |    Solar elevation, refraction corrected   {round(cor_elev,3)}°")
print(f" |    Solar Azimuth (clockwise from north)   {round(saz, 3)}°")
print(green_text)
print(" Julian Date (JD) for current time and date", round(jd_selected,6))
print(" Julian Century JC", round(jc,8))
print(f" Sun declination   {round(sd,6)}°")
print(f" Approx. atmospheric refraction {round(refract,5)}°")

"""
This is now OK as I changed it more functional: used only input variables, no global variables 
direct calls. That is just the way to avoid hidden errors, if the variables are afterwards
changed globally.
"""
