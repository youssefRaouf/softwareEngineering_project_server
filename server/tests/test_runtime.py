import random

from django.test import SimpleTestCase
import time
from server.routes import classify_tweet, classify_tweets
from server.tests.test_labels import ClassifySingle_tweet_dict,ClassifyMultiple_tweet_dict


class TestRunTime(SimpleTestCase):
    def test_Classifytweet(self):

        # Choose Random tweet
        rand = random.randint(0, len(ClassifySingle_tweet_dict)-1);
        print(rand);
        # Tweet
        tweet = ClassifySingle_tweet_dict[rand]['text'];
        print(tweet);
        # Start timer
        start_time = time.time()
        #Classify
        classify_tweet(tweet)
        # End Timer
        timeTaken = time.time()-start_time;

        # In milliseconds
        #print(f"Time Taken in milliseconds Classify Single Random Tweet {timeTaken*1000}")

        # threshold
        threshold = 500

        assert timeTaken<=threshold

    def test_MultipleTweets(self):
        # Start timer
        start_time = time.time()
        # Classify
        classify_tweets(ClassifyMultiple_tweet_dict['texts'])
        # End Timer
        timeTaken = time.time() - start_time;

        # In milliseconds
        #print(f"Time Taken in milliseconds Classify Multiple tweets {timeTaken*1000}")

        # threshold 500 * number of tweets
        threshold = 500*len(ClassifyMultiple_tweet_dict['texts']);

        assert timeTaken <= threshold

