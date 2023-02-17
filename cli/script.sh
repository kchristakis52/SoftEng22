python3 se2221 healthcheck
python3 se2221 questionnaire --questionnaire_id QQ003 --format json

python3 se2221 getquestionanswers --questionnaire_id QQ003 --question_id Q03 --format json
python3 se2221 resetall
python3 se2221 questionnaire-upd --source ../test/smoking_questionnaire.json
python3 se2221 questionnaire --questionnaire_id QQ003 --format json