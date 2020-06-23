from tqdm import tqdm
from datetime import date, datetime
import unicodecsv
import json
import math

def _to_int(num):
    return round(float(num))

def _strip_chars(chars, text):
    if text == None:
        text = ""
    for char in chars:
        if text.startswith(char):
            text = text[1:]
        if text.endswith(char):
            text = text[:-1]
    return text


def _get_array(string):
    string = _strip_chars(["[", "]"], string)
    data = string.split('", "')
    if '", "' in string:
        data = string.split('", "')
    elif "', '" in string:
        data = string.split("', '")
    elif ', ' in string:
        data = string.split(", ")
    else:
        data = [string]
    return [
        _strip_chars(["'", '"'], item)
        for item in filter(lambda k: k.strip() != "", data)
    ]


def try_op(operation, data, default=None):
    try:
        return operation(data)
    except:
        return default


def clean_row(raw, archive):
    # Turn tweetid, follower_count, following_count, quote_count, reply_count, like_count, retweet_count to #'s
    # Turn user_mentions,   to a proper array
    # Turn tweet_time to a datetime
    # Turn account_creation_date into a date
    # Set the `_id` field
    raw.update(
        {
            # Turn to integers
            "tweetid": int(raw["tweetid"]),
            "follower_count": try_op(_to_int, raw["follower_count"]),
            "following_count": try_op(_to_int, raw["following_count"]),
            "quote_count": try_op(_to_int, raw["quote_count"]),
            "reply_count": try_op(_to_int, raw["reply_count"]),
            "like_count": try_op(_to_int, raw["like_count"]),
            "retweet_count": try_op(_to_int, raw["retweet_count"]),
            # Turn to booleans
            "is_retweet": raw["is_retweet"] == "true",
            # Turn to real array
            "user_mentions": _get_array(raw["user_mentions"]),
            "hashtags": _get_array(raw["hashtags"]),
            "urls": _get_array(raw["urls"]),
            "poll_choices": _get_array(raw["poll_choices"]),
            # Turn to valid times
            "tweet_time": datetime.strptime(raw["tweet_time"], "%Y-%m-%d %H:%M"),
            "account_creation_date": datetime.strptime(
                raw["account_creation_date"], "%Y-%m-%d"
            ),
            # Add custom fields
            "_archive": archive,
            "_id": int(raw["tweetid"]),
        }
    )
    return raw


def process_csv(csvfile, archive, function, batch_size=1000):
    reader = unicodecsv.DictReader(csvfile)
    queue = []
    for row in tqdm(reader):
        queue.append(clean_row(row, archive))
        if len(queue) >= batch_size:
            function(queue)
            queue = []
    function(queue)