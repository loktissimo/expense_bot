from flask import Flask, render_template, redirect, url_for, request, flash
# from flask.json import jsonify
from flaskext.mysql import MySQL
from flask_basicauth import BasicAuth
from dotenv import load_dotenv
import os
import util

app = Flask(__name__)

# Load environment variables
load_dotenv('../.env')

# Settings
app.config['SECRET_KEY'] = 'secret-key-akjsdggffkjasdgfh'

# Settings SQL
app.config['MYSQL_DATABASE_HOST'] = os.environ.get("DB_HOST")
app.config['MYSQL_DATABASE_USER'] = os.environ.get("DB_USER")
app.config['MYSQL_DATABASE_PASSWORD'] = os.environ.get("DB_PASSWORD")
app.config['MYSQL_DATABASE_DB'] = os.environ.get("DB_DATABASE")
app.config['BASIC_AUTH_USERNAME'] = os.environ.get("WEB_USER")
app.config['BASIC_AUTH_PASSWORD'] = os.environ.get("WEB_PASSWORD")
app.config['BASIC_AUTH_FORCE'] = True
app.config['MYSQL_DATABASE_CHARSET'] = "utf8"

mysql = MySQL(app)
basic_auth = BasicAuth(app)

# SQL Queries
front_page = """SELECT e.id, u.name, e.text, e.write_date, e.accept_date, e.accepted
                 FROM users u
                 INNER JOIN expense e
                 ON u.telegram_id = e.telegram_id
                 ORDER BY e.write_date DESC"""

update_id = f"UPDATE expense" \
            f"SET accepted = 0, accept_date=now()" \
            f"WHERE id = {id}"

send_report = f"SELECT telegram_id, text FROM expense WHERE id = {id}"

rename_id = f"UPDATE users" \
            f"SET name = {name}" \
            f"WHERE telegram_id = {id}"


@app.route('/')
@basic_auth.required
def index():
    conn = mysql.connect()
    cur = conn.cursor()
    cur.execute(front_page)
    exp = cur.fetchall()
    cur.execute("SELECT * from users")
    usr = cur.fetchall()

    return render_template('table.html', users=usr, expense=exp)


@app.route('/update/<id>', methods=['GET'])
def update(id):
    if request.method == 'GET':
        conn = mysql.connect()
        cur = conn.cursor()
        cur.execute(update_id)
        conn.commit()

        cur.execute(send_report)
        id, text = cur.fetchone()
        util.send_telegramm_message(id, f'{text}: \nВнёс в журнал.')

        flash('Updated Successfully')
        return redirect(url_for('index'))


@app.route('/rename', methods=['GET', 'POST'])
def rename():
    if request.method == 'POST':
        id = request.form.get('user-id')
        xname = request.form.get('user-xname')
        name = request.form.get('user-name')

        conn = mysql.connect()
        cur = conn.cursor()
        cur.execute(rename_id)
        conn.commit()

        flash(f'{xname} renamed to {name}')

        return redirect(url_for('index'))
