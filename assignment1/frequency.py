# 1.4. Derive the sentiment of new terms
# Joyce Tipping
# Coursera | Intro to Data Sci | Dr. Howe

# This script takes a file of twitter data and outputs a histogram of term
# frequencies.

import json
import string
import sys

def main():
    # Grab the name of our tweet file from the arguments list.
    tweet_file = open(sys.argv[1])

    # Build a dictionary of terms and how many times we encounter each.
    # Also keep a running total of all terms encountered.
    frequencies = {}
    total_terms = 0
    for line in tweet_file:
        # Split each line into a list of words, making sure to strip leading and trailing punctuation and lowercasing everything.
        tweet = json.loads(line)
        words = map(lambda word: word.strip(string.punctuation).lower(), tweet['text'].split()) if 'text' in tweet.keys() else []
        total_terms += len(words)
        for word in words:
            if word in frequencies.keys():
                frequencies[word] += 1
            else:
                frequencies[word] = 1

    # Output the frequency of each term.
    for word in frequencies:
      print word + ' ' + str(frequencies[word] / float(total_terms))

if __name__ == '__main__':
    main()
