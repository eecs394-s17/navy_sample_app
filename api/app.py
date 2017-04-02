from flask import Flask
from flask_restful import Resource, Api
import csv


app = Flask(__name__)
api = Api(app)


class Notes(Resource):

    def __init__(self):

        self.notes = []

        with open('notes.csv', 'rb') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                # TODO: strip excess spaces
                self.notes.append(row)

    def get(self):
        """
        serves the get endpoint
        when hit it will return all the notes
        """

        notes_json = { "notes" : self.notes }
        return notes_json

    def post(self):
        return "Not implemented"


api.add_resource(Notes, "/api/v1/notes")


if __name__ == '__main__':
    app.run(debug=True)
