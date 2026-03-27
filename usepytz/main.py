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
runmode = 'r'
t=''

for j in range(0, len(suncities)):
    t += suncities[j]['cityNumber'] + '. ' + suncities[j]['cityName']
    if j == 5 or j == 9: t += '\n'
    else: t += ', '

t += "99. Enter values of your own"

print(t)

cNr =  input(f"City number (1 - {len(suncities)}): ") or "1"
cNr = int(cNr) - 1

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
    tz_city = input("Enter your time zone (west neg., east pos. ): ") or 2.0
    tz_city = float(tz_city)
    cityName = "No name"
else:
    print("Index out of range!")
    print("Nr", cNr )
    cNr = 0
    print("Using location", suncities[0]['cityName'])

dlsHour = "NO DLS"
dlhour = 0
if cityNumber not in [7, 11]: dlsHour = input("Y = Day Light Saving (+ 1 hour): ") # no DLS in Japan
if dlsHour.upper() == 'Y': dlhour = 1.0
dlhour = float(dlhour)

d = datetime.now()
runmode = 'r'
if runmode == 'd':
    print("Current local time", d.strftime("%Y-%m-%d %T %Z"))

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
est_hours = utc_hours - 5
edt_hours = utc_hours - 4

tz_offset = time.timezone / 3600
# NEW: Show the sign (+/-) of timezone offset correctly
# Note, the sign is inverted when showing UTC offset
tz_sign = ''

if tz_offset > 0:
    tz_sign = '-'
elif tz_offset == 0: tz_sign = ' '
else :
    tz_sign = '+'

est_sign = '-'

if runmode == 'd': print(f"Timezone Offset {tz_offset} hours from UTC")

# Local time 
hki_tz = pytz.timezone('Europe/Helsinki')
stock_tz = pytz.timezone('Europe/Stockholm')
east_tz = pytz.timezone('US/Eastern')
central_tz = pytz.timezone('US/Central')
japan_tz = pytz.timezone('Asia/Tokyo')

x = datetime.now(tz = hki_tz)
tloc = hr + mn / 60 + sc / 3600 # Local time in hours decimal

# UTC Time

if utc_hours >=  22:
    d_ -= 1
    
# CET time
#if cet_hours > 24 + tz_offset:
#    d_ -= 1

if cet_hours > 23:
    cet_hours -= 24
    d_ += 1

#utc = pytz.utc
#datetime = datetime.datetime
utc_time = datetime.now(pytz.utc) # UTC time
et = datetime.now(pytz.timezone('Europe/Berlin')) # CET time
est = datetime.now(pytz.timezone('America/New_York')) # EST and EDT time 
#edt = datetime.datetime(y, m, d_, edt_hours, mn, sc) # EDT time 

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
est_offset = 5
cst_offset = 6
edt_offset = 4
cdt_offset = 5

print(" Local time: ", utc_time.astimezone(hki_tz).strftime(strfmt))
print(" CET time:   ", utc_time.astimezone(stock_tz).strftime(strfmt))
print(" UTC time:   ", utc_time.strftime(strfmt))
print(" US Eastern: ", utc_time.astimezone(east_tz).strftime(strfmt))
print(" US Central: ", utc_time.astimezone(central_tz).strftime(strfmt))
print(" Tokyo Japan:", utc_time.astimezone(japan_tz).strftime(strfmt))

if 0 <= cNr < len(suncities):
    print(cyan_text)
    print(f"{cityName}: Latitude {latitude}°, Longitude {longitude}°")
elif cNr != 98: print("index out of range!", cNr)

haSunR = haSunrise(latitude, sd)
if runmode == 'd': print("haSunrise", round(haSunR,6))


tst = true_solar_time(longitude, hr, mn, sc, tz_offset, jc)
if runmode == 'd': print("True Solar Time (minutes)", round(tst,6))

hourAngle = hour_angle(tst)
if runmode == 'd': print("hourAngle=", round(hourAngle,6))

if tz_info in ['Europe/Stockholm', 'Europe/Paris', 'Europe/Madrid']:
    #cet_offset = -1
    print(yellow_text)
    #if dlhour == 0: print(" |  Central European Time UTC + 1 h")
    #else: print(" |   Central European Summer Time UTC + 2 h")
    cetNoon   = solar_noon(longitude, jc, tz_info)
    print(' |    Noon time        ', cetNoon[0])

if tz_info in ['UTC', 'Atlantic/Reykjavik']:
    utc_offset =  0
    utNoon    = solar_noon(longitude, jc, tz_info)
    print(yellow_text, "|    Western European Time UTC + 00:00")
    print(' |    Noon time        ', utNoon[0])


