import time, datetime
from math import pi, sin, asin, cos, tan, acos
from solfuns import *

d = datetime.datetime.now()
y, m, d_ = d.year, d.month, d.day
hr,mn,sc = d.hour, d.minute, d.second

longitude =  input("Enter your longitude in degrees (east +, west -): ") or  "24.18"
longitude = float(longitude)

latitude = input("Enter your latitude in degrees (north +, south -): ") or "65.85"
latitude = float(latitude)

symLat, symLon  = "", ""
if latitude >= 0.0 :
    symLat = "° N"
else:
    symLat = "° S"

if longitude >= 0.0 :
    symLon = "° E"
else:
    symLon = "° W"

print("\nLatitude", latitude, symLat,  "Longitude", longitude, symLon) 
jdn = jdn_from_date(y, m, d_)

print("Julian Day Number JDN", jdn)
print("year",y,"month",m,"day",d_)


tposix = time.mktime(d.timetuple())
tday = 24*3600
seconds = tposix % 60

# days = tposix // tday

dsecs = tposix % tday

utc_hours = int(dsecs // 3600)

tz_offset = time.timezone / 3600
tz_sign = ''

if tz_offset >= 0:
    tz_sign = '-'
else :
    tz_sign = '+'

print(f"Timezone Offset {tz_offset} hours from UTC")

# Local time 
x = datetime.datetime(y, m, d_, hr, mn, sc)
print("Local time:", x.strftime("%A, %Y-%m-%d %H:%M:%S"), f"Timezone UTC {tz_sign}{abs(tz_offset)} h")
tloc = hr + mn / 60 + sc / 3600 # Local time in hours decimal
# UTC Time
ut = datetime.datetime(y, m, d_, utc_hours, mn, sc) # UTC time
print("UTC time:  ", ut.strftime("%A, %Y-%m-%d %H:%M:%S"))

"""
if hr == 0:
    utc_hours = (23 + int(tz_offset) % 24)
    if utc_hours < 0:
        utc_hours += 24
        y -= 1
        if m == 1:
            m = 12
            y -= 1
        else:
            m -= 1
        # Get the correct day of previous month
        if m in [1,3,5,7,8,10,12]:
            d_ = 31
        elif m in [4,6,9,11]:
            d_ = 30
        elif m == 2:
            # Check for leap year
            if (y % 4 == 0 and y % 100 != 0) or (y % 400 == 0):
                d_ = 29
            else:
                d_ = 28
    ut_day = d_ -1
else:
    utc_hours = (hr - int(tz_offset)) % 24
    ut_day = d_
    ut = datetime.datetime(y, m, ut_day, utc_hours, mn, sc)
"""

jd_morning = jdn - 1.5 + (hr + tz_offset) / 24 + mn / 60 / 24 + sc / 3600 / 24
# Forcing now value to be jd_morning += 1
jd_morning += 1.0 
jd_afternoon =   jdn - 0.5 + (hr + tz_offset) / 24 + mn / 60 / 24 + sc / 3600 / 24
jd_selected = jd_morning if (utc_hours < 12) else jd_afternoon
jc = julian_century(jd_selected) 
print("Selected JD", round(jd_selected,6), "fraction of century", round(jc,6))

# You can check the calculation with online JD calculators
# Example : https://www.aavso.org/jd-calculator
# https://ssd.jpl.nasa.gov/tools/jdc/#/jd_calculator
# We can also use astropy to verify the result
# from astropy.time import Time, requires special installation.
# t = Time(x, scale='utc')
# print("Astropy JD", round(t.jd,6))
# Solar position (elevation and azimuth angle) is calculated
# for given location and time using NOAA solar model, see
# https://gml.noaa.gov/grad/solcalc/solareqns.PDF
# The required functions follow model of NOAA's spreadsheet


gmls = geom_mean_long_sun(jc)

gmas = geom_mean_anom_sun(jc)

eoe = eccent_earth_orbit(jc)

sec = sun_eq_of_center(jc, gmas)

stl = sun_true_long(gmls, sec)

sal = sun_app_long(jc, stl)

moe = mean_obliq_ecliptic(jc)

oc = obliq_corr(jc, moe)

sd = sun_declination(oc, sal)

print("Sun Declination (degrees)", round(sd,6))

y_var = y_variable(jc, oc)

eot = equation_of_time(y_var, gmls, eoe, gmas)

ha = ha_sunrise(jc, latitude, sd)

haSunR = haSunrise(latitude, sd)

tst = true_solar_time(longitude, hr, mn, sc, tz_offset, eot)

solarNoon = solar_noon(longitude, eot, tz_offset)

hourAngle = hour_angle(tst, jc, longitude)

def sunrise_time(df, haSunR):
    srt = df - 4 *  haSunR / 1440
    return srt

def sun_time(dayf, haSunR):
    sunT = sunrise_time(solarNoon[1], haSunR)
    sunH = 24 * sunT
    sunMinutes = 60 * sunH
    sunHours = int(sunH)
    sMinutes = int(sunMinutes) % 60
    sunSeconds = 60 * sunMinutes % 60 
    return f"{sunHours}:{sMinutes}:{round(sunSeconds)}"

sunrise_str = sun_time(solarNoon[1], haSunR)
print("\nSunrise time \t", sunrise_str)
sunset_str = sun_time(solarNoon[1], -haSunR)
print("Sunset time \t", sunset_str)


noon_str = sun_time(solarNoon[1], 0.0)
print("Noon time \t", noon_str)


dayLength = 2 * haSunR / 15 # in decimal hours

dlhr = int(dayLength)
dlmn = int((dayLength - dlhr) * 60)
dlsc = (dayLength - dlhr - dlmn / 60) * 3600
print(f"Daylength \t {dlhr} h {dlmn} min {round(dlsc)} sec")

sza = solar_zenith_angle(tst, hourAngle, latitude, sd)
print("\nSolar Zenith Angle (degrees)", round(sza,2))
print("Solar Elevation Angle (degrees)", round(90.0 - sza,2))


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
print('\nApprox. atmospheric refraction (deg)', round(refract,5))

cor_elev = 90.0 - sza + refract
print(f'\nSolar elevation, corrected for atmosph. refraction \t {round(cor_elev,3)} °')

saz = solar_azimuth(hourAngle, sza, sd, latitude)
print(f"\nSolar Azimuth Angle (clockwise from north) \t \t {round(saz, 2)} °")
