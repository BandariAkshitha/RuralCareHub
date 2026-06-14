from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# DATABASE CONFIGURATION
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ruralcarehub.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


# USER TABLE
class User(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(100))

    email = db.Column(db.String(100), unique=True)

    phone = db.Column(db.String(20))

    address = db.Column(db.String(200))

    password = db.Column(db.String(100))

class Appointment(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    patient_name = db.Column(db.String(100))

    doctor_name = db.Column(db.String(100))

    appointment_date = db.Column(db.String(50))

    appointment_time = db.Column(db.String(50))
    
class HealthRecord(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    patient_name = db.Column(db.String(100))

    age = db.Column(db.String(10))

    blood_group = db.Column(db.String(10))

    history = db.Column(db.String(500))

    checkup_date = db.Column(db.String(50))

    doctor = db.Column(db.String(100))

    status = db.Column(db.String(100))
class Doctor(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(100))

    specialization = db.Column(db.String(100))

    city = db.Column(db.String(100))
    
class Notification(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    title = db.Column(db.String(200))

    message = db.Column(db.String(500))

# HOME PAGE
@app.route('/')
def home():
    return render_template('index.html')


# LOGIN
@app.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == 'POST':

        email = request.form['email']
        password = request.form['password']

        # TEMPORARY LOGIN
        if email and password:

            return redirect('/patient')

        else:
            return "Invalid Login"

    return render_template('login.html')

# REGISTER
@app.route('/register', methods=['GET', 'POST'])

def register():

    if request.method == 'POST':

        email = request.form['email']

        password = request.form['password']

        new_user = User(
            email=email,
            password=password
        )

        db.session.add(new_user)

        db.session.commit()

        return redirect('/login')

    return render_template('register.html')


# ADMIN
@app.route('/admin')
def admin():
    return render_template('admin_dashboard.html')


# DOCTOR
@app.route('/doctor')
def doctor():
    return render_template('doctor_dashboard.html')


# PATIENT
@app.route('/patient')
def patient():
    return render_template('patient_dashboard.html')


# DOCTOR DIRECTORY
@app.route('/directory')
def directory():

    doctors = Doctor.query.all()

    if len(doctors) == 0:

        doctor1 = Doctor(
            name="Dr. Ravi Kumar",
            specialization="General Physician",
            city="Hyderabad"
        )

        doctor2 = Doctor(
            name="Dr. Priya Sharma",
            specialization="Cardiologist",
            city="Hyderabad"
        )

        doctor3 = Doctor(
            name="Dr. Suresh Reddy",
            specialization="Pediatrician",
            city="Hyderabad"
        )

        db.session.add(doctor1)
        db.session.add(doctor2)
        db.session.add(doctor3)

        db.session.commit()

        doctors = Doctor.query.all()

    return render_template(
        'doctor_directory.html',
        doctors=doctors
    )    

# APPOINTMENT
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

        return redirect('/patient')

    return render_template('appointment.html')

# HEALTH RECORDS
@app.route('/records')

def records():

    latest_appointment = Appointment.query.order_by(
        Appointment.id.desc()
    ).first()

    if latest_appointment:

        record = {

            "patient_name":
            latest_appointment.patient_name,

            "age":"20",

            "blood_group":"O+",

            "history":"No major illnesses",

            "checkup_date":
            latest_appointment.appointment_date,

            "doctor":
            latest_appointment.doctor_name,

            "status":"Healthy"
        }

    else:

        record = {

            "patient_name":"No Patient",

            "age":"-",

            "blood_group":"-",

            "history":"No records available",

            "checkup_date":"-",

            "doctor":"-",

            "status":"-"
        }

    return render_template(
        'health_records.html',
        record=record
    )


# ARTICLES
@app.route('/articles')
def articles():
    return render_template('articles.html')


# EMERGENCY
@app.route('/emergency')
def emergency():
    return render_template('emergency_contacts.html')


# NOTIFICATIONS
@app.route('/notifications')
def notifications():

    notifications = Notification.query.all()

    if len(notifications) == 0:

        n1 = Notification(
            title="Appointment Confirmed",
            message="Your appointment confirmed successfully."
        )

        n2 = Notification(
            title="Health Camp Alert",
            message="Free health camp available this Sunday."
        )

        db.session.add(n1)
        db.session.add(n2)

        db.session.commit()

        notifications = Notification.query.all()

    return render_template(
        'notifications.html',
        notifications=notifications
    )

# VOICE ASSISTANT
@app.route('/voice')
def voice():
    return render_template('voice_assistant.html')


# LANGUAGE SUPPORT
@app.route('/language')
def language():
    return render_template('language_support.html')
# PROFILE
@app.route('/profile')
def profile():

    latest_appointment = Appointment.query.order_by(
        Appointment.id.desc()
    ).first()

    if latest_appointment:

        profile_data = {

            "name":
            latest_appointment.patient_name,

            "age":"28",

            "blood_group":"O+",

            "phone":"9876543210",

            "address":"Hyderabad",

            "doctor":
            latest_appointment.doctor_name
        }

    else:

        profile_data = {

            "name":"No Patient",

            "age":"-",

            "blood_group":"-",

            "phone":"-",

            "address":"-",

            "doctor":"-"
        }

    return render_template(
        'profile.html',
        profile=profile_data
    )

@app.route('/symptomchecker')
def symptomchecker():
    return render_template('symptom_checker.html')


# CREATE DATABASE
with app.app_context():
    db.create_all()


# RUN APP
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)