from numpy import unique
from numpy import where
from numpy import linalg
import numpy as np
from sklearn.datasets import make_classification
from sklearn.cluster import MeanShift
from matplotlib import pyplot
from riotwatcher import LolWatcher, ApiError
import pyodbc
import json
import statistics

#Test the created clusters based on seperated test users

api_key = ''
watcher = LolWatcher(api_key)
my_region = 'euw1'

conn = pyodbc.connect(r'Driver={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=C:\Users\...\testapi.accdb;')
cursor = conn.cursor()
cursor.execute('select * from Clusters')

latest = watcher.data_dragon.versions_for_region(my_region)['n']['champion']

static_champ_list = watcher.data_dragon.champions(latest, False, 'en_US')


champ_dict = {}
for key in static_champ_list['data']:
    row = static_champ_list['data'][key]
    if row['id'] != "Akshan":
        champ_dict[row['key']] = row['id']

#me = watcher.summoner.by_name(my_region, "Frassefrass")
#print(me)
#champMastery = watcher.champion_mastery.by_summoner(my_region, me['id'])


clusters = cursor.fetchall()


cursor.execute('select * from TestSummoners')

Summoners = cursor.fetchall()

distanceList = list()
for champMastery in Summoners:
    minDist = -1
    minDistIndex = -1
    champMastery = champMastery[2:]
    for i, cluster in enumerate(clusters):
        cluster = list(cluster[1:])
        dist = linalg.norm(np.array(champMastery) - np.array(cluster))
        if minDist == -1:
            minDist = dist
            minDistIndex = i
        elif dist < minDist:
            minDist = dist
            minDistIndex = i
    distanceList.append(minDist)
#print(champMastery)
#print(clusters[minDistIndex])

print("Mean:")
print(statistics.mean(distanceList))
print("Median:")
print(statistics.median(distanceList))
#print("Mode:")
#print(statistics.mode(distanceList))
print("stdev:")
print(statistics.stdev(distanceList))

championNames = ['Aatrox', 'Ahri', 'Akali', 'Alistar', 'Amumu', 'Anivia', 'Annie', 'Aphelios', 'Ashe', 'AurelionSol', 'Azir', 'Bard', 'Blitzcrank', 'Brand', 'Braum', 'Caitlyn', 'Camille', 'Cassiopeia', 'Chogath', 'Corki', 'Darius', 'Diana', 'Draven', 'DrMundo', 'Ekko', 'Elise', 'Evelynn', 'Ezreal', 'Fiddlesticks', 'Fiora', 'Fizz', 'Galio', 'Gangplank', 'Garen', 'Gnar', 'Gragas', 'Graves', 'Gwen', 'Hecarim', 'Heimerdinger', 'Illaoi', 'Irelia', 'Ivern', 'Janna', 'JarvanIV', 'Jax', 'Jayce', 'Jhin', 'Jinx', 'Kaisa', 'Kalista', 'Karma', 'Karthus', 'Kassadin', 'Katarina', 'Kayle', 'Kayn', 'Kennen', 'Khazix', 'Kindred', 'Kled', 'KogMaw', 'Leblanc', 'LeeSin', 'Leona', 'Lillia', 'Lissandra', 'Lucian', 'Lulu', 'Lux', 'Malphite', 'Malzahar', 'Maokai', 'MasterYi', 'MissFortune', 'MonkeyKing', 'Mordekaiser', 'Morgana', 'Nami', 'Nasus', 'Nautilus', 'Neeko', 'Nidalee', 'Nocturne', 'Nunu', 'Olaf', 'Orianna', 'Ornn', 'Pantheon', 'Poppy', 'Pyke', 'Qiyana', 'Quinn', 'Rakan', 'Rammus', 'RekSai', 'Rell', 'Renekton', 'Rengar', 'Riven', 'Rumble', 'Ryze', 'Samira', 'Sejuani', 'Senna', 'Seraphine', 'Sett', 'Shaco', 'Shen', 'Shyvana', 'Singed', 'Sion', 'Sivir', 'Skarner', 'Sona', 'Soraka', 'Swain', 'Sylas', 'Syndra', 'TahmKench', 'Taliyah', 'Talon', 'Taric', 'Teemo', 'Thresh', 'Tristana', 'Trundle', 'Tryndamere', 'TwistedFate', 'Twitch', 'Udyr', 'Urgot', 'Varus', 'Vayne', 'Veigar', 'Velkoz', 'Vi', 'Viego', 'Viktor', 'Vladimir', 'Volibear', 'Warwick', 'Xayah', 'Xerath', 'XinZhao', 'Yasuo', 'Yone', 'Yorick', 'Yuumi', 'Zac', 'Zed', 'Ziggs', 'Zilean', 'Zoe', 'Zyra']

maxMasteryClusterIndex = -1
maxMasteryCluster = -1
distanceList = list()
# for i, name in enumerate(championNames):
#     distanceList.append(champMastery[i] - clusters[minDistIndex][i])
#     if maxMasteryCluster < clusters[minDistIndex][i]:
#         maxMasteryClusterIndex = i
#         maxMasteryCluster = clusters[minDistIndex][i]
#   print(name + " Distance: " + str(champMastery[i] - clusters[minDistIndex][i]) + " Summ: " + str(champMastery[i]) + " Cluster: " + str(clusters[minDistIndex][i]))

#print(championNames[maxMasteryClusterIndex])


#for champ, dist in [(x, y) for y, x in sorted(zip(distanceList, championNames))]:
#   print(champ + " " + str(dist))
