from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root@iddqd:192.168.10.110'

db = SQLAlchemy(app)


@app.route('/')
def hello():
    return render_template('table.html')
