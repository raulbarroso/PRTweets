from time import sleep
import json
import os
import urllib.request
from PIL import Image # pip install Pillow
import pytesseract

def get_tweets(twarc, df, handles, start_date, end_date):
    if os.stat('backups/tweets_backup.txt').st_size != 0:
        with open('backups/tweets_backup.txt', 'r') as filehandle:
            tweet_backup = json.load(filehandle)
        print("Tweets backup file found")
        return tweet_backup

    all_lines = []
    for handle in handles:
        print(handle)
        sleep(1) # Twitter Academy API has a 1 second per request limit
        for line in twarc.search_all(query="from:"+handle, start_time=start_date, end_time=end_date):
            all_lines.append(line)

    all_tweets = []
    for line in all_lines:
        for tweet in line['data']:
            tweet['img_url'] = '' # only stores first image found
            if 'attachments' in tweet and 'media_keys' in tweet['attachments']:
                media_keys = tweet['attachments']['media_keys']
                for key in media_keys:
                    for media in line['includes']['media']:
                        if key == media['media_key']:
                            if media['type'] == "photo":
                                tweet['img_url'] = media['url']
                            break
                    if tweet['img_url'] != '':
                        break
            all_tweets.append(tweet)
    return all_tweets

def image_to_text(tweets):
    tweets.append(0)

    if os.stat('backups/img_tweets_backup.txt').st_size != 0:
        with open('backups/img_tweets_backup.txt', 'r') as filehandle:
            tweets = json.load(filehandle)
        print("Image tweets backup file found")

    t_len = len(tweets)
    start = tweets[-1]
    for i in range(start, t_len - 1):
        if i == 100:
            print(str(round((i*100)/t_len,2)) + "% completed")
        if i % 500 == 0 and i > 0:
            print(str(round((i*100)/t_len,2)) + "% completed")
            tweets[-1] = i
            with open('backups/img_tweets_backup.txt', 'w') as filehandle:
                json.dump(tweets, filehandle)
            print("First " + str(i) + " tweets backed up")
            with open('backups/img_tweets_backup2.txt', 'w') as filehandle:
                json.dump(tweets, filehandle)
        tweets[i]['img_text'] = ''
        img_url = tweets[i]['img_url']
        if img_url != '':
            #print(img_url)
            try:
                conn = urllib.request.urlopen(img_url)
            except:
                print("Error with url, skipping image")
                print(img_url)
            else:
                urllib.request.urlretrieve(img_url, "image.png")
                img = Image.open("image.png")
                tweets[i]['img_text'] = pytesseract.image_to_string(img,lang='spa+eng').replace('\x0C', '')
    tweets.pop()
    return tweets
