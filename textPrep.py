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