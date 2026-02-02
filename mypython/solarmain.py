import time, datetime
from math import pi, sin, asin, cos, tan, acos
from solfuns import jdn_from_date, julian_century, geom_mean_long_sun, geom_mean_anom_sun, eccent_earth_orbit, sun_eq_of_center, sun_true_long, sun_app_long, mean_obliq_ecliptic, obliq_corr

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
print("Selected JD", round(jd_selected,6))

# You can check the calculation with online JD calculators
# Example : https://www.aavso.org/jd-calculator
# https://ssd.jpl.nasa.gov/tools/jdc/#/jd_calculator
# We can also use astropy to verify the result
# from astropy.time import Time
# t = Time(x, scale='utc')
# print("Astropy JD", round(t.jd,6))

# for given location and time using NOAA solar model, see
# https://gml.noaa.gov/grad/solcalc/solareqns.PDF
# The required functions follow model of NOAA's spreadsheet


def rad(x):
    return(pi * x / 180.0)

def deg(x):
    return(180.0 * x / pi)

jc = julian_century(jd_selected) 

gmls = geom_mean_long_sun(jc)

gmas = geom_mean_anom_sun(jc)

eoe = eccent_earth_orbit(jc)

sec = sun_eq_of_center(jc, gmas)

stl = sun_true_long(gmls, sec)

sal = sun_app_long(jc, stl)

moe = mean_obliq_ecliptic(jc)

oc = obliq_corr(jc, moe)

def sun_declination(oc, sal):
# Calculate the Sun's Declination (in degrees)
    sd = deg(asin(sin(rad(oc))*sin(rad(sal))))
    return sd

sd = sun_declination(oc, sal)
print("Sun's Declination (degrees)", round(sd,6))

def y_variable(jc, oc):
    """Calculate the Y variable for the equation of time"""
    y = tan(rad(oc) / 2.0) * tan(rad(oc) / 2.0)
    return y

y_var = y_variable(jc, oc)

"""Equation of Time (in minutes)"""
def equation_of_time(y, gmls, eoe, gmas):
    eot = y * sin(2 * rad(gmls)) - 2 * eoe * sin(rad(gmas)) \
            + 4 * eoe * y * sin(rad(gmas)) * cos(2 * rad(gmls)) \
            - 0.5 * y * y * sin(4 * rad(gmls)) - 1.25 * eoe * eoe * sin(2 * rad(gmas))

    eot = deg(eot) * 4.0  # Convert to minutes
    return eot
eot = equation_of_time(y_var, gmls, eoe, gmas)

def ha_sunrise(jc, lat):
    """Calculate the Hour Angle at Sunrise (in degrees)"""
    sd = sun_declination(obliq_corr(jc, mean_obliq_ecliptic(jc)), sun_app_long(jc, sun_true_long(geom_mean_long_sun(jc), sun_eq_of_center(jc, geom_mean_anom_sun(jc)))))
    ha = deg(acos(cos(rad(90.833)) / (cos(rad(lat)) * cos(rad(sd))) - tan(rad(lat)) * tan(rad(sd))))
    return ha
ha = ha_sunrise(jc, latitude)

def haSunrise(latitude, sd):
    haS = deg(acos(cos(rad(90.833)) / (cos(rad(latitude)) * cos(rad(sd))) - tan(rad(latitude)) * tan(rad(sd))))
    return haS

haSunR = haSunrise(latitude, sd)

def true_solar_time(jd, longitude, hr, mn, sc, tz_offset, eot=0.0):
    # Calculate the True Solar Time (in minutes)
    # time_in_minutes: local time in minutes (0..1440)
    time_in_minutes = hr * 60 + mn + sc / 60
    # tz_offset from time.timezone is seconds west of UTC -> hours west of UTC
    # spreadsheet/timezone convention: positive for east of Greenwich
    tz = -tz_offset
    # Apply equation of time (minutes) and longitude/timezone offsets
    tst = (time_in_minutes + eot + 4 * longitude - 60 * tz) % 1440
    return tst
tst = true_solar_time(jd_selected, longitude, hr, mn, sc, tz_offset, eot)

def solar_noon(longitude, eot, tzoffs):
    # =(720-4*$B$4-V2+$B$5*60)/1440
    day_fraction = (720 - 4 * longitude - eot - tzoffs * 60) / 1440
    noon_as_minutes = 720 - 4 * longitude - eot - tzoffs * 60
    noon_hours = int(noon_as_minutes) // 60
    noon_minutes = int(noon_as_minutes) % 60
    noon_seconds = (60*noon_as_minutes) % 60
    noon_hr_mn_str = (f"Noon time {noon_hours}:{noon_minutes}:{round(noon_seconds, 2)}")
    return [noon_hr_mn_str, day_fraction]
solarNoon = solar_noon(longitude, eot, tz_offset)


def hour_angle(tcurrent, jc, lon):
    """Calculate the Hour Angle (in degrees)"""
    ha = (tcurrent / 4.0) - 180.0 # + lon
    if ha < -180.0:
        ha += 360.0
    return ha

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
print("Sunrise time", sunrise_str)
sunset_str = sun_time(solarNoon[1], -haSunR)
print("Sunset time ", sunset_str)


noon_str = sun_time(solarNoon[1], 0.0)
print("Noon time ", noon_str)


dayLength = 2 * haSunR / 15 # in decimal hours

dlhr = int(dayLength)
dlmn = int((dayLength - dlhr) * 60)
dlsc = (dayLength - dlhr - dlmn / 60) * 3600
print(f"Daylength {dlhr} h {dlmn} min {round(dlsc)} sec")


def solar_zenith_angle(tcurrent, ha, lat, sd):
    """Calculate the Solar Zenith Angle (in degrees)"""
    sins = sin(rad(lat)) * sin(rad(sd))
    coss = cos(rad(lat)) * cos(rad(sd)) * cos(rad(ha))
    sza = deg(acos(sins + coss))
    return sza

sza = solar_zenith_angle(tst, hourAngle, latitude, sd)
print("Solar Zenith Angle (degrees)", round(sza,6))
print("Solar Elevation Angle (degrees)", round(90.0 - sza,6))


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
print('Approx. atmospheric refraction (deg)', round(refract,5))

cor_elev = 90.0 - sza + refract
print('Solar elevation, corrected for atmosph. refraction', round(cor_elev,4))

def solar_azimuth(ha, sza, sd, lat):
    """Calculate the Solar Azimuth Angle (in degrees clockwise from north)"""
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
print("Solar Azimuth Angle (degrees clockwise from north)", round(saz, 6))
