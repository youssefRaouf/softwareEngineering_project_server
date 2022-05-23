from django.urls import path

from . import routes
urlpatterns = [
    path('classify', routes.index, name='index'),
    path('tweets', routes.get_tweets, name='get_tweets'),
    path('classifyMultipleTweets', routes.classify_multiple_tweets, name='classify_multiple_tweets'),
    path('checkFollow', routes.check_follow, name='check_follow'),
]