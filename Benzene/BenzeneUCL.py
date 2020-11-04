import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as dates
from datetime import datetime
import matplotlib.dates as mdates

# Handle date time conversions between pandas and matplotlib
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

# Read the data
db93 = pd.read_csv(r'/Users/Henry/Desktop/1993 UCL data.csv')
db94 = pd.read_csv(r'/Users/Henry/Desktop/1994 UCL data.csv')
db95 = pd.read_csv(r'/Users/Henry/Desktop/1995 UCL data.csv')
db96 = pd.read_csv(r'/Users/Henry/Desktop/1996 UCL data.csv')
db97 = pd.read_csv(r'/Users/Henry/Desktop/1997 UCL data.csv')
db98 = pd.read_csv(r'/Users/Henry/Desktop/1998 UCL data.csv')
db99 = pd.read_csv(r'/Users/Henry/Desktop/1999 UCL data.csv')
db00 = pd.read_csv(r'/Users/Henry/Desktop/2000 UCL data.csv')

datasets = [db93,db94,db95,db96,db97,db98,db99,db00]

x=[]
y=[]

for i in range(len(datasets)):

    Date = datasets[i]['Date']

    voc = datasets[i].iloc[:,2]

    # Remove No data 
    A = voc[voc!='No data']

    # Find indices of the rows with no data
    B = voc[voc == 'No data'].index.tolist()

    # Drop those dates associated with no data
    Date = Date.drop(Date.index[B])

    # Reset the indices
    NewDate = Date.reset_index(drop=True)
    NewVOC = A.reset_index(drop=True)

    # Convert dates to format that can be plotted
    NewDate = pd.to_datetime(NewDate,dayfirst=True)
    Dates = dates.date2num(NewDate)

    # Convert data to floats
    for i in range(len(NewVOC)):
        NewVOC[i] = float(NewVOC[i])
    
    years = mdates.YearLocator()   # every year
    otheryears = mdates.YearLocator()  # other years
    years_fmt = mdates.DateFormatter('%Y')

    xfmt = mdates.DateFormatter('%d-%m-%y')

    # Add data to arrays to be plotted
    x.append(Dates)
    y.append(NewVOC)
    
fig, ax = plt.subplots(figsize=(10.5,6))
ax.xaxis.set_major_locator(years)
ax.xaxis.set_major_formatter(years_fmt)
ax.xaxis.set_minor_locator(otheryears)

for i in range(len(x)):
    #plt.plot_date(x[i],y[i],color='blue')
    plt.plot(x[i],y[i],c='#1f77b4')
#fig.autofmt_xdate()
plt.title('Benzene levels in University College London from 1993-2001')
plt.xlabel('Time')
plt.ylabel('Micrograms per metre cubed')
plt.show()

