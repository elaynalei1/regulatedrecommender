import numpy as np
import nltk
# nltk.download('all')
from nltk.tokenize import word_tokenize
from nltk import pos_tag
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from sklearn.preprocessing import LabelEncoder
from collections import defaultdict
from nltk.corpus import wordnet as wn
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn import model_selection, svm
from sklearn import metrics
import pandas as pd


combo_df = pd.read_csv("data/monkeypox.csv", encoding='latin-1')

np.random.seed(333)

#remove any blank rows
combo_df['text'].dropna(inplace=True)

#convert all to lowercase
combo_df['text'] = combo_df['text'].astype(str)
combo_df['text'] = combo_df['text'].str.lower()
# print(combo_df.head(10))

#tokenization
combo_df['tokenized_text'] = combo_df.apply(lambda row: nltk.word_tokenize(row["text"]), axis=1)
# print(combo_df['tokenized_text'].head(10))

#WordNetLemmatizer: remove stop words, non-alpha text, and word lemmatization
pos_map = defaultdict(lambda : wn.NOUN)
pos_map['J'] = wn.ADJ
pos_map['V'] = wn.VERB
pos_map['R'] = wn.ADV

for i, text in enumerate(combo_df['tokenized_text']):
    final_words = []
    word_lem = WordNetLemmatizer()
    for word, tag in pos_tag(text):
        if word not in stopwords.words('english') and word.isalpha():
            word_final = word_lem.lemmatize(word, pos=pos_map[tag[0]])
            final_words.append(word_final)
    combo_df.loc[i, 'tokenized_text'] = str(final_words)

#split data into training and testing set: 30% testing, 70% training
train_x, test_x, train_y, test_y = model_selection.train_test_split(combo_df['tokenized_text'], combo_df['binary_class'], test_size=0.3)

#encoding to numerical values that the model can understand
Encoder = LabelEncoder()
train_y = Encoder.fit_transform(train_y)
test_y = Encoder.fit_transform(test_y)

#word vectorization--turn collection of text into numerical feature vectors using
# term frequency -- inverse document (TF-IDF)

Tfidf_vect = TfidfVectorizer(max_features=5000)
Tfidf_vect.fit(combo_df['tokenized_text'])

train_x_Tfidf = Tfidf_vect.transform(train_x)
test_x_Tfidf = Tfidf_vect.transform(test_x)

# print(Tfidf_vect.vocabulary_)
# print(train_x_Tfidf)

SVM = svm.SVC(C=1.0, kernel='linear', degree=3, gamma='auto')
SVM.fit(train_x_Tfidf, train_y)
prediction_SVM = SVM.predict(test_x_Tfidf)

# Assuming you have a new dataset in a CSV file named 'new_data.csv'
new_data = pd.read_csv("data/monkeypox-followup.csv", encoding='latin-1')

# print(new_data.columns)

# Preprocess the new dataset
new_data['text'].dropna(inplace=True)
new_data['text'] = new_data['text'].astype(str)
new_data['text'] = new_data['text'].str.lower()

new_data['tokenized_text'] = new_data.apply(lambda row: nltk.word_tokenize(row["text"]), axis=1)

for i, text in enumerate(new_data['tokenized_text']):
    final_words = []
    word_lem = WordNetLemmatizer()
    for word, tag in pos_tag(text):
        if word not in stopwords.words('english') and word.isalpha():
            word_final = word_lem.lemmatize(word, pos=pos_map[tag[0]])
            final_words.append(word_final)
    new_data.loc[i, 'tokenized_text'] = str(final_words)

# Vectorize the text data in the new dataset
new_data_text = new_data['tokenized_text']
new_data_tfidf = Tfidf_vect.transform(new_data_text)

# Make predictions using the trained SVM model
new_data_predictions = SVM.predict(new_data_tfidf)

# Add predictions to the new dataset
new_data['predictions'] = new_data_predictions

# Save the new dataset with predictions
new_data[['ï»¿number', 'predictions']].to_csv('data/followup_predictions.csv', index=False)

mean_retweet_count = combo_df['retweet_count'].mean()
mean_follower_count = combo_df['followers count'].mean()
total_tweet_count = combo_df.size
def cred_score(retweets, followers, user_tweet_count):
    utility = abs(((retweets * followers)/user_tweet_count) - ((mean_retweet_count * mean_follower_count)/total_tweet_count))
    standardized = np.sqrt((utility ** 2)/(total_tweet_count-1))
    return 10 - (standardized * 100)
combo_df['credibility'] = cred_score(combo_df['retweet_count'],
                                         combo_df['followers count'],
                                         combo_df['tweet count'])
#if the score is less than 0, then make it 0 because the score is low enough to not recommend the user in the algorithm
combo_df.loc[combo_df['credibility'] < 0, "credibility"] = 1.0
print(combo_df['credibility'])
print("The maximum social credibility score is: ", combo_df['credibility'].max())
print("The minimumsocial credibility score is: ", combo_df['credibility'].min())
print("The mean social credibility score is: ", combo_df['credibility'].mean())

combo_df[['ï»¿number', 'credibility']].to_csv('data/credibility_scores.csv', index=False)

print(combo_df.columns)