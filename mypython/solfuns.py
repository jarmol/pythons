# Module for solar functions

from math import pi, sin, asin, cos, tan, acos

def rad(x):
    return(pi * x / 180.0)

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

def sun_eq_of_center(jc, gmas):
    """Calculate the Sun's Equation of the Center (in degrees)"""
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

def mean_obliq_ecliptic(jc):
    """Calculate the Mean Obliquity of the Ecliptic (in degrees)"""
    moe = 23.0 + (26.0 + ((21.448 - jc * (46.815 \
     + jc * (0.00059 - jc * 0.001813)))) / 60.0) / 60.0
    return moe

def obliq_corr(jc, moe):
    """Calculate the Obliquity Correction (in degrees)"""
    omega = 125.04 - 1934.136 * jc
    oc = moe + 0.00256 * cos(rad(omega))
    return oc
