New Python3 stuff
=================

I have composed the new version of my old favorite suncalculator, this time all in Python 3 language.

First, extract the files of the package sunpos.tar.gz to your project folder with any name:
```bash
   tar -xf sunpos.tar.gz
```

Before running it, you have to install <b>Flask</b> web framework, see instructions in https://flask.palletsprojects.com/en/1.1.x

Do activate the virtual environment:
```bash
source ./env/bin/activate
```

Run the python file in virtual environment debug mode:
```bash
   cd solarpos/app
   python sunpos.py
```

Open in the browser http://localhost:5000/sunpos

Enter the optional Calculation Date and Time into the form.

Enter the Latitude and the Longitude in degrees of your calculation location.

Send the values through clicking the send button.

The date and time shall be left empty if you use the current date and time.

The program calculates in the first round a relatively accurate estimate of the noon time and the Day length.

Using the noon time for the next round, calculation shall give quite accurate Sunrise and Sunset times for any date and location on Earth.

Note, at the noon time, Azimuth is 180 deg, Hour Angle is 0 deg and True Solar Time 720 minutes.

If you enter either Sunrise or Sunset time for calculation, you'll get the respective Azimuth and Altitude without Atmospheric refraction approximately -0.833 deg below horizon (coresponding to Zenith 90.833 deg).

I have made my Sunposition Calculator mainly for learning purpose to myself and for those who may be interested in it. I know there are already many others, much better than mine. 

You may compare the calculation results e.g. to NOAA Calculator:
   https://www.esrl.noaa.gov/gmd/grad/solcalc/
   

Old Python stuff
==================
Miscellaneous stuff and examples about Python programming
Examples run on i686 GNU/Linux with Python 2.6.6

GUI-programming
---------------

Module Tkinter
--------------
This module contains tools for GUI
- http://zetcode.com/gui/tkinter/introduction/
