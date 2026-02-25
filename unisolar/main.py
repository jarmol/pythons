# We are building a new version of solar calculator using Python
# First we need to convert the current local time to Julian Day (JD)
# The solar astronomic calculation is based on the algorithm from
# "Astronomical Algorithms" by Jean Meeus, 1991

import time, datetime
from math import pi, sin, asin, cos, tan, acos

black_bg = "\033[40m"
white_text = "\033[97m"
green_text = "\033[92m"
yellow_text = "\033[93m"
clear_screen = "\033[2J"
print(black_bg, white_text, clear_screen + "Welcome to the Python Solar Calculator!")
#runmode = input("Use mode d for debuging: ") or 'r'
runmode = 'r'

print("city number 1 Helsinki, 2 Tornio, 3 Stockholm, 4 Madrid ")

cityNumber =  input("City number: ") or "0"
if cityNumber == "1":
    latitude = 60.2
    longitude = 24.9
    tz_city = 2
    cityName = "Helsinki"
elif cityNumber == "2":
    latitude = 65.85
    longitude = 24.18
    tz_city = 2
    cityName = "Tornio"
elif cityNumber == "3":
    latitude = 59.3294
    longitude = 18.0686
    tz_city = 1
    cityName = "Stockholm"
elif cityNumber == "4":
    latitude  = 40.433
    longitude = -3.70
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

# Conversion factor from degrees to radians
deg2rad = pi / 180.0

def rad(x):
    return(pi * x / 180.0)

def deg(x):
    return(180.0 * x / pi)

def julian_century(jd):
# Calculate Julian Century from Julian Day
    jc = (jd - 2451545.0) / 36525.0
    return jc

jc = julian_century(jd_selected) 

def geom_mean_long_sun(jc):
    gmls = 280.46646 + jc * (36000.76983 + jc * 0.0003032)
    # More elegant way to keep angle within 0-360 degrees
    gmls = gmls % 360.0
    return gmls
gmls = geom_mean_long_sun(jc)
if runmode == 'd': print("Geometric Mean Longitude of the Sun (degrees)", round(gmls,6))

def geom_mean_anom_sun(jc):
    """Calculate the Geometric Mean Anomaly of the Sun (in degrees)"""
    gmas = 357.52911 + jc * (35999.05029 - 0.0001537 * jc)
    return (gmas % 360.0)

gmas = geom_mean_anom_sun(jc)
if runmode == 'd': print("Geometric Mean Anomaly of the Sun (degrees)", round(gmas,6))

def eccent_earth_orbit(jc):
    eoe = 0.016708634 - jc * (0.000042037 + 0.0000001267 * jc)
    return eoe
eoe = eccent_earth_orbit(jc)
if runmode == 'd': print("Eccentricity of Earth's orbit", round(eoe,8))

def sun_eq_of_center(jc):
    gmas = geom_mean_anom_sun(jc) 
    gmas_rad = deg2rad*gmas
    sec = (sin(gmas_rad) * (1.914602 - jc * (0.004817 + 0.000014 * jc)) +
           sin(2 * gmas_rad) * (0.019993 - 0.000101 * jc) +
           sin(3 * gmas_rad) * 0.000289)
    return sec

sec = sun_eq_of_center(jc)
if runmode == 'd': print("Sun's Equation of the Center (degrees)", round(sec,6))

def sun_true_long(jc):
    gmls = geom_mean_long_sun(jc)
    sec = sun_eq_of_center(jc)
    stl = gmls + sec
    return (stl % 360.0)
stl = sun_true_long(jc)
if runmode == 'd': print("Sun's True Longitude (degrees)", round(stl,6))

def sun_app_long(jc, stl):
    omega = 125.04 - 1934.136 * jc
    sal = stl - 0.00569 - 0.00478 * sin(omega * deg2rad)
    return sal
sal = sun_app_long(jc, stl)
if runmode == 'd': print("Sun's Apparent Longitude (degrees)", round(sal,6))

def mean_obliq_ecliptic(jc):
    moe = 23.0 + (26.0 + ((21.448 - jc * (46.815 \
     + jc * (0.00059 - jc * 0.001813)))) / 60.0) / 60.0
    return moe
moe = mean_obliq_ecliptic(jc)
if runmode == 'd': print("Mean Obliquity of the Ecliptic (degrees)", round(moe,6))

def obliq_corr(jc):
    omega = 125.04 - 1934.136 * jc
    moe = mean_obliq_ecliptic(jc)
    oc = moe + 0.00256 * cos(omega * deg2rad)
    return oc
oc = obliq_corr(jc)
if runmode == 'd': print("Obliquity Correction (degrees)", round(oc,6))

def sun_declination(jc):
    oc = obliq_corr(jc)
    sal = sun_app_long(jc, stl)
    sd = deg(asin(sin(rad(oc))*sin(rad(sal))))
    return sd

