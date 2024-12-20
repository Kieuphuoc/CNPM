import math
from flask import render_template, request, redirect, session, jsonify
import dao
from app import app
from flask_login import login_user, logout_user
from app.models import UserRole

@app.route("/")
def index():
    kw = request.args.get('kw')

    patients = dao.load_patients(kw)
    medicines = dao.load_medicines(kw)



    return render_template('index.html')


@app.route("/patients")
def show_patients():
    kw = request.args.get('kw')
    patients = dao.load_patients(kw)

    return render_template('index.html', patients=patients, show_patients=True)


@app.route("/medicines")
def show_medicines():


    return render_template('index.html', medicines=medicines, show_medicines=True)



@app.route("/login", methods=['get', 'post'])
def login_process():

    return render_template('login.html')

if __name__ == '__main__':
    app.run(debug=True)
