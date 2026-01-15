from textblob import TextBlob

def get_sentiment(text):
    polarity = TextBlob(text).sentiment.polarity
    if polarity < -0.3:
        return "angry"
    elif polarity > 0.3:
        return "happy"
    return "neutral"
