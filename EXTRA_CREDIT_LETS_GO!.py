from collections import Counter
from pymongo import MongoClient
import emoji
import folium
import os
import random

client = MongoClient('localhost', 27017)
db = client['usa_db']
collection = db['usa_tweets_collection']

statedicti = {}

tweets_iterator = collection.find()

for tweet in tweets_iterator:
    for stuff in tweet['text']:
        if stuff in emoji.UNICODE_EMOJI and tweet['place']['full_name'][-2:] != "SA" \
                and 65 <= ord(tweet['place']['full_name'][-1]) <= 90:
            if tweet['place']['full_name'][-2:] not in statedicti:
                statedicti[tweet['place']['full_name'][-2:]] = [stuff]
            else:
                statedicti[tweet['place']['full_name'][-2:]].append(stuff)

for states in statedicti:
    print(str(states) + "   " + str(statedicti[states]))

for emojies2 in statedicti:
    statedicti[emojies2] = Counter(statedicti[emojies2]).most_common(2)

for states in statedicti:
    print(str(states) + "   " + str(statedicti[states]))

massiveannoyingdict = {
    'AL': [32, -86],
    'AK': [64, -152],
    'AZ': [34, -111],
    'AR': [34, -92],
    'CA': [37, -119],
    'CO': [38, -105],
    'CT': [41, -72],
    'DE': [38, -75],
    'FL': [28, -82],
    'GA': [32, -83],
    'HI': [20, -156],
    'ID': [44, -114],
    'IL': [40, -89],
    'IN': [39, -86],
    'IA': [42, -93],
    'KS': [38, -98],
    'KY': [37, -85],
    'LA': [31, -91.99],
    'ME': [45, -69],
    'MD': [39, -76],
    'MA': [42, -71.8],
    'MI': [44, -85],
    'MN': [46, -94],
    'MS': [32, -89],
    'MO': [38, -92],
    'MT': [47, -109],
    'NE': [41, -99],
    'NV': [39, -116],
    'NH': [43.6, -71.5],
    'NJ': [40.19, -74.67],
    'NM': [34.4, -106],
    'NY': [42.9, -75.5],
    'NC': [35.55, -79],
    'ND': [47, -100],
    'OH': [40.2, -82.7],
    'OK': [35.5, -97.49],
    'OR': [43.9, -120.5],
    'PA': [40.87, -77.799],
    'RI': [41.67, -71.55],
    'SC': [33.991, -80.89],
    'SD': [44.44, -100.23],
    'TN': [35.85, -86.35],
    'TX': [31.47, -99.33],
    'UT': [39.30, -111.67],
    'VT': [44.06, -72.66],
    'VA': [37.52, -78.85],
    'WA': [47.38, -120],
    'WV': [38.64, -80.622],
    'WI': [44.62, -89.99],
    'WY': [42.99, -107.55]
}


dir_path = os.path.dirname(os.path.abspath(__file__))
filenamemap = os.path.join(dir_path, "mapemoji.html")
colors = ['green', 'red', 'orange', 'purple']

map_osm = folium.Map(location=[39, -98.1], zoom_start=4)

for states in massiveannoyingdict:
    if states not in statedicti:
        folium.Marker(massiveannoyingdict[states], popup=(str(states) + ": No Emoji Tweets from this State!"), icon=folium.Icon(color='black', icon='cloud')).add_to(map_osm)
    else:
        try:
            folium.Marker(massiveannoyingdict[states],
                      popup=(str(states) + ": " + str(statedicti[states][0][0]) + str(statedicti[states][1][0])), icon=folium.Icon(color=random.choice(colors))).add_to(map_osm)
        except IndexError:
            folium.Marker(massiveannoyingdict[states],
                      popup=(str(states) + ": " + str(statedicti[states][0][0])), icon=folium.Icon(color='blue')).add_to(map_osm)

map_osm.save(filenamemap)