if tz_info == 'Europe/Helsinki':
#    tz_offset =  0
    solarNoon = solar_noon(longitude, jc, tz_info)

    print(yellow_text)
    print(' |    Noon time        ', solarNoon[0])

    sunrise_str = sun_time(solarNoon[1], haSunR, tz_info)
    print(" |    Sunrise time     ", sunrise_str)
    sunset_str = sun_time(solarNoon[1], -haSunR, tz_info)
    print(" |    Sunset time      ", sunset_str)


if tz_info in ['Europe/Stockholm', 'Europe/Paris', 'Europe/Madrid']:
    #tz_offset = -1
    sunrise_cet = sun_time(cetNoon[1], haSunR, tz_info)
    print(" |    Sunrise time     ", sunrise_cet)
    sunset_cet = sun_time(cetNoon[1], -haSunR, tz_info)
    print(" |    Sunset time      ", sunset_cet)


if tz_info in ['UTC', 'Atlantic/Reykjavik']:
    utc_offset = 0
    sunrise_utc = sun_time(utNoon[1], haSunR, tz_info)
    print(" |    Sunrise time     ", sunrise_utc)
    sunset_utc = sun_time(utNoon[1], -haSunR, tz_info)
    print(" |    Sunset time      ", sunset_utc)

if tz_info in ['America/Chicago', 'America/New_York']:
    estNoon    = solar_noon(longitude, jc, tz_info)
    cstNoon    = solar_noon(longitude, jc, tz_info)
    print(yellow_text)
    if dlhour == 0:
        if tz_info == 'America/New_York': print(" |    Eastern Standard Time EST, UTC - 05:00")
        elif tz_info == 'America/Chicago': print(" |    Central Standard Time CST, UTC - 06:00") 
    elif dlhour == 1.0:
        if tz_info == 'America/New_York': print(" |    Eastern Daylight Time EDT, UTC - 04:00")
        elif tz_info == 'America/Chicago': print(" |    Central Daylight Time CDT, UTC - 05:00")

    if tz_info == 'America/New_York':
        print(' |    Noon time        ', estNoon[0])
        sunrise_est = sun_time(estNoon[1], haSunR, tz_info)
        print(" |    Sunrise time     ", sunrise_est)
        sunset_est = sun_time(estNoon[1], -haSunR, tz_info)
        print(" |    Sunset time      ", sunset_est) 
    elif tz_info == 'America/Chicago':
        print(' |    Noon time        ', cstNoon[0])
        sunrise_cst = sun_time(cstNoon[1], haSunR, tz_info)
        print(" |    Sunrise time     ", sunrise_cst)
        sunset_cst = sun_time(cstNoon[1], -haSunR, tz_info)
        print(" |    Sunset time      ", sunset_cst) 
# to be added next CST Central Standard Time UTC - 6
# and CDT Central Daylight Time UTC - 5 for Chicago
# Lat 41.88° Lon -87.63°

if tz_info == 'Asia/Tokyo':
    jpn_offset = -9
    jpnNoon = solar_noon(longitude, jc, tz_info)
    print(yellow_text)
    print(" |    Japan Standard Time JST, UTC + 09:00")
    print(' |    Noon time        ', jpnNoon[0]) 
    sunrise_jpn = sun_time(jpnNoon[1], haSunR, tz_info)
    print(" |    Sunrise time     ", sunrise_jpn)
    sunset_jpn = sun_time(jpnNoon[1], -haSunR, tz_info)
    print(" |    Sunset time      ", sunset_jpn)

dayLength = 2 * haSunR / 15 # in decimal hours
if runmode == 'd': print("Daylength (hours)     ", round(dayLength,4))
dlhr = int(dayLength)
dlmn = int((dayLength - dlhr) * 60)
dlsc = (dayLength - dlhr - dlmn / 60) * 3600
print(f" |    Daylength         {dlhr} h {dlmn} min {round(dlsc)} sec")

sza = solar_zenith_angle(hourAngle, latitude, sd)
if runmode == 'd': print("Solar Zenith Angle (degrees)", round(sza,6))

saz = solar_azimuth(hourAngle, sza, sd, latitude)

print(f" |    Sun Altitude without refraction corr.   {round(90.0 - sza, 3)}°")

refract = atmosRefract(90.0 - sza)
cor_elev = 90.0 - sza + refract
print(f" |    Sun Altitude with refraction correction {round(cor_elev,3)}°")
print(f" |    Solar Azimuth (clockwise from north)   {round(saz, 3)}°")
print(green_text)
print(" Julian Date (JD) for current time and date", round(jd_selected,6))
print(" Julian Century JC", round(jc,8))
print(f" Sun declination   {round(sd,6)}°")
print(f" Approx. atmospheric refraction {round(refract,5)}°")