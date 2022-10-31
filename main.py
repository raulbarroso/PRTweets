import json
from datetime import datetime
import search_timeline
from twarc import Twarc2
import pandas as pd

# Authentication using Twarc2
# For App-only autherization the Bearer Token is the only code needed
bt = 'AAAAAAAAAAAAAAAAAAAAAPBwQQEAAAAAQWKEwRsPRX2gBPmn3GKxp7zjk8Q%3DitFTrSwSFZ5oR5hLa1uxx3ruJK4fJswNZS0l7SREqmnfBv8NBE'
t = Twarc2(bearer_token = bt)

# Read excel file with handles
df = pd.read_excel("authors.xlsx")

# Start and end dates
s_date = datetime(2017, 1, 1)
e_date = datetime(2020, 11, 3)
e_date = datetime(2017, 1, 3)

# Column name with list of handles
# Multiple handles in a cell should be separated by a ", "
handles = []
for i in range(len(df)):
    handles_str = df.at[i, "Handles"]
    if isinstance(handles_str, str):
        handles_list = handles_str.split(", ")
        for handle in handles_list:
            # Removes '@' from handles
            if handle[0] == '@':
                handle = handle[1:]
            handles.append(handle)
print(handles)

# Request tweets
tweets = search_timeline.get_tweets(t, df, handles, s_date, e_date)
print("\nTotal tweets: " + str(len(tweets)))

# Backup tweet data
with open('backups/tweets_backup.txt', 'w') as filehandle:
    json.dump(tweets, filehandle)

# Add image_to_text column with corresponding data
print("\nProcessing images...")
#tweets = search_timeline.image_to_text(tweets)

# Get users
users = []
for line in t.user_lookup(handles, usernames=True):
    for user in line['data']:
        users.append(user)

# Adds handles to tweets
# Adds author informarion to tweets
# Clean tweets data and flatten nested dictionaries
# Discards start and end positions of entities
# Discards annotations (from entities), context_annotations, and attachments
# Multiple values in a cell are separated by a single ','
for tweet in tweets:
    i = 0
    while i < len(users):
        if tweet['author_id'] == users[i]['id']:
            tweet['user_handle'] = '@' + users[i]['username']
            if 'description' in users[i]:
                tweet['user_description'] = users[i]['description']
            if 'location' in users[i]:
                tweet['user_location'] = users[i]['location']
            tweet['user_metrics'] = users[i]['public_metrics']
            tweet['user_created_at'] = users[i]['created_at']
            tweet['user_display_name'] = users[i]['name']
            break
        else:
            i += 1
    j = 0
    while j < len(df):
        handles_str = df.at[j, "Handles"]
        if isinstance(handles_str, str) and tweet['user_handle'] in handles_str:
            if "Cuerpo" in df.columns:
                tweet['position'] = df.at[j, "Cuerpo"]
            if "Partido" in df.columns:
                tweet['party'] = df.at[j, "Partido"]
            if "Nombre" in df.columns:
                tweet['author_name'] = df.at[j, "Nombre"]
            break
        else:
            j += 1
    if 'entities' in tweet:
        if 'hashtags' in tweet['entities']:
            tweet['hashtags'] = []
            for i in tweet['entities']['hashtags']:
                tweet['hashtags'].append(i['tag'])
            tweet['hashtags'] = ",".join(tweet['hashtags'])
        if 'mentions' in tweet['entities']:
            tweet['mentions'] = []
            for i in tweet['entities']['mentions']:
                tweet['mentions'].append(i['username'])
            tweet['mentions'] = ",".join(tweet['mentions'])
        if 'urls' in tweet['entities']:
            tweet['url'] = tweet['entities']['urls'][0]['url']
            tweet['expanded_url'] = tweet['entities']['urls'][0]['expanded_url']
        del tweet['entities']
    if 'public_metrics' in tweet:
        tweet['retweet_count'] = tweet['public_metrics']['retweet_count']
        tweet['reply_count'] = tweet['public_metrics']['reply_count']
        tweet['like_count'] = tweet['public_metrics']['like_count']
        tweet['quote_count'] = tweet['public_metrics']['quote_count']
        del tweet['public_metrics']
    if 'referenced_tweets' in tweet:
        refs = []
        for i in tweet['referenced_tweets']:
            refs.append(i['type'] + ": " + i['id'])
        tweet['referenced_tweet_ids'] = ",".join(refs)
        del tweet['referenced_tweets']
    if 'attachments' in tweet:
        del tweet['attachments']
    if 'context_annotations' in tweet:
        del tweet['context_annotations']

# Turns lists into dataframes
tweets_df = pd.DataFrame(tweets)
users_df = pd.DataFrame(users)

# Exports dataframes as excel files
tweets_df.to_excel("tweets.xlsx", index=False)
users_df.to_excel("users.xlsx", index=False)

# Deletes backup files
open('backups/tweets_backup.txt', 'w').close()
open('backups/img_tweets_backup.txt', 'w').close()

print("Completed!")
