#!/usr/local/bin/python3
""" 
11.05.2026
Now the input times can be acc. to target location, i.e. tz_info.
Now it is possible to enter any date and time, either past or
future, not only the current date and time.
The time entered is for given location so as the results too,
thus no time conversion manually is needed.

That way it is easier to define special time points such as sun direction
(azimuth angle) at sunrise and sunset or maximum solar elevation during the
day (at solar noon).

 This may be developed further so that the altitude and azimuth is calculated
 for noon time, sunrise and sunset times in the second phase without entering
 manually the times calculated in the first phase. The solution could be
 preferaly a for-loop or a while-loop rather than lots of if-conditions. 

04.05.2026
 Here is expained, how to find the max height of sun. It's known that the sun
 is at its highest point at solar noon. The solar noon is the time when the sun
 is directly above the local meridian. The time of solar noon is output always in
 this code, but the altitude and azimuth are calculated just for the time entered 
 by the user. Having the time of solar noon, you can run this code second time to
 get the altitude and azimuth. However, running second time you must enter all
 input values including the time of solar noon.

 It's the purpose to develope this code further so that the wanted results
 (incl. max solar altitude) are calculated in the first round automatically 
 without extra manual handling.
  
 As sun is on the local meridian at solar noon, the azimuth is either 180°
(northern latitudes) or 0° (southern latitudes) depending on the location.
Having azimuths calculated near to 0° or 180° at solar noon, you can evaluate
 whether the time of solar noon is as accurate as possible in practise and 
 the solar elevation as well.
 """
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
i_date_time = input("Enter date e.g. 2026-05-04 : ")
i_time = input("Enter time e.g. 12:35:10 : ")
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
   """ Tornio has timezone same as in whole Finland. We must check other times. Note, Sweden tz is UTC +2 in summer as
 Finland is UTC +3, thus the real reason may be just this difference of one hour used in summer time,
 but we have same months for summer in all EU countries.
 I'll check next New York with bigger difference in tz. New York has UTC -5 in winter and UTC -4 in summer,
 thus the difference to Finland is 7 hours in winter and 6 hours in summer.
 tst = true_solar_time(longitude, hr - summer, mn, sc, tz_offset, jc)
 New York: retested with noon time, everything is
 correct - same as in spreadsheet!
 True Solar Time (minutes) 719.998353 rounded is very near to the
 720 minutes, which is the exact time at solar noon.
-----------------------
 Calculation times for New York  :
 Local time:  Sunday, 2026-05-10 19:52:27 EEST (summer = 1)
 UTC time:    Sunday, 2026-05-10 16:52:27 UTC
 America/New_York Sunday, 2026-05-10 12:52:27 EDT

New York  : Latitude 40.71°, Longitude -74.01°

 |    Sunrise time      Sunday  2026-05-10 05:43:40 EDT
 |    Sunset time       Sunday  2026-05-10 20:01:13 EDT
 |    Noon time         Sunday  2026-05-10 12:52:27 EDT
 |    Midnight time     Monday  2026-05-11 00:52:27 EDT
 |    Daylength         14 h 17 min 33 sec
 |    Sun Altitude without refraction corr.   67.044°
 |    Sun Altitude with refraction correction 67.051°
 |    Solar Azimuth (clockwise from north)   179.999°
   ------------------------------------------
 Berlin has all results accurately same as in spreadsheet,
 including azimuth. Of course solar noon is correct, because
 the azimuth output is 180° at solar noon.
 thus the time of solar noon is correct. 
Calculation times for Berlin:
 Local time:  Sunday, 2026-05-10 14:00:00 EEST (summer = 1)
 UTC time:    Sunday, 2026-05-10 11:00:00 UTC
 Europe/Berlin Sunday, 2026-05-10 13:00:00 CEST

Berlin: Latitude 52.52°, Longitude 13.405°

 |    Sunrise time      Sunday  2026-05-10 05:18:06 CEST
 |    Sunset time       Sunday  2026-05-10 20:47:27 CEST
 |    Noon time         Sunday  2026-05-10 13:02:47 CEST
 |    Midnight time     Monday  2026-05-11 01:02:47 CEST
 |    Daylength         15 h 29 min 21 sec
 |    Sun Altitude without refraction corr.   55.166°
 |    Sun Altitude with refraction correction 55.177°
 |    Solar Azimuth (clockwise from north)   178.833°

 Tokyo and Sydney AUS results match quite well with the current values by the sites
  https://www.timeanddate.com/sun/japan/tokyo
  https://www.timeanddate.com/sun/australia/sydney
 """
except NameError as err: print("Exception:", err)

try:
    hourAngle = hour_angle(tst)
except NameError as e:
     print('Exception:', e)

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
