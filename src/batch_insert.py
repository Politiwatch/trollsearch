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
    db.tweets.create_index([("$**", pymongo.TEXT)], name="text_index")

    print("Loading tweets...")
    tweets = csv_reader.read_csv(file, archive_name)

    print("Inserting tweets into database...")
    for tweet in tqdm(tweets):
        try:
            db.tweets.insert_one(tweet)
        except Exception as e:
            # print("Some issues occured while inserting the tweets:")
            # print(e)
            pass

    print("Done!")

if __name__ == "__main__":
    if not len(sys.argv) == 3:
        print("usage: ./batch_insert.py archive_path archive_name")
        sys.exit(1)
    file_name = sys.argv[1]
    archive_name = sys.argv[2]
    with open(file_name, "rb") as infile:
        batch_insert(infile, archive_name)