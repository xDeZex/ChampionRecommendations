from riotwatcher import LolWatcher, ApiError
import pyodbc
import json

#Add mastery for each user for each champ to access table
watcher = LolWatcher('')

my_region = 'euw1'
regions = ['euw1', 'kr', 'na1']
regionIndex = 0

#summoners = watcher.league.entries(my_region, 'RANKED_SOLO_5x5', 'DIAMOND', 'I', 1)
#print(summoners[0])

conn = pyodbc.connect(r'Driver={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=C:\Users\...\testapi.accdb;')
cursor = conn.cursor()
cursor.execute('select * from Summoners')

latest = watcher.data_dragon.versions_for_region(my_region)['n']['champion']

static_champ_list = watcher.data_dragon.champions(latest, False, 'en_US')

champ_dict = {}
for key in static_champ_list['data']:
    row = static_champ_list['data'][key]
    if row['id'] != "Akshan":
        champ_dict[row['key']] = row['id']


#for s in cursor.fetchall():

    #print(s[0])
test = cursor.fetchall()
for i, summoner in enumerate(test):
    if sum(summoner[2:]) != 0:
        continue
    print(i)
    ID = summoner[0]
    notDone = True
    while notDone:
        try:
            champions = watcher.champion_mastery.by_summoner(regions[regionIndex], summoner[1])
            if len(champions) == 0:
                raise NameError("Could not find user in searched region")
            notDone = False
        except:
            regionIndex = (regionIndex + 1) % 3
            print(str(regionIndex) + " region")
    for champion in champions:
        champID = champion['championId']


        #print(champion)

        champMastery = champion['championPoints']
        #print('update summoners set ' + str(champ_dict[str(champID)]) + ' = ' + str(champMastery) + " where ID = '" + ID + "';")
        if champID != 166:
            cursor.execute('update summoners set ' + str(champ_dict[str(champID)]) + ' = ' + str(champMastery) + " where ID = '" + ID + "';")
    conn.commit()
conn.commit()
