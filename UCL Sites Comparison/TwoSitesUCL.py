import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as dates
from datetime import datetime,timedelta
import matplotlib.dates as mdates
from scipy import stats
from sklearn.linear_model import LinearRegression

# Handle date time conversions between pandas and matplotlib
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

# Read the data
dbm = pd.read_csv(r'./2000 M.csv')
dbucl = pd.read_csv(r'./2000 UCL.csv')

# Create empty lists
UCL_Avg19, Marylebone_Avg19 = ([] for i in range(2))

# Create array of lists of each of the sites
val = []

Date = dbm['Date']

# Benzene at London Marylebone road
vocM = dbm.iloc[:,2]

# Benzene at UCL
vocUCL = dbucl.iloc[:,2]

VOCList = [vocM,vocUCL]

for i in range(len(VOCList)):
    voc = VOCList[i].reset_index(drop=True)

    # Replace No data with NaN
    NewVOC = voc.replace('No data',np.NaN)

    # Convert dates to format that can be plotted
    NewDate = pd.to_datetime(Date,dayfirst=True)
    Dates = dates.date2num(NewDate)

    # Convert data to floats
    for j in range(len(NewVOC)):
        NewVOC[j] = float(NewVOC[j])   

    # Add data to arrays to be plotted
    val.append(NewVOC)

# Loop to create date range with hours
def datetime_range(start, end, delta):
    current = start
    if not isinstance(delta, timedelta):
        delta = timedelta(**delta)
    while current < end:
        yield current
        current += delta

start = datetime(2000,1,1,0,0,0)
end = datetime(2000,12,31,23,59,59)

List=[]
for dt in datetime_range(start, end, {'hours':1}):
    dt = dates.date2num(dt)
    List.append(dt)
    
fig, ax = plt.subplots(figsize=(10.5,6))

months = mdates.MonthLocator() # every month
days = mdates.DayLocator()
months_fmt = mdates.DateFormatter('%b')

ax.xaxis.set_major_locator(months)
ax.xaxis.set_major_formatter(months_fmt)
ax.xaxis.set_minor_locator(days)

plt.plot(List,val[0],c='#1f77b4',label='Marylebone Road London') #m
plt.plot(List,val[1], c = 'r',label='University College London') #ucl
plt.title('Benzene levels on Marylebone Road London and University College London in 2000')
plt.xlabel('Time')
plt.ylabel('Micrograms per metre cubed')
ax.legend()
plt.show()

# Set the range of the time period
start_ind = 2952
end_ind = 3026

# Benzene in London Marylebone road for time period
MayM =val[0][start_ind:end_ind]

# Benzene in London UCL for time period
MayUCL = val[1][start_ind:end_ind]

hours = mdates.HourLocator()
months = mdates.MonthLocator()
days = mdates.DayLocator()
days_fmt = mdates.DateFormatter('%d %b')

fig, ax = plt.subplots(figsize=(10.5,6))

ax.xaxis.set_major_locator(days)
ax.xaxis.set_major_formatter(days_fmt)
ax.xaxis.set_minor_locator(hours)

plt.plot(List[start_ind:end_ind],MayM,c='#1f77b4',label='Marylebone Road London')
plt.plot(List[start_ind:end_ind],MayUCL, c = 'r',label='University College London')
plt.title('Benzene levels on Marylebone Road London and University College London in May 2000',fontweight="bold")
plt.xlabel('Time')
plt.ylabel('Micrograms per metre cubed')
ax.legend()
plt.show()

M_data = np.array(val[0])
UCL_data = np.array(val[1])
Error = []

# Edit the start index to account for T
start_ind = start_ind+3

for T in range(0, 4): # Looping over T=0,1,2,3
    #Compute L2 norm of distance between vectors
    E = np.linalg.norm(M_data[start_ind:end_ind] - UCL_data[start_ind-T:end_ind-T])
    #Normalise to number of data points - "Error per data pt"
    E = E/(end_ind-start_ind)
    Error.append(E)
    print('Error at time diff ' + str(T) + ' is ' + str(E) + '\n')

start_ind = start_ind-3

TransformError = []
Xvals = []
Yvals =[]
Ynewvals = []
Ypredvals = []

for T in range(0, 4):
    start_ind = 2952
    end_ind = 3026
    X = MayUCL.iloc[0:end_ind-start_ind-T].values.reshape(-1, 1)
    Y = MayM.iloc[T:end_ind-start_ind].values.reshape(-1, 1)

    linear_regressor = LinearRegression()  # create object for the class
    linear_regressor.fit(Y,X)  # perform linear regression
    #print(linear_regressor.coef_) #b value
    #print(linear_regressor.intercept_) #a value
    Y_pred = linear_regressor.predict(Y) #new Y values

    newY = linear_regressor.intercept_+linear_regressor.coef_*Y

    #Compute error of transformed data set.
    start_ind = 0
    end_ind = len(X)
    #Compute L2 norm between two vectors
    E = np.linalg.norm(X[start_ind:end_ind] - newY[start_ind:end_ind])
    #Normalise for number of data sets.
    E = E/(end_ind-start_ind)
    print('Error betweeen Marylebone and transformed UCL at time ' +str(T) + ' is '+ str(E))

    TransformError = TransformError + [E]
    Xvals = Xvals + [X]
    Yvals = Yvals + [Y]
    Ynewvals = Ynewvals + [newY]
    Ypredvals = Ypredvals + [Y_pred]


    
# Pick the T with the smallest error
T = TransformError.index(min(TransformError))
#T = 1

# Reset the start index
start_ind = 2952
end_ind = 3026

fig, ax = plt.subplots(figsize=(10.5,6))
#plotting line of best fit
plt.scatter(Yvals[T], Xvals[T])
plt.plot(Yvals[T], Ypredvals[T], color='red')
plt.title('Correlation between benzene levels on Marylebone Road London and University College London in May 2000')
plt.xlabel('Marylebone Road London (micrograms per metre cubed)')
plt.ylabel('University College London (micrograms per metre cubed)')
plt.show()

#newY = linear_regressor.intercept_+linear_regressor.coef_*X

#Plotting new transformed Marylebone
fig, ax = plt.subplots(figsize=(10.5,6))

ax.xaxis.set_major_locator(days)
ax.xaxis.set_major_formatter(days_fmt)
ax.xaxis.set_minor_locator(hours)

plt.plot(List[start_ind+T:end_ind],Ynewvals[T], c = '#1f77b4',label='Marylebone Road London')
plt.plot(List[start_ind+T:end_ind],Xvals[T],c='r',label='University College London')
plt.title('Benzene levels on University College London and the time-shift \n transform applied to Marylebone Road in May 2000',fontweight="bold")
plt.xlabel('Time')
plt.ylabel('Micrograms per metre cubed')
ax.legend()
plt.show()



