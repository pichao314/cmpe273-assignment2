import os, sqlite3, json

db_file = os.path.join(os.path.dirname(__file__), 'tests.db')
if os.path.isfile(db_file):
    os.remove(db_file)

conn = sqlite3.connect('tests.db')
cur = conn.cursor()

init_test = "CREATE TABLE test(\
    test_id INTEGER PRIMARY KEY,\
    subject VARCHAR(20),\
    answer_keys VARCHAR(1000))"

ans_key = json.dumps({str(k): ['A', 'B', 'C', 'D'][k % 4] for k in range(50)})

insert_test = "INSERT INTO test\
    VALUES (null,'Test',?)"

init_sub = "CREATE TABLE submission(\
    scantron_id INTEGER PRIMARY KEY,\
    scantron_url VARCHAR(100),\
    subject VARCHAR(20),\
    name VARCHAR(20),\
    score INTEGER,\
    result VARCHAR(1000))"

sub_key = json.dumps({str(k): ['A', 'A', 'C', 'C'][k % 4] for k in range(50)})
insert_sub = "INSERT INTO submission\
    VALUES (null,'http://1.pdf','foo','bar',25,?)"

cur.execute(init_test)
# cur.execute(insert_test,(ans_key,))
cur.execute(init_sub)
# cur.execute(insert_sub,(sub_key,))
cur.close()
conn.commit()
conn.close()
