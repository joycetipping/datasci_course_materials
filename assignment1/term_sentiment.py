# 1.3. Derive the sentiment of new terms
# Joyce Tipping
# Coursera | Intro to Data Sci | Dr. Howe

# This script takes an AFINN file and a file of twitter data and derives scores
# for the unknown terms in the tweets based on the known terms around them.
#
# Each computed score adheres to the original scoring schema of being an
# integer between -5 and 5.

import json
import string
import sys

def main():
    # Grab our files from the names given:
    # 1) The AFINN file
    # 2) The tweet data
    afinn_file = open(sys.argv[1])
    tweet_file = open(sys.argv[2])

    # Parse the AFINN scores into a dictionary; create a list of AFINN terms.
    afinn_pairs = {}
    afinn_terms = []
    for line in afinn_file:
        term, score = line.split("\t")
        afinn_pairs[term] = int(score)
        afinn_terms.append(term)

    # Build a dictionary of new terms and their association data.
    #
    # Let us define "associated terms" as known terms that appear in the same
    # tweet as our new term. Each entry will be as follows:
    #
    #    new term => [ sum of AFINN scores of associated terms, number of associated terms ]
    #
    # Note that other new terms are not counted.
    #
    # We store running totals instead of calculating the mean of each tweet
    # (and later taking the mean of means) because that would weight the result
    # in favor of tweets with fewer known terms.
    #
    assc_scores = {}
    for line in tweet_file:
        # Split each line into a list of words, making sure to strip leading and trailing punctuation and lowercasing everything.
        tweet = json.loads(line)
        words = map(lambda word: word.strip(string.punctuation).lower(), tweet['text'].split()) if 'text' in tweet.keys() else []

        # Loop through the words, compiling a list of new words and scoring the tweet's existing words.
        new = []
        old = []
        score = 0
        for word in words:
            if word in afinn_terms:
                old.append(word)
                score += afinn_pairs[word]
            else:
                new.append(word)

        # Enter each new word in the association dictionary, along with its running totals as detailed above.
        for new_term in new:
            if new_term in assc_scores.keys():
                assc_scores[new_term][0] += score
                assc_scores[new_term][1] += len(old)
            else:
                assc_scores[new_term] = [score, len(old)]

    # For each new term, calculate the mean of the AFINN score of associated terms; round to the nearest integer.
    for term in assc_scores:
      total, count = assc_scores[term]
      score = int(round(float(total) / count)) if count > 0 else 0
      print term + ' ' + str(score)

if __name__ == '__main__':
    main()
