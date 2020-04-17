from flask import Flask, escape, request, jsonify

app = Flask(__name__)

@app.route('/')
def hello():
    name = request.args.get("name", "World")
    return f'Hello, {escape(name)}!'

# store all tests
db = [{
    "test_id":1,
    "subject":"Mock",
    "answer_keys":{
        "1":"A",
        "2":"A",
        "3":"A"
    },
    "submissions":[]
}]

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
    return False

# create a new test by request
def create_test(info,db):
    # check if the test existed
    tid = getId(info['subject'],db)
    if not tid:
        tid = len(db) + 1
        db.append({})
    # update or add new test
    db[tid-1]['test_id'] = tid
    db[tid-1]['subject'] = info['subject']
    db[tid-1]['answer_keys'] = info['answer_keys']
    db[tid-1]['submissions'] = []
    return db[tid-1]

# post a new test
@app.route('/tests', method=['POST'])
def post_test():
    if not request.json:
        return "Wrong Value"
    info = request.json
    return jsonify(create_test(info,db)),201

"""
process new submission
"""

# convert a pdf file into json format submissions
def pdf2json(pdf):
    submission = {
        "subject":"unknown",
        "name":"unknown",
        "answer":{
            "1":"A",
            "2":"B",
            "3":"C"
        }
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
    for k,v in db[tid-1]['answer_keys'].items():
        sv = submission["answer"][k]
        result["result"][k] = {
            "actual":sv,
            "expected":v
        }
        if sv == v:
            score += 1
    result["score"] = score
    db[tid-1]["submissions"].append(result)
    return result

# post a pdf submission and return the result
@app.route('/tests/<int:id>/scantrons',method=['POST'])
def post_sub(id):
    tid = id
    pdf = request.body
    submission = pdf2json(pdf)
    return grade(submission,db,tid)

# get all scantron submissions
@app.route('/tests/<int:id>')
def get(id):
    return jsonify(db[id-1])