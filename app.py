from flask import Flask, escape, request, jsonify
import sqlite3

app = Flask(__name__)

@app.route('/')
def hello():
    name = request.args.get("name", "World")
    return f'Hello, {escape(name)}!'


"""
process new test
"""

# get test id by subject name
def getId(subject_name,db):
    for test in db:
        # found test
        if test['subject'] == subject_name:
            return test["test_id"]
    # test not found
    return -1

# create a new test by request
def create_test(info,db):
    # check if the test existed
    tid = getId(info['subject'],db)
    if tid<0:
        tid = len(db)
        db.append({})
    # update or add new test
    db[tid]['test_id'] = tid
    db[tid]['subject'] = info['subject']
    db[tid]['answer_keys'] = info['answer_keys']
    db[tid]['submissions'] = []
    return db[tid]

# post a new test
@app.route('/tests', methods=['POST'])
def post_test():
    if not request.json:
        return "Wrong Value"
    info = request.json
    return jsonify(create_test(info,db)),201

"""
process new submission
"""

#todo use ocr to read actual input
# convert a pdf file into json format submissions
def pdf2json(pdf):
    submission = {
        "subject":pdf["subject"],
        "name":pdf["name"],
        "answer":pdf["answer"]
    }
    return submission


# grade a submission, add the submission into test db
def grade(submission,db,tid):
    # tid = getId(submission['subject'],db)
    # if not tid:
    #     return False
    result = {
        "scantron_id": 1,
        "scantron_url": "http://localhost:5000/files/1.pdf",
        "name": submission['name'],
        "subject": submission['subject'],
        "result": {}
    }
    score = 0
    for k,v in db[tid]['answer_keys'].items():
        sv = submission["answer"][k]
        result["result"][k] = {
            "actual":sv,
            "expected":v
        }
        if sv == v:
            score += 1
    result["score"] = score
    db[tid]["submissions"].append(result)
    return result

# post a pdf submission and return the result
@app.route('/tests/<int:id>/scantrons',methods=['POST'])
def post_sub(id):
    if id >= len(db):
        return "Test not exist!"
    tid = id
    # todo change input into pdf
    pdf = request.json
    submission = pdf2json(pdf)
    return grade(submission,db,tid),201

# get all scantron submissions
@app.route('/tests/<int:id>')
def get(id):
    if id >= len(db):
        return "Test not exist!"
    return jsonify(db[id])