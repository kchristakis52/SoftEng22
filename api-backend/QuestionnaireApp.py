from flask import Flask, request, render_template

import pymongo
import flask_pymongo

# create app and set directory for html code (default is "./templates")
app = Flask(__name__, template_folder="../frontend")
client = pymongo.MongoClient("localhost", 27017)
db = client.queDB

@app.route("/")
def questionnaire_test():
    questionnaires = []
    for questr in db.questionnaire.find():
        questionnaires.append((questr['_id'], questr['questionnaireTitle']))
    return render_template("main.html", questionnaires=questionnaires)

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


@app.route("/RadioQuestion/<string:questionnaire_id>/<string:question_id>")
def setRadioQuestion(questionnaire_id ,question_id): #Έστω πως μπορούμε να βάλουμε ερωτήσεις με έως 6 πιθανές απαντήσεις
    qOptions = []
    for x in range(6):
        qOptions.append('None')
    questionForm = list(db.questionnaire.aggregate([{'$match':{'_id': questionnaire_id}}, {'$unwind': {'path': '$questions'}}, {'$match': {'questions.qID': question_id}}, {'$unset':['keywords', 'questionnaireTitle']}, {'$project': {'qID': '$questions.qID','qtext': '$questions.qtext','required': '$questions.required','type': '$questions.type','options': '$questions.options'}}]))
    print(len(questionForm[0].get('options')))#Gia svisimo
    if (questionForm[0].get('options')[0].get('optID'))[3] == 'T' or (questionForm[0].get('options')[0].get('optID'))[3] == 'X':
        return render_template("question_textfield.html", Question=questionForm[0].get('qtext'))
    else:
        for i in range(len(questionForm[0].get('options'))):
            
            qOptions[i] = questionForm[0].get('options')[i].get('opttxt')
        return render_template("question_radio.html", Question=questionForm[0].get('qtext'), Option1=qOptions[0], Option2=qOptions[1], Option3=qOptions[2], Option4=qOptions[3], Option5=qOptions[4], Option6=qOptions[5])


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


