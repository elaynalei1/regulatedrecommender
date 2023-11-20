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
from SVM import SVM, Tfidf_vect, pos_map

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

accuracy = metrics.accuracy_score(new_data['binary_class'], new_data_predictions)
precision = metrics.precision_score(new_data['binary_class'], new_data_predictions)
recall = metrics.recall_score(new_data['binary_class'], new_data_predictions)
f1_score = metrics.f1_score(new_data['binary_class'], new_data_predictions)

print(f'Accuracy: {accuracy:.2f}')
print(f'Precision: {precision:.2f}')
print(f'Recall: {recall:.2f}')
print(f'F1 Score: {f1_score:.2f}')