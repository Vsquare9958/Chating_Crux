from urlextract import URLExtract
from wordcloud import WordCloud
import pandas as pd
from collections import Counter

f = open('stop_hinglish.txt','r')
stop_words = f.read()

extractor = URLExtract()
def fetch_stat(selected_user, df):
    
    if selected_user != 'overall':
        df = df[df['user'] == selected_user]
    num_messages = df.shape[0]
    words = []
    for message in df['message']:
        words.extend(message.split())
          
    num_media = df[df['message'] == '<Media omitted>\n'].shape[0]  
    
    links = []
    for message in df['message']:
        links.extend(extractor.find_urls(message))
    
    return num_messages, len(words), num_media, len(links)
    
def most_busy(df):
    
    x = df['user'].value_counts().head()
    df = round((df['user'].value_counts()/df.shape[0])*100,2).reset_index().rename(columns = {'index':'name', 'user':'percent'})
    return x, df

def create_wordcloud(selected_user, df):
    if selected_user != 'overall':
        df = df[df['user'] == selected_user]
    
    temp = df[df['user'] != 'group_notification']
    temp = temp[temp['message'] != '<Media omitted>\n']
    
    def remove_stopwords(message):
        y = []
        for word in message.lower().split():
            if word not in stop_words:
                y.append(word)
        return " ".join(y)
    
    wc = WordCloud(width = 500, height = 500, min_font_size = 10, background_color = 'white')
    temp['message'] = temp['message'].apply(remove_stopwords)
    df_wc = wc.generate(temp['message'].str.cat(sep = " "))
    return df_wc

def most_common_word(selected_user, df):
    if selected_user != 'overall':
        df = df[df['user'] == selected_user]
        
    temp = df[df['user'] != 'group_notification']
    temp = temp[temp['message'] != '<Media omitted>\n']
    
    words = []
    for message in temp['message']:
        for word in message.lower().split():
            if word not in stop_words:
                words.append(word)
    

    most_commom_df = pd.DataFrame(Counter(words).most_common(20))
    return most_commom_df

def monthly_timeline(selected_user, df):
    if selected_user != 'overall':
        df = df[df['user'] == selected_user]
    timeline = df.groupby(['year','month_num','month']).count()['message'].reset_index()
    time = []
    for i in range (timeline.shape[0]):
        time.append(timeline['month'][i] + " - " + str(timeline['year'][i]))
    timeline['time'] = time
    return timeline

def daily_timeline(selected_user, df):
    if selected_user != 'overall':
        df = df[df['user'] == selected_user]
        
    daily_timeline = df.groupby('only_date').count()['message'].reset_index()
    return daily_timeline

def activity_heatmap(selected_user, df):
    if selected_user != 'overall':
        df = df[df['user'] == selected_user]
    user_heatmap = df.pivot_table(index = 'day_name', columns = 'period', values = 'message', aggfunc = 'count').fillna(0)
    return user_heatmap