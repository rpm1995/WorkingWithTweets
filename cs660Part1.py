from pymongo import MongoClient
from textblob import TextBlob


def tweet_sentiment(tweety):

    goodbadugly = TextBlob(tweety)

    if goodbadugly.sentiment.polarity > 0:
        return 'Positive'
    elif goodbadugly.sentiment.polarity == 0:
        return 'Neutral'
    else:
        return 'Negative'


client = MongoClient('localhost', 27017)
db = client['twitterdb']
collection = db['twitter_search']
tweets_iterator = collection.find()

addicted = {}

for tweets in tweets_iterator:

    text = tweets['text']
    senti = tweet_sentiment(text)
    addicted[text] = senti

for items in addicted:
    print(str(addicted[items]) + " sentiments for the tweet: " + str(items))


print("\n \n")
print("Number of Tweets that have the Word \"data\" (Case Insensitive): " + str(collection.find({
    "text": {"$regex": "data", "$options": "i"}}).count()))
print("Number of Tweets that are geo_enabled: " + str(collection.find({"user.geo_enabled": True}).count()))
