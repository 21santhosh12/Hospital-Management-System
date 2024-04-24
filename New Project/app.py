from flask import Flask, render_template, request, session, url_for, redirect,flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
from flask_login import UserMixin, login_user, logout_user, login_manager, LoginManager,current_user,login_required
from werkzeug.security import generate_password_hash, check_password_hash
import json


with open('config.json','r') as c:
    params = json.load(c)["params"]


app = Flask(__name__)
app.secret_key = 'santhosh'

# This is for getting unique user access
login_manager = LoginManager(app)
login_manager.login_view = 'login'




@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/hospital management'
db = SQLAlchemy(app)


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50))
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(1000))

class Patient(db.Model):
    pid=db.Column(db.Integer,primary_key=True)
    email=db.Column(db.String(50))
    name=db.Column(db.String(50))
    gender=db.Column(db.String(50))
    slot=db.Column(db.String(50))
    disease=db.Column(db.String(50))
    time=db.Column(db.String(50),nullable=False)
    date=db.Column(db.String(50),nullable=False)
    dept=db.Column(db.String(50))
    number=db.Column(db.String(50))

class Doctor(db.Model):
    did=db.Column(db.Integer,primary_key=True)
    doctorname=db.Column(db.String(50))
    email=db.Column(db.String(50))
    dept=db.Column(db.String(50))

class Trig(db.Model):
    tid=db.Column(db.Integer,primary_key=True)
    pid=db.Column(db.Integer)
    email=db.Column(db.String(50))
    name=db.Column(db.String(50))
    action=db.Column(db.String(50))
    time=db.Column(db.String(50))


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/doctor',methods=['POST','GET'])
@login_required
def doctor():
    if request.method=="POST":
        doctorname=request.form.get('doctorname')
        email=request.form.get('email')
        dept=request.form.get('dept')
        new_doctor=Doctor(doctorname=doctorname,email=email,dept=dept)
        db.session.add(new_doctor)
        db.session.commit()
        flash("Booking is Confirmed","info")
    return render_template('doctor.html')


@app.route('/patient',methods=['POST','GET'])
@login_required
def patient():
    sql_query=text("SELECT * FROM doctor")
    doct=db.session.execute(sql_query)
    if request.method=="POST":
        email=request.form.get('email')
        name=request.form.get('name')
        gender=request.form.get('gender')
        slot=request.form.get('slot')
        disease=request.form.get('disease')
        time=request.form.get('time')
        date=request.form.get('date')
        dept=request.form.get('dept')
        number=request.form.get('number')

        new_patient=Patient(email=email,name=name,gender=gender,slot=slot,disease=disease,time=time,date=date,dept=dept,number=number)
        db.session.add(new_patient)
        db.session.commit()
        flash("Booking Confirmed","info")


    return render_template('patient.html',doct=doct)


@app.route('/bookings')
@login_required
def bookings():
    em=current_user.email
    query=Patient.query.filter_by(email=em).all()
    return render_template('bookings.html',query=query)

@app.route("/edit/<string:pid>", methods=['POST', 'GET'])
@login_required
def edit(pid):
    posts = Patient.query.filter_by(pid=pid).first()
    if request.method == "POST":
        email = request.form.get('email')
        name = request.form.get('name')
        gender = request.form.get('gender')
        slot = request.form.get('slot')
        disease = request.form.get('disease')
        time = request.form.get('time')
        date = request.form.get('date')
        dept = request.form.get('dept')
        number = request.form.get('number')
        
        sql_query = text(f"""
            UPDATE Patient
            SET email='{email}', name='{name}', gender='{gender}', slot='{slot}', disease='{disease}',
                time='{time}', date='{date}', dept='{dept}', number='{number}'
            WHERE pid={pid}
        """)

        try:
            db.session.execute(sql_query)
            db.session.commit()
            flash("Booking updated successfully", "success")
            return redirect(url_for('bookings'))
        except Exception as e:
            flash(f"An error occurred: {str(e)}", "danger")
            return redirect(url_for('bookings'))
        
    return render_template('edit.html', posts=posts)


@app.route('/details')
@login_required
def details():
    posts=Trig.query.all()
    return render_template('trigers.html',posts=posts)


@app.route("/delete/<int:pid>", methods=['POST', 'GET'])
@login_required
def delete(pid):
    patient_to_delete = Patient.query.get(pid)
    if patient_to_delete:
        db.session.delete(patient_to_delete)
        db.session.commit()
        flash("Slot Deleted Successfully", "danger")
    else:
        flash("Patient not found", "warning")
    
    return redirect(url_for('bookings')) 

@app.route('/search',methods=['POST','GET'])
@login_required
def search():
    if request.method == "POST":
        query=request.form.get('search')
        dept=Doctor.query.filter_by(dept=query).first()
        if dept:
            flash("Department is Available","success")
        else:
            flash("Sorry! Currently is not Available","warning")
    return render_template('index.html')

@app.route('/signup', methods=['POST', 'GET'])
def signup():
    if request.method == "POST":
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()
        if user:
            flash("email already exists",'danger')
            return render_template('/signup.html')
        encpassword = generate_password_hash(password)
        new_user = User(username=username, email=email, password=encpassword)
        db.session.add(new_user)

        # Commit the session to persist changes to the database
        db.session.commit()
        flash("Please Login","warning")
        return render_template('login.html')

    return render_template('signup.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("Logout Successfully","primary")
    return redirect(url_for('login')) 


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == "POST":
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()

        if user and check_password_hash(user.password, password):
            login_user(user)
            flash("Login Success","primary")
            return redirect(url_for('index'))

        flash('invalid credentials','danger')
        return render_template('login.html')
    return render_template('login.html')


if __name__ == '__main__':
    app.run(debug=False)
