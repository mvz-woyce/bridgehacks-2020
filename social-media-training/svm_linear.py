# Dataset: Polarity dataset v2.0
# http://www.cs.cornell.edu/people/pabo/movie-review-data/
#
# Discussion at https://medium.com/@vasista/sentiment-analysis-textblob-vs-svm-338d418e3ff1

from sklearn.feature_extraction.text import TfidfVectorizer

import re
import time
from sklearn import svm
from sklearn.metrics import classification_report
import preprocessor as p
import nltk
from nltk import word_tokenize, FreqDist
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
nltk.download
nltk.download('wordnet')
nltk.download('stopwords')
from nltk.tokenize import TweetTokenizer

import pandas as pd

# train Data
trainData = pd.read_csv("data/covid-train.csv")

# test Data
testData = pd.read_csv("data/covid-test.csv")

# Create a function to clean the tweets
def cleanTxt(text):
  emoji_pattern = re.compile("["
         u"\U0001F600-\U0001F64F"  # emoticons
         u"\U0001F300-\U0001F5FF"  # symbols & pictographs
         u"\U0001F680-\U0001F6FF"  # transport & map symbols
         u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
         u"\U00002702-\U000027B0"
         u"\U000024C2-\U0001F251"
         "]+", flags=re.UNICODE)
  text = emoji_pattern.sub(r'', text)
  text = re.sub('@[A-Za-z0–9]+', '', text) #Removing @mentions
  text = re.sub('#', '', text) # Removing '#' hash tag
  text = re.sub('RT[\s]+', '', text) # Removing RT
  text = re.sub('https?:\/\/\S+', '', text) # Removing hyperlink
  text = re.sub('\d+', '', text) # Removing numbers
#after tweepy preprocessing the colon symbol left remain after
#removing mentions
  text = re.sub(r':', '', text)
  text = re.sub(r'‚Ä¶', '', text)
#replace consecutive non-ASCII characters with a space
  text = re.sub(r'[^\x00-\x7F]+',' ', text)
  return text

print('Cleaning the tweets')

# Clean the tweets
trainData['Content'] = [p.clean(entry) for entry in trainData['Content']]
testData['Content'] = [p.clean(entry) for entry in testData['Content']]

print('Running the cleanTxt')

trainData['Content'] = trainData['Content'].apply(cleanTxt)
testData['Content'] = testData['Content'].apply(cleanTxt)

print('Running dropNa')

trainData['Content'].dropna(inplace=True)
testData['Content'].dropna(inplace=True)

print('Running lower')

trainData['Content'] = [entry.lower() for entry in trainData['Content']]
testData['Content'] = [entry.lower() for entry in testData['Content']]

print(testData)

# Create feature vectors
vectorizer = TfidfVectorizer(min_df = 5,
                             max_df = 0.8,
                             sublinear_tf = True,
                             use_idf = True)

train_vectors = vectorizer.fit_transform(trainData['Content'])
test_vectors = vectorizer.transform(testData['Content'])

# Perform classification with SVM, kernel=linear
classifier_linear = svm.SVC(kernel='linear')
t0 = time.time()
classifier_linear.fit(train_vectors, trainData['Label'])
t1 = time.time()
prediction_linear = classifier_linear.predict(test_vectors)
t2 = time.time()
time_linear_train = t1-t0
time_linear_predict = t2-t1

# results
print("Results for SVC(kernel=linear)")
print("Training time: %fs; Prediction time: %fs" % (time_linear_train, time_linear_predict))
report = classification_report(testData['Label'], prediction_linear, output_dict=True)
print('other_useful_information: ', report['other_useful_information'])
print('treatment: ', report['treatment'])
print('disease_transmission: ', report['disease_transmission'])
print('disease_signs_or_symptoms: ', report['disease_signs_or_symptoms'])
print('not_related_or_irrelevant: ', report['not_related_or_irrelevant'])
print('prevention: ', report['prevention'])
print('deaths_reports: ', report['deaths_reports'])
print('affected_people: ', report['affected_people'])

import pickle
# pickling the vectorizer
pickle.dump(vectorizer, open('models/vectorizer.sav', 'wb'))
# pickling the model
pickle.dump(classifier_linear, open('models/classifier.sav', 'wb'))

print('Both vectorizer and classifier has been pickled. Check "classifier_flask" to load and use in flask app')