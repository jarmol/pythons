#!/usr/local/bin/python3
import datetime
#from math import pi 
from citydata import *
from solarfuncs import *
import pytz

utc = pytz.utc
strfmt = "%A, %Y-%m-%d %T %Z"

black_bg = "\033[40m"
white_text = "\033[97m"
cyan_text = "\033[96m"
green_text = "\033[92m"
yellow_text = "\033[93m"
clear_screen = "\033[2J"

print(black_bg, white_text, clear_screen + "Welcome to the Python Solar Calculator!")
# Creating the list of cities available as a string for output

t=''

for j in range(0, len(suncities)):
    t += str(j + 1) + '. ' + suncities[j]['cityName']
    if j == 4 or j == 9 or j == 14: t += '\n'
    else: t += ', '

t += "99. Enter values of your own"

print(t)
cityNr =  input(f"City number (1 - {len(suncities)}): ") or "1"
cityNr = int(cityNr)
if (len(suncities) < cityNr < 99):
    cityNr = 1 # Invalid index forced to 1 
elif cityNr > 99:
    cityNr = 1 
    print("Not existing city, using Helsinki")

# Converting here the city number to the row number of the data table
cityNr = cityNr - 1

if -1 < cityNr < len(suncities):
        latitude = suncities[cityNr]['latitude']
        longitude = suncities[cityNr]['longitude']
        longitude = float(longitude)
        latitude = float(latitude)
        tz_info = suncities[cityNr]['tz_info']
        cityName = suncities[cityNr]['cityName']
        cityNumber = cityNr + 1
elif cityNr == 98:
        longitude = input("Enter your longitude in degrees (east +, west -): ") or 24.938
        longitude = float(longitude)
        latitude = input("Enter your latitude in degrees (north +, south -): ") or 60.196
        latitude = float(latitude)
        tz_info = input("Enter Timezone info e.g. Europe/Berlin ): ") or "Europe/Helsinki"
        cityName = "Test City"

print('tz_info', tz_info)
today = datetime.now()
blank_date = pytz.timezone('Europe/Helsinki').localize(today)
default_date =  blank_date.astimezone(pytz.timezone(tz_info))
default_datestr = default_date.strftime('%Y-%m-%d ')
current_time = blank_date.astimezone(pytz.timezone(tz_info))
current_timestr = current_time.strftime('%H:%M:%S ')
print("Today", default_datestr)
i_date_time = input("Enter date e.g. " + default_datestr) or default_datestr
i_time = input("Enter time e.g. " + current_timestr + ' : ') or current_timestr
ls_date = i_date_time.split('-')
ls_time = i_time.split(':')

# d = datetime.now(pytz.timezone('Europe/Helsinki')) # local

ys, ms, ds = ls_date[0], ls_date[1], ls_date[2]
y, m, d_ = int(ys), int(ms), int(ds)
hrs, mns, scs = ls_time[0], ls_time[1], ls_time[2]
hr, mn, sc = int(hrs), int(mns), int(scs)

d = datetime(y, m, d_, hr, mn, sc)
print("Naive date and time = ", d)
dt_foreign = pytz.timezone(tz_info).localize(d)
print("Localized to foreign timezone", dt_foreign.strftime(strfmt))

dutc = dt_foreign.astimezone(pytz.utc) # utc
print("The same as UTC time ", dutc.strftime('%T %Z'))
utc_time = dutc
tz = dt_foreign.hour - dutc.hour

if tz < 0: tz += 24
tz_offset = -tz

localTime_str = dt_foreign.astimezone(pytz.timezone('Europe/Helsinki')).strftime(strfmt) 
tz_id = localTime_str[-4:]
if tz_id in ['EEST', 'CEST']:
    summer = 1
else: summer = 0

print(f" Local time:   {localTime_str} (summer = {summer})")

# Time UTC elements used in JD calculation
uthr,utmn,utsc = dutc.hour, dutc.minute, dutc.second

def jdn_from_date(yr: int, mnt: int, day: int) -> int :
    result = 367*yr - 7*(yr + (mnt + 9)//12)//4 \
    - 3*((yr + (mnt - 9)//7)//100 + 1)//4 \
    + 275*mnt//9 + day + 1721029
    return(result)

# The integer part of JD number from the date
jdn = jdn_from_date(dutc.year, dutc.month, dutc.day)

#utc_time = datetime.now(pytz.utc) # UTC time
summer = 0 # Day Light Saving in local time 
jd_morning = jdn - 1.5 + uthr / 24 + utmn / 60 / 24 + utsc / 3600 / 24
jd_morning += 1.0 
jd_afternoon =   jdn - 0.5 + uthr / 24 + utmn / 60 / 24 + utsc / 3600 / 24


def julian_century(jd: float) -> float:
# Calculate Julian Century from Julian Day
    jc = (jd - 2451545.0) / 36525.0
    return jc
jd_selected = jd_morning 
if (uthr >= 12): jd_selected = jd_afternoon
print('jd_morning',jd_morning)
print('jd_afternoon', jd_afternoon)
jc = julian_century(jd_selected) 

sd = sun_declination(jc)
localTime_str = dt_foreign.astimezone(pytz.timezone('Europe/Helsinki')).strftime(strfmt) 
tz_id = localTime_str[-4:]
if tz_id in ['EEST', 'CEST', 'EDT']:
    summer = 1
else: summer = 0

print(clear_screen + "Calculation times for " + cityName + ":")
print(f" Local time:  {localTime_str} (summer = {summer})")
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
   tst = true_solar_time(longitude, hr, mn, sc, tz_offset, jc) # This works for Tornio and Stockholm if summer = 1 is not used

except NameError as err: print("Exception:", err)

try:
    hourAngle = hour_angle(tst)
except NameError as e:     print('Exception:', e)

try:
    if tz_info in tzinfos:
        solarNoon = solar_noon(longitude, jc, tz_info, y, m, d_)
        noon = solarNoon[2]
        delta = timedelta(minutes = 4 * haSunR)
        midnight = (noon + timedelta(hours = 12)).astimezone(pytz.timezone(tz_info))  # the next midnight
        sunriseTime = (noon - delta).astimezone(pytz.timezone(tz_info))
        sunsetTime =  (noon + delta).astimezone(pytz.timezone(tz_info)) 
        tform = "%A  %Y-%m-%d %T %Z"
        oform = "%A  %Y-%m-%d %H:%M %Z"
        print(yellow_text)
        print(" |    Sunrise time     ", sunriseTime.strftime(tform))
        print(" |    Sunset time      ", sunsetTime.strftime(tform))
        print(' |    Noon time        ', solarNoon[0])
        print(' |    Midnight time    ', midnight.strftime(tform))
except NameError as e: print('Exception:', e)

dayLength = 2 * haSunR / 15 # in decimal hours

#d = datetime.now(pytz.timezone(tz_info))
day_asSeconds = dayLength * 3600
day_asHMS = datetime(d.year, d.month, d.day,0,0,0) + timedelta(seconds = day_asSeconds)
print(" |    Daylength        ", day_asHMS.strftime("%H h %M min %S sec"))

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
