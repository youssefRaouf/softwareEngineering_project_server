from django.test import TestCase
from server.routes import classify_tweet, classify_tweets

# command python3.9 manage.py test server.tests.test_labels.TestLabels
# command python3.9 manage.py test server.tests.test_runtime.TestRunTime

ClassifySingle_tweet_dict = [{'text': 'Al Ahly just reached the third final in a row.What an amazing achievement.',
                              'label': 'joy'},

                             {'text': 'The goals in yesterday match was unexpected 😯😯😯',
                              'label': 'surprise'
                              },
                              {'text': "I can't tolerate that anymore 😡",
                                'label': 'anger'},
                                {
                                    'text': "I'm very upset from her reaction",
                                    'label':  'sadness'
                                },
                                {
                                    'text': "the food in this restaurant was so awful",
                                    'label': "disgust"
                                },
                                {
                                    'text': "I'm worried about my upcoming exams",
                                    'label':"fear"
                                },
                                {
                                    'text': "What is now the fully developed Las Vegas strip, 1955.",
                                    'label': 'neutral'
                                }
                              ]

ClassifyMultiple_tweet_dict = {
    'texts': [
        "Al Ahly just reached the third final in a row.What an amazing achievement.",
        "The goals in yesterday match was unexpected 😯😯😯",
        "I can't tolerate that anymore 😡",
        "I'm very upset from her reaction",
        "the food in this restaurant was so awful",
        "I'm worried about my upcoming exams",
        "What is now the fully developed Las Vegas strip, 1955.",

        "Pablo's new song is very bad to be honest",
        "Did the sphinx close his eyes ? 🤔",
        "I am a bit frustrated about Mo Salah injury",
        "What happened yesterday was not fair! Nobody could score a penalty in the face of multiple lasers in their eyes!  #MoSalah #Egypt #FIFAWorldCup",
        "Enough is Enough !",
        "i'm fear of corona virus",
        "I'm really afraid from this situation 😬",
        "In love with supportive people ❤️❤️❤️",
        "Sadness is temporary it's not the end",
        "It was a great birthday surprise",
        "Meeting my swedish friend made me happy yesterday",
        "My last breakup made me feel sad",
        "It is such a shame that we play strangers, no act to change what we have become :(("
    ],
    'labels': [
        'joy',
        'surprise',
        'anger',
        'sadness',
        'disgust',
        'fear',
        'neutral',

        'sadness',
        'surprise',
        'anger',
        'anger',
        'neutral',
        'fear',
        'fear',
        'joy',
        'neutral', 
        'joy',
        'joy',
        'sadness',
        'sadness'
        
    ]}
class TestLabels(TestCase):

    def test_ClassifySingleTweet(self):
        # Assert
        for tweet in ClassifySingle_tweet_dict:
            self.assertEquals(classify_tweet(tweet['text']),tweet['label'])


    def test_ClassiftMultipleTweets(self):
        self.assertEquals(classify_tweets(ClassifyMultiple_tweet_dict['texts']),ClassifyMultiple_tweet_dict['labels'])










