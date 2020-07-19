# bridgehacks-2020
Mannan's submission to Bridgehacks 2020

#social-media-training

##To install the dependencies
pip3 install -r requirements.txt

##To train the model using the data in the data/ folder:
python3 svm_linear.py

##To stream tweets and classify them and store them in the local sqlite database
python3 stream_tweets.py

#social-media-backend

##To install the requirements
npm install

##To run the backend server
node server.js
(listens on port 8000)

#social-media-frontend

##To install the requirements
npm install

##To run the frontend server
ng serve --port 8081
