from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# DATABASE CONFIGURATION
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ruralcarehub.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class User(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(100))

    email = db.Column(db.String(100), unique=True)

    phone = db.Column(db.String(20))

    address = db.Column(db.String(200))

    password = db.Column(db.String(100))

    role = db.Column(db.String(50))


# APPOINTMENT TABLE
class Appointment(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    patient_name = db.Column(db.String(100))

    doctor_name = db.Column(db.String(100))

    appointment_date = db.Column(db.String(50))

    appointment_time = db.Column(db.String(50))
    
    symptoms = db.Column(db.String(500))
    
    age = db.Column(db.String(10))
    blood_group = db.Column(db.String(10))


# HEALTH RECORD TABLE
class HealthRecord(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    patient_name = db.Column(db.String(100))

    age = db.Column(db.String(10))

    blood_group = db.Column(db.String(10))

    history = db.Column(db.String(500))

    checkup_date = db.Column(db.String(50))

    doctor = db.Column(db.String(100))

    status = db.Column(db.String(100))


# DOCTOR TABLE
class Doctor(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(100))

    specialization = db.Column(db.String(100))

    city = db.Column(db.String(100))


# NOTIFICATION TABLE
class Notification(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    title = db.Column(db.String(200))

    message = db.Column(db.String(500))


# PRESCRIPTION TABLE
class Prescription(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    patient_name = db.Column(db.String(100))

    medicine = db.Column(db.String(200))

    dosage = db.Column(db.String(100))

    symptoms = db.Column(db.String(500))

def get_medicine(symptoms):
    symptoms = symptoms.lower()

    if "fever" in symptoms:
        return "Paracetamol"
    elif "cold" in symptoms:
        return "Cetirizine"
    elif "headache" in symptoms:
        return "Dolo 650"
    elif "cough" in symptoms:
        return "Benadryl Syrup"
    elif "stomach" in symptoms or "stomach pain" in symptoms:
        return "Pantoprazole"
    else:
        return "Consult Doctor"

# HOME PAGE
@app.route('/')
def home():
    return redirect('/login')

# LOGIN PAGE
@app.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == 'POST':

        email = request.form.get('email')
        password = request.form.get('password')
        role = request.form.get('role')

        # Admin Login
        if role == "admin":
                return redirect('/admin')

        # Patient Login
        elif role == "patient":
            user = User.query.filter_by(
                email=email,
                password=password
            ).first()

            if user:
                return redirect('/patient')
            else:
                return "Invalid Patient Login"

        # Doctor Login
        elif role == "doctor":
            return redirect('/doctor-dashboard')

    return render_template('login.html')
@app.route('/select-role')
def select_role():
    return render_template('select_role.html')


# REGISTER PAGE
@app.route('/register', methods=['GET', 'POST'])
def register():

    if request.method == 'POST':

        name = request.form.get('name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        address = request.form.get('address')
        password = request.form.get('password')
        role = request.form.get('role')

        new_user = User(
            name=name,
            email=email,
            phone=phone,
            address=address,
            password=password,
            role=role
        )

        db.session.add(new_user)
        db.session.commit()

        return redirect('/login')

    return render_template('register.html')
# ADMIN DASHBOARD
@app.route('/admin')
def admin():
    return render_template('admin_dashboard.html')


# DOCTOR DASHBOARD
@app.route('/doctor-dashboard')
def doctor():
    return render_template('doctor_dashboard.html')


# PATIENT DASHBOARD
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


# APPOINTMENT BOOKING
@app.route('/appointment', methods=['GET', 'POST'])
def appointment():

    if request.method == 'POST':

        patient_name = request.form['patient_name']
        symptoms = request.form['symptoms']
        appointment_date = request.form['appointment_date']
        appointment_time = request.form['appointment_time']
        age = request.form['age']
        blood_group = request.form['blood_group']

        # Automatic doctor selection
        doctor_name = request.form.get("doctor_name")

        new_appointment = Appointment(
    patient_name=patient_name,
    doctor_name=doctor_name,
    symptoms=symptoms,
    appointment_date=appointment_date,
    appointment_time=appointment_time,
    age=age,
    blood_group=blood_group
)

        db.session.add(new_appointment)
        db.session.commit()
        

        return redirect('/appointments')

    return render_template('appointment.html')

# PATIENT RECORDS
@app.route('/patients')
def patients():

    appointments = Appointment.query.all()

    return render_template(
        'patients.html',
        appointments=appointments
    )


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

            "doctor":
            latest_appointment.doctor_name,

            "disease": latest_appointment.symptoms,

            "medicine": get_medicine(latest_appointment.symptoms),

            "date":
            latest_appointment.appointment_date

        }

    else:

        record = {

            "patient_name":"No Patient",

            "doctor":"-",

            "disease":"-",

            "medicine":"-",

            "date":"-"

        }

    return render_template(
        'health_records.html',
        record=record
    )


# HEALTH ARTICLES
@app.route('/articles')
def articles():
    return render_template('articles.html')


# EMERGENCY SERVICES
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


# SYMPTOM CHECKER
@app.route('/symptomchecker')
def symptomchecker():
    return render_template('symptom_checker.html')


# TODAY APPOINTMENTS
@app.route('/appointments')
def appointments():

    appointments = Appointment.query.all()

    return render_template(
        'doctor_appointments.html',
        appointments=appointments
    )


# PRESCRIPTIONS
@app.route('/prescriptions')
def prescriptions():

    appointments = Appointment.query.all()

    prescription_list = []

    for appointment in appointments:

        symptoms = appointment.symptoms.lower()

        if "fever" in symptoms:
            medicine = "Paracetamol"
            dosage = "1 Tablet - Twice Daily"

        elif "cold" in symptoms:
            medicine = "Cetirizine"
            dosage = "1 Tablet - Night"

        elif "headache" in symptoms:
            medicine = "Dolo 650"
            dosage = "1 Tablet - After Food"

        elif "cough" in symptoms:
            medicine = "Benadryl Syrup"
            dosage = "10 ml - Twice Daily"

        elif "stomach pain" in symptoms:
            medicine = "Pantoprazole"
            dosage = "1 Tablet - Before Breakfast"

        elif "body pain" in symptoms:
            medicine = "Aceclofenac"
            dosage = "1 Tablet - After Food"

        else:
            medicine = "Consult Doctor"
            dosage = "As Directed"

        prescription_list.append({
            "patient_name": appointment.patient_name,
            "doctor_name": appointment.doctor_name,
            "symptoms": appointment.symptoms,
            "medicine": medicine,
            "dosage": dosage
        })

    return render_template(
        "prescriptions.html",
        prescriptions=prescription_list
    )
# PATIENT HISTORY
@app.route('/history')
def history():

    latest_appointment = Appointment.query.order_by(
        Appointment.id.desc()
    ).first()

    if latest_appointment:

        record = {
            "patient_name": latest_appointment.patient_name,
            "doctor": latest_appointment.doctor_name,
            "date": latest_appointment.appointment_date,
            "time": latest_appointment.appointment_time,
            "age": latest_appointment.age,
            "blood_group": latest_appointment.blood_group,
            "history": "General Health Checkup"
        }

    else:

        record = {
            "patient_name": "No Patient",
            "doctor": "-",
            "date": "-",
            "time": "-",
            "age": "-",
            "blood_group": "-",
            "history": "-"
        }

    return render_template(
        'patient_history.html',
        record=record
    )

# AVAILABILITY STATUS
@app.route('/availability')
def availability():

    return render_template('availability.html')


# DOCTOR PROFILE
@app.route('/doctor-profile')
def doctor_profile():

    latest_appointment = Appointment.query.order_by(
        Appointment.id.desc()
    ).first()

    if latest_appointment:

        doctor = {

            "name": latest_appointment.doctor_name,

            "specialization": "General Physician",

            "hospital": "RuralCareHub Hospital",

            "experience": "10 Years",

            "phone": "9876543210",

            "email": "doctor@ruralcarehub.com"

        }

    else:

        doctor = {

            "name": "No Doctor",

            "specialization": "-",

            "hospital": "-",

            "experience": "-",

            "phone": "-",

            "email": "-"

        }

    return render_template(
        'doctor_profile.html',
        doctor=doctor
    )


# MANAGE DOCTORS
@app.route('/manage-doctors')
def manage_doctors():

    doctors = Doctor.query.all()

    return render_template(
        'manage_doctors.html',
        doctors=doctors
    )


# MANAGE PATIENTS
@app.route('/manage-patients')
def manage_patients():

    users = User.query.all()

    return render_template(
        'manage_patients.html',
        users=users
    )


# MANAGE APPOINTMENTS
@app.route('/manage-appointments')
def manage_appointments():

    appointments = Appointment.query.all()

    return render_template(
        'manage_appointments.html',
        appointments=appointments
    )


# REPORTS
@app.route('/reports')
def reports():

    total_users = User.query.count()

    total_doctors = Doctor.query.count()

    total_appointments = Appointment.query.count()

    return render_template(
        'reports.html',
        users=total_users,
        doctors=total_doctors,
        appointments=total_appointments
    )


# SETTINGS
@app.route('/settings')
def settings():
    return render_template('settings.html')


# FEEDBACK
@app.route('/feedback')
def feedback():
    return render_template('feedback.html')


# VERIFICATION
@app.route('/verification')
def verification():
    return render_template('verification.html')


# DATABASE MONITORING
@app.route('/database')
def database():
    return render_template('database.html')


# CREATE DATABASE
with app.app_context():
    db.create_all()


# RUN APP
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)