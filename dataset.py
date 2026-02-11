#exploring the saved dataset
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.decomposition import NMF

#load the dataset
transcript_df = pd.read_csv(f"transcript_files/71op1DQ2gyo_transcript.csv")
print("\n", transcript_df.head())

transcript_df['start'] = pd.to_numeric(transcript_df['start'], errors='coerce')

print("\nDataset Overview:")
print(transcript_df.info())
print("\nBasic Statistics:")
print(transcript_df.describe())

#plot distribution of text lengths
transcript_df['text_length'] = transcript_df['text'].apply(len)
plt.figure(figsize=(5, 10))
plt.hist(transcript_df['text_length'], bins=50, color='blue', alpha=0.7)
plt.title('Distribution of Text Lengths')
plt.xlabel('Text Length')
plt.ylabel('Frequency')
plt.show()

#plot the most common words
vectorizer = CountVectorizer(stop_words='english')
word_counts = vectorizer.fit_transform(transcript_df['text'])
word_counts_df = pd.DataFrame(
  word_counts.toarray(), columns=vectorizer.get_feature_names_out())
common_words = word_counts_df.sum().sort_values(ascending=False).head(20)
plt.figure(figsize=(10, 5))
common_words.plot(kind='bar', color='green', alpha = 0.7)
plt.title('Top 20 Common Words')
plt.xlabel('Words')
plt.ylabel('Frequency')
plt.show()

#topic modelling using NMF
n_features = 100
n_topics = 10
n_top_words = 10

tf_vectorizer = CountVectorizer(max_df=0.95, min_df=2, stop_words='english')
tf = tf_vectorizer.fit_transform(transcript_df['text'])
nmf = NMF(n_components=n_topics, random_state=42).fit(tf)
tf_feature_names = tf_vectorizer.get_feature_names_out()

def display_topics(model, feature_names, n_top_words):
  topics = []
  for topic_idx, topic in enumerate(model.components_):
    topic_words = [feature_names[i] for i in topic.argsort()]
    topics.append(" ".join(topic_words))
  return topics  

topics = display_topics(nmf, tf_feature_names, n_top_words)
print("\nIdentified Topics:")
for i, topic in enumerate(topics):
  print(f"Topic {i+1}: {topic}")

#get topic distribution for each segment
topic_distribution = nmf.transform(tf)

#align the lengths by trimming the extra row in topic_distribution
topic_distribution_trimmed = topic_distribution[:len(transcript_df)]

#compute the dominant topic for each text segment
transcript_df['dominant_topic'] = topic_distribution_trimmed.argmax(axis=1)

#analyze the  content of each text segment to manually identify logicla breaks
logical_breaks = []

for i in range(1, len(transcript_df)):
  if (transcript_df['dominant_topic'].iloc[i] !=
       transcript_df['dominant_topic'].iloc[i-1]):
    logical_breaks.append(transcript_df['start'].iloc[i])

#consolidate the logical breaks into broader chapters
threshold = 60 #seconds
consolidated_breaks = []
last_break = None

for break_point in logical_breaks:
  if last_break is None or break_point - last_break >= threshold:
    consolidated_breaks.append(break_point)
    last_break = break_point


#merge consecutive breaks with the same dominant topic
final_chapters = []
last_chapter = (consolidated_breaks[0], transcript_df['dominant_topic'][0])

for break_point in consolidated_breaks[1:]:
  current_topic = transcript_df[transcript_df['start'] == 
                                break_point]['dominant_topic'].values[0]
  if current_topic == last_chapter[1]:
    last_chapter = (last_chapter[0], current_topic)
  else:
    final_chapters.append(last_chapter)
    last_chapter = (break_point, current_topic)

final_chapters.append(last_chapter)

# Convert the final chapters to a readable time format
chapter_points = []
chapter_names = []

for i, (break_point, topic_idx) in enumerate(final_chapters):
    chapter_time = pd.to_datetime(break_point, unit='s').strftime('%H:%M:%S')
    chapter_points.append(chapter_time)

    # get the context for the chapter name
    chapter_text = transcript_df[(transcript_df['start'] >= break_point) & (transcript_df['dominant_topic'] == topic_idx)]['text'].str.cat(sep=' ')

    # extract key phrases to create a chapter name
    vectorizer = TfidfVectorizer(stop_words='english', max_features=3)
    tfidf_matrix = vectorizer.fit_transform([chapter_text])
    feature_names = vectorizer.get_feature_names_out()
    chapter_name = " ".join(feature_names)

    chapter_names.append(f"Chapter {i+1}: {chapter_name}")

# display the final chapter points with names
print("\nFinal Chapter Points with Names:")
for time, name in zip(chapter_points, chapter_names):
    print(f"{time} - {name}")