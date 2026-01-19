#Last login: Fri Jan 16 11:36:30 on ttys000
import time, datetime
d = datetime.datetime.now()
print("Current local time", d.strftime("%Y-%m-%d %H:%M:%S"))
y, m, d_ = d.year, d.month, d.day
hr,mn,sc = d.hour, d.minute, d.second

def jdn_from_date(yr, mnt, day) :
    result = 367*yr - 7*(yr + (mnt + 9)//12)//4 \
    - 3*((yr + (mnt - 9)//7)//100 + 1)//4 \
    + 275*mnt//9 + day + 1721029
    return(result)


jdn = jdn_from_date(y, m, d_)

print("Julian Day Number JDN", jdn)
print("year",y,"month",m,"day",d_)

tposix = time.mktime(d.timetuple())
print("Epoch seconds", tposix)
tday = 24*3600
seconds = tposix % 60
print("Current time seconds part", seconds)

days = tposix // tday
print("Epoch (1970-01-01) posix daynumber", days)

dsecs = tposix % tday
print(f"remaining of today {dsecs} sec")

utc_hours = dsecs // 3600
print("Hours of current UTC time", utc_hours)

tz_offset = utc_hours - d.hour
print(f"Timezone Offset {tz_offset} hours from UTC")

# Local time 
x = datetime.datetime(y, m, d_, hr, mn, sc)
print("Local time:", x.strftime("%A, %Y-%m-%d %H:%M:%S"), f"UTC {-tz_offset} h")

# UTC Time
ut = datetime.datetime(y, m, d_, hr + int(tz_offset), mn, sc) # UTC time
print("UTC time:  ", ut.strftime("%A, %Y-%m-%d %H:%M:%S"))

jd_afternoon = jdn + (hr + tz_offset - 12) / 24 + mn / 60 / 24 + sc / 3600 / 24
jd_morning = jdn - 0.5 + (hr + tz_offset) / 24 + mn / 60 / 24 + sc / 3600 / 24

jd_selected = jd_morning if (utc_hours < 12) else jd_afternoon

print("Selected JD", round(jd_selected,6))
# You can check the calculation with online JD calculators
# Example : https://www.aavso.org/jd-calculator
# https://ssd.jpl.nasa.gov/tools/jdc/#/jd_calculator
# We can also use astropy to verify the result
# from astropy.time import Time
# t = Time(x, scale='utc')
# print("Astropy JD", round(t.jd,6))

# Next we continue with calculating the solar position for given location and time
# using NOAA solar model, see https://gml.noaa.gov/grad/solcalc/solareqns.PDF
# The required functions are translated manually from the NOAA's spreadsheet
# and attached in the file noaa-solar.py
