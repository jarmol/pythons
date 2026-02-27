import time, datetime
from math import pi 
from solarfuncs import *

black_bg = "\033[40m"
white_text = "\033[97m"
green_text = "\033[92m"
yellow_text = "\033[93m"
clear_screen = "\033[2J"
print(black_bg, white_text, clear_screen + "Welcome to the Python Solar Calculator!")
#runmode = input("Use mode d for debuging: ") or 'r'
runmode = 'r'

print("city number 1 Helsinki, 2 Tornio, 3 Stockholm, 4 Paris, 5 Madrid ")

cityNumber =  input("City number: ") or "0"
if cityNumber == "1":
    latitude  = 60.195627
    longitude = 24.938103
    tz_city = 2
    cityName = "Helsinki"
elif cityNumber == "2":
    latitude = 65.85
    longitude = 24.18
    tz_city = 2
    cityName = "Tornio"
elif cityNumber == "3":
    latitude =  59.32424
    longitude = 18.061364
    tz_city = 1
    cityName = "Stockholm"
elif cityNumber == "4":
    latitude  = 48.85687
    longitude =  2.342136
    tz_city = 1
    cityName = "Paris"
elif cityNumber == "5":
    latitude  = 40.415869
    longitude = -3.691138
    tz_city = 1
    cityName = "Madrid"
else:
    longitude = input("Enter your longitude in degrees (east +, west -): ") or 25
    latitude = input("Enter your latitude in degrees (north +, south -): ") or 60
    cityName = "No name"

longitude = float(longitude)
latitude = float(latitude)

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
cet_offset = -1

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
if utc_hours >=  24 + tz_offset:
    d_ -= 1

ut = datetime.datetime(y, m, d_, utc_hours, mn, sc) # UTC time
et = datetime.datetime(y, m, d_, cet_hours, mn, sc) # CET time

jd_morning = jdn - 1.5 + (hr + tz_offset) / 24 + mn / 60 / 24 + sc / 3600 / 24
jd_morning += 1.0 
jd_afternoon =   jdn - 0.5 + (hr + tz_offset) / 24 + mn / 60 / 24 + sc / 3600 / 24
print("morning", round(jd_morning,6), "afternoon", round(jd_afternoon,6))

# The JD starts at noon UTC, so we need to adjust the time accordingly
# We also calculate the timezone offset from UTC
jd_selected = jd_morning if (utc_hours < 12) else jd_afternoon

print(" Selected JD", round(jd_selected,6))
# You can check the calculation with online JD calculators
# Example : https://www.aavso.org/jd-calculator

def rad(x): # converting degrees to radians
    return(pi * x / 180.0)

def deg(x): # converting radians to degrees
    return(180.0 * x / pi)

def julian_century(jd):
# Calculate Julian Century from Julian Day
    jc = (jd - 2451545.0) / 36525.0
    return jc

jc = julian_century(jd_selected) 

sd = sun_declination(jc)
print(clear_screen, f"{cityName}: Latitude {latitude}°, Longitude {longitude}°")
#print(clear_screen, cityName, "latitude", latitude, "longitude", longitude)
print(" Local time:", x.strftime("%A, %Y-%m-%d %H:%M:%S"), f"Timezone UTC {tz_sign}{abs(tz_offset)} h")
print(" CET time:  ", et.strftime("%A, %Y-%m-%d %H:%M:%S"), f"Timezone UTC {tz_sign}{abs(cet_offset)} h")
print(" UTC time:  ", ut.strftime("%A, %Y-%m-%d %H:%M:%S"))

haSunR = haSunrise(latitude, sd)
if runmode == 'd': print("haSunrise", round(haSunR,6))


tst = true_solar_time(longitude, hr, mn, sc, tz_offset, jc)
if runmode == 'd': print("True Solar Time (minutes)", round(tst,6))

hourAngle = hour_angle(tst)
if runmode == 'd': print("hourAngle=", round(hourAngle,6))

solarNoon = solar_noon(longitude, jc, tz_offset)
cetNoon   = solar_noon(longitude, jc, cet_offset)

if tz_city == 2:
    print(yellow_text, "|    Eastern European normal time UTC + 2 h")
    print(' |    Noon time        ', solarNoon[0])

if tz_city == 1:
    print(yellow_text, "|    Central European normal time UTC + 1 h")
    print(' |    Noon time        ', cetNoon[0])


if tz_city == 2:
    sunrise_str = sun_time(solarNoon[1], haSunR, tz_offset)
    print(" |    Sunrise time     ", sunrise_str)
    sunset_str = sun_time(solarNoon[1], -haSunR, tz_offset)
    print(" |    Sunset time      ", sunset_str)

if tz_city == 1:
    sunrise_cet = ce_time(cetNoon[1], haSunR, cet_offset)
    print(" |    Sunrise time     ", sunrise_cet)
    sunset_cet = ce_time(cetNoon[1], -haSunR, cet_offset)
    print(" |    Sunset time      ", sunset_cet)

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
print(" Julian Century JC", round(jc,8))
print(f" Sun declination   {round(sd,6)}°")
print(f" Approx. atmospheric refraction {round(refract,5)}°")

"""
This is now OK as I changed it more functional: used only input variables, no global variables 
direct calls. That is just the way to avoid hidden errors, if the variables are afterwards
changed globally.
"""