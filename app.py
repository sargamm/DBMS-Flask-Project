# IMPORTS
from flask import Flask, url_for
from flask import request
from flask import render_template, redirect
from flask import session, jsonify
from datetime import date, datetime
from config import *
from flask_mysqldb import MySQL
from werkzeug.security import check_password_hash, generate_password_hash
import mysql.connector


#INITIALIZATIONS
app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY
app.config['MYSQL_HOST'] = MYSQL_DATABASE_HOST
app.config['MYSQL_USER'] = MYSQL_DATABASE_USER
app.config['MYSQL_PASSWORD'] = MYSQL_DATABASE_PASSWORD
app.config['MYSQL_DB'] = MYSQL_DATABASE_DB
app.config['MYSQL_PORT'] = 3306


#mydb = mysql.connector.connect(
#  host="localhost",
#  user="binaryblood",
#  password='vg261999',
#)

#mydb.close()

#print(mydb)

mysql = MySQL(app)

# APP ROUTES
@app.route('/', methods=['GET'])
def hello_world():
    return render_template('home.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if (request.method  == 'POST'):
        query = "SELECT name, userID, password, roleID from AuthUsers WHERE emailID LIKE (%s)"
        email = request.form.get('email')
        password = request.form.get('password')
        if (email == None or password == None):
            return 'error'
        cur = mysql.connection.cursor()
        cur.execute(str(query), [email])
        x = cur.fetchone()
        if (x == None):
            cur.close()
            return render_template('index.html', errors=["Email does not exist"])
        if (password != x[2]):
            cur.close()
            return render_template('index.html', errors=["Email and Password do not match"])
        #print(result)
        #mysql.connection.commit()
        else:
            session['loggedIn'] = True
            session['userId'] = x[1]
            session['userName'] = x[0].upper()
            session['roleID'] = x[3]
            print(x[3])
            cur.close()
            return render_template('index.html')
    else:
        return render_template('index.html')

@app.route('/signup',methods=['GET','POST'])
def signup():
    if(request.method == 'POST'):
        role = int(request.form.get('role'))
        roles_dictionary={1:"HealthCentreRegister", 2:"MedPractitionerRegister", 3: "GovtOfficialRegister"}
        return redirect(url_for(roles_dictionary[role]))     
    else:
        return render_template('RoleSelect.html')

@app.route('/HealthCentreSignup', methods=['GET', 'POST'])
def HealthCentreRegister():
    if request.method == 'POST':
        if (session.get("loggedIn") != None):
            return render_template('RegisterHealthCentre.html')
        else:
            errors = []
            name = request.form.get('name')
            contact = request.form.get('contact')
            email = request.form.get('email')
            password = request.form.get('password')
            c_password = request.form.get('c_password')
            pincode = request.form.get('pincode')
            address=request.form.get('address')
            NoOfHealthCamps=request.form.get('NoOfHealthCamps')
            OperationalSince=request.form.get('OperationalSince')
            State=request.form.get('state')
            city=request.form.get('City')
            if (password != c_password):
                errors.append("Passwords don't match")
            if (len(pincode) < 6):
                errors.append("Pincode too short")
            if (len(errors) == 0):
                cur = mysql.connection.cursor()
                cur.execute("INSERT INTO AuthUsers(password, emailID, contact, roleID, name) VALUES (%s, %s, %s, %s, %s)", [password, email, contact, 1, name])
                AuthuserId = cur.lastrowid
                cur.execute("INSERT INTO PublicHealthCentre(id,name,pincode,address,NumberOfHealthCamps,OperationalSince,city,state,Contact) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)",[51,name,pincode,address,NoOfHealthCamps,OperationalSince,city,State,contact])
                healthCentreID=cur.lastrowid
                #cur.execute("INSERT INTO AuthUserHealthCentreRelation(AuthUserID,HealthCentreID) VALUES (%s,%s)",[AuthuserId,healthCentreID])
                mysql.connection.commit()
                cur.close()
                return redirect(url_for('login'))
            else:
                return render_template('RegisterHealthCentre.html', errors=errors)
            
    else:
        return render_template('RegisterHealthCentre.html')

@app.route('/MedicalPractitionerSignup', methods=['GET', 'POST'])
def MedPractitionerRegister():
    if request.method == 'POST':
        if (session.get("loggedIn") != None):
            return render_template('RegisterMedPractitioner.html')
        else:
            errors = []
            name = request.form.get('name')
            contact = request.form.get('contact')
            email = request.form.get('email')
            password = request.form.get('password')
            c_password = request.form.get('c_password')
            PracticingSince=request.form.get('PracticingSince')
            licenseNo=request.form.get('license')
            HealthCentreID=request.form.get('healthCentreID')
            if (password != c_password):
                errors.append("Passwords don't match")
            if (len(errors) == 0):
                cur = mysql.connection.cursor()
                cur.execute("INSERT INTO AuthUsers(password, emailID, contact, roleID, name) VALUES (%s, %s, %s, %s, %s)", [password, email, contact, 2, name])
                AuthuserId = cur.lastrowid
                cur.execute("INSERT INTO RegisteredPractitioners(userID, LicenseNumber,name,practicingSince, healthCentreID) Values (%s,%s,%s,%s,%s)", [AuthuserId,licenseNo,name,PracticingSince,HealthCentreID])
                userID=cur.lastrowid
                #cur.execute("INSERT INTO AuthUserHealthCentreRelation(AuthUserId,HealthCentreID) VALUES (%s,%s)",[AuthuserId,userID])
                mysql.connection.commit()
                cur.close()
                return redirect(url_for('login'))
            else:
                return render_template('RegisterMedPractitioner.html', errors=errors)
            
    else:
        return render_template('RegisterMedPractitioner.html')

@app.route('/GovtOfficialSignup', methods=['GET', 'POST'])
def GovtOfficialRegister():
    if (request.method  == 'POST'):
        if (session.get("loggedIn") != None):
            return render_template('signup.html')
        else:
            errors = []
            name = request.form.get('name')
            email = request.form.get('email')
            dateString = request.form.get('dob')
            dob = datetime.strptime(dateString, '%Y-%m-%d').date()
            print(dob)
            password = request.form.get('password')
            c_password = request.form.get('c_password')
            gender = request.form.get('gender')
            pincode = request.form.get('pincode')
            contact = request.form.get('contact')
            if (password != c_password):
                errors.append("Passwords don't match")
            if (len(pincode) < 6):
                errors.append("Pincode too short")
            if (len(errors) == 0):
                cur = mysql.connection.cursor()
                cur.execute("INSERT INTO AuthUsers(password, emailID, roleID, name) VALUES(%s, %s, %s, %s)", [password, email, 1, name])
                mysql.connection.commit()
                cur.close()
                return redirect(url_for('login'))
            else:
                return render_template('signup.html', errors=errors)
            
    else:
        return render_template('signup.html')

@app.route('/logout')
def logout():
    session.pop('loggedIn', None)
    session.pop('userId', None)
    session.pop('userName', None)
    return redirect('/login')

@app.route('/addRecord')
def addRecord():
    return 'record'

@app.route('/generalQuery', methods=['POST'])
def generalQuery():
    country=request.form.get('country')
    country.lower()
    country.capitalize()
    cur = mysql.connection.cursor()
    cur. execute("Select V.name from Vaccinations V where V.VaccineID=(Select VaccinationID from CountryImmunizationRecords,DiseaseVaccineRelation where VaccinationID= VaccineID and CountryName=%s and ICDCode in (select ICD10 from Disease))",[country])
    records = cur.fetchall()
    header_list = ["Vaccines"]
    return jsonify({'data': render_template('result.html', object_list=records, header_list=header_list)})

@app.route('/deleteRecord')
def deleteRecord():
    return 'delete record'

@app.route('/viewRecords')
def viewRecords():
    return 'view records'

@app.route('/covidTimeMap')
def covidTimeMap():
    target = request.args.get('id')
    if target == '1':
        return render_template('nationalTimeLine.html')
    elif target == '2':
        return render_template('nationalTimeLine_recovered.html')
    elif target == '3':
        return render_template('nationalTimeLine_deaths.html')
    else:
        return render_template('nationalTimeLine.html')
    