sd = sun_declination(jc)
print(clear_screen, f"{cityName}: Latitude {latitude}°, Longitude {longitude}°")
#print(clear_screen, cityName, "latitude", latitude, "longitude", longitude)
print(" Local time:", x.strftime("%A, %Y-%m-%d %H:%M:%S"), f"Timezone UTC {tz_sign}{abs(tz_offset)} h")
print(" CET time:  ", et.strftime("%A, %Y-%m-%d %H:%M:%S"), f"Timezone UTC {tz_sign}{abs(cet_offset)} h")
print(" UTC time:  ", ut.strftime("%A, %Y-%m-%d %H:%M:%S"))

def y_variable(jc):
    # Calculate the Y variable for the equation of time
    moe = mean_obliq_ecliptic(jc)
    obliq_corr(jc)
    y = tan(rad(oc) / 2.0) * tan(rad(oc) / 2.0)
    return y

y_var = y_variable(jc)
if runmode == 'd': print("Y variable for equation of time", round(y_var,6))

def equation_of_time(jc):
    geom_mean_long_sun(jc)
    eoe = eccent_earth_orbit(jc)
    gmas = geom_mean_anom_sun(jc)
    y = y_variable(jc)
    eot = y * sin(2 * rad(gmls)) - 2 * eoe * sin(rad(gmas)) \
            + 4 * eoe * y * sin(rad(gmas)) * cos(2 * rad(gmls)) \
            - 0.5 * y * y * sin(4 * rad(gmls)) - 1.25 * eoe * eoe * sin(2 * rad(gmas))

    eot = deg(eot) * 4.0  # Convert to minutes
    return eot
eot = equation_of_time(jc)
if runmode == 'd': print("Equation of Time (minutes)", round(eot,6))

def ha_sunrise(jc, lat):
    sd = sun_declination(jc)
    ha = deg(acos(cos(rad(90.833)) / (cos(rad(lat)) * cos(rad(sd))) - tan(rad(lat)) * tan(rad(sd))))
    return ha
ha = ha_sunrise(jc, latitude)
if runmode == 'd': print("Hour Angle at Sunrise (degrees)", round(ha,6))

def haSunrise(latitude, sd):
    haS = deg(acos(cos(rad(90.833)) / (cos(rad(latitude)) * cos(rad(sd))) - tan(rad(latitude)) * tan(rad(sd))))
    return haS

haSunR = haSunrise(latitude, sd)
if runmode == 'd': print("haSunrise", round(haSunR,6))

def true_solar_time(longitude, hr, mn, sc, tz_offset, jc):
    # Calculate the True Solar Time (in minutes)
    # time_in_minutes: local time in minutes (0..1440)
    time_in_minutes = hr * 60 + mn + sc / 60
    # tz_offset from time.timezone is seconds west of UTC -> hours west of UTC
    # spreadsheet/timezone convention: positive for east of Greenwich
    tz = -tz_offset
    eot = equation_of_time(jc)
    # Apply equation of time (minutes) and longitude/timezone offsets
    tst = (time_in_minutes + eot + 4 * longitude - 60 * tz) % 1440
    return tst
    # If tst < 0 then tst = tst + 1440


def solar_noon(longitude, jc, tzoffs):
    eot = equation_of_time(jc)
    day_fraction = (720 - 4 * longitude - eot - tzoffs * 60) / 1440
    noon_as_minutes = 720 - 4 * longitude - eot - tzoffs * 60
    noon_hours = int(noon_as_minutes) // 60
    noon_minutes = int(noon_as_minutes) % 60
    noon_seconds = int((60*noon_as_minutes) % 60)
    xt = datetime.datetime(y, m, d_, noon_hours, noon_minutes, noon_seconds) # noon time
    solarNoon = xt.strftime("%A, %Y-%m-%d %H:%M:%S" + f" Timezone UTC {tz_sign}{abs(tzoffs)}")
    return [solarNoon, day_fraction]
tst = true_solar_time(longitude, hr, mn, sc, tz_offset, jc)
if runmode == 'd': print("True Solar Time (minutes)", round(tst,6))

def hour_angle(tcurrent):
    ha = (tcurrent / 4.0) - 180.0
    if ha < -180.0:
        ha += 360.0
    return ha

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



def sunrise_time(df, haSunR):
    srt = df - 4 *  haSunR / 1440
    return srt


def sun_time(dayf, haSunR, tz_offset):
    sunT = sunrise_time(dayf, haSunR)
    sunH = 24 * sunT
    sunMinutes = 60 * sunH
    sunHours = int(sunH)
    sMinutes = int(sunMinutes) % 60
    sunSeconds = int(60 * sunMinutes % 60)
    xt = datetime.datetime(y, m, d_, sunHours, sMinutes, sunSeconds)
    suntime_eet = xt.strftime("%A, %Y-%m-%d %H:%M:%S" + f" Timezone UTC {tz_sign}{abs(tz_offset)}") 
    return suntime_eet

