
from collections import Counter
from wordcloud import WordCloud
from wordcloud import STOPWORDS
import matplotlib.pyplot as plt
import os

def main():
    campaign = input("Please enter the campaign name: ")
    session = input("Please enter desired session # or 'all': ")
    while not isinstance(int(session), int):
        session = input("Session must be an integer or 'all'. Please try again: ")
    



def dnd_word_cloud(campaign, session, prev=False, filtering_level=3): 
    if session == "all":
        session = file_count(campaign)
        prev = True
    text = file_read(campaign, session)
    frequency = preprocessing(text, filtering_level)
    wordcloud_plotting(frequency)
    if session > 1 and prev:
        dnd_word_cloud(campaign, session-1, prev, filtering_level)

def file_count(campaign):
    files = [f for f in os.listdir(campaign) if os.path.isfile(os.path.join(campaign, f))]
    file_count = len(files) - 1
    return file_count


def file_read(campaign, session):
    ses = str(session)
    file = open(campaign + "/" + campaign + " session " + ses + " transcript.txt")
    return file.read()

def preprocessing(text, filtering_level):
    text = text.lower()
    wordList = text.split()
    if filtering_level > 0:
        stop_words = set(STOPWORDS)
        if filtering_level > 1:
            custom_stopwords = {"uh", "um", "like", "yeah", "okay", "alright", "hmm", "oh", "hey", "well", "huh", "look", "see", "i'm", "kind", "right", "go", "going", "know", "guys", "one", "back", "gonna"}
            stop_words.update(custom_stopwords)
        wordList = [word for word in wordList if word not in stop_words]
    cnt = Counter(wordList)
    total_words = sum(cnt.values())
    word_freq = {word: count / total_words for word, count in cnt.items()}
    #print(word_freq)
    return word_freq

def wordcloud_plotting(word_freq):
    wordcloud = WordCloud(width=800, height=400, background_color="black").generate_from_frequencies(word_freq)

    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis("off")
    plt.show()



dnd_word_cloud("Ravenloft", "all", prev=True, filtering_level=3)
#main()