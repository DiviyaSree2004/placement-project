from flask import Flask, request, jsonify
import pandas as pd
import sqlite3

app = Flask(__name__)

# Load CSV into the SQLite database
def init_db():
    df = pd.read_csv('employees.csv')  # Or replace with .read_json() later
    conn = sqlite3.connect('data.db')
    df.to_sql('employees', conn, if_exists='replace', index=False)
    conn.close()

@app.route('/employees', methods=['GET'])
def get_all_employees():
    conn = sqlite3.connect('data.db')
    cur = conn.cursor()
    cur.execute("SELECT * FROM employees")
    rows = cur.fetchall()
    col_names = [description[0] for description in cur.description]
    data = [dict(zip(col_names, row)) for row in rows]
    conn.close()
    return jsonify(data)

@app.route('/employee', methods=['GET'])
def get_employee_by_id():
    emp_id = request.args.get('id')
    conn = sqlite3.connect('data.db')
    cur = conn.cursor()
    cur.execute("SELECT * FROM employees WHERE id=?", (emp_id,))
    row = cur.fetchone()
    col_names = [description[0] for description in cur.description]
    data = dict(zip(col_names, row)) if row else {}
    conn.close()
    return jsonify(data)

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
