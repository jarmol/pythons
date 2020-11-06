from flask import Flask, render_template, request, redirect, url_for
#from forms import ContactForm
#from jinja2 import Template
from werkzeug.datastructures import MultiDict
import os
import datetime
from datetime import datetime, date
import time
from datetime import time
from time import gmtime, strftime
from time import strptime
import math

app = Flask(__name__)
SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = 'vanha_varis_vaakkui'

@app.route('/')
def index():
        msg = """
        Something exceptional in values.\n
        Check values of latitude, longitude and timezone
        """
        return msg

@app.route('/sunpos/', methods=['post', 'get'])
def location():
    def ymd(i):
        pvm = date.today()
        gmd = gmtime()
        dl =[gmd.tm_year, gmd.tm_mon, gmd.tm_mday]
        return dl[i]

    def jdncalc(day, month, year):
        Y = year; M = month; D = day
        a = (14 - M)//12
        y = Y + 4800 - a
        m = M + 12*a - 3
        JDN = D + (153*m + 2)//5 + 365*y + y//4 - y//100 + y//400 - 32045
        return JDN

    def jdcalc(jdn, hr, mn, sc):
        jd = jdn + (hr - 12)/24 + mn/1440 + sc/86400
        return jd

    def datestamp( ):
        gmd = gmtime()
        gmobj = (gmd.tm_year, gmd.tm_mon, gmd.tm_mday)
        return gmobj


    def gettime(isodt):
        dtobj = strptime(isodt, "%Y-%m-%d")
        y = dtobj.tm_year
        m = dtobj.tm_mon
        d = dtobj.tm_mday
        return (y, m, d)


    def timestamp( ):
        gmt = gmtime()
        g = strftime("%H:%M:%S", gmt)
        return g

    def gmhrmns(i):
          gmt = gmtime(); gmhr = gmt.tm_hour
          gmmin = gmt.tm_min; gmsec = gmt.tm_sec
          t = [gmhr, gmmin, gmsec]
          return t[i]


    isot = request.form.get('isot')
    if isot:    # time value entered to form used for calculation
        t1 = time.fromisoformat(isot)
        (hour, minute, second) = (t1.hour, t1.minute, t1.second)
    else:       # no time entered, thus the current time is used
        (hour, minute, second) = (gmhrmns(0), gmhrmns(1), gmhrmns(2))

    if isot: calctime = isot
    else: calctime = timestamp()

    print('Calculation time:', calctime)

    ipdt = request.form.get('isodt')
    if ipdt:        # Date read from form input
        reqdt = gettime(ipdt)
        jdn = jdncalc(reqdt[2], reqdt[1], reqdt[0])
    else:           # Crrent date used
        jdn = jdncalc(ymd(2), ymd(1), ymd(0))

    jd = jdcalc(jdn, hour, minute, second)


    def jcentcalc(h0, m0, s0):
        jday = jdcalc(jdn, h0, m0, s0)

        cent = (jday - 2451545)/36525
        jc = cent - int(cent)
        return jc

#   Mean Longitude of Sun, OK tested 10.11.2019

    def calcSunML(cent):
        a = 280.46646
        b = 36000.76983
        c = 3.032e-4
        x = a + cent * (b + cent * c)
        return math.fmod(x, 360)

#  Mean anomality of Sun, OK tested 10.11.2019

    def calcAnomalSun(cent):
        a = 357.52911
        b = 35999.05029
        c = 1.537e-4

        x = a + cent * (b + cent * c)
        return math.fmod(x, 360)

