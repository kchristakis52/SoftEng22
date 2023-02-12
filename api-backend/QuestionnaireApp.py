from flask import Flask, render_template, jsonify, request
from pymongo import MongoClient
import json, jsonschema

schema = {
    "type": "object",
    "properties": {
        "name": {"type": "string"},
        "value": {"type": "integer"}
    },
    "required": ["name", "value"]
}

# create app and set directory for html code (default is "./templates")
app = Flask(__name__, template_folder="../frontend")


@app.route("/")
def questionnaire_test():
    return render_template("main.html")

@app.route('/submit', methods=['POST'])
def handle_submit():
    """
    print(request)
    print(request.json)
    client = MongoClient()
    db = client.questionnaire
    collection_name = 'responses'
    db[collection_name].insert_one(request.json)
    client.close()

    for i in request.json:
        print(i, request.json.get(i))
    input_data = request.json.get('input')
    # process the data
    response_data = {'input': input_data}
    resp = jsonify(response_data)
    print(resp)
    return resp
    """
    try:
        jsonschema.validate(request.json, schema)
        print("Valid JSON")
        return '{"submission":"Valid"}'
    except jsonschema.exceptions.ValidationError as e:
        print("Invalid JSON")
        return '{"submission":"Invalid"}'



if __name__ == '__main__':
    app.run(host="0.0.0.0",debug=True)