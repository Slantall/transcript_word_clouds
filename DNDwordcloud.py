
from collections import Counter
import wordcloud
from wordcloud import STOPWORDS


def main(campaign, session): #change to *arg to work with a range 
    text = file_read(campaign, session)
    preprocessing(text)


def file_read(campaign, session):
    ses = str(session)
    file = open(campaign + "/" + campaign + " session " + ses + " transcript.txt")
    return file.read()

def preprocessing(text):
    text = text.lower()
    #possibly add Lemmatization in the future
    wordList = text.split()
    stop_words = set(STOPWORDS)
    custom_stopwords = {"uh", "um", "like", "yeah", "okay", "alright", "hmm", "oh", "hey", "well", "huh", "look", "see", "i'm", "kind", "right"}
    stop_words.update(custom_stopwords)
    filtered_words = [word for word in wordList if word not in stop_words]
    cnt = Counter(filtered_words)
    print(cnt)
    return cnt


main("Ravenloft", 1)