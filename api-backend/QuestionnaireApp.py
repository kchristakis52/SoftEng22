from flask import Flask, request, render_template, jsonify
import csv
import pymongo
import flask_pymongo

def normalize_json(data: dict) -> dict:
    new_data = dict()
    for key, value in data.items():
        if not isinstance(value, dict):
            new_data[key] = value
        else:
            for k, v in value.items():
                new_data[key + "_" + k] = v
      
    return new_data

# create app and set directory for html code (default is "./templates")
app = Flask(__name__, template_folder="../frontend")
client = pymongo.MongoClient("localhost", 27017)
db = client.queDB
app.config['JSON_AS_ASCII'] = False


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
    if (format=="csv"):
        return 
    return jsonify(questionnaire), 200


@app.route("/intelliq_api/question/<string:slug1>/<string:slug2>", methods=["GET"])
def get_questionnairequestion(slug1, slug2):
    format = request.args.get('format', "json")
    if format != "json" and format != "csv":
        return "Bad request", 400
    question = list(db.questionnaire.aggregate([{'$match': {'_id': slug1}}, {'$unwind': {'path': '$questions'}}, {'$match': {'questions.qID': slug2}}, {'$unset': ['keywords', 'questionnaireTitle']}, {
                    '$project': {'qID': '$questions.qID', 'qtext': '$questions.qtext', 'required': '$questions.required', 'type': '$questions.type', 'options': '$questions.options'}}]))
    if (not bool(question)):
        return "No data", 402
    return jsonify(question[0]), 200


@app.route("/intelliq_api/getsessionanswers/<string:slug1>/<string:slug2>", methods=["GET"])
def get_sessionanswers(slug1, slug2):
    format = request.args.get('format', "json")
    if format != "json" and format != "csv":
        return "Bad request", 400
    question = list(db.responses.aggregate([
        {
            '$match': {
                'questionnaireID': slug1,
                'session': slug2
            }
        }, {
            '$group': {
                '_id': '$questionnaireID',
                'session': {
                    '$first': '$session'
                },
                'answers': {
                    '$push': {
                        'qID': '$qID',
                        'ans': '$ans'
                    }
                }
            }
        }
    ]))

    if (not bool(question)):
        return "No data", 402
    return question, 200


@app.route("/intelliq_api/doanswer/<string:questionnaireID>/<string:questionID>/<string:session>/<string:optionID>", methods=["POST"])
def postreponse(questionnaireID, questionID, session, optionID):
    db.responses.insert_one({
        "questionnaireID": questionnaireID,
        "session": session,
        "qID": questionID,
        "ans": optionID
    })


# The aboves are APIs                  --/\--
#                                          ||
#                                          ||
#                                                              ||
#                                                              ||
# The belows are pages of the website                      --\/--


@app.route("/RadioQuestion/<string:questionnaire_id>/<string:question_id>")
def setRadioQuestion(questionnaire_id, question_id):
    qOptions = []
    qNextIDs = []
    questionForm = list(db.questionnaire.aggregate([{'$match': {'_id': questionnaire_id}}, {'$unwind': {'path': '$questions'}}, {'$match': {'questions.qID': question_id}}, {'$unset': [
                        'keywords', 'questionnaireTitle']}, {'$project': {'qID': '$questions.qID', 'qtext': '$questions.qtext', 'required': '$questions.required', 'type': '$questions.type', 'options': '$questions.options'}}]))
    print(len(questionForm[0].get('options')))  # Gia svisimo
    if (questionForm[0].get('options')[0].get('optID'))[3] == 'T' or (questionForm[0].get('options')[0].get('optID'))[3] == 'X':
        return render_template("question_textfield.html", Question=questionForm[0].get('qtext'), questionnaire_id=questionnaire_id, nextQuestion_id=questionForm[0].get('options')[0].get('nextqID'))
    else:
        for i in range(len(questionForm[0].get('options'))):
            qOptions.append(questionForm[0].get('options')[i].get('opttxt'))
            qNextIDs.append(questionForm[0].get('options')[i].get('nextqID'))
            # print(qNextIDs[j]) # gia svisimo
        return render_template("question_radio.html", Question=questionForm[0].get('qtext'), qOptions=qOptions, questionnaire_id=questionnaire_id, qNextIDs=qNextIDs)


@app.route("/")
def questionnaire_test():
    questionnaires = []
    for questr in db.questionnaire.find():
        questionnaires.append(
            (questr['_id'], questr['questionnaireTitle'], questr['questions'][0]['qID']))
    return render_template("main.html", questionnaires=questionnaires)


if __name__ == '__main__':
    app.run(debug=True, port=9103)