# Eccentricy of Earth Orbit

    def calcEccentrEO(cent):
       x = 0.016708634 - cent * (4.2037e-5 + 1.267e-7 * cent)
       return x

    PI      = math.pi
    rad     = lambda x: PI * x / 180.0
    sinDeg  = lambda x: math.sin(rad(x))
    cosDeg  = lambda x: math.cos(rad(x))
    tanDeg  = lambda x: math.tan(rad(x))

    deg     = lambda x: 180.0 * x / PI
    asinDeg = lambda y: deg(math.asin(y))
    acosDeg = lambda y: deg(math.acos(y))
    atan2Deg = lambda y, x: deg(math.atan2(y, x))


    # Sun true anomality

    def calcSunEqCntr(cent):
        ma = calcAnomalSun(cent)
        y = sinDeg(ma)*(1.914602 - cent*(0.004817 + 1.4e-5 * cent))\
        + sinDeg(2.0*ma) *(0.019993 - 1.01e-4 * cent)\
        + sinDeg (3.0 * ma)*2.89e-4

        return y


    calcSunTrueAnom = lambda cent: calcAnomalSun(cent) + calcSunEqCntr(cent)

    #Sun true longitude
    calcTrueLongSun = lambda cent: calcSunML(cent) + calcSunEqCntr(cent)

    #-- Sun apparent longitude, OK tested 22.10.19

    def calcAppLongSun(cent):
        y = calcTrueLongSun(cent) - 5.69e-3\
        - 4.78e-3 *sinDeg(125.04 - 1934.136 * cent)
        return y


    # -- Mean Obliquity of Ecliptic

    def calcMeanObliqEcl(cent) :
        y = 23.0 + (26.0 + (21.448 - cent *\
                (46.815 + cent * (5.9e-4 - cent * 1.813e-3))) / 60.0) / 60
        return y


    #-- Corrected obliquity

    def calcObliqCorr(cent):
        y = calcMeanObliqEcl(cent) + 0.00256 * cosDeg (125.04 - 1934.136 * cent)
        return y

    def calcRectAsc(cent):
        oblCorr = calcObliqCorr(cent)
        appLongS = calcAppLongSun(cent)
        x = cosDeg(appLongS)
        y = cosDeg(oblCorr) * sinDeg(appLongS)
        z = atan2Deg(y, x)
        return z


    # -- Used in Equation of Time

    def variableY(cent):
        oblCorr = calcObliqCorr(cent)
        x = tanDeg(0.5*oblCorr)
        return x*x

    # -- Equation of Time:

    def equatTime(cent):
        varY =  variableY(cent)
        meanLongS =  calcSunML(cent)
        eOrbitEx = calcEccentrEO(cent)
        meanAnomS = calcAnomalSun(cent)
        TODEG = 180.0/math.pi

        z = TODEG *(varY * sinDeg(2.0 * meanLongS)\
            - 2.0 * eOrbitEx * sinDeg(meanAnomS)\
            + 4.0 * eOrbitEx * varY\
            * sinDeg(meanAnomS) * cosDeg(2.0 * meanLongS)\
            - 0.5 * varY * varY * sinDeg(4.0 * meanLongS)\
            - 1.25 * eOrbitEx * eOrbitEx * sinDeg(2.0 * meanAnomS)\
        ) * 4.0
        return z


    # -- Sun Declination, OK tested 24.10.2019

    def calcSunDeclination(cent):
        y = asinDeg(sinDeg(calcObliqCorr(cent)) * sinDeg(calcAppLongSun(cent)))
        return y


    jcent         = jcentcalc(hour, minute, second); fCent  = f'{jcent:6.8f}'
    sunML         = calcSunML(jcent);         fSunML        = f'{sunML:6.4f}'
    sunAnom       = calcAnomalSun(jcent);     fAnom         = f"{sunAnom:6.4f}"
    eccEO         = calcEccentrEO(jcent);     fEccEO        = f"{eccEO:6.5f}"
    sunEqCntr     = calcSunEqCntr(jcent);     fSunEqCntr    = f"{sunEqCntr:6.4f}"
    sunTrueAnom   = calcSunTrueAnom(jcent);   fSunTrueAnom  = f"{sunTrueAnom:6.4f}"
    trueLongSun   = calcTrueLongSun(jcent);   fTrueLongSun  = f"{trueLongSun:6.4f}"
    appLongSun    = calcAppLongSun(jcent);    fAppLongSun   = f"{appLongSun:6.4f}"
    meanObliqEcl  = calcMeanObliqEcl(jcent);  fMeanObliqEcl = f"{meanObliqEcl:6.4f}"
    obliqCorr     = calcObliqCorr(jcent);     fObliqCorr    = f"{obliqCorr:6.4f}"
    rectAsc       = calcRectAsc(jcent);       fRectAsc      = f"{rectAsc:7.4f}"
    varY          = variableY(jcent);         fvarY         = f"{varY:6.4f}"
    equTime       = equatTime(jcent);         fEquationTime = f"{equTime:6.4f}"
    sunDeclination = calcSunDeclination(jcent)
    fSunDeclination = f"{sunDeclination:6.4f}"

    def getHA(cent, geolat, zenith):
        declin = calcSunDeclination(cent)
        x = (cosDeg(zenith) / (cosDeg(geolat) * cosDeg(declin))\
                - tanDeg(geolat) * tanDeg(declin)
            )

        if x >= 1.0  and declin < 0.00:

            z = 0.00

        elif x < -1.0 and declin > 0.00:
            z = 180.0

        else: z = acosDeg(x)

        return z


    # -- Noon time as minutes since midnight

    def getNoon(cent, geoLong, timeZone):
        equTime = equatTime(cent)
        z = (720.0 - 4.0 * geoLong) - equTime + timeZone * 60
        return z


    # -- Sunrise in minutes, option = -1
    #-- Sunset  in minutes, option = +1

    def calcRiSetMins(cent, geoLong, geoLat, timeZone, zenith, rsOption):
        noonTime = getNoon(cent, geoLong, timeZone)
        #zenith = 90.833    # in degrees for Sunrise and Sunset
        srHA = getHA(cent, geoLat, zenith)
        return noonTime + 4.0 * rsOption * srHA


    def trueSolTime(cent, geoLong, tz):
        if hour: (hr, mn, sc) = (hour, minute, second)
        else:    (hr, mn, sc) = (gmhrmns(0), gmhrmns(1), gmhrmns(2))

        e2 = 60.0*( hr + tz ) + mn + sc/60.0
        v2 = equatTime(cent)
        b4 = geoLong

        return e2 + v2 + 4.0 * b4 - 60.0 * tz

    # -- Hour Angle degr. OK tested 17.11.2019

    def hourAngle(cent, geoLong, tz):
        tSt = trueSolTime(cent, geoLong, tz)
        if tSt > 0.0:
            hra = 0.25 * tSt - 180.0
        else:
            hra = 0.25 * tSt + 180.0

        return hra


    # -- Solar Zenith (degrees)

    def solZenith(cent, geoLat, geoLong, tz):
        b3  = geoLat
        t2 =  calcSunDeclination(cent)
        hrA = hourAngle(cent, geoLong, tz)

        zen = acosDeg(sinDeg(b3)*sinDeg(t2)\
                + cosDeg(b3)*cosDeg(t2)*cosDeg(hrA))

        return zen


    def sunAltitude(cent, geoLat, geoLong, tz):
        zen = solZenith(cent, geoLat, geoLong, tz)
        return 90.0 - zen


    # Max Altitude at Noon: 90 + Sun Declination - gegraphic Latitude

    def maxAltitude(cent, geoLatit):
        altit = 90.0 - abs(geoLatit - calcSunDeclination(cent))
        return altit


    # --  Solar Azimuth angle clockwise from north, OK tested 19.11.2019

    def preAzimuth(cent, geoLat, geoLong, tz):
        ac = hourAngle(cent, geoLong, tz)
        b3 = geoLat
        ad = solZenith(cent, geoLat, geoLong, tz)
        t  = calcSunDeclination(cent)

        z  =  acosDeg((sinDeg(b3)*cosDeg(ad)\
                - sinDeg(t))/(cosDeg(b3)*sinDeg(ad)))

        return z


    def solAzimuth(cent, geoLat, geoLong, tz):
        preAz = preAzimuth(cent, geoLat, geoLong, tz)
        ac    = hourAngle(cent, geoLong, tz)

        if ac > 0.0:
            z = math.fmod((preAz + 180.0), 360)

        else:
            z = math.fmod((540.0 - preAz), 360)

        return z

    # -- Atmospheric Refraction Correction of Solar Elevation

    def atmosRefract(solElev):
        #solElev = 90.0 - solZenith(cent, geoLat, geoLong, tz)
        x = tanDeg(solElev)

        if solElev > 85.0: r = 0.0

        elif solElev > 5.0:
            r = (58.1 / x - 0.07 / math.pow(x, 3) + 8.6e-5 / math.pow(x, 5)) / 3600.0

        elif solElev >  -0.575:
            r = (1735.0 + solElev * (-518.2 + solElev * (103.4 + solElev*(-12.79 + solElev*0.711)))) / 3600.0

        else:
            r = -20.772 / x / 3600.0

        return solElev + r


    def time_to_hrmnsc(seconds):
        t = float(seconds)
        d = t // (24*3600)
        t = t  % (24*3600)
        h = int(t // 3600)
        t %= 3600
        mn = int(t // 60)
        t %= 60
        sc = math.floor(t + 0.4); sc = int(sc)
        if sc > 59: sc = 59
        ts = time(h, mn, sc)
        return str(ts)


    dt = datestamp(); datestamp = date(dt[0], dt[1], dt[2])
    timestamp = timestamp()
    print('datestamp',datestamp)

    if request.method == 'POST':
        calcdate = request.form.get('isodt')
        if calcdate:
            #datestamp = calcdate
            print('post calcdate', calcdate)

        latitude = request.form.get('latit')
        longitude = request.form.get('longit')
        #hour = request.form.get('hour')
        #if hour: hr0 = int(hour)
        lat = float(latitude)
        lon = float(longitude)
        TZ = request.form.get('tzone') # Timezone in hours
        tz = float(TZ)

        if abs(lat) <= 90 and abs(lon) <= 180 and abs(tz) <= 12:
            msg1 = latitude
            msg2 = longitude
            srHA = getHA(jcent, lat, 90.833)
            fSrHA = f"{srHA:6.4f}"
            minutesDaylight = 8.0*srHA
            hoursHA = minutesDaylight/60.0
            gHoursDL = time_to_hrmnsc(60*8*srHA)
            noonTime = getNoon(jcent, lon, tz)
            gNoonTime   = time_to_hrmnsc(60*noonTime)
            riseCivilTwil    = calcRiSetMins(jcent, lon, lat, tz, 96.0, -1)
            riseTime    = calcRiSetMins(jcent, lon, lat, tz, 90.83, -1)
            sunsetTime  = calcRiSetMins(jcent, lon, lat, tz, 90.83, 1)
            setCivilTwil  = calcRiSetMins(jcent, lon, lat, tz, 96.0, 1)
            gRiseCivTwl   = time_to_hrmnsc(60*riseCivilTwil)
            gRiseTime   = time_to_hrmnsc(60*riseTime)
            gSunsetTime = time_to_hrmnsc(60*sunsetTime)
            gSetCivTwl  = time_to_hrmnsc(60*setCivilTwil)
            trueST   = trueSolTime(jcent, lon, tz)
            hrAngle  = hourAngle(jcent, lon, tz)
            current_zenith = solZenith(jcent, lat, lon, tz)
            sunAlt   = sunAltitude(jcent, lat, lon, tz)
            maxAlt   = maxAltitude(jcent, lat)
            sunAzim  = solAzimuth(jcent, lat, lon, tz)
            correctElevation = atmosRefract(sunAlt)
            maxCorrEl = atmosRefract(maxAlt)
            fZenith  = f"{current_zenith:6.4f}"
            fTrueST  = f"{trueST:6.4f}"
            fHRangle = f"{hrAngle:6.4f}"
            fSunAlt  = f"{sunAlt:6.4f}"
            fMaxAlt  = f"{maxAlt:6.4f}"
            fSunAzim = f"{sunAzim:6.4f}"
            fCorrectElevation = f"{correctElevation:6.4f}"
            fMaxCorrEl = f"{maxCorrEl:6.4f}"

        else:
            if tz > 12: print("Error: timezone > 12?", TZ)
            if abs(lat) >  90: print("Error: latitude < -90 or > +90", lat)
            if abs(lon) > 180: print("Error: longitude < -180 or > 180", lon)
            error_context = dict(tz = tz, lat = lat, lon = lon)
            return render_template('public/locationerror.html', **error_context)
            return redirect(url_for('index'))

    template_context = dict(datestamp = datestamp, timestamp = timestamp,
            calctime = calctime,
            jdn = jdn, jd = jd, fCent = fCent, fSunML = fSunML,
            fAnom = fAnom, fEccEO = fEccEO, fSunEqCntr = fSunEqCntr,
            fSunTrueAnom = fSunTrueAnom, fTrueLongSun = fTrueLongSun,
            fAppLongSun = fAppLongSun, fMeanObliqEcl = fMeanObliqEcl,
            fObliqCorr = fObliqCorr, fRectAsc = fRectAsc, fvarY = fvarY,
            fEquationTime = fEquationTime,
            fSunDeclination = fSunDeclination)


    if request.method == 'POST':
        template_context2 = dict(fSrHA = fSrHA,
            msg1 = msg1, msg2 = msg2, TZ = TZ, calcdate = calcdate,
            gHoursDL = gHoursDL, gNoonTime = gNoonTime,
            gRiseTime = gRiseTime, gSunsetTime = gSunsetTime,
            gRiseCivTwl = gRiseCivTwl,
            gSetCivTwl     = gSetCivTwl,
            fTrueST = fTrueST, fHRangle = fHRangle, fMaxAlt = fMaxAlt,
            fSunAlt = fSunAlt, fZenith = fZenith, fSunAzim = fSunAzim,
            fCorrectElevation = fCorrectElevation,
            fMaxCorrEl = fMaxCorrEl )

        template_context.update(template_context2)

    return render_template('public/isotime.html', **template_context)

if __name__ == "__main__":
    app.run(debug=True)

