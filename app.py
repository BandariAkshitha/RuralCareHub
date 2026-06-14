from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# DATABASE
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ruralcarehub.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


# USER TABLE
class User(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(100))

    email = db.Column(db.String(100), unique=True)

    password = db.Column(db.String(100))


# APPOINTMENT TABLE
class Appointment(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    patient_name = db.Column(db.String(100))

    doctor_name = db.Column(db.String(100))

    appointment_date = db.Column(db.String(50))

    appointment_time = db.Column(db.String(50))


# HOME
@app.route('/')
def home():
    return render_template('index.html')


# LOGIN
@app.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == 'POST':

        return redirect('/patient')

    return render_template('login.html')


# REGISTER
@app.route('/register', methods=['GET', 'POST'])
def register():

    if request.method == 'POST':

        email = request.form['email']

        password = request.form['password']

        user = User(
            email=email,
            password=password
        )

        db.session.add(user)

        db.session.commit()

        return redirect('/login')

    return render_template('register.html')


# PATIENT DASHBOARD
@app.route('/patient')
def patient():
    return render_template('patient_dashboard.html')


# DOCTOR DASHBOARD
@app.route('/doctor')
def doctor():
    return render_template('doctor_dashboard.html')


# APPOINTMENT PAGE
@app.route('/appointment', methods=['GET', 'POST'])
def appointment():

    if request.method == 'POST':

        patient_name = request.form['patient_name']

        doctor_name = request.form['doctor_name']

        appointment_date = request.form['appointment_date']

        appointment_time = request.form['appointment_time']

        new_appointment = Appointment(

            patient_name=patient_name,

            doctor_name=doctor_name,

            appointment_date=appointment_date,

            appointment_time=appointment_time
        )

        db.session.add(new_appointment)

        db.session.commit()

        return redirect('/appointments')

    return render_template('appointment.html')


# TODAY APPOINTMENTS
@app.route('/appointments')
def appointments():

    appointments = Appointment.query.all()

    return render_template(
        'appointments.html',
        appointments=appointments
    )


# PATIENT LIST
@app.route('/patients')
def patients():

    appointments = Appointment.query.all()

    return render_template(
        'patients.html',
        appointments=appointments
    )


# REPORTS
@app.route('/reports')
def reports():
    return render_template('reports.html')


# NOTIFICATIONS
@app.route('/notifications')
def notifications():
    return render_template('notifications.html')


# CREATE DATABASE
with app.app_context():
    db.create_all()


# RUN APP
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)