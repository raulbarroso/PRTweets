# PRTweets

PRTweets is a python program for mining a large amount of tweets from multiple accounts and exporting the data to excel. It was designed specifically for retrieving tweets from Puerto Rican lawmakers with the Twitter API v2.

## Installation

You need a registered application with Twitter API v2 to use this program. The application will generate a bearer code which will connect PRTweets to twitter's API.

The following modules must be installed:

```bash
pip install twarc
pip install pandas
pip install pillow
pip install pytesseract
```

Twarc is a python wrapper that does the work of connecting us to the Twitter API v2. Pandas allows us to read and write excel tables as dataframes. Pillow allows us to work with images in python. Pytesseract is an optical character recognition program that can translate text from images into strings.

## Usage

Upon running the main.py file in PRTweets, the program will look for an excel file with a list of twitter handles. By default it will look for them in a column titled "Handles" in a file titled "authors.xlsx". Multiple handles can be in a single cell as long as they're separated by a comma and a space. It will then look for the tweets of all the handles starting from a set date to another. The dates can be modified easily:

```python
# Start and end dates
s_date = datetime(2017, 1, 1)
e_date = datetime(2020, 11, 3)
```

After retrieving the tweets it will find the first image of each tweet, if it exists, and translate any text in the image into a string. This will take approximately 2 to 3 seconds for each tweet with an image; it is very time-consuming for large batches of tweets. This part of the program can be skipped without causing an error simply by commenting the function call:

```python
# Add image_to_text column with corresponding data
print("\nProcessing images...")
#tweets = search_timeline.image_to_text(tweets)
```

The program will also retrieve the user data from each handle and format the tweet data. The tweet data and the user data will be exported to two files: "tweets.xlsx" and "users.xlsx". If these files are in the folder and the program runs again, it will overwrite the existing files.

## Backups

Retrieving the tweets can be time-consuming. If the program is stopped before finishing, the data could be lost. To avoid this, the program creates backup files in the backup folder. It creates one file titled "tweets_backup.txt" after the first timeline scrape. It creates and then overwrites a second file titled "img_tweets_backup.txt" for every 500 images translated into text. Because creating this backup file takes time, it runs the risk of being interrupted. For this reason, a second identical backup is written titled "img_tweets_backup2.txt". This one should be duplicated and renamed "img_tweets_backup.txt" if the original is corrupted.

## Author

This code was written by Raúl Barroso Suárez for use in a data analysis investigation by Dr. Mayra Vélez Serrano.
