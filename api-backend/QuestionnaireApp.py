from flask import Flask, request, render_template, jsonify, Response
import pymongo
import flask_pymongo
import uuid
import json
from urllib.request import urlopen
import pandas as pd
from pymongo.errors import ConnectionFailure

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
    if (format == "csv"):
        concatstring = ''
        for i in questionnaire['keywords']:
            concatstring += i+" "
        questionnaire['keywords'] = concatstring
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
def healthcheck():
    response = {"status": "OK", "dbconnection": "localhost, 27017"}
    try:
        client.admin.command('ismaster')
    except Exception as e:
        response = {"status": "failed", "dbconnection": str(e)}
        return jsonify(response), 500
    return jsonify(response), 200


@app.route("/intelliq_api/admin/questionnaire_upd", methods=["POST"])
def questionnaireupd():
    file = request.files['file']
    if file:
        try:
            filename = file.filename
            if filename.endswith('.json') or filename.endswith('.csv'):
                Collection = db.questionnaire
                data = json.loads(file.read().decode('utf-8'))
                if type(data) == dict:
                    data = [data]
                for file_data in data:
                    file_data["_id"] = file_data.pop("questionnaireID")
                    Collection.insert_one(file_data)
                response = {"status": "OK"}
                return jsonify(response), 200

            else:
                response = {"status": "failed", "reason": "Invalid file type"}
                return jsonify(response), 500
                
        except Exception as e:
            response = {"status": "failed", "dbconnection": str(e)}
            return jsonify(response), 500
    else:
        response = {"status": "failed", "reason": "No file found!"}
        return jsonify(response), 500


@app.route("/intelliq_api/admin/resetall", methods=["POST"])
def resetall():
    result = {"status": "OK"}
    try:
        db.responses.drop() 
        db.questionnaire.drop()
        return jsonify(result), 200
    except Exception as e:
        result = {"status": "failed", "reason": str(e)}
        return jsonify(result), 500


@app.route("/intelliq_api/admin/resetq/<string:questionnaireID>", methods=["POST"])
def questionnaireIDreset(questionnaireID):
    result = {"status": "OK"}
    try:
        db.responses.delete_many({'questionnaireID': questionnaireID})
        return jsonify(result), 200

    except Exception as e:
        result = {"status": "failed", "reason": str(e)}
        return jsonify(result), 500


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
    # Convert bytes to string type and string type to dict
    response = urlopen(url)
    string = response.read().decode('utf-8')
    questionForm = json.loads(string)
    questionForm = [questionForm]

    if (len(questionForm[0].get('options'))) == 1:
        return render_template("question_textfield.html", Question=questionForm[0].get('qtext'), questionnaire_id=questionnaire_id, nextQuestion_id=questionForm[0].get('options')[0].get('nextqID'), optionID=questionForm[0].get('options')[0].get('optID'), question_id=question_id, session_id=session_id)
    else:
        for i in range(len(questionForm[0].get('options'))):
            qOptions.append(questionForm[0].get('options')[i].get('opttxt'))
            qNextIDs.append(questionForm[0].get('options')[i].get('nextqID'))
            qDiffOptions.append(questionForm[0].get('options')[i].get('optID'))

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
        
        response2 = urlopen(url2)
        string2 = response2.read().decode('utf-8')
        bigQuestion = json.loads(string2)
        j['qID'] = bigQuestion['qtext']
        for k in bigQuestion['options']:
            if k['optID'] == j['ans']:
                j['ans'] = k['opttxt']

    return render_template("session_answers.html", session_dict=session_dict)

# Give Questions of a Questionnaire(with IDs)


@app.route("/intelliq_api/showquestions/<string:questionnaireID>", methods=["GET"])
def questions(questionnaireID):
    url = "http://127.0.0.1:9103/intelliq_api/questionnaire/" + questionnaireID
    
    response = urlopen(url)
    string = response.read().decode('utf-8')
    questionSet = json.loads(string)

    questionText = []
    for q in questionSet['questions']:
        questionText.append((q['qtext'], q['qID']))

    return render_template("question_List.html", questions=questionText, questionnaireID=questionnaireID)

# Pass question stats to pie chart - Unfinished


@app.route("/intelliq_api/showquestionanswers/<string:questionnaireID>/<string:qID>", methods=["GET"])
def question_answers(questionnaireID, qID):
    statistics = list(db.responses.aggregate([
        {
            '$match': {
                'questionnaireID': questionnaireID,
                'qID': qID
            }
        }, {
            '$sortByCount': '$ans'
        }
    ]))
    print(statistics)

    url = "http://127.0.0.1:9103/intelliq_api/question/" + questionnaireID + '/' + qID
    
    response = urlopen(url)
    string = response.read().decode('utf-8')
    questionForm = json.loads(string)

    qOptions = []  # [Πρασινο, Q01A1]

    for i in range(len(questionForm.get('options'))):
        qOptions.append((questionForm.get('options')[i].get(
            'opttxt'), questionForm.get('options')[i].get('optID')))

    qAnswers = [ans[0] for ans in qOptions]
    qData = []
    for option in qOptions:
        qData.append(0)
        for stat in statistics:
            if option[1] == stat['_id']:
                qData[-1] = stat['count']
                break

    return render_template("chart.html", qAnswers=qAnswers, qData= qData)
    

@app.route("/intelliq_api/showsessions/<string:questionnaireID>", methods=["GET"])
def sessions(questionnaireID):
    sessions = list(db.responses.aggregate([
        {
            '$match': {
                'questionnaireID': questionnaireID
            }
        }, {
            '$group': {
                '_id': None,
                'uniqueValues': {
                    '$addToSet': '$session'
                }
            }
        }
    ]))
    if (not bool(sessions)):
        return "No data", 402

    sessions = sessions[0]['uniqueValues']

    return render_template("question_answers.html", sessions=sessions, questionnaireID=questionnaireID)


@app.route("/")
def questionnaire_test():
    session_id = str(uuid.uuid4())[:4]

    questionnaires = []
    for questr in db.questionnaire.find():
        questionnaires.append(
            (questr['_id'], questr['questionnaireTitle'], questr['questions'][0]['qID']))
    return render_template("main.html", questionnaires=questionnaires, session_id=session_id)


if __name__ == '__main__':
    app.run(debug=True, port=9103)
