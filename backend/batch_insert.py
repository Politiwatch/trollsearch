#!/usr/bin/env python3

import sys
import database
from tqdm import tqdm
import csv_reader
import pymongo

def batch_insert(file, archive_name):
    print("Connecting to database...")
    db = database.get_client()["twitter"]

    print("Creating indexes...")
    db.tweets.create_index([("$**", pymongo.TEXT)], name="text_index", background=True)
    db.tweets.create_index([("tweet_language", pymongo.ASCENDING)], name="language_index", background=True)
    db.tweets.create_index([("_archive", pymongo.ASCENDING)], name="archive_index", background=True)
    db.tweets.create_index([("like_count", pymongo.DESCENDING)], name="like_index", background=True)
    db.tweets.create_index([("retweet_count", pymongo.DESCENDING)], name="retweet_index", background=True)
    db.tweets.create_index([("follower_count", pymongo.DESCENDING)], name="follower_index", background=True)


    print("Loading & inserting tweets...")
    def _insert(queue):
        try:
            db.tweets.insert_many(queue)
        except Exception as e:
            print(e)
            # Try individually
            for item in queue:
                try:
                    db.tweets.insert_one(item)
                except Exception as e2:
                    # print(e2)
                    pass
    csv_reader.process_csv(file, archive_name, _insert, batch_size=20000)

    print("Done!")

if __name__ == "__main__":
    if not len(sys.argv) == 3:
        print("usage: ./batch_insert.py archive_path archive_name")
        sys.exit(1)
    file_name = sys.argv[1]
    archive_name = sys.argv[2]
    with open(file_name, "rb") as infile:
        batch_insert(infile, archive_name)