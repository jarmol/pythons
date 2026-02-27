from math import pi, sin, cos, asin, acos, tan
import datetime, time

def rad(x):
    return(pi * x / 180.0)

def deg(x):
    return(180.0 * x / pi)

deg2rad = pi / 180.0

def geom_mean_long_sun(jc):
    gmls = 280.46646 + jc * (36000.76983 + jc * 0.0003032)
    # More elegant way to keep angle within 0-360 degrees
    gmls = gmls % 360.0
    return gmls


def geom_mean_anom_sun(jc):
    gmas = 357.52911 + jc * (35999.05029 - 0.0001537 * jc)
    return (gmas % 360.0)

def eccent_earth_orbit(jc):
    eoe = 0.016708634 - jc * (0.000042037 + 0.0000001267 * jc)
    return eoe

def mean_obliq_ecliptic(jc):
    moe = 23.0 + (26.0 + ((21.448 - jc * (46.815 \
     + jc * (0.00059 - jc * 0.001813)))) / 60.0) / 60.0
    return moe

def obliq_corr(jc):
    omega = 125.04 - 1934.136 * jc
    moe = mean_obliq_ecliptic(jc)
    oc = moe + 0.00256 * cos(omega * deg2rad)
    return oc

def sun_eq_of_center(jc):
    gmas = geom_mean_anom_sun(jc) 
    gmas_rad = deg2rad*gmas
    sec = (sin(gmas_rad) * (1.914602 - jc * (0.004817 + 0.000014 * jc)) +
           sin(2 * gmas_rad) * (0.019993 - 0.000101 * jc) +
           sin(3 * gmas_rad) * 0.000289)
    return sec

def sun_true_long(jc):
    gmls = geom_mean_long_sun(jc)
    sec = sun_eq_of_center(jc)
    stl = gmls + sec
    return (stl % 360.0)

def sun_app_long(jc, stl):
    omega = 125.04 - 1934.136 * jc
    sal = stl - 0.00569 - 0.00478 * sin(omega * deg2rad)
    return sal

def sun_declination(jc):
    oc = obliq_corr(jc)
    stl = sun_true_long(jc)
    sal = sun_app_long(jc, stl)
    sd = deg(asin(sin(rad(oc))*sin(rad(sal))))
    return sd

def y_variable(jc):
    # Calculate the Y variable for the equation of time
    #moe = mean_obliq_ecliptic(jc)
    oc = obliq_corr(jc)
    y = tan(rad(oc) / 2.0) * tan(rad(oc) / 2.0)
    return y

def equation_of_time(jc):
    gmls = geom_mean_long_sun(jc)
    eoe = eccent_earth_orbit(jc)
    gmas = geom_mean_anom_sun(jc)
    y = y_variable(jc)
    eot = y * sin(2 * rad(gmls)) - 2 * eoe * sin(rad(gmas)) \
            + 4 * eoe * y * sin(rad(gmas)) * cos(2 * rad(gmls)) \
            - 0.5 * y * y * sin(4 * rad(gmls)) - 1.25 * eoe * eoe * sin(2 * rad(gmas))

    eot = deg(eot) * 4.0  # Convert to minutes
    return eot

def haSunrise(latitude, sd):
    haS = deg(acos(cos(rad(90.833)) / (cos(rad(latitude)) * cos(rad(sd))) - tan(rad(latitude)) * tan(rad(sd))))
    return haS


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

def hour_angle(tcurrent):
    ha = (tcurrent / 4.0) - 180.0
    if ha < -180.0:
        ha += 360.0
    return ha

d = datetime.datetime.now()
y, m, d_ = d.year, d.month, d.day
hr,mn,sc = d.hour, d.minute, d.second

tz_sign = ''

tz_offset = time.timezone / 3600

if tz_offset > 0:
    tz_sign = '-'
elif tz_offset == 0: tz_sign = ' '
else :
    tz_sign = '+'

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

def solar_zenith_angle(ha, lat, sd):
    sins = sin(rad(lat)) * sin(rad(sd))
    coss = cos(rad(lat)) * cos(rad(sd)) * cos(rad(ha))
    sza = deg(acos(sins + coss))
    return sza


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