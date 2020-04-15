#!/usr/bin/env python3

import database
import pymongo
import os
import datetime
import json
import dateparser
from flask import Flask, make_response
from flask_cors import CORS
from flask_restful import Resource, Api, reqparse

app = Flask(__name__)
api = Api(app)
db = database.get_client()["twitter"]
CORS(app)


@api.representation("application/json")
def output_json(data, code, headers=None):
    def _clean(o):
        if isinstance(o, list):
            return [_clean(item) for item in o]
        if isinstance(o, dict):
            return {k: _clean(v) for k, v in o.items()}
        if isinstance(o, datetime.datetime):
            return o.__str__()
        return o

    resp = make_response(json.dumps(_clean(data)), code)
    resp.headers.extend(headers or {})
    return resp


class SearchResource(Resource):
    def get(self):
        parser = reqparse.RequestParser()

        # PARSE ARGUMENTS

        # Page
        parser.add_argument("page", type=int, help="Page to display")

        # Archives
        parser.add_argument(
            "archive", type=str, action="append", help="Archive to include"
        )

        # Languages
        parser.add_argument(
            "language", type=str, action="append", help="Language to include"
        )

        # Content
        parser.add_argument("query", type=str, help="Text search query")

        # Date
        parser.add_argument(
            "min_time", type=dateparser.parse, help="Minimum publishing date"
        )
        parser.add_argument(
            "max_time", type=dateparser.parse, help="Maximum publishing date"
        )

        # Likes
        parser.add_argument("min_likes", type=int, help="Minimum likes")
        parser.add_argument("max_likes", type=int, help="Maximum likes")

        # Followers
        parser.add_argument("min_followers", type=int, help="Minimum followers")
        parser.add_argument("max_followers", type=int, help="Maximum followers")

        # Retweets
        parser.add_argument("min_retweets", type=int, help="Minimum retweets")
        parser.add_argument("max_retweets", type=int, help="Maximum retweets")

        # Hashtags
        parser.add_argument(
            "hashtag", type=str, action="append", help="Hashtag to include"
        )

        # Account
        parser.add_argument(
            "account", type=str, action="append", help="Account to include"
        )

        # Sorts (likes, retweets, quotes, followers, time published)
        def sort_field(s):
            if s[0:4] not in ["asc_", "dec_"]:
                raise "sort must start with + or -"
            if s[4:] not in [
                "like_count",
                "retweet_count",
                "quote_count",
                "follower_count",
                "tweet_time",
            ]:
                raise "invalid sort field"
            return (s[4:], pymongo.ASCENDING if s[0:4] == "asc_" else pymongo.DESCENDING)

        parser.add_argument(
            "sort",
            type=sort_field,
            help="Sort field (starts with asc_ or dec_)",
            default="dec_like_count",
        )

        args = parser.parse_args()

        # PERFORM SEARCH
        params = {}

        if args["archive"] != None:
            params["archive"] = {"$in": args["archive"]}

        if args["language"] != None:
            params["tweet_language"] = {"$in": args["language"]}

        if args["query"] != None:
            params["$text"] = {"$search": args["query"]}

        time_range = {}
        if args["min_time"] != None:
            time_range["$gte"] = args["min_time"]
        if args["max_time"] != None:
            time_range["$lte"] = args["max_time"]
        if time_range != {}:
            params["tweet_time"] = time_range

        like_range = {}
        if args["min_likes"] != None:
            like_range["$gte"] = args["min_likes"]
        if args["max_likes"] != None:
            like_range["$lte"] = args["max_likes"]
        if like_range != {}:
            params["like_count"] = like_range

        follower_range = {}
        if args["min_followers"] != None:
            follower_range["$gte"] = args["min_followers"]
        if args["max_followers"] != None:
            follower_range["$lte"] = args["max_followers"]
        if follower_range != {}:
            params["follower_count"] = follower_range

        retweet_range = {}
        if args["min_retweets"] != None:
            retweet_range["$gte"] = args["min_retweets"]
        if args["max_retweets"] != None:
            retweet_range["$lte"] = args["max_retweets"]
        if retweet_range != {}:
            params["retweet_count"] = retweet_range

        if args["hashtag"] != None:
            params["hashtags"] = {"$elemMatch": {"$in": args["hashtag"]}}

        if args["account"] != None:
            params["userid"] = {"$in": args["account"]}

        if type(args["sort"]) == str:
            args["sort"] = [args["sort"]]

        return {
            "total": db.tweets.count_documents(params),
            "results": list(
                db.tweets.find(params).sort(*args["sort"]).skip((args["page"] or 0) * 25).limit(25)
            ),
        }


class StatsResource(Resource):
    def get(self):
        # total # of tweets
        # names & counts of each archive
        # last updated
        # eventually: aggregate stats (averages, etc)
        return {
            "total_tweets": db.tweets.count_documents({}),
            "archives": [
                {
                    "name": archive,
                    "tweets": db.tweets.count_documents({"_archive": archive}),
                }
                for archive in db.tweets.distinct("_archive")
            ],
        }


api.add_resource(StatsResource, "/")
api.add_resource(SearchResource, "/search")

if __name__ == "__main__":
    app.run(debug=os.getenv("DEBUG", "False") == "True")
