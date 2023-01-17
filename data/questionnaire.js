// pushing some data to fill mongodb database with
// use command: mongo < questionnaire.js

db.questions.drop()
db.responses.drop()

db.createCollection("questions")
db.createCollection("responses")

db.questions.insertOne({
    "questionnaireId": "1",
    "name": "Questionnaire for students",
    "questions": [
        {
            "questionId": "1",
            "question": "What is your favorite color?",
            "options": ["red", "blue", "green", "other"]
        },
        {
            "questionId": "2",
            "question": "How often do you exercise?",
            "options": ["daily", "3-4 times a week", "once a week", "rarely"]
        },
        {
            "questionId": "3",
            "question": "What is your preferred method of communication?",
            "options": ["email", "phone", "text", "in-person"]
        }
    ]
})
db.questions.insertOne({
    "questionnaireId": "2",
    "name": "Questionnaire about internet usage and addiction",
    "questions": [
        {
            "questionId": "1",
            "question": "How old are you?",
            "options": ["0-17", "18-39", "40-64", "65+"]
        },
        {
            "questionId": "2",
            "question": "How much time do you spend online?",
            "options": ["many hours daily (4+ hours)", "some hours daily (2-4 hours)", "a few hours daily (<2 hours)", "i dont use internet on a daily base"]
        },
        {
            "questionId": "3",
            "question": "how long can you withstand without internet connection? ",
            "options": ["some hours", "1-2 days", "a week", "i can live without internet at all"]
        }
    ]
})
db.responses.insertOne({
    "userId": "1",
    "questionnaireId": "1",
    "answers": [
        {"questionId": "1", "answer": "blue"},
        {"questionId": "2", "answer": "3-4 times a week"},
        {"questionId": "3", "answer": "email"}
    ]
})
db.responses.insertOne({
    "userId": "2",
    "questionnaireId": "2",
    "answers": [
        {"questionId": "1", "answer": "0-17"},
        {"questionId": "2", "answer": "some hours daily (2-4 hours)"},
        {"questionId": "3", "answer": "1-2 days"}
    ]
})