from numpy import unique
from numpy import where
from sklearn.datasets import make_classification
from sklearn.cluster import MeanShift
from sklearn import cluster as models
from matplotlib import pyplot
from riotwatcher import LolWatcher, ApiError
import pyodbc
import json
import statistics

#Make clusters of users based on mastery points and add to access table

api_key = ''
watcher = LolWatcher(api_key)
my_region = 'euw1'

conn = pyodbc.connect(r'Driver={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=C:\Users\...\testapi.accdb;')
cursor = conn.cursor()
cursor.execute('select * from Summoners')

latest = watcher.data_dragon.versions_for_region(my_region)['n']['champion']

static_champ_list = watcher.data_dragon.champions(latest, False, 'en_US')

# champ static list data to dict for looking up
champ_dict = {}
for key in static_champ_list['data']:
    row = static_champ_list['data'][key]
    champ_dict[row['key']] = row['id']



cleanUp = cursor.fetchall()
cleanedUp = list()
for i, clean in enumerate(cleanUp):
    cleanedUp.append(list(clean[2:]))

# define dataset
#X, _ = make_classification(n_samples=1000, n_features=2, n_informative=2, n_redundant=0, n_clusters_per_class=1, random_state=4)

X = list(cleanedUp)
#X = X[:100]
#print(type(X))
#print(type(X[0]))
#print(len(X[0]))
# define the model
#model = MeanShift()
model = models.Birch(threshold=0.01, n_clusters=2000)
# fit model and predict clusters
yhat = model.fit_predict(X)
# retrieve unique clusters
clusters = unique(yhat)
# create scatter plot for samples from each cluster
#print(yhat)
#print(len(yhat))
print(clusters)
temp = list()

for i, cluster in enumerate(clusters):
    row_ix = where(yhat == cluster)
    #print(row_ix)
    if len(row_ix[0]) > 2:
        print(row_ix[0])
        temp.append(len(row_ix[0]))
        results = [0] * 155
        for row in row_ix[0]:
            results = map(lambda x, y: x + y, results, X[row])

        results = map(lambda x: x / len(row_ix[0]), results)
        results = list(results)
        resultsString = ""
        #print(len(results))
        for x in results:
            resultsString = resultsString + (str(x) + ", ")
        resultsString = resultsString[:-2]
        #print(resultsString)
        #print("insert into Clusters values (" + str(i) + ", " + resultsString + ")")
        cursor.execute("insert into Clusters values (" + str(i) + ", " + resultsString + ")")
        conn.commit()

    #create scatter of these samples
    #pyplot.scatter(X[row_ix, 0], X[row_ix, 1])
    #pyplot.scatter(X[row_ix[0]][0], X[row_ix[0]][1])
#show the plot
#pyplot.show()

print("Mean:")
print(statistics.mean(temp))
print("Median:")
print(statistics.median(temp))
#print("Mode:")
#print(statistics.mode(temp))
print("stdev:")
print(statistics.stdev(temp))
