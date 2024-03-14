from urlextract import URLExtract
from wordcloud import WordCloud
import pandas as pd
from collections import Counter
import emoji

def fetch_stats(selected_user, df):

    if selected_user != "Overall":
        df = df[df['user'] == selected_user]

    #1. number of messages
    num_messages = df.shape[0]

    #2. Number of Words
    words = []
    for message in df['message']:
        words.extend(message.split(' '))

    #3. Number of Media files
    num_media = df[df['message'] == '<Media omitted>\n'].shape[0]

    #4. Number of Links
    links = []
    extractor = URLExtract()
    for message in df['message']:
        links.extend(extractor.find_urls(message))


    return num_messages, len(words), num_media, len(links)

def fetch_most_busy_users(df):
    x = df['user'].value_counts().head()
    temp = df[df['user'] != 'group_noti']
    df = round(temp['user'].value_counts()/temp.shape[0]*100,2).reset_index().rename(columns={'user':'Name','count':'Percentage'})
    return x,df

def create_wordcloud(selected_user,df):
    f = open('stop_hinglish.txt', 'r')
    stop_words = f.read()

    if selected_user != "Overall":
        df = df[df['user'] == selected_user]

    temp = df[df['user'] != 'group_noti']
    temp = temp[df['message'] != '<Media omitted>\n']

    def remove_stop_words(message):
        y = []
        for word in message.lower().split():
            if word not in stop_words:
                y.append(word)
        return " ".join(y)

    temp['message'] = temp['message'].apply(remove_stop_words)
    wc = WordCloud(width=500, height=500, min_font_size=10, background_color='white')
    df_wc = wc.generate(temp['message'].str.cat(sep=" "))
    return df_wc

def most_common_words(selected_user,df):
    f = open('stop_hinglish.txt', 'r')
    stop_words = f.read()

    if selected_user != "Overall":
        df = df[df['user'] == selected_user]

    temp = df[df['user'] != 'group_noti']
    temp = temp[temp['message'] != '<Media omitted>\n']

    words = []
    for message in temp['message']:
        for word in message.lower().split():
            if word not in stop_words:
                words.append(word)

    most_common_df = pd.DataFrame(Counter(words).most_common(20))
    return most_common_df

def emoji_data(selected_user,df):

    if selected_user != "Overall":
        df = df[df['user'] == selected_user]

    emojis = []
    for message in df['message']:
        for e in message:
            if e in emoji.EMOJI_DATA:
                emojis.extend(e)

    emoji_df = pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))
    return emoji_df


def monthly_timeline(selected_user,df):
    if selected_user != "Overall":
        df = df[df['user'] == selected_user]

    timeline = df.groupby(['year', 'month_num', 'month']).count()['message'].reset_index()
    t = []
    for i in range(timeline.shape[0]):
        t.append(timeline['month'][i] + "-" + str(timeline['year'][i]))
    timeline['time'] = t

    return timeline

def daily_timeline(selected_user,df):
    if selected_user != "Overall":
        df = df[df['user'] == selected_user]

    timeline = df.groupby(['only_date']).count()['message'].reset_index()

    return timeline

def week_activity_map(selected_user,df):
    if selected_user != "Overall":
        df = df[df['user'] == selected_user]

    return df['day_name'].value_counts()

def month_activity_map(selected_user,df):
    if selected_user != "Overall":
        df = df[df['user'] == selected_user]

    return df['month'].value_counts()