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

# Create empty lists
Avg93,Avg94,Avg95,Avg96,Avg97,Avg98,Avg99,Avg00 = ([] for i in range(8))

# Create array of lists of each of the years
MonthlyAverages = [Avg93,Avg94,Avg95,Avg96,Avg97,Avg98,Avg99,Avg00]

for i in range(len(datasets)):

    Date = datasets[i]['Date']

    voc = datasets[i].iloc[:,2]

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

# Insert NaN into missing Jan in Avg93
MonthlyAverages[0][0] = MonthlyAverages[0][0].reset_index(drop=True)
MonthlyAverages[0][0].index = MonthlyAverages[0][0].index + 1  
MonthlyAverages[0][0] = pd.concat([pd.Series([np.NaN]), MonthlyAverages[0][0]])

# Calculate total monthly average for each month over the years 1998-2019
y=[]
for m in range(12):
    y.append(np.nanmean(np.dstack((MonthlyAverages[0][0][m],MonthlyAverages[1][0][m]\
                                   ,MonthlyAverages[2][0][m],MonthlyAverages[3][0][m]\
                                   ,MonthlyAverages[4][0][m],MonthlyAverages[5][0][m]\
                                   ,MonthlyAverages[6][0][m],MonthlyAverages[7][0][m])),2))         

    # Convert the averages to floats
    y[m]=np.float(y[m])

x = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul','Aug', 'Sep', 'Oct', 'Nov', 'Dec']

# Plot a bar chart
fig, ax = plt.subplots(figsize=(10.5,6))
plt.bar(x,y,color='#1f77b4')
plt.title('Average benzene levels per month in University College London from 1993-2001')
plt.xlabel('Months')
plt.ylabel('Micrograms per metre cubed')
plt.show()
