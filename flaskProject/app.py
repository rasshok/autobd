from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)
DATABASE = 'auto_repair.db'

def get_db():
    conn = sqlite3.connect(DATABASE)
    return conn

@app.route('/')
def index():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM requests")
    requests = cursor.fetchall()
    conn.close()
    return render_template('index.html', requests=requests)

@app.route('/add', methods=['GET', 'POST'])
def add_request():
    if request.method == 'POST':
        data = (
            request.form['request_number'],
            request.form['date_added'],
            request.form['car_type'],
            request.form['car_model'],
            request.form['problem_description'],
            request.form['client_name'],
            request.form['phone_number'],
            'new'
        )
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO requests (request_number, date_added, car_type, car_model, problem_description, client_name, phone_number, status) VALUES (?, ?, ?, ?, ?, ?, ?, ?)", data)
        conn.commit()
        conn.close()
        return redirect(url_for('index'))
    return render_template('add_request.html')

@app.route('/edit/<int:request_id>', methods=['GET', 'POST'])
def edit_request(request_id):
    conn = get_db()
    cursor = conn.cursor()
    if request.method == 'POST':
        data = (
            request.form['problem_description'],
            request.form['status'],
            request.form['assigned_mechanic'],
            request_id
        )
        cursor.execute("UPDATE requests SET problem_description = ?, status = ?, assigned_mechanic = ? WHERE id = ?", data)
        conn.commit()
        conn.close()
        return redirect(url_for('index'))
    cursor.execute("SELECT * FROM requests WHERE id = ?", (request_id,))
    request_data = cursor.fetchone()
    conn.close()
    return render_template('edit_request.html', request=request_data)

@app.route('/view/<int:request_id>')
def view_request(request_id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM requests WHERE id = ?", (request_id,))
    request_data = cursor.fetchone()
    conn.close()
    return render_template('view_request.html', request=request_data)

if __name__ == '__main__':
    app.run(debug=True)
