from flask import Flask, request, render_template

import pymongo
import flask_pymongo

# create app and set directory for html code (default is "./templates")
app = Flask(__name__, template_folder="../frontend")
client = pymongo.MongoClient("localhost", 27017)
db = client.queDB

@app.route("/")
def questionnaire_test():
    return render_template("main.html")


@app.route("/intelliq_api/questionnaire/<string:slug>", methods=["GET"])
def get_questionnaire(slug):
    format = request.args.get('format', "json")
    if format != "json" and format != "csv":
        return "Bad request", 400
    questionnaire = db.questionnaire.find_one({"_id": slug})
    if questionnaire is None:
        return "No data", 402
    for question in questionnaire["questions"]:
        del question["options"]
    return questionnaire, 200


@app.route("/intelliq_api/question/<string:slug1>/<string:slug2>", methods=["GET"])
def get_questionnairequestion(slug1, slug2):
    format = request.args.get('format', "json")
    if format != "json" and format != "csv":
        return "Bad request", 400
    question = list(db.questionnaire.aggregate([{'$match':{'_id': slug1}}, {'$unwind': {'path': '$questions'}}, {'$match': {'questions.qID': slug2}}, {'$unset':['keywords', 'questionnaireTitle']}, {'$project': {'qID': '$questions.qID','qtext': '$questions.qtext','required': '$questions.required','type': '$questions.type','options': '$questions.options'}}]))
    if (not bool(question))  :
        return "No data", 402
    return question, 200


if __name__ == '__main__':
    app.run(debug=True, port=9103)
