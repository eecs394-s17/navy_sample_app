from flask import Flask
from flask_restful import Resource, Api, reqparse
import csv



app = Flask(__name__)
api = Api(app)


class Notes(Resource):

    def __init__(self):

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
        """
        args = self.parser.parse_args()
        notes = args["notes"]

        print notes

        with open(self.notes_filepath, 'a') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow([notes])

        return "Notes Uploaded"


api.add_resource(Notes, "/api/v1/notes")


if __name__ == '__main__':
    app.run(debug=True)
