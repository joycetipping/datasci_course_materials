# 1.2. Derive the sentiment of each tweet
# Joyce Tipping
# Coursera | Intro to Data Sci | Dr. Howe

# This script takes an AFINN file and a file of twitter data and calculates the
# sentiment score of each tweet as the sum of the AFINN scores of the known
# words it contains. Unknown words are ignored.

import json
import string
import sys

def main():
    # Grab our files from the names given:
    # 1) The AFINN file
    # 2) The tweet data
    afinn_file = open(sys.argv[1])
    tweet_file = open(sys.argv[2])

    # Read the AFINN scores into a dictionary
    scores = {}
    for line in afinn_file:
        term, score = line.split("\t")
        scores[term] = int(score)

    # Parse each tweet into words and total up their AFINN scores.
    tweet_scores = []
    for line in tweet_file:
        tweet = json.loads(line)
        words = tweet['text'].split() if 'text' in tweet.keys() else []

        tweet_score = 0
        for word in words:
            bare_word = word.strip(string.punctuation).lower() # Strip leading and trailing punctuation and convert to lowercase
            afinn_terms = scores.keys()
            tweet_score += scores[bare_word] if bare_word in afinn_terms else 0

        tweet_scores.append(tweet_score)

    print "\n".join(map(str, tweet_scores))

if __name__ == '__main__':
    main()
