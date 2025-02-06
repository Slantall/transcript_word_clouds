
from collections import Counter
from wordcloud import WordCloud
from wordcloud import STOPWORDS
import os

def main():
    campaign = campaign_check()
    session = session_check(campaign)
    prev = prev_check(session)
    filtering_level = filter_check()
    dnd_word_cloud(campaign, session, prev, filtering_level)


def campaign_check():
    while True:
        campaign = input("Please enter the campaign name: ").strip()
        valid_folders = [
            f for f in os.listdir() 
            if os.path.isdir(f) and f not in {"__pycache__", "word clouds", ".git"}
        ]

        if os.path.exists(campaign):
            return campaign
        else:
            print("Campaign folder not found. Valid campaign folders:")
            for folder in valid_folders:
                print(f"- {folder}")


    
def session_check(campaign):
    while True:
        session = input("Please enter desired session # or 'all': ").strip()
        if session.lower() == "all":
            return "all" 
        try:
            session = int(session)
            if file_count(campaign) < session or session < 1:
                print(f"Session number not found. Valid sessions are 1 to {file_count(campaign)}")
            else:
                return session
        except ValueError:
            print("Session must be an integer or 'all'. Please try again.")

def prev_check(session):
    if session == "all":
        return True
    if session == 1:
        return False
    while True:
        prev = input("Include all previous sessions? Y/N: ").strip().lower()
        if prev == "y" or prev == "yes" or prev == "1" or prev == "true" or prev == "t":
            return True
        if prev == "n" or prev == "no" or prev == "0" or prev == "false" or prev == "f":
            return False
        print("Invalid selection. Please enter (Y)es or (N)o")

def filter_check():
    while True:
        filtering_level = input("What level filtering would you like? Enter 0, 1, 2, or 'help' for info: ")
        try:
            filtering_level = int(filtering_level)
            if filtering_level >= 0:
                return filtering_level
            print("Please enter a value greater than or equal to 0.")
        except ValueError:
            print("""Valid filter levels are:
            0: No filtering. Word cloud contains many stop words, such as 'is' and 'the' as well as some uninteresting D&D terms.
            1: Stop words are filtered. All other common roleplaying terms are retained, such as "see" and "go" as well as some filler phrases like "uh".
            2: Filters out stop words and some uninteresting roleplaying terms. Combat terms were retained.
            """)





def dnd_word_cloud(campaign, session, prev=False, filtering_level=2): 
    if session == "all":
        session = file_count(campaign)
        prev = True
    text = file_read(campaign, session)
    frequency = preprocessing(text, filtering_level)
    wordcloud_plotting(frequency,campaign, session, filtering_level)
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

def wordcloud_plotting(word_freq, campaign, session, filtering_level):
    wordcloud = WordCloud(width=800, height=400, background_color="black").generate_from_frequencies(word_freq)

    base_dir = "word clouds"
    filtering_level_dir = os.path.join(base_dir, campaign, "filtering level " + str(filtering_level))
    os.makedirs(filtering_level_dir, exist_ok=True)

    filename = f"{campaign} session {session} filter level {filtering_level}.png"
    file_path = os.path.join(filtering_level_dir, filename)
    wordcloud.to_file(file_path)

main()
