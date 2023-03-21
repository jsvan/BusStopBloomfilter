'curl -X GET --header "Accept: application/json" --header "Authorization: Bearer  8dfc4d27587b1addbd6aae85884501e2" "https://api.deutschebahn.com/freeplan/v1/location/b"'

"""
Can curl every location by going through German alphabet
https://api.deutschebahn.com/freeplan/v1/location/b
"""

import requests
dealpha = "A, B, C, D, E, F, G, H, I, J, K, L, M, N, O, P, Q, R, S, T, U, V, W, X, Y, Z, Ä, Ö, Ü, ß".lower().split(', ')

"""
GET ALL STOPS
"""
allstations = dict()
for letter in dealpha:
    try:
        r = requests.get(f'https://api.deutschebahn.com/freeplan/v1/location/{letter}', params={"Accept": "application/json", "Authorization": "Bearer  8dfc4d27587b1addbd6aae85884501e2"})
        rj = r.json()
        print(rj[0])
        # [{'name': 'Berlin Hbf', 'lon': 13.369549, 'lat': 52.525589, 'id': 8011160},
        #  {'name': 'Bielefeld Hbf', 'lon': 8.532723, 'lat': 52.029259, 'id': 8000036},
        #   ... ]
        for stop in rj:
            allstations[stop['id']] = stop['name']
    except Exception as e:
        print(e, e.__doc__)



"""
GET ALL TIME TABLES
"""
alltimetables = dict()
alltrains = dict()
for station_id in allstations.keys():
    try:
        alltimetables[station_id] = dict()
        r = requests.get(f'https://api.deutschebahn.com/freeplan/v1/departureBoard/{station_id}?date=2022-01-15', params={"Accept": "application/json", "Authorization": "Bearer  8dfc4d27587b1addbd6aae85884501e2"})
        rj = r.json()

        for train in rj:
            n = train['name']
            if train['track'] not in alltimetables[station_id]:
                alltimetables[station_id][train['track']] = []

            alltimetables[station_id][train['track']].append(n)
            if n not in alltrains:
                alltrains[n] = []

            alltrains[n].append(station_id)

    except Exception as e:
        print(e, e.__doc__)

"""  
  {
    "name": "ICE 618",
    "type": "ICE",
    "boardId": 8000105,
    "stopId": 8000105,
    "stopName": "Frankfurt&#x0028;Main&#x0029;Hbf",
    "dateTime": "2022-01-15T04:46",
    "track": "19",
    "detailsId": "594015%2F200777%2F989772%2F296881%2F80%3fstation_evaId%3D8000105"
  },
  {
    "name": "ICE 827",
    "type": "ICE",
    "boardId": 8000105,
    "stopId": 8000105,
    "stopName": "Frankfurt&#x0028;Main&#x0029;Hbf",
    "dateTime": "2022-01-15T04:54",
    "track": "7",
    "detailsId": "982503%2F330968%2F696966%2F20982%2F80%3fstation_evaId%3D8000105"
  },
"""



import pickle
print('dumping')
with open("./pickles/allstations.pkl", 'wb') as F:
    pickle.dump(allstations, F)

with open("./pickles/alltimetables.pkl", 'wb') as F:
    pickle.dump(alltimetables, F)

with open("./pickles/alltrains.pkl", 'wb') as F:
    pickle.dump(alltrains, F)
print('dumped')


print(alltrains)
input()
print(alltimetables)
input()
print(allstations)