def ce_time(dayf, haSunR, cet_offset):
    sunT = sunrise_time(dayf, haSunR)
    sunH = 24 * sunT
    sunMinutes = 60 * sunH
    sunHours = int(sunH)
    sMinutes = int(sunMinutes) % 60
    sunSeconds = int(60 * sunMinutes % 60)
    cet = datetime.datetime(y, m, d_, sunHours, sMinutes, sunSeconds)
    suntime_cet = cet.strftime("%A, %Y-%m-%d %H:%M:%S" + f" Timezone UTC {tz_sign}{abs(cet_offset)}") 
    return suntime_cet

if tz_city == 2:
    sunrise_str = sun_time(solarNoon[1], haSunR, tz_offset)
    print(" |    Sunrise time     ", sunrise_str)
    sunset_str = sun_time(solarNoon[1], -haSunR, tz_offset)
    print(" |    Sunset time      ", sunset_str)
#else: print()

if tz_city == 1:
    sunrise_cet = ce_time(cetNoon[1], haSunR, cet_offset)
#   print(yellow_text, "|    Central European normal time UTC + 1 h")
    print(" |    Sunrise time     ", sunrise_cet)
    sunset_cet = ce_time(cetNoon[1], -haSunR, cet_offset)
    print(" |    Sunset time      ", sunset_cet)
else: print()

dayLength = 2 * haSunR / 15 # in decimal hours
if runmode == 'd': print("Daylength (hours)     ", round(dayLength,4))
dlhr = int(dayLength)
dlmn = int((dayLength - dlhr) * 60)
dlsc = (dayLength - dlhr - dlmn / 60) * 3600
print(f" |    Daylength         {dlhr} h {dlmn} min {round(dlsc)} sec")


def solar_zenith_angle(ha, lat, sd):
    sins = sin(rad(lat)) * sin(rad(sd))
    coss = cos(rad(lat)) * cos(rad(sd)) * cos(rad(ha))
    sza = deg(acos(sins + coss))
    return sza

sza = solar_zenith_angle(hourAngle, latitude, sd)
if runmode == 'd': print("Solar Zenith Angle (degrees)", round(sza,6))

print(f" |    Sun elevation                         {round(90.0 - sza, 3)}°")

# Three categories of elevations angle: < 0, < 5, < 85
# used for refraction angles
def belowZero(hx):
        return -20.774 / tan(rad(hx)) / 3600.0
    
def belowEightyFive(hx):
        v1 = tan(rad(hx))
        v2 = pow(tan(rad(hx)), 3.0)
        v3 = pow(tan(rad(hx)), 5.0)
        v = ((58.1 / v1) - (0.07 / v2) + (8.6e-5 / v3)) / 3600.0
        return v
    
def belowFive(hx):
        v = (1735.0 - 518.2 * hx + 103.4 * pow(hx, 2.0) \
           - 12.79 * pow(hx, 3.0) + 0.711 * pow(hx, 4.0)) / 3600.0
        return v
    
# Calculation of atmospheric refraction correction angle
# h = solar elevation (degrees)
# res = result of calculation

def atmosRefract(h):

    if runmode == 'd': print('h', h)

    res = -999

    if h < -0.575:
        res = belowZero(h)
    elif h <= 5.0:
        res = belowFive(h)
    elif h <= 85.0:
        res = belowEightyFive(h)
    else:
        res = 0.0 
        
    return res

refract = atmosRefract(90.0 - sza)
cor_elev = 90.0 - sza + refract
print(" |    Solar elevation, refraction corrected", round(cor_elev,3), '°')
print(green_text)
print(" Julian Century JC", round(jc,8))
print(f" Sun declination   {round(sd,6)}°")
print(f" Approx. atmospheric refraction {round(refract,5)}°")

def solar_azimuth(ha, sza, sd, lat):
    saz = 0.0
    sin_az = (cos(rad(sd)) * sin(rad(ha))) / sin(rad(sza))
    cos_az = ( (sin(rad(sd)) - sin(rad(lat)) * cos(rad(sza))) /
               (cos(rad(lat)) * sin(rad(sza))) )
    az_rad = acos(cos_az)
    az_deg = deg(az_rad)
    if sin_az < 0:
        saz = az_deg
    else:
        saz = 360.0 - az_deg
    return saz

saz = solar_azimuth(hourAngle, sza, sd, latitude)
print(" Solar Azimuth Angle (clockwise from north)   ", round(saz, 4), '°')

"""
This is now OK as I changed it more functional: used only input variables, no global variables 
direct calls. That is just the way to avoid hidden errors, if the variables are afterwards
changed globally.
"""
