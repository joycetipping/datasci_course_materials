# 1.5. Which state is happiest?
# Joyce Tipping
# Coursera | Intro to Data Sci | Dr. Howe

# This script takes an AFINN file and a file of twitter data and determines
# which state is the happiest based on scores of the tweets coming from it.

import json
import re
import string
import sys


def main():
    # Grab our files from the names given:
    # 1) The AFINN file
    # 2) The tweet data
    afinn_file = open(sys.argv[1])
    tweet_file = open(sys.argv[2])

    # Read the AFINN scores into a dictionary
    afinn_scores = {}
    for line in afinn_file:
        term, score = line.split("\t")
        afinn_scores[term] = int(score)

    # Define a dictionary for mapping state names to abbreviations {{{
    # Thanks to http://code.activestate.com/recipes/577305/
    state_to_abbreviation = {
                          'Alaska': 'AK',
                         'Alabama': 'AL',
                        'Arkansas': 'AR',
                  'American Samoa': 'AS',
                         'Arizona': 'AZ',
                      'California': 'CA',
                        'Colorado': 'CO',
                     'Connecticut': 'CT',
            'District of Columbia': 'DC',
                        'Delaware': 'DE',
                         'Florida': 'FL',
                         'Georgia': 'GA',
                            'Guam': 'GU',
                          'Hawaii': 'HI',
                            'Iowa': 'IA',
                           'Idaho': 'ID',
                        'Illinois': 'IL',
                         'Indiana': 'IN',
                          'Kansas': 'KS',
                        'Kentucky': 'KY',
                       'Louisiana': 'LA',
                   'Massachusetts': 'MA',
                        'Maryland': 'MD',
                           'Maine': 'ME',
                        'Michigan': 'MI',
                       'Minnesota': 'MN',
                        'Missouri': 'MO',
        'Northern Mariana Islands': 'MP',
                     'Mississippi': 'MS',
                         'Montana': 'MT',
                        'National': 'NA',
                  'North Carolina': 'NC',
                    'North Dakota': 'ND',
                        'Nebraska': 'NE',
                   'New Hampshire': 'NH',
                      'New Jersey': 'NJ',
                      'New Mexico': 'NM',
                          'Nevada': 'NV',
                        'New York': 'NY',
                            'Ohio': 'OH',
                        'Oklahoma': 'OK',
                          'Oregon': 'OR',
                    'Pennsylvania': 'PA',
                     'Puerto Rico': 'PR',
                    'Rhode Island': 'RI',
                  'South Carolina': 'SC',
                    'South Dakota': 'SD',
                       'Tennessee': 'TN',
                           'Texas': 'TX',
                            'Utah': 'UT',
                        'Virginia': 'VA',
                  'Virgin Islands': 'VI',
                         'Vermont': 'VT',
                      'Washington': 'WA',
                       'Wisconsin': 'WI',
                   'West Virginia': 'WV',
                         'Wyoming': 'WY'
    }
    # }}}

    # Find the happiest state.
    state_scores = {}
    for line in tweet_file:
        tweet = json.loads(line)

        # We only consider tweet data that is a new tweet (as opposed to a deletion), that has a 'place' attribute, and that is in the US.
        if 'text' in tweet.keys() and tweet['place'] and tweet['place']['country_code'] == 'US':

            # Determine which state the user is tweeting from. If a state cannot be found, the tweet is skipped.
            #
            # The most useful data attribute is the place -> full_name. This comes in two flavors:
            #     1. city, state  =>  Albuquerque, NM
            #     2. state, US    =>  New Mexico, US
            # We will assume the first case and then check for and handle the second case.
            #
            match = re.search('^([^,]*),\s*([A-Z]+$)', tweet['place']['full_name'])
            if match:
                state = match.group(2).upper()
                if state == 'US':
                    state = state_to_abbreviation[match.group(1)]

                # Find the AFINN score of the tweet.
                words = tweet['text'].split() if 'text' in tweet.keys() else []
                tweet_score = 0
                for word in words:
                    bare_word = word.strip(string.punctuation).lower() # Strip leading and trailing punctuation and convert to lowercase
                    tweet_score += afinn_scores[bare_word] if bare_word in afinn_scores.keys() else 0

                # Keep a running total of each state's tweet scores.
                if state in state_scores.keys():
                    state_scores[state] += tweet_score
                else:
                    state_scores[state] = tweet_score

    # Print out the happiest state. In the case of a tie, print all of them.
    highest_score = 0
    happiest_state = []
    for state in state_scores:
        score = state_scores[state]
        if score > highest_score:
            highest_score = score
            happiest_state = [state]
        elif score == highest_score:
            happiest_state.append(state)
    print "\n".join(happiest_state)

if __name__ == '__main__':
    main()
