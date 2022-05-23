from rest_framework.response import Response
from rest_framework import status
from django.apps import apps
from django.http import HttpResponse
from rest_framework.decorators import api_view
import json
import numpy as np
import tweepy


def tokonize(sentences, tokenizer, max_len):
    input_ids, attention_mask = [], []
    for sentence in sentences:
        inputs = tokenizer.encode_plus(sentence, add_special_tokens=True,   max_length=max_len, pad_to_max_length=True,
                                       return_attention_mask=True)
        input_ids.append(inputs['input_ids'])
        attention_mask.append(inputs['attention_mask'])

    return np.array(input_ids, dtype='int32'), np.array(attention_mask, dtype='int32')


def tokenize_data(tweet, tokenizer):
    '''
    Toknize Data sets 
    and return input_ids,attention masks  and labels
    '''
    max_len = 40
    input_ids, attention_masks = tokonize(tweet, tokenizer, max_len)
    return input_ids, attention_masks


def classify_tweet(tweet):
    server_config = apps.get_app_config('server')
    server_tokenizer = server_config.server_tokenizer
    server_model = server_config.server_model

    map = {0: 'anger', 1: 'disgust', 2: 'fear', 3: 'joy',
           4: 'sadness', 5: 'surprise', 6: 'neutral'}

    tweet_ids, tweet_mask = tokenize_data(
        [tweet], server_tokenizer)
    predictions_probabilities = server_model.predict(
        [tweet_ids, tweet_mask])
    prediction_label = map[list(
        predictions_probabilities[0]).index(max(predictions_probabilities[0]))]
    return prediction_label


@api_view(['POST'])
def index(request):
    try:
        tweet = json.loads(request.body)["text"]
        prediction = classify_tweet(tweet)
        return HttpResponse("Classification {}".format(prediction))
    except ValueError as e:
        return Response(e.args[0], status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def get_tweets(request):
    body = json.loads(request.body)
    userId = body['userId']
    # Access Token of user
    accessToken = body['accessToken']
    # Access Token secret of user
    accessTokenSecret = body['accessTokenSecret']
    # Max Result to retrieve
    max_results = 2000
    if userId:
        # Auth
        auth = tweepy.OAuth1UserHandler(
            consumer_key="pqCKc0wsOiBHZ5Sfxj5Qf0OUA",
            consumer_secret="AFeIj1XGAGyHezOVm1cGAG563rUKDqAAGshRXUuBflDTM7ZwH1",
            access_token=f"{accessToken}",
            access_token_secret=f"{accessTokenSecret}"
        )
        # Call twitter api
        global api
        api = tweepy.API(auth)
        # Get user tweets
        response = api.user_timeline(id=userId, count=max_results)
        # Getting tweets from responsse
        tweets = []
        # Labeling tweets
        text = []
        for tweet in response:
            text.append(tweet.text)
        classifications = classify_tweets(text)
        for i in range(len(response)):
            labeled_tweet = {}
            labeled_tweet['tweet'] = response[i].text
            labeled_tweet['date'] = response[i].created_at.isoformat()
            labeled_tweet['label'] = classifications[i]
            tweets.append(labeled_tweet)
        tweets = json.dumps(tweets)
        return HttpResponse(tweets)
    else:
        return Response("bad request", status.HTTP_400_BAD_REQUEST)


def classify_tweets(tweets):
    server_config = apps.get_app_config('server')
    server_tokenizer = server_config.server_tokenizer
    server_model = server_config.server_model

    map = {0: 'anger', 1: 'disgust', 2: 'fear', 3: 'joy',
           4: 'sadness', 5: 'surprise', 6: 'neutral'}
    tweet_ids, tweet_mask = tokenize_data(
        tweets, server_tokenizer)
    predictions_probabilities = server_model.predict(
        [tweet_ids, tweet_mask])
    predictions_labels = []
    for i in range(len(predictions_probabilities)):
        predictions_labels.append(map[list(
            predictions_probabilities[i]).index(max(predictions_probabilities[i]))])
    return predictions_labels


@api_view(['POST'])
def classify_multiple_tweets(request):
    body = json.loads(request.body)
    tweets = body['tweets']
    result = []
    text = []
    # Labeling tweets
    for tweet in tweets:
        text.append(tweet['text'])
    classifications = classify_tweets(text)
    for i in range(len(tweets)):
        labeled_tweet = {}
        labeled_tweet['id'] = tweets[i]['id']
        labeled_tweet['text'] = tweets[i]['text']
        labeled_tweet['label'] = classifications[i]

        labeled_tweet['userHandle'] = tweets[i]['userHandle']
        result.append(labeled_tweet)
    result = json.dumps(result)
    return HttpResponse(result)


@api_view(['POST'])
def check_follow(request):
    body = json.loads(request.body)
    screen_name = body['screen_name']
    source_id = body['source_id']
    r = api.get_friendship(source_id=source_id, target_screen_name=screen_name)
    result = json.dumps({"following": r[0].following})
    return HttpResponse(result)
