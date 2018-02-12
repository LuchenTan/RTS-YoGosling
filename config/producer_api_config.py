#!/usr/bin/env python

# kafka topic to write to
topic = 'tweets_api'

# keyword of tweets to search for, if set to 'all', it will get a sample of all tweets
keyword = 'all'

# the number of bytes to batch in memory before writing to kafka (this number should be smaller than your machine's memory)
batchsize = 100000

oauth = {
"app_key":"YRGmn95TwDBmbA0qYfHDmqK7O",
"app_secret":"IL4ptelhPxDOZbNQYSWtJmd24RPfsBdMx6zR2mmGK1A7JGLRCu",
"oauth_token":"3181517148-qtozMbindYbrYNxmhekAA7c5n5GbKoAjNxO7fRz",
"oauth_token_secret":"OGdowBugJQ2e629kWAKfcfg1gyGdHhJ2JfVFZpFlOgekW"
}

