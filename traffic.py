import pandas
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import math

data = pandas.read_csv("Location_data1.csv")
df={}
min_Crash={}
max_Crash={}
mean_Crash={}
median_Crash={}
std_Crash={}

crash_Count={}
casualty_Count={}
pdo_count={}

percent_casualty={}
percent_pdo={}
max_location={}
std_Casualty={}
std_pdo={}

for x in range(2009,2014):
    df["data_{0}".format(x)]= data[data['Year'] == x]
    min_Crash["min_Crash_{0}".format(x)]= np.amin(df["data_{0}".format(x)]['CrashCount'])
    max_Crash["max_Crash_{0}".format(x)]= np.amax(df["data_{0}".format(x)]['CrashCount'])
    mean_Crash["mean_Crash_{0}".format(x)]= round(np.mean(df["data_{0}".format(x)]['CrashCount']), 2)
    median_Crash["median_Crash_{0}".format(x)]= round(np.median(df["data_{0}".format(x)]['CrashCount']), 2)
    std_Crash["std_Crash_{0}".format(x)]= round(np.std(df["data_{0}".format(x)]['CrashCount']), 2)

    crash_Count["crash_Count_{0}".format(x)] = df["data_{0}".format(x)]['CrashCount'].sum()
    casualty_Count["casualty_Count_{0}".format(x)] = \
        df["data_{0}".format(x)].loc[df["data_{0}".format(x)]['CrashType'].str.contains('Casualty')]['CrashCount'].sum()
    pdo_count["pdo_count_{0}".format(x)] = \
        df["data_{0}".format(x)].loc[df["data_{0}".format(x)]['CrashType'].str.contains('PDO')]['CrashCount'].sum()
    std_Casualty["std_Casualty_{0}".format(x)] = \
        round(np.std(df["data_{0}".format(x)].loc[df["data_{0}".format(x)]['CrashType'].str.contains('Casualty')]['CrashCount']), 2)
    std_pdo["std_pdo_{0}".format(x)] = \
        round(np.std(df["data_{0}".format(x)].loc[df["data_{0}".format(x)]['CrashType'].str.contains('pdo')]['CrashCount']), 2)


    percent_casualty["percent_casualty_{0}".format(x)] = \
        round(float(df["data_{0}".format(x)].loc[df["data_{0}".format(x)]['CrashType'].str.contains('Casualty')]['CrashCount'].sum())/\
        df["data_{0}".format(x)]['CrashCount'].sum()*100, 2)
    percent_pdo["percent_pdo_{0}".format(x)] = \
        round(float(df["data_{0}".format(x)].loc[df["data_{0}".format(x)]['CrashType'].str.contains('PDO')]['CrashCount'].sum())/\
        df["data_{0}".format(x)]['CrashCount'].sum()*100, 2)
    max_location["max_location_{0}".format(x)] = df["data_{0}".format(x)].loc[df["data_{0}".format(x)]\
        ['CrashCount'].idxmax()]['Location']



###### Pie Chart with Casualties and PDO #####
###### Refercence: http://matplotlib.org/examples/pie_and_polar_charts/pie_demo_features.html
for x in range(2009, 2014):
    labels = 'Casualties', 'PDO'
    sizes = [percent_casualty["percent_casualty_{0}".format(x)], percent_pdo["percent_pdo_{0}".format(x)]]
    colors = ['red', 'yellow']
    explode = (0.1, 0)  # only "explode" the 1st slice (i.e. 'Fatalities')
    plt.pie(sizes, explode=explode, labels=labels, colors=colors,
            autopct='%1.1f%%', shadow=True, startangle=90)
            # Set aspect ratio to be equal so that pie is drawn as a circle.
    plt.axis('equal')

    total = mpatches.Patch(color='black', label='Total Accidents: ' + str(crash_Count["crash_Count_{0}".format(x)]))
    cas = mpatches.Patch(color='red', label='Casualties: ' + str(casualty_Count["casualty_Count_{0}".format(x)]))
    pdo = mpatches.Patch(color='yellow', label='PDO: ' + str(pdo_count["pdo_count_{0}".format(x)]))

    first = plt.legend(handles=[total], loc=1)
    ax = plt.gca().add_artist(first)
    second = plt.legend(handles=[cas], loc=2)
    ax = plt.gca().add_artist(second)
    third = plt.legend(handles=[pdo], loc=4)

    plt.suptitle('Crash Data {0}'.format(x), fontsize=14, fontweight='bold')
    plt.show()

###### Stacked Bar Chart #####
###### Refercence: http://matplotlib.org/examples/pylab_examples/bar_stacked.html
N = 5
casualties = (casualty_Count['casualty_Count_2009'], \
    casualty_Count['casualty_Count_2010'], casualty_Count['casualty_Count_2011'], \
    casualty_Count['casualty_Count_2012'], casualty_Count['casualty_Count_2013'])
pdo = (pdo_count['pdo_count_2009'], \
    pdo_count['pdo_count_2010'], pdo_count['pdo_count_2011'], \
    pdo_count['pdo_count_2012'], pdo_count['pdo_count_2013'])
casualtySTD = (std_Casualty['std_Casualty_2009'], \
    std_Casualty['std_Casualty_2010'], std_Casualty['std_Casualty_2011'], \
    std_Casualty['std_Casualty_2012'], std_Casualty['std_Casualty_2013'])
pdoSTD = (std_pdo['std_pdo_2009'], \
    std_pdo['std_pdo_2010'], std_pdo['std_pdo_2011'], \
    std_pdo['std_pdo_2012'], std_pdo['std_pdo_2013'])
ind = np.arange(N)    # the x locations for the groups
width = 0.35       # the width of the bars: can also be len(x) sequence

p1 = plt.bar(ind, pdo, width, color='y', yerr=pdoSTD)
p2 = plt.bar(ind, casualties, width, color='r',
             bottom=pdo, yerr=casualtySTD)

plt.ylabel('Number of Crashes')
plt.title('Crash Breakdown by Year')
plt.xticks(ind + width/2., ('2009', '20010', '2011', '2012', '2013'))
plt.yticks(np.arange(0, 25000, 1000))
plt.legend((p1[0], p2[0]), ('PDO', 'Casualties'), loc = 4)

plt.show()
