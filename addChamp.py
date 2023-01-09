from riotwatcher import LolWatcher, ApiError
import pyodbc
import json
import sys

#Add each champ to a access tabke
conn = pyodbc.connect(r'Driver={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=C:\Users\...\testapi.accdb;')
cursor = conn.cursor()
cursor.execute('select * from Summoners')

api_key = ''
watcher = LolWatcher(api_key)
my_region = 'euw1'



latest = watcher.data_dragon.versions_for_region(my_region)['n']['champion']

static_champ_list = watcher.data_dragon.champions(latest, False, 'en_US')

champ_dict = {}
for key in static_champ_list['data']:
    row = static_champ_list['data'][key]
    champ_dict[row['key']] = row['id']

for champion in champ_dict:
    print(champ_dict[champion])
    print('Alter table clusters add ' + str(champ_dict[champion]) + ' int NOT NULL;')
    cursor.execute('Alter table clusters add ' + str(champ_dict[champion]) + ' int NOT NULL;')


conn.commit()
