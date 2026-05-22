#!/usr/local/bin/python3
import datetime
from datetime import timedelta
from decimal import Decimal 
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
# Creating the list of cities available as the string t for output

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

print('tz_info :', tz_info)
today = datetime.now()
blank_date = pytz.timezone('Europe/Helsinki').localize(today)
default_date =  blank_date.astimezone(pytz.timezone(tz_info))
default_datestr = default_date.strftime('%Y-%m-%d ')
current_timestr = default_date.strftime('%H:%M:%S ')
print("Today", default_datestr)
i_date_time = input("Enter date e.g. " + default_datestr) or default_datestr
i_time = input("Enter time e.g. " + current_timestr + '  ') or current_timestr
delta_hours = input("Step hours (default 1): ") or "1"
delta_hours = int(delta_hours)
ls_date = i_date_time.split('-')
ls_time = i_time.split(':')


ys, ms, ds = ls_date[0], ls_date[1], ls_date[2]
y, m, d_ = int(ys), int(ms), int(ds)
hrs, mns, scs = ls_time[0], ls_time[1], ls_time[2]
hr, mn, sc = int(hrs), int(mns), int(scs)

def jdn_from_date(yr: int, mnt: int, day: int) -> int :
  result = 367*yr - 7*(yr + (mnt + 9)//12)//4 \
        - 3*((yr + (mnt - 9)//7)//100 + 1)//4 \
        + 275*mnt//9 + day + 1721029
  return(result)

def julian_century(jd: float) -> float:
  # Calculate Julian Century from Julian Day
    jc = (jd - 2451545.0) / 36525.0
    return jc


d = datetime(y, m, d_, hr, mn, sc)
dt_foreign = pytz.timezone(tz_info).localize(d)
dutc = dt_foreign.astimezone(pytz.utc) # utc
print("Localized to foreign timezone", dt_foreign.strftime(strfmt))
print("Naive date and time = ", d)
print("The same as UTC time ", dutc.strftime('%T %Z'))

start_foreign = dt_foreign


for i in range(1,7):

    # compute the datetime for this row in the target timezone
    dt_step = start_foreign + timedelta(hours = (i-1) * delta_hours)
    dutc = dt_step.astimezone(pytz.utc)
    try:
        offset_hours_east = dt_step.utcoffset().total_seconds() / 3600
        tz_offset = -offset_hours_east
    except Exception:
        tz_offset = 0

    uthr, utmn, utsc = dutc.hour, dutc.minute, dutc.second
    jdn = jdn_from_date(dutc.year, dutc.month, dutc.day)
    jd_morning = jdn - 1.5 + uthr / 24 + utmn / 60 / 24 + utsc / 3600 / 24
    jd_morning += 1.0
    jd_afternoon = jdn - 0.5 + uthr / 24 + utmn / 60 / 24 + utsc / 3600 / 24
    jd_selected = jd_afternoon if uthr >= 12 else jd_morning
    jc = julian_century(jd_selected)
    sun_declin = sun_declination(jc)

    if i == 1:
        localTime_str = dt_step.astimezone(pytz.timezone('Europe/Helsinki')).strftime(strfmt)
        tz_id = localTime_str[-4:]
        summer = 1 if tz_id in ['EEST', 'CEST', 'EDT'] else 0
        print(clear_screen + "Calculation times for " + cityName + ":")
        print(f" Local time:  {localTime_str} (summer = {summer})")
        print(" UTC time:   ", dutc.strftime(strfmt))
        try:
            print(" " + tz_info, dutc.astimezone(pytz.timezone(tz_info)).strftime(strfmt))
        except pytz.UnknownTimeZoneError as err:
            print('Wrong timezone:', err)
        print(cyan_text)
        print(f"{cityName}: Latitude {latitude}°, Longitude {longitude}°")

    if latitude + sun_declin > 89.166997:
        haSunR = 179.999
    else:
        haSunR = haSunrise(latitude, sun_declin)

    try:
        true_sol_tim = true_solar_time(longitude, dt_step.hour, dt_step.minute, dt_step.second, tz_offset, jc)

    except NameError as err: print("Exception:", err)

    try:
        hourAngle = hour_angle(true_sol_tim)
    except NameError as e:     print('Exception:', e)

    if tz_info in tzinfos:
        solarNoon = solar_noon(longitude, jc, tz_info, y, m, d_)
        noon = solarNoon[2]
        delta = timedelta(minutes=4 * haSunR)
        sunriseTime = (noon - delta).astimezone(pytz.timezone(tz_info))
        sunsetTime = (noon + delta).astimezone(pytz.timezone(tz_info))
        dayLength = 2 * haSunR / 15  # in decimal hours

        day_asSeconds = dayLength * 3600
        day_asHMS = datetime(d.year, d.month, d.day, 0, 0, 0) + timedelta(seconds=day_asSeconds)
        bform = "%T"
        oform = "%H:%M"
        timei = dt_step.strftime(oform)
        if i == 1:
            print("next time", timei)
            print(yellow_text)
            print(" | Calcul-                                       Elevation    Elevation   Solar      Solar")
            print(" | ation                   Noon      Day         without      with        Azimuth    Declination")
            print(" | Times Sunrise  Sunset   time      length      refraction   refraction  angle      angle")

        out1 = sunriseTime.strftime(bform)
        out2 = sunsetTime.strftime(bform)
        out3 = noon.astimezone(pytz.timezone(tz_info)).strftime(bform)
        out4 = ' ' + day_asHMS.strftime("%H:%M:%S")


    try:
        sol_zenith = solar_zenith_angle(hourAngle, latitude, sun_declin)

        sol_azim = solar_azimuth(hourAngle, sol_zenith, sun_declin, latitude)
    
        refract = atmosRefract(90.0 - sol_zenith)
        cor_elev = 90.0 - sol_zenith + refract
        out5 = f"   {Decimal(90.0 - sol_zenith).quantize(Decimal('1.000')):>7}°     {Decimal(cor_elev).quantize(Decimal('1.000')):>7}°"
        out7 = f"   {Decimal(sol_azim).quantize(Decimal('1.000')):>8}°   {round(sun_declin, 3)}°"
        print(" |", timei, out1, out2, out3, out4, out5, out7)
    except NameError as e: print('Exception:', e)
