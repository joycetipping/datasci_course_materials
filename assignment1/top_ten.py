# 1.6. Find the top ten hashtags
# Joyce Tipping
# Coursera | Intro to Data Sci | Dr. Howe

import json
import sys

def main():
    tweet_file = open(sys.argv[1])

    # Retrieve the hashtags in each tweet and record its occurence.
    hashtags_count = {}
    for line in tweet_file:
        tweet = json.loads(line)
        hashtags = map(lambda tag: tag['text'], tweet['entities']['hashtags'])
        for hashtag in hashtags:
            if hashtag in hashtags_count.keys():
                hashtags_count[hashtag] += 1
            else:
                hashtags_count[hashtag] = 1

    # Reverse the hashtag dictionary so that each hashtag is listed under its count.
    count_hashtags = {}
    for tag, count in hashtags_count.items():
        if count in count_hashtags.keys():
            count_hashtags[count].append(tag)
        else:
            count_hashtags[count] = [tag]

    # Print the ten hashtags with the highest counts. In the event of an n-way tie, the tags are taken in alphabetical order.
    sorted_counts = sorted(count_hashtags.keys(), reverse=True)
    number = 0
    for count in sorted_counts:
        for tag in sorted(count_hashtags[count]):
            if number < 10:
                print tag + ' ' + str(float(count))
                number += 1

if __name__ == '__main__':
    main()
