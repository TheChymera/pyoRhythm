#!/usr/bin/env python
__author__ = 'Horea Christian'
#creates a linear time-based plot of three daily life satisfaction measurements
#and a superimposed log plot of daily measured social interactions
#requires an input file reading Start:day.month.year (eg. Start:11.11.2011) on the first row
#and three comma-separated values per row afterwards (1st - waking, 2nd - after waking, 3rd - before going to bed
#4th - approaches, 5th - conversations)
import gtk
import numpy as np
import matplotlib.dates as mdates
import itertools
from pylab import math, datetime, figure, tick_params, legend, xlabel, ylabel, title, matplotlib, show

if gtk.pygtk_version < (2,3,90):
    print "PyGtk 2.3.90 or later required for Plot-It"
    raise SystemExit
dialog = gtk.FileChooserDialog("Choose satisfaction monitoring file...",
                               None,
                               gtk.FILE_CHOOSER_ACTION_OPEN,
                               (gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL,
                                gtk.STOCK_OPEN, gtk.RESPONSE_OK))
dialog.set_default_response(gtk.RESPONSE_OK)

dafilter = gtk.FileFilter()
dafilter.set_name("Text files")
dafilter.add_mime_type("text/plain")
dafilter.add_pattern("*.txt")
dialog.add_filter(dafilter)

dafilter = gtk.FileFilter()
dafilter.set_name("All files")
dafilter.add_pattern("*")
dialog.add_filter(dafilter)

response = dialog.run()
if response == gtk.RESPONSE_OK:
    filename = dialog.get_filename()
    print dialog.get_filename(), 'selected'
elif response == gtk.RESPONSE_CANCEL:
    print 'Closed, no files selected'
dialog.destroy()

data = np.genfromtxt(filename, skip_header=1, delimiter=",")
data_raw = [line.strip().split() for line in open(filename)]
date = datetime.datetime.strptime(''.join(data_raw[0]), 'Start:%d.%m.%Y')
col=list(itertools.izip(*data))

y1 = [value for value in col[0] if not math.isnan(value)]
y2 = [value for value in col[1] if not math.isnan(value)]
y3 = [value for value in col[2] if not math.isnan(value)]
y4 = [value for value in col[3] if not math.isnan(value)]
y5 = [value for value in col[4] if not math.isnan(value)]
y6 = [value for value in col[5] if not math.isnan(value)]

x1 = [i for i, value in enumerate(col[0]) if not math.isnan(value)]
x2 = [i for i, value in enumerate(col[1]) if not math.isnan(value)]
x3 = [i for i, value in enumerate(col[2]) if not math.isnan(value)]
x4 = [i for i, value in enumerate(col[3]) if not math.isnan(value)]
x5 = [i for i, value in enumerate(col[4]) if not math.isnan(value)]
x6 = [i for i, value in enumerate(col[5]) if not math.isnan(value)]

ts1 = []
for i in x1: ts1.append(date + datetime.timedelta(i))
ts2 = []
for i in x2: ts2.append(date + datetime.timedelta(i))
ts3 = []
for i in x3: ts3.append(date + datetime.timedelta(i))
ts4 = []
for i in x4: ts4.append(date + datetime.timedelta(i))
ts5 = []
for i in x5: ts5.append(date + datetime.timedelta(i))
ts6 = []
for i in x6: ts6.append(date + datetime.timedelta(i))

fig = figure(facecolor='#eeeeee')
ax1 = fig.add_subplot(111)
ax1.set_ylim(-0.7, 10.7)
matplotlib.axis.Axis.zoom(ax1.xaxis, -0.4)
ax1.plot(ts1, y1, 'y-', linewidth=2, alpha=0.7)
ax1.plot(ts2, y2, 'c-', linewidth=2, alpha=0.7)
ax1.plot(ts3, y3, 'm-', linewidth=2, alpha=0.7)
legend(('Waking up', 'After Waking', 'Going to Bed'), 'upper left', shadow=False, frameon=False, prop= matplotlib.font_manager.FontProperties(size='11'))
ylabel('Self-Evaluated Satisfaction [1-10]', fontsize='12')

ax1.xaxis.set_major_formatter(mdates.DateFormatter('%d/%m/%y'))
tick_params(axis='x', labelsize='9')
tick_params(axis='y', labelsize='12')
fig.autofmt_xdate()

ax2 = ax1.twinx()
ax2.set_yscale('symlog')
ax2.plot(ts4, y4, 'k-', linewidth=0, alpha=0.1)
ax2.fill_between(ts4,y4,0.00001, color='k', alpha = 0.1)
ax2.plot(ts5, y5, 'g-', linewidth=0, alpha=1)
ax2.fill_between(ts5,y5,0.00001, color='g', alpha = 0.2)
ax2.plot(ts6, y6, 'g-', linewidth=0, alpha=1)
ax2.fill_between(ts6,y6,0.00001, color='g', alpha = 0.4)
legend(('Approaches','Conversations','New Contacts'), 'upper right', shadow=False, frameon=False, prop= matplotlib.font_manager.FontProperties(size='11'))
ylabel('Interaction #', fontsize='12')
xlabel('Time [date]', fontsize='12')
title('')
show()
#test