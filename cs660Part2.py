from pymongo import MongoClient
import emoji
import folium
import os
import csv

client = MongoClient('localhost', 27017)
db = client['usa_db']
collection = db['usa_tweets_collection']


# ############################################## PART 2 B (1)################################################

emojidicti = {}

tweets_iterator = collection.find()

for tweet in tweets_iterator:
    # print("\nTweet Text: " + str(tweet['text']))
    for stuff in tweet['text']:
        if stuff in emoji.UNICODE_EMOJI:
            # print("Tweet Emoji: " + str(stuff))
            if stuff not in emojidicti:
                emojidicti[stuff] = 1
            else:
                emojidicti[stuff] += 1
sortedthingy = sorted(emojidicti.items(), key=lambda x: x[1], reverse=True)
print("\nTop 15 emojis:")
for freq in range(15):
    print(sortedthingy[freq])


# ##############################################PART 2 B (2)##################################################

christytreedicti = {}

tweets_iterator = collection.find()

for tweet in tweets_iterator:
    for stuff in tweet['text']:
        if stuff == emoji.emojize(':christmas_tree:', use_aliases=True) and tweet['place']['full_name'][-2:] != "SA"\
                and 65 <= ord(tweet['place']['full_name'][-1]) <= 90:
            if tweet['place']['full_name'][-2:] not in christytreedicti:
                christytreedicti[tweet['place']['full_name'][-2:]] = 1
            else:
                christytreedicti[tweet['place']['full_name'][-2:]] += 1

sortedthingy = sorted(christytreedicti.items(), key=lambda x: x[1], reverse=True)
print("\nTop 5 States that use " + emoji.emojize(':christmas_tree:', use_aliases=True))
for freq in range(5):
    print(sortedthingy[freq])


# #############################################PART 2 B (3)####################################################

massamoji = {}

tweets_iterator = collection.find()

for tweet in tweets_iterator:
    for stuff in tweet['text']:
        if stuff in emoji.UNICODE_EMOJI and tweet['place']['full_name'][-2:] == "MA":
            if stuff not in massamoji:
                massamoji[stuff] = 1
            else:
                massamoji[stuff] += 1

sortedthingy = sorted(massamoji.items(), key=lambda x: x[1], reverse=True)
print("\nTop 5 emojis in Massachusetts:")
for freq in range(5):
    print(sortedthingy[freq])


# #############################################PART 2 B (4)####################################################

statemoji = {}
tweets_iterator = collection.find()

for tweet in tweets_iterator:
    for stuff in tweet['text']:
        if stuff in emoji.UNICODE_EMOJI and tweet['place']['full_name'][-2:] != "SA"\
                and 65 <= ord(tweet['place']['full_name'][-1]) <= 90:
            if tweet['place']['full_name'][-2:] not in statemoji:
                statemoji[tweet['place']['full_name'][-2:]] = 1
            else:
                statemoji[tweet['place']['full_name'][-2:]] += 1

sortedthingy = sorted(statemoji.items(), key=lambda x: x[1], reverse=True)
print("\nTop 5 States that use Emojis:")
for freq in range(5):
    print(sortedthingy[freq])


# ###########################################PART 2 C (1)######################################################

statetweet = {}
tweets_iterator = collection.find()

for tweet in tweets_iterator:
    if tweet['place'] is not None and tweet['place']['full_name'][-2:] != "SA" and \
                            65 <= ord(tweet['place']['full_name'][-1]) <= 90:
        if tweet['place']['full_name'][-2:] not in statetweet:
            statetweet[tweet['place']['full_name'][-2:]] = 1
        else:
            statetweet[tweet['place']['full_name'][-2:]] += 1

sortedthingy = sorted(statetweet.items(), key=lambda x: x[1], reverse=True)
print("\nTop 5 Tweeting States:")
for freq in range(5):
    print(sortedthingy[freq])


# ##########################################PART 2 C (2)##########################################################

calicity = {}
tweets_iterator = collection.find()

for tweets in tweets_iterator:
    if tweets['place'] is not None and tweets['place']['full_name'][-2:] == "CA":
        if tweets['place']['name'] not in calicity:
            calicity[tweets['place']['name']] = 1
        else:
            calicity[tweets['place']['name']] += 1

sortedthingy = sorted(calicity.items(), key=lambda x: x[1], reverse=True)
print("\nTop 5 Tweeting Cities in California:")
for freq in range(5):
    print(sortedthingy[freq])


# #########################################PART 2 D ############################################################

dir_path = os.path.dirname(os.path.abspath(__file__))
filename = os.path.join(dir_path, "usa_tweets.csv")
filenamemap = os.path.join(dir_path, "Part2-D.html")

map_osm = folium.Map(location=[39, -98.1], zoom_start=4)
prompt = 'Click for screen_name!'

with open(filename, 'rt', encoding="utf8") as csvfile:
    lineReader = csv.reader(csvfile, delimiter=',')
    next(csvfile)                                                           # skip header line
    linecount = 0
    for row in lineReader:
        # print(linecount)
        if linecount == 50:
            break
        if not row:
            continue
        twonumbers = row[3][34:len(row[3])-2]
        twonumbers = [float(num) for num in twonumbers.split(', ')]
        screenname = row[1].split("screen_name': '")[1].split('\'')[0]
        folium.Marker(twonumbers, popup=screenname).add_to(map_osm)
        linecount += 1
        # folium.Marker([float(row[3][34:len(row[3])-2])]).add_to(map_osm)
        # print(row[3][33:len(row[3])-1])

map_osm.save(filenamemap)
