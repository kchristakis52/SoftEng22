// pushing some data to fill mongodb database with
// use command: mongo < questionnaire.js

db.questionnaire.drop()
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
        { "questionId": "1", "answer": "blue" },
        { "questionId": "2", "answer": "3-4 times a week" },
        { "questionId": "3", "answer": "email" }
    ]
})
db.responses.insertOne({
    "userId": "2",
    "questionnaireId": "2",
    "answers": [
        { "questionId": "1", "answer": "0-17" },
        { "questionId": "2", "answer": "some hours daily (2-4 hours)" },
        { "questionId": "3", "answer": "1-2 days" }
    ]
})

db.questionnaire.insertOne({
    "questionnaireID": "QQ000",
    "questionnaireTitle": "My first research questionnaire",
    "keywords": [
        "footbal",
        "islands",
        "timezone"
    ],
    "questions": [
        {
            "qID ": "P00",
            "qtext": "Ποιο είναι το mail σας;",
            "required": "FALSE",
            "type": "profile",
            "options": [
                {
                    "optID": "P00TXT",
                    "opttxt": "<open string>",
                    "nextqID": "P01"
                }
            ]
        },
        {
            "qID ": "P01",
            "qtext": "Ποια είναι η ηλικία σας;",
            "required": "TRUE",
            "type": "profile",
            "options": [
                {
                    "optID": "P01A1",
                    "opttxt": "<30",
                    "nextqID": "Q01"
                },
                {
                    "optID": "P01A2",
                    "opttxt": "30-50",
                    "nextqID": "Q01"
                },
                {
                    "optID": "P01A3",
                    "opttxt": "50-70",
                    "nextqID": "Q01"
                },
                {
                    "optID": "P01A4",
                    "opttxt": ">70",
                    "nextqID": "Q01"
                }
            ]
        },
        {
            "qID ": "Q01",
            "qtext": "Ποιο είναι το αγαπημένο σας χρώμα;",
            "required": "TRUE",
            "type": "question",
            "options": [
                {
                    "optID": "Q01A1",
                    "opttxt": "Πράσινο",

                    "nextqID": "Q02"
                },
                {
                    "optID": "Q01A2",
                    "opttxt": "Κόκκινο",
                    "nextqID": "Q02"
                },
                {
                    "optID": "Q01A3",
                    "opttxt": "Κίτρινο",
                    "nextqID": "Q02"
                }
            ]
        },
        {
            "qID ": "Q02",
            "qtext": "Ασχολείστε με το ποδόσφαιρο;",
            "required": "TRUE",
            "type": "question",
            "options": [
                {
                    "optID": "Q02A1",
                    "opttxt": "Ναι",
                    "nextqID": "Q03"
                },
                {
                    "optID": "Q02A2",
                    "opttxt": "Οχι",
                    "nextqID": "Q04"
                }
            ]
        },
        {
            "qID ": "Q03",
            "qtext": "Τι ομάδα είστε;",
            "required": "TRUE",
            "type": "question",
            "options": [
                {
                    "optID": "Q03A1",
                    "opttxt": "Παναθηναϊκός",
                    "nextqID": "Q04"
                },
                {
                    "optID": "Q03A2",
                    "opttxt": "Ολυμπιακός ",
                    "nextqID": "Q04"
                },
                {
                    "optID": "Q03A3",
                    "opttxt": "ΑΕΚ",
                    "nextqID": "Q04"
                }
            ]
        },
        {
            "qID ": "Q04",
            "qtext": "Έχετε ζήσει σε νησί;",
            "required": "TRUE",
            "type": "question",
            "options": [
                {
                    "optID": "Q04A1",
                    "opttxt": "Ναι",
                    "nextqID": "Q05"
                },

                {
                    "optID": "Q04A2",
                    "opttxt": "Οχι",
                    "nextqID": "Q06"
                }
            ]
        },
        {
            "qID ": "Q05",
            "qtext": "Με δεδομένο ότι απαντήσατε [*Q04A1] στην ερώτηση [*Q04]: Ποια η σχέση σας με το θαλάσσιο σκι;",
            "required": "TRUE",
            "type": "question",
            "options": [
                {
                    "optID": "Q05A1",
                    "opttxt": "Καμία",
                    "nextqID": "Q07"
                },
                {
                    "optID": "Q05A2",
                    "opttxt": "Μικρή",
                    "nextqID": "Q07"
                },
                {
                    "optID": "Q05A3",
                    "opttxt": "Μεγάλη",
                    "nextqID": "Q07"
                }
            ]
        },
        {
            "qID ": "Q06",
            "qtext": "Είστε χειμερινός κολυμβητής",
            "required": "TRUE",
            "type": "question",
            "options": [
                {
                    "optID": "Q06A1",
                    "opttxt": "Ναι",
                    "nextqID": "Q07"
                },
                {
                    "optID": "Q06A2",
                    "opttxt": "Οχι",
                    "nextqID": "Q07"
                }
            ]
        },
        {
            "qID ": "Q07",
            "qtext": "Κάνετε χειμερινό σκι;",
            "required": "TRUE",
            "type": "question",
            "options": [
                {
                    "optID": "Q07A1",
                    "opttxt": "Σπάνια - καθόλου",
                    "nextqID": "Q08"
                },
                {
                    "optID": "Q07A2",
                    "opttxt": "Περιστασιακά",
                    "nextqID": "Q08"
                },
                {

                    "optID": "Q07A3",
                    "opttxt": "Τακτικά",
                    "nextqID": "Q08"
                }
            ]
        },
        {
            "qID ": "Q08",
            "qtext": "Συμφωνείτε να αλλάζει η ώρα κάθε χρόνο;",
            "required": "TRUE",
            "type": "question",
            "options": [
                {
                    "optID": "Q08A1",
                    "opttxt": "Ναι",
                    "nextqID": "Q09"
                },
                {
                    "optID": "Q08A2",
                    "opttxt": "Οχι",
                    "nextqID": "-"
                }
            ]
        },
        {
            "qID ": "Q09",
            "qtext": "Με δεδομένο ότι απαντήσατε [*Q08A2] στην ερώτηση [*Q08]: Προτιμάτε τη θερινή ή την χειμερινή ώρα;",
            "required": "TRUE",
            "type": "question",
            "options": [
                {
                    "optID": "Q09A1",
                    "opttxt": "Θερινή",
                    "nextqID": "-"
                },
                {
                    "optID": "Q09A2",
                    "opttxt": "Χειμερινή",
                    "nextqID": "-"
                }
            ]
        }
    ]
})