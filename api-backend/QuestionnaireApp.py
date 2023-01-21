from flask import Flask, render_template
import pymongo
import flask_pymongo

# create app and set directory for html code (default is "./templates")
app = Flask(__name__, template_folder="../frontend")
client = pymongo.MongoClient("localhost", 27017)
db=client.queDB


@app.route("/")
def questionnaire_test():
    return render_template("main.html")

@app.route("/questionnaire/<string:slug>", methods=["GET"])
def get_questionnaire(slug):
    questionnaire = db.questionnaire.find_one({"_id": slug})
    for question in questionnaire["questions"]:
        del question["options"]
    return questionnaire


if __name__ == '__main__':
    app.run(debug=True)
