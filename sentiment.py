import pandas as pd
import matplotlib.pyplot as plt
from nltk.sentiment import SentimentIntensityAnalyzer
import nltk
from nltk import bigrams
from collections import Counter
import seaborn as sns

df1 = pd.read_csv('hashtag_joebiden.csv', lineterminator='\n', parse_dates=True)
df2 = pd.read_csv('hashtag_donaldtrump.csv', lineterminator='\n', parse_dates=True)

df1['created_at'] = pd.to_datetime(df1['created_at'])
df2['created_at'] = pd.to_datetime(df2['created_at'])

nltk.download('vader_lexicon')

sia = SentimentIntensityAnalyzer()
df1['sentiment_scores'] = df1['tweet'].apply(lambda tweet: sia.polarity_scores(tweet))
df1['compound'] = df1['sentiment_scores'].apply(lambda score_dict: score_dict['compound'])

df2['sentiment_scores'] = df2['tweet'].apply(lambda tweet: sia.polarity_scores(tweet))
df2['compound'] = df2['sentiment_scores'].apply(lambda score_dict: score_dict['compound'])

# Save df1 to a new CSV file
df1.to_csv('hashtag_joebiden_sentiment.csv', index=False)

# Save df2 to a new CSV file
df2.to_csv('hashtag_donaldtrump_sentiment.csv', index=False)
