from numpy import unique
from numpy import where
from numpy import linalg
import numpy as np
from riotwatcher import LolWatcher, ApiError
import pyodbc
import json
import sys, os
sys.stdout = open(os.devnull, 'w')


#gets a username and matches it to a cluster, the champion with the biggest difference between the cluster and user gets recommended
def main(name):
    api_key = ''
    watcher = LolWatcher(api_key)
    my_region = 'euw1'

    conn = pyodbc.connect(r'Driver={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=C:\Users\...\testapi.accdb;')
    cursor = conn.cursor()
    cursor.execute('select * from Clusters')
    clusters = cursor.fetchall()
    latest = watcher.data_dragon.versions_for_region(my_region)['n']['champion']

    static_champ_list = watcher.data_dragon.champions(latest, False, 'en_US')

    columns = [column[0] for column in cursor.description][1:]

    champ_dict = {}
    for key in static_champ_list['data']:
        row = static_champ_list['data'][key]
        champ_dict[row['key']] = row['id']

    me = watcher.summoner.by_name(my_region, name)
    #print(me)
    champMastery = watcher.champion_mastery.by_summoner(my_region, me['id'])
    #print(champMastery)
    listofc = []
    for champion in champMastery:
        champID = champion['championId']
        champM = champion['championPoints']
        listofc.append((champ_dict[str(champID)], champM))
        print(champ_dict[str(champID)], champM)

    championNames = ['Aatrox', 'Ahri', 'Akali', 'Alistar', 'Amumu', 'Anivia', 'Annie', 'Aphelios', 'Ashe', 'AurelionSol', 'Azir', 'Bard', 'Blitzcrank', 'Brand', 'Braum', 'Caitlyn', 'Camille', 'Cassiopeia', 'Chogath', 'Corki', 'Darius', 'Diana', 'Draven', 'DrMundo', 'Ekko', 'Elise', 'Evelynn', 'Ezreal', 'Fiddlesticks', 'Fiora', 'Fizz', 'Galio', 'Gangplank', 'Garen', 'Gnar', 'Gragas', 'Graves', 'Gwen', 'Hecarim', 'Heimerdinger', 'Illaoi', 'Irelia', 'Ivern', 'Janna', 'JarvanIV', 'Jax', 'Jayce', 'Jhin', 'Jinx', 'Kaisa', 'Kalista', 'Karma', 'Karthus', 'Kassadin', 'Katarina', 'Kayle', 'Kayn', 'Kennen', 'Khazix', 'Kindred', 'Kled', 'KogMaw', 'Leblanc', 'LeeSin', 'Leona', 'Lillia', 'Lissandra', 'Lucian', 'Lulu', 'Lux', 'Malphite', 'Malzahar', 'Maokai', 'MasterYi', 'MissFortune', 'MonkeyKing', 'Mordekaiser', 'Morgana', 'Nami', 'Nasus', 'Nautilus', 'Neeko', 'Nidalee', 'Nocturne', 'Nunu', 'Olaf', 'Orianna', 'Ornn', 'Pantheon', 'Poppy', 'Pyke', 'Qiyana', 'Quinn', 'Rakan', 'Rammus', 'RekSai', 'Rell', 'Renekton', 'Rengar', 'Riven', 'Rumble', 'Ryze', 'Samira', 'Sejuani', 'Senna', 'Seraphine', 'Sett', 'Shaco', 'Shen', 'Shyvana', 'Singed', 'Sion', 'Sivir', 'Skarner', 'Sona', 'Soraka', 'Swain', 'Sylas', 'Syndra', 'TahmKench', 'Taliyah', 'Talon', 'Taric', 'Teemo', 'Thresh', 'Tristana', 'Trundle', 'Tryndamere', 'TwistedFate', 'Twitch', 'Udyr', 'Urgot', 'Varus', 'Vayne', 'Veigar', 'Velkoz', 'Vi', 'Viego', 'Viktor', 'Vladimir', 'Volibear', 'Warwick', 'Xayah', 'Xerath', 'XinZhao', 'Yasuo', 'Yone', 'Yorick', 'Yuumi', 'Zac', 'Zed', 'Ziggs', 'Zilean', 'Zoe', 'Zyra']
    print(columns)
    for champ in columns:
        if champ not in [x for x, y in listofc]:
                listofc.append((champ, 0))

    listofc = sorted(listofc, key=lambda x: x[0])
    print([x for x, y in listofc])
    print([x for x in [q for q, y in listofc] if x not in columns])
    print([x for x in columns if x not in [q for q, y in listofc]])
    listofc = [x for y, x in listofc if y in columns]
    minDist = -1
    minDistIndex = -1
    champMastery = champMastery[2:]
    for i, cluster in enumerate(clusters):
        cluster = list(cluster[1:])
        dist = linalg.norm(np.array(listofc) - np.array(cluster))
        if minDist == -1:
            minDist = dist
            minDistIndex = i
        elif dist < minDist:
            minDist = dist
            minDistIndex = i


    mevsc = np.array(listofc) - np.array(clusters[minDistIndex][1:])
    min1 = np.where(mevsc == min(mevsc))[0][0]


    print(len(championNames), len(listofc))
    print(championNames[min1], min(mevsc), minDistIndex)
    print(listofc[min1], clusters[minDistIndex][1:][min1])

    sortedC = sorted([(columns[i], x) for i, x in enumerate(mevsc)], key=lambda x: x[1])
    for i, x in sortedC:
        print(i, listofc[championNames.index(i)], x)
    sys.stdout = sys.__stdout__
    return championNames[min1]
