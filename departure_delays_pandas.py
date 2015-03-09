from dbconnect import *
import mysql.connector
import scipy as sp
import matplotlib.pyplot as plt

config={
    'user':'mbusch',
    'passwd':open("password.txt").readline().rstrip(),
    'database':'insightdb',
    'table':'281486765_T_ONTIME'}

# find the (departure) market with the greatest cancellation rate, and plot

columns=['DEST_CITY_MARKET_ID',
         'ORIGIN_CITY_MARKET_ID',
         'ARR_DELAY',
         'DEP_DELAY']

data = getDFfromDB(columns,config)

cities = list(set(data['ORIGIN_CITY_MARKET_ID']))

rates = []
for city in cities:
    deps = data[data['ORIGIN_CITY_MARKET_ID']==city]
    arrs = data[data['DEST_CITY_MARKET_ID']==city]
    rates.append((city,
                 arrs[arrs['ARR_DELAY'] > 15].ARR_DELAY.values.shape[0]/arrs.shape[0],
                 deps[deps['DEP_DELAY'] > 15].DEP_DELAY.values.shape[0]/deps.shape[0]))

# plot
cityname=getDictA2B("L_CITY_MARKET_ID.csv")
rates = sorted(rates,key=lambda x: -x[2]) # sort descending
rates = rates[:10]
rates.reverse()

key = [cityname[str(int(i[0]))] for i in rates]
arr_delay_rates = [i[1] for i in rates]
dep_delay_rates = [i[2] for i in rates]

fig, ax = plt.subplots()

index = sp.arange(len(rates))
bar_width = 0.35

opacity = 0.4

rects1 = plt.barh(index, arr_delay_rates, bar_width,
                 alpha=opacity,
                 color='b',
                 label='Arrival Delay')

rects2 = plt.barh(index + bar_width, dep_delay_rates, bar_width,
                 alpha=opacity,
                 color='r',
                 label='Departure Delay')

plt.xlabel('Delays Per Flights')
plt.ylabel('Cities')
plt.title('Expected Delay Rate')
plt.yticks(index + bar_width, key)
plt.legend(loc='center left', bbox_to_anchor=(0.5, 0.2)).draggable()
plt.tight_layout()
#plt.savefig('Delay_Rate.pdf')
plt.show()
