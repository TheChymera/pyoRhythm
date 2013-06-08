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
import pandas as pd
from os import path
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

full_df = pd.read_csv(filename)

start_date = datetime.datetime.strptime(path.split(filename)[1].split('_')[1], '%Y-%m-%d.csv')
dates = []
for i in range(len(full_df['Going to bed'])): dates.append(start_date + datetime.timedelta(i))

fig = figure(facecolor='#eeeeee',  tight_layout=True)
ax1 = fig.add_subplot(111)
ax1.set_ylim(-0.7, 10.7)
matplotlib.axis.Axis.zoom(ax1.xaxis, -0.4)
ax1.plot(dates, full_df['Waking up'], 'y-', linewidth=2, alpha=0.7)
ax1.plot(dates, full_df['Woken up'], 'c-', linewidth=2, alpha=0.7)
ax1.plot(dates, full_df['Going to bed'], 'm-', linewidth=2, alpha=0.7)
legend(('Waking up', 'Woken up', 'Going to Bed'), 'upper left', shadow=False, frameon=False, prop= matplotlib.font_manager.FontProperties(size='11'))
ylabel('Self-Evaluated Satisfaction [1-10]', fontsize='12')

ax1.xaxis.set_major_formatter(mdates.DateFormatter('%d/%m/%y'))
tick_params(axis='x', labelsize='9')
tick_params(axis='y', labelsize='12')
fig.autofmt_xdate()

ax2 = ax1.twinx()
ax2.set_yscale('symlog')
ax2.fill_between(dates, full_df['Very short approaches'],0.00001, color='k', alpha = 0.1)
ax2.fill_between(dates, full_df['Indirect approaches'],0.00001, color='g', alpha = 0.2)
ax2.fill_between(dates, full_df['Direct approaches'],0.00001, color='g', alpha = 0.4)
ax2.fill_between(dates, full_df['Closes (physical)'],0.00001, color='r', alpha = 0.6)
#~ legend(('Short Approaches','Indirect Approaches','Direct Approaches','Closes(physical)'), 'upper right', shadow=False, frameon=False, prop= matplotlib.font_manager.FontProperties(size='11'))
ylabel('Interaction #', fontsize='12')
xlabel('Time [date]', fontsize='12')
title(path.split(filename)[1].split('_')[0]+'\'s Life Satisfaction and Social Contacts Timeline.')
show()
