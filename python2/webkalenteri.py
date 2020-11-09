import datetime
from datetime import date
import calendar

nyt = date.today()

suomikuu = calendar.LocaleHTMLCalendar(0,"fi_FI")
x = suomikuu.formatmonth(nyt.year, nyt.month)
print x
