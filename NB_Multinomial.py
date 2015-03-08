from dbconnect import *
import scipy as sp
from sklearn.naive_bayes import MultinomialNB
from time import time
import matplotlib.pyplot as plt
from sklearn.cross_validation import train_test_split
from sklearn.metrics import confusion_matrix

#############################

def getFeatureVec(row,carriers):
    vec=[]

    # AIRLINE_ID
    feature = [0 for i in range(len(carriers))]
    feature[carriers[str(int(row[0]))]]=1
    vec.extend(feature)

    # DAY_OF_WEEK
    feature = [0 for i in range(7)]
    feature[int(row[1])-1]=1
    vec.extend(feature)

    # types of delays
    vec.extend(row[2:])

    return sp.array(vec)

#############################

config={
    'user':'mbusch',
    'passwd':open("password.txt").readline().rstrip(),
    'database':'insightdb',
    'table':'281486765_T_ONTIME'}

allCarriers = getDictA2B('L_AIRLINE_ID.csv')
allMarkets = getDictA2B('L_CITY_MARKET_ID.csv')

# Use Naive-Bayes approach to classify airport based on...
'''
# pull data from DB
tstart=time()

columns=['ORIGIN_CITY_MARKET_ID',
         'AIRLINE_ID',
         'DAY_OF_WEEK',
         'CARRIER_DELAY',
         'WEATHER_DELAY',
         'NAS_DELAY',
         'SECURITY_DELAY',
         'LATE_AIRCRAFT_DELAY',
         'TAXI_OUT',
         'TAXI_IN']

rows = getColumnItems(columns,config)
rows = sp.array(rows)
city = rows[:,1]
rows = rows[:,2:10]

# use the cities found in factors.py
origin_cities=set([31123.0, 34819.0, 32474.0, 30325.0, 35356.0, 30977.0, 33459.0, 30165.0, 32320.0, 33076.0])
mCity=sp.zeros(city.shape)
mRow=sp.zeros(rows.shape)
k=0
for i in range(len(city)):
    if city[i] in origin_cities:
        mCity[k]=city[i]
        mRow[k,:]=rows[i,:]
        k=k+1

city=mCity[:k]
rows=mRow[:k]

print('Finished pulling data. Time taken: {0:.2f} sec.'.format(time()-tstart))

# map carrier to a feature ID
uniqueCarriers = list(set(rows[:,0].tolist()))
uniqueCarriers.sort()
carriers = {str(int(uniqueCarriers[c])):c for c in range(len(uniqueCarriers))}

# construct feature matrix
tstart=time()
X=sp.zeros((rows.shape[0],len(carriers)+7+(rows.shape[1]-2)))
y=sp.zeros(rows.shape[0])
for i in range(rows.shape[0]):
    X[i,:]=getFeatureVec(rows[i,:],carriers)
    y[i]=city[i]

print('Finished Constructing feature matrix. Time taken: {0:.2f} sec.'.format(time()-tstart))

sp.save('X.npy',X)
sp.save('y.npy',y)
'''
X=sp.load('X.npy')
y=sp.load('y.npy')


# Do the NB classifier

X_train, X_test, y_train, y_test = train_test_split(X, y, train_size=0.9, random_state=0)

tstart=time()
clf = MultinomialNB()
clf.fit(X_train, y_train)
print('Finished computing NB classifier. Time taken: {0:.2f} sec.'.format(time()-tstart))

# Compute confusion matrix
labels=list(set(y_train.tolist()))
nameLabels=[allMarkets[str(int(i))] for i in labels]
cm = confusion_matrix(y_test, clf.predict(X_test),labels)

print(cm)

# Show confusion matrix in a separate window
fig = plt.figure()
axes = fig.add_subplot(111)
cax = axes.matshow(cm)
plt.title('Confusion matrix')
plt.colorbar(cax)
plt.ylabel('True label')
plt.xlabel('Predicted label')

#axes.set_yticklabels([''] + [allMarkets[str(int(i))] for i in labels])
i = range(len(labels))
axes.xaxis.set_tick_params(labelbottom='on',labeltop='off')
axes.set(xticks=i, xticklabels=nameLabels, yticks=i, yticklabels=nameLabels)
plt.xticks(rotation='vertical')
plt.show()
