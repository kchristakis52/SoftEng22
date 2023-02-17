import os
import io

# Get questionnaire
def test_session_answers():
    try:
        response = os.popen('python3 se2221 questionnaire --questionnaire_id QQ003 --format json','r').read()
        assert "Status Code: 200" in response
    except:
        assert False

# Get question
def test_session_answers():
    try:
        response = os.popen('python3 se2221 question --questionnaire_id QQ003 --question_id Q03 --format json','r').read()
        assert "Status Code: 200" in response
    except:
        assert False

# Get session answers
def test_session_answers():
    try:
        response = os.popen('python3 se2221 getsessionanswers --questionnaire_id QQ003 --session_id ee29 --format json','r').read()
        assert "Status Code: 200" in response
    except:
        assert False

# Get question answers
def test_question_answers():
    try:
        response = os.popen('python3 se2221 getquestionanswers --questionnaire_id QQ003 --question_id Q03 --format json','r').read()
        assert "Status Code: 200" in response
    except:
        assert False

# Admin Healthcheck
def test_healthcheck():
    try:
        response = os.popen('python3 se2221 healthcheck','r').read()
        assert "OK" in response
    except:
        assert False

# Do answer before reset
def test_answer():
    try:
        response = os.popen('python3 se2221 doanswer --questionnaire_id QQ003 --question_id Q03 --session_id AAAA --option_id Q03A1','r').read()
        assert "Status Code: 204" in response
    except:
        assert False

# Admin reset questionnaire
def test_resetall():
    try:
        response = os.popen('python3 se2221 resetq --questionnaire_id QQ003','r').read()
        assert "OK" in response
    except:
        assert False

# Do answer after reset
def test_answer_reset():
    try:
        response = os.popen('python3 se2221 doanswer --questionnaire_id QQ003 --question_id Q03 --session_id AAAA --option_id Q03A02','r').read()
        assert "Status Code: 400" in response
    except:
        assert False

# Admin Post questionnaire
def test_questionnaire_upd():
    try:
        response = os.popen('python3 se2221 questionnaire-upd --source ../test/smoking_questionnaire.json','r').read()
        assert "OK" in response
    except:
        assert False

# Admin reset all
def test_resetall():
    try:
        response = os.popen('python3 se2221 resetall','r').read()
        assert "OK" in response
    except:
        assert False

# Admin Post questionnaire after reset
def test_questionnaire_upd_reset():
    try:
        response = os.popen('python3 se2221 questionnaire-upd --source ../test/smoking_questionnaire.json','r').read()
        assert not("OK" in response)
    except:
        assert False

# Do bad answer
def test_answer_reset():
    try:
        response = os.popen('python3 se2221 doanswer --questionnaire_id QQ003 --question_id Q03 --session_id ^AAA --option_id Q03A02','r').read()
        assert "Status Code: 400" in response
    except:
        assert False