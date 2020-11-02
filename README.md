New Python3 stuff
=================
I have composed the new version of my old favorite suncalculator, this time all in Python 3 language.
First, extract the files of the package sunpos.tar.gz to your project folder with any name.
Before running it, you have to install Flask web framework, see instructions in https://flask.palletsprojects.com/en/1.1.x/
Run the python file in virtual environment:
python isotime.py
Open in the browser http://localhost:5000/sunpos
Enter the optional calculation date and time into the form
Enter the latitude and the longitude degrees of your calculation location
Send the values through clicking the send button.
The date and time shall be left empty if you use the current date and time.
The program calculates in the first round a relative accurate estimate of the noon time
Using the noon time for the next round calculation will give quite accurate Sunrise and Sunset times for any date and location on Earth.
Note, at the noon time, Azimuth is 180 deg, Hour Angle 0 deg and True Solar Time 720 minutes.
If you enter either Sunrise or Sunset time for calculation, you'll get the resective azimuths and altitudes without atmospheric refraction approximately -0.833 deg below horizon (coresponding Zenith 90.83 deg)

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
