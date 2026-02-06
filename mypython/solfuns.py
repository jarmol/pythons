# Module for solar functions

from math import pi, sin, asin, cos, tan, acos

def rad(x):
    return(pi * x / 180.0)

def deg(x):
    return(180.0 * x / pi)

def jdn_from_date(yr, mnt, day) :
    result = 367*yr - 7*(yr + (mnt + 9)//12)//4 \
    - 3*((yr + (mnt - 9)//7)//100 + 1)//4 \
    + 275*mnt//9 + day + 1721029
    return(result)

def julian_century(jd):
# "Calculate Julian Century from Julian Day
    jc = (jd - 2451545.0) / 36525.0
    return jc

def geom_mean_long_sun(jc):
  # Calculate the Geometric Mean Longitude of the Sun (in degrees)
    gmls = 280.46646 + jc * (36000.76983 + jc * 0.0003032)

    gmls = gmls % 360.0
    return gmls

def geom_mean_anom_sun(jc):
    """Calculate the Geometric Mean Anomaly of the Sun (in degrees)"""
    gmas = 357.52911 + jc * (35999.05029 - 0.0001537 * jc)
    return (gmas % 360.0)

def eccent_earth_orbit(jc):
    """Calculate the eccentricity of Earth's orbit"""
    eoe = 0.016708634 - jc * (0.000042037 + 0.0000001267 * jc)
    return eoe

def sun_eq_of_center(jc):
    """Calculate the Sun's Equation of the Center (in degrees)"""
    gmas = geom_mean_anom_sun(jc)
    gmas_rad = rad(gmas)
    sec = (sin(gmas_rad) * (1.914602 - jc * (0.004817 + 0.000014 * jc)) +
           sin(2 * gmas_rad) * (0.019993 - 0.000101 * jc) +
           sin(3 * gmas_rad) * 0.000289)
    return sec

def sun_true_long(gmls, sec):
    """Calculate the Sun's True Longitude (in degrees)"""
    stl = gmls + sec
    return (stl % 360.0)

def sun_app_long(jc, stl):
    """Calculate the Sun's Apparent Longitude (in degrees)"""
    omega = 125.04 - 1934.136 * jc
    sal = stl - 0.00569 - 0.00478 * sin(rad(omega))
    return sal

# sal = sun_app_long(jc, stl)

def mean_obliq_ecliptic(jc):
    """Calculate the Mean Obliquity of the Ecliptic (in degrees)"""
    moe = 23.0 + (26.0 + ((21.448 - jc * (46.815 \
     + jc * (0.00059 - jc * 0.001813)))) / 60.0) / 60.0
    return moe

def obliq_corr(jc):
    """Calculate the Obliquity Correction (in degrees)"""
    moe = mean_obliq_ecliptic(jc)
    omega = 125.04 - 1934.136 * jc
    oc = moe + 0.00256 * cos(rad(omega))
    return oc


def sun_declination(jc, sal):
# Calculate the Sun's Declination (in degrees)
    moe = mean_obliq_ecliptic(jc)
    oc = obliq_corr(jc)
    sd = deg(asin(sin(rad(oc))*sin(rad(sal))))
    return sd

# sd = sun_declination(oc, sal)

def y_variable(jc, oc):
    """Calculate the Y variable for the equation of time"""
    y = tan(rad(oc) / 2.0) * tan(rad(oc) / 2.0)
    return y

"""Equation of Time (in minutes)"""
def equation_of_time(y, gmls, eoe, gmas):
    a = rad(gmls)
    b = rad(gmas)
    eot = y * sin(2 * a) - 2 * eoe * sin(b) \
    + 4 * eoe * y * sin(b) * cos(2 * a) \
    - 0.5 * y * y * sin(4 * a) - 1.25 * eoe * eoe * sin(2 * b)
    eot = deg(eot) * 4.0  # Convert to minutes
    return eot

def ha_sunrise(jc, lat, sd):
    """Calculate the Hour Angle at Sunrise (in degrees)"""
    ha = deg(acos(cos(rad(90.833)) / (cos(rad(lat)) * cos(rad(sd))) - tan(rad(lat)) * tan(rad(sd))))
    return ha

def haSunrise(lat, sd):
    haS = deg(acos(cos(rad(90.833)) / (cos(rad(lat)) * cos(rad(sd))) - tan(rad(lat)) * tan(rad(sd))))
    return haS

def true_solar_time(longitude, hr, mn, sc, tz_offset, eot=0.0):
    # Calculate the True Solar Time (in minutes)
    # time_in_minutes: local time in minutes (0..1440)
    time_in_minutes = hr * 60 + mn + sc / 60
    # tz_offset from time.timezone is seconds west of UTC -> hours west of UTC
    # spreadsheet/timezone convention: positive for east of Greenwich
    tz = -tz_offset
    # Apply equation of time (minutes) and longitude/timezone offsets
    tst = (time_in_minutes + eot + 4 * longitude - 60 * tz) % 1440
    return tst

def solar_noon(longitude, eot, tzoffs):
    # =(720-4*$B$4-V2+$B$5*60)/1440
    day_fraction = (720 - 4 * longitude - eot - tzoffs * 60) / 1440
    noon_as_minutes = 720 - 4 * longitude - eot - tzoffs * 60
    noon_hours = int(noon_as_minutes) // 60
    noon_minutes = int(noon_as_minutes) % 60
    noon_seconds = (60*noon_as_minutes) % 60
    noon_hr_mn_str = (f"Noon time {noon_hours}:{noon_minutes}:{round(noon_seconds, 2)}")
    return [noon_hr_mn_str, day_fraction]

def hour_angle(tcurrent, jc, lon):
    """Calculate the Hour Angle (in degrees)"""
    ha = (tcurrent / 4.0) - 180.0 # + lon
    if ha < -180.0:
        ha += 360.0
    return ha

def sun_time(dayf, haSunR):
    sunT = dayf - haSunR / 360.0
    sunH = 24 * sunT
    # compute total seconds and split to HH:MM:SS with zero-padding
    total_seconds = int(round(sunH * 3600))
    sunHours = total_seconds // 3600
    sMinutes = (total_seconds % 3600) // 60
    sunSeconds = total_seconds % 60
    return f"{sunHours:02d}:{sMinutes:02d}:{sunSeconds:02d}"

def solar_zenith_angle(tcurrent, ha, lat, sd):
    """Calculate the Solar Zenith Angle (in degrees)"""
    sins = sin(rad(lat)) * sin(rad(sd))
    coss = cos(rad(lat)) * cos(rad(sd)) * cos(rad(ha))
    sza = deg(acos(sins + coss))
    return sza


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
