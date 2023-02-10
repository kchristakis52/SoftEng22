from flask import Flask, request, render_template, jsonify, Response
import pymongo
import flask_pymongo
import uuid
import json
from urllib.request import urlopen
import pandas as pd
#from pymongo.errors import ConnectionFailure

app = Flask(__name__, template_folder="../frontend")
client = pymongo.MongoClient("localhost", 27019)
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
    if (format == "csv"):
        concatstring = ''
        for i in questionnaire['keywords']:
            concatstring += i+" "
        questionnaire['keywords']=concatstring
        df = pd.json_normalize(questionnaire, record_path=['questions'], meta=[
                               '_id', 'questionnaireTitle', 'keywords'])
        return Response(df.to_csv(), mimetype="text/csv", status=200)
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
    if (format == "csv"):
        df = pd.json_normalize(question[0], record_path=['options'], meta=[
                               '_id', 'qID', 'qtext', 'required', 'type'])
        return Response(df.to_csv(), mimetype="text/csv", status=200)
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
    if (format == "csv"):
        df = pd.json_normalize(question[0], record_path=[
                               'answers'], meta=['_id', 'session'])
        return Response(df.to_csv(), mimetype="text/csv", status=200)
    return jsonify(question[0]), 200


@app.route("/intelliq_api/getquestionanswers/<string:slug1>/<string:slug2>", methods=["GET"])
def get_questionanswers(slug1, slug2):
    format = request.args.get('format', "json")
    if format != "json" and format != "csv":
        return "Bad request", 400
    question = list(db.responses.aggregate([
        {
            '$match': {
                'questionnaireID': slug1,
                'qID': slug2
            }
        }, {
            '$group': {
                '_id': '$questionnaireID',
                'qID': {
                    '$first': '$qID'
                },
                'answers': {
                    '$push': {
                        'session': '$session',
                        'ans': '$ans'
                    }
                }
            }
        }
    ]))
    if (not bool(question)):
        return "No data", 402
    if (format == "csv"):
        df = pd.json_normalize(question[0], record_path=[
                               'answers'], meta=['_id', 'qID'])
        return Response(df.to_csv(), mimetype="text/csv", status=200)
    return jsonify(question[0]), 200


@app.route("/intelliq_api/doanswer/<string:questionnaireID>/<string:questionID>/<string:session>/<string:optionID>", methods=["POST"])
def postreponse(questionnaireID, questionID, session, optionID):
    db.responses.insert_one({
        "questionnaireID": questionnaireID,
        "session": session,
        "qID": questionID,
        "ans": optionID
    })
    return Response(status=204)

# diaxeiristika 
@app.route("/intelliq_api/admin/healthcheck", methods=["GET"])



@app.route("/intelliq_api/admin/questionnaire_upd", methods=["POST"])




@app.route("/intelliq_api/admin/resetall", methods=["POST", "GET"])
def resetall():
    result =  {"status":"OK"}
    try:
        if db.responses.drop():
            if db.questionnaire.drop():
                return jsonify(result), 200
    except:
        if db.responses == None or db.questionnaire == None:
            result =  {"status":"failed", "reason": "Bad request"}
            return jsonify(result), 400
        
    result =  {"status":"failed", "reason": "Internal server error"}
    return jsonify(result), 500
        
# resets all questionnaires, answers, users
# success -> json object: {"status":"OK"}
# else -> {"status":"failed", "reason":<...>}






@app.route("/intelliq_api/admin/resetq/<string:questionnaireID>", methods=["POST"])
# deletion of answers of the questionnaire with id questionnaireID,
# success -> json object: {"status":"OK"}
# else -> {"status":"failed", "reason":<...>}








# The aboves are APIs                    --/\--
#                                          ||
#                                          ||
#                                                              ||
#                                                              ||
# The belows are pages of the website                        --\/--


@app.route("/intelliq_api/answerquestion/<string:session_id>/<string:questionnaire_id>/<string:question_id>")
def setRadioQuestion(questionnaire_id, question_id, session_id):
    if question_id == '-':
        return render_template("landingpage.html")
    qOptions = []  # Yes No Maybe
    qNextIDs = []  # Next question is nextqID
    qDiffOptions = []  # optID(Yes) optID(No) optID(Maybe)

    url = "http://127.0.0.1:9103/intelliq_api/question/" + questionnaire_id + '/' + question_id
    response = urlopen(url)    # Convert bytes to string type and string type to dict
    string = response.read().decode('utf-8')
    questionForm = json.loads(string)
    questionForm = [questionForm]

#    questionForm = list(db.questionnaire.aggregate([{'$match': {'_id': questionnaire_id}}, {'$unwind': {'path': '$questions'}}, {'$match': {'questions.qID': question_id}}, {'$unset': [
#                        'keywords', 'questionnaireTitle']}, {'$project': {'qID': '$questions.qID', 'qtext': '$questions.qtext', 'required': '$questions.required', 'type': '$questions.type', 'options': '$questions.options'}}]))
    
#    print(len(questionForm[0].get('options')))  # Gia svisimo
    print(question_id)
   
    if (len(questionForm[0].get('options'))) == 1:
        return render_template("question_textfield.html", Question=questionForm[0].get('qtext'), questionnaire_id=questionnaire_id, nextQuestion_id=questionForm[0].get('options')[0].get('nextqID'), optionID=questionForm[0].get('options')[0].get('optID'), question_id=question_id, session_id=session_id)
    else:
        for i in range(len(questionForm[0].get('options'))):
            qOptions.append(questionForm[0].get('options')[i].get('opttxt'))
            qNextIDs.append(questionForm[0].get('options')[i].get('nextqID'))
            qDiffOptions.append(questionForm[0].get('options')[i].get('optID'))
            # print(qNextIDs[j]) # gia svisimo
        return render_template("question_radio.html", Question=questionForm[0].get('qtext'), qOptions=qOptions, questionnaire_id=questionnaire_id, qNextIDs=qNextIDs, qDiffOptions=qDiffOptions, question_id=question_id, session_id=session_id)


@app.route("/intelliq_api/showsessionanswers/<string:slug1>/<string:slug2>", methods=["GET"])
def session_answers(slug1, slug2):
    url = "http://127.0.0.1:9103/intelliq_api/getsessionanswers/" + slug1 + '/' + slug2
    # Convert bytes to string type and string type to dict
    response = urlopen(url)
    string = response.read().decode('utf-8')
    session_dict = json.loads(string)

    for j in session_dict['answers']:
        url2 = "http://127.0.0.1:9103/intelliq_api/question/" + slug1 + '/' + j['qID']
        response2 = urlopen(url2)    # Convert bytes to string type and string type to dict
        string2 = response2.read().decode('utf-8')
        bigQuestion =  json.loads(string2)
        j['qID'] = bigQuestion['qtext']
        for k in bigQuestion['options']:
            if k['optID'] == j['ans']:
                j['ans']=k['opttxt']
    
    
    for i in session_dict['answers']:
        print(i)
    print(session_dict)
    return render_template("session_answers.html", session_dict=session_dict)


@app.route("/")
def questionnaire_test():
    session_id = str(uuid.uuid4())[:4]
    print(session_id)
    questionnaires = []
    for questr in db.questionnaire.find():
        questionnaires.append(
            (questr['_id'], questr['questionnaireTitle'], questr['questions'][0]['qID']))
    return render_template("main.html", questionnaires=questionnaires, session_id=session_id)


if __name__ == '__main__':
    app.run(debug=True, port=9103)
