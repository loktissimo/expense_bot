from flask import Flask, render_template, redirect, url_for, request, flash
from flaskext.mysql import MySQL
from flask_basicauth import BasicAuth
from dotenv import load_dotenv
import os
import util

load_dotenv('../.env')
app = Flask(__name__)

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


@app.route('/')
@basic_auth.required
def index():
    conn = mysql.connect()
    cur = conn.cursor()
    cur.execute("SELECT e.id, u.name, e.text, e.write_date, e.accept_date, e.accepted \
                 FROM users u INNER \
                 JOIN expense e \
                 ON u.telegram_id = e.telegram_id \
                 ORDER BY e.write_date DESC \
                ")
    exp = cur.fetchall()
    cur.execute("SELECT * from users")
    usr = cur.fetchall()

    return render_template('table.html', users=usr, expense=exp)


@app.route('/update/<id>', methods=['GET'])
def update(id):
    if request.method == 'GET':
        conn = mysql.connect()
        cur = conn.cursor()
        cur.execute("""
            UPDATE expense
            SET accepted = 0, accept_date=now()
            WHERE id = %s
        """, (id, ))
        conn.commit()

        cur.execute(f"SELECT telegram_id, text FROM expense WHERE id = {id}")
        id, text = cur.fetchone()
        util.send_telegramm_message(id, f'{text} \nвнёс в журнал.')

        flash('Updated Successfully')
        return redirect(url_for('index'))
