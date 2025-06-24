def fetch_stat(selected_user, df):
    
    if selected_user != 'overall':
        df = df[df['user'] == selected_user]
    num_messages = df.shape[0]
    words = []
    for message in df['message']:
        words.extend(message.split())
          
    num_media = df[df['message'] == '<Media omitted>/n'].shape[0]  
    
    return num_messages, len(words), num_media
    
    