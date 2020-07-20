from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
import json
import sqlite3
from unidecode import unidecode
import time
import pickle

#consumer key, consumer secret, access token, access secret.
ckey="SCfFS3fYP8rJP1LEEoe13YaXG"
csecret="rzw5utCEcZeU5ZDqHDkes2T8ZzSG3thI53muJoVqBqjwA2jS30"
atoken="1275138405358120960-or02GXNey8WQ3mQXIhv3m0cUdWsdGq"
asecret="Wr1pyPKe7sGL1VSHjYtEWMdeufdLeAdHxRjpeGDB6N51S"

vectorizer = pickle.load(open('models/vectorizer.sav', 'rb'))
classifier = pickle.load(open('models/classifier.sav', 'rb'))

conn = sqlite3.connect('twitter.db')
c = conn.cursor()

def create_table():
    try:
        c.execute("CREATE TABLE IF NOT EXISTS tweet_category(unix REAL, tweet TEXT, tweet_category TEXT)")
        c.execute("CREATE INDEX fast_unix ON tweet_category(unix)")
        c.execute("CREATE INDEX fast_tweet ON tweet_category(tweet)")
        c.execute("CREATE INDEX fast_tweet_category ON tweet_category(tweet_category)")
        conn.commit()
    except Exception as e:
        print(str(e))
create_table()



class listener(StreamListener):

    def on_data(self, data):
        try:
            global vectorizer, classifier
            data = json.loads(data)
            tweet = unidecode(data['text'])
            time_ms = data['timestamp_ms']
            text_vector = vectorizer.transform([tweet])
            result = classifier.predict(text_vector)
            tweet_category = result[0]
            print(time_ms, tweet, tweet_category)
            c.execute("INSERT INTO tweet_category (unix, tweet, tweet_category) VALUES (?, ?, ?)",
                  (time_ms, tweet, tweet_category))
            conn.commit()
            time.sleep(5)
        except KeyError as e:
            print(str(e))
        return(True)

    def on_error(self, status):
        print(status)


while True:

    try:
        auth = OAuthHandler(ckey, csecret)
        auth.set_access_token(atoken, asecret)
        twitterStream = Stream(auth, listener())
        twitterStream.filter(track=["covid", "coronavirus"])
    except Exception as e:
        print(str(e))
        time.sleep(5)
