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

-----------------------
Tokyo and Sydney AUS results match quite well with the current values by the sites
  https://www.timeanddate.com/sun/japan/tokyo
  https://www.timeanddate.com/sun/australia/sydney
