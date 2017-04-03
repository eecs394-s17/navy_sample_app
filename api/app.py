from flask import Flask
from flask_restful import Resource, Api, reqparse
from flask import abort

import csv

import uuid

import base64

import boto3
import sys, os
from os import listdir
from os.path import isfile, join
from botocore.client import ClientError

app = Flask(__name__)
api = Api(app)


class Notes(Resource):

    def __init__(self):

        # Hit AWS
        self.s3 = boto3.resource('s3')
        self.client = boto3.client('s3')

        self.notes_filepath = "notes.csv"
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('notes', type=str, required=True)


    def get(self):
        """
        serves the get endpoint
        when hit it will return all the notes
        """
        notes = []
        with open(self.notes_filepath, 'rb') as csvfile:
                    reader = csv.reader(csvfile)
                    for row in reader:
                        # TODO: strip excess spaces
                        notes.append(row)

        notes_json = { "notes" : notes }
        return notes_json

    def post(self):
        """
        a post endpoint that adds notes
        """

        args = self.parser.parse_args()
        notes = args["notes"]

        # try to save base64 image
        image = base64.decodestring(notes)

        # save base64 to somewhere on machine
        # TODO: handle different filetypes
        unique_filename = str(uuid.uuid4())
        # Upload to AWS bucket
        bucket = self.s3.Bucket("team-navy")
        exists = True
        self.s3.meta.client.head_bucket(Bucket=bucket.name)
        self.s3.Bucket(bucket.name).put_object(Key=unique_filename, Body=image)
        # write file where image was saved to csv
        with open(self.notes_filepath, 'a') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow([unique_filename])
        link_name = "https://s3.amazonaws.com/"+bucket.name+"/"+unique_filename

        info = {"bucket": "team-navy",
                "name": unique_filename}

        return info



api.add_resource(Notes, "/api/v1/notes")


if __name__ == '__main__':
    app.run(debug=True)
