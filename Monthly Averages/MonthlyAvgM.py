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
db97 = pd.read_csv(r'/Users/Henry/Desktop/1997 VOC data.csv')
db98 = pd.read_csv(r'/Users/Henry/Desktop/1998 VOC data.csv')
db99 = pd.read_csv(r'/Users/Henry/Desktop/1999 VOC data.csv')
db00 = pd.read_csv(r'/Users/Henry/Desktop/2000 VOC data.csv')
db01 = pd.read_csv(r'/Users/Henry/Desktop/2001 VOC data.csv')
db02 = pd.read_csv(r'/Users/Henry/Desktop/2002 VOC data.csv')
db03 = pd.read_csv(r'/Users/Henry/Desktop/2003 VOC data.csv')
db04 = pd.read_csv(r'/Users/Henry/Desktop/2004 VOC data.csv')
db05 = pd.read_csv(r'/Users/Henry/Desktop/2005 VOC data.csv')
db06 = pd.read_csv(r'/Users/Henry/Desktop/2006 VOC data.csv')
db07 = pd.read_csv(r'/Users/Henry/Desktop/2007 VOC data.csv')
db08 = pd.read_csv(r'/Users/Henry/Desktop/2008 VOC data.csv')
db09 = pd.read_csv(r'/Users/Henry/Desktop/2009 VOC data.csv')
db11 = pd.read_csv(r'/Users/Henry/Desktop/2011 VOC data.csv')
db12 = pd.read_csv(r'/Users/Henry/Desktop/2012 VOC data.csv')
db13 = pd.read_csv(r'/Users/Henry/Desktop/2013 VOC data.csv')
db14 = pd.read_csv(r'/Users/Henry/Desktop/2014 VOC data.csv')
db15 = pd.read_csv(r'/Users/Henry/Desktop/2015 VOC data.csv')
db17 = pd.read_csv(r'/Users/Henry/Desktop/2017 VOC data.csv')
db18 = pd.read_csv(r'/Users/Henry/Desktop/2018 VOC data.csv')
db19 = pd.read_csv(r'/Users/Henry/Desktop/2019 VOC data.csv')

datasets = [db97,db98,db99,db00,db01,db02,db03,db04,db05,db06,db07,db08,db09,db11,db12,db13,db14,db15,db17,db18,db19]
x=[]
y=[]

# Create empty lists
Avg97,Avg98,Avg99,Avg00,Avg01,Avg02,Avg03,\
Avg04,Avg05,Avg06,Avg07,Avg08,Avg09,Avg11,Avg12,Avg13,Avg14,\
Avg15,Avg17,Avg18,Avg19 = ([] for i in range(21))

# Create array of lists of each of the years
MonthlyAverages = [Avg97,Avg98,Avg99,Avg00,Avg01,Avg02,Avg03,
Avg04,Avg05,Avg06,Avg07,Avg08,Avg09,Avg11,Avg12,Avg13,Avg14,
Avg15,Avg17,Avg18,Avg19]

for i in range(len(datasets)):

    Date = datasets[i]['Date']

    voc = datasets[i].iloc[:,170]

    # Replace No data with NaN
    NewVOC = voc.replace('No data',np.NaN)

    # Convert dates to format that can be plotted
    NewDate = pd.to_datetime(Date,dayfirst=True)
    Dates = dates.date2num(NewDate)

    # Convert data to floats
    for j in range(len(NewVOC)):
        NewVOC[j] = float(NewVOC[j])   

    # Set the indices as the date
    NewVOC.index = NewDate
    NewVOC = pd.to_numeric(NewVOC)

    # Calculate the monthly averages for each year
    MonthAvg = NewVOC.resample('M').mean()

    # Add the monthly averages to the corresponding year
    MonthlyAverages[i].append(MonthAvg)
    
# Calculate total monthly average for each month over the years 1998-2019
y=[]
for m in range(12):
    y.append(np.nanmean(np.dstack((MonthlyAverages[0][0][m],MonthlyAverages[1][0][m]\
                                   ,MonthlyAverages[2][0][m],MonthlyAverages[3][0][m]\
                                   ,MonthlyAverages[4][0][m],MonthlyAverages[5][0][m]\
                                   ,MonthlyAverages[6][0][m],MonthlyAverages[7][0][m]\
                                   ,MonthlyAverages[8][0][m],MonthlyAverages[9][0][m]\
                                   ,MonthlyAverages[10][0][m],MonthlyAverages[11][0][m]\
                                   ,MonthlyAverages[12][0][m],MonthlyAverages[13][0][m]\
                                   ,MonthlyAverages[14][0][m],MonthlyAverages[15][0][m]\
                                   ,MonthlyAverages[16][0][m],MonthlyAverages[17][0][m]\
                                   ,MonthlyAverages[18][0][m],MonthlyAverages[19][0][m]\
                                   ,MonthlyAverages[20][0][m])),2))         

    # Convert the averages to floats
    y[m]=np.float(y[m])

x = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul','Aug', 'Sep', 'Oct', 'Nov', 'Dec']

# Plot a bar chart
fig, ax = plt.subplots(figsize=(10.5,6))
plt.bar(x,y,color='#1f77b4')
plt.title('Average benzene levels per month on Marylebone Road London from 1997-2020')
plt.xlabel('Months')
plt.ylabel('Micrograms per metre cubed')
plt.show()
