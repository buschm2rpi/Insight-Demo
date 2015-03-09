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

rows = getColumnItems(columns,config)

#sp.save('rows',rows)
#rows=sp.load('rows.npy')

uniqueCities=list(set([i[1] for i in rows]))

rows = sp.array(rows)
rows = rows[:,1:]

rates = []
for city in uniqueCities:
    arr_city_mask = rows[:,0]==city
    dep_city_mask = rows[:,1]==city
    arr_delay_mask = rows[:,2]>15
    dep_delay_mask = rows[:,3]>15
    rates.append((city, 
                 sp.sum(arr_city_mask*arr_delay_mask)/sp.sum(arr_city_mask), 
                 sp.sum(dep_city_mask*dep_delay_mask)/sp.sum(dep_city_mask)))

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

# find the (departure) airport with the greatest cancellation rate, and plot

# find the (departure) airport with the greatest expected delay

# find the (arrival) airport with the greatest expected delay

# factors that may cause delays/cancellations: previous delays en route, carrier, source airport, source market, distance, day of week, month

## how are causes of delay related to day of week or month

## naive bayes: can we predict which market a delay/cancellation occurred at, if given the carrier, day of week, month

# if we know the average price per flight, what are expected losses?

# length of delay wrt. cause of delay

## random forrests, neural networks, naive-bayes

## clustering with ordinal parameters, perhaps condition these runs based on the categorical variables

## svd on relationships between flight time, taxi time, dep/arr delay length

