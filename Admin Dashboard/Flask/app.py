
from flask import Flask,render_template,request,session,redirect
import mysql.connector
import csv


app = Flask(__name__)


@app.route('/import-csv',methods=['POST'])
def Import_Csv ():
    filename = request.files["csv_file"]
    file_text = filename.read().decode('utf-8')
    
    Reader = csv.DictReader(file_text.splitlines())
    
    data = []

    for each_user in Reader:
        data.append(each_user)

    
    if data :
             
        Mydb = mysql.connector.connect(
        host = "localhost",
        user = "root",
        password = "admin",
        database = 'sis'
        )
        
        cursor = Mydb.cursor()
        
        for each_user in data:
            
            Name = each_user['First_Name']
            Last = each_user['Last_Name']
            Phone = each_user['Phone']
            Email = each_user['Email']
            Register_Number= each_user['Register_Number']
            Institution_Name = each_user['Institution_Name']
            Course_Name = each_user['Course_Name']
            Total = each_user['Total']
            Entry_Date = each_user['Entry_Date']
            Payment_Status = each_user['Payment_Status']
            
            cursor.execute("""INSERT INTO students (First_Name, Last_Name, Phone,
                Email , Register_Number, Institution_Name, Course_Name,
                Total, Entry_Date,Payment_Status) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);""",(Name,Last,Phone,Email,Register_Number,Institution_Name,
                Course_Name,Total,Entry_Date,Payment_Status,))
        
        Mydb.commit()
        cursor.close()
        Mydb.close()
        
        return redirect('/admin')


@app.route('/admin')
def Admin_Page ():
    try:
        Name = session['Name']
        Last = session['Last']
        Email = session['Email']
    
        return render_template('admin.html')
    
    except:

        return redirect('/')

@app.route('/')
def index ():
    
    try:
        print(session['login_error'])
        if session["login_error"] == 'none':
            error = 'none'
        
        else:
            error = session['login_error']
            
    except:
        error = 'none'

    return render_template("index.html",error = error)


@app.route('/login-data',methods = ['POST'])
def Login_process():
    Name_Email = request.form['uname']
    Password = request.form['psw']
    
    if Name_Email and Password:
        Name_Email_found = False

        mydb = mysql.connector.connect(
            host = 'localhost',
            user = "root",
            password = 'admin',
            database = 'sis'
        )
        
        c = mydb.cursor()
        
        if "@" in Name_Email and ".com" in Name_Email:
            
            c.execute("SELECT * FROM sis.admin WHERE Email = %s AND Password = %s;",(Name_Email,Password))
            
            data = c.fetchall()
            
            if data:
                session['Name'] = data[0][0]
                session['Last'] = data[0][1]
                session['Email'] = data[0][2]
                Name_Email_found = True
                
        else:
            
            c.execute("SELECT * FROM sis.admin WHERE First_Name  = %s AND Password = %s;",(Name_Email.lower(),Password))
            data = c.fetchall()
            
            if data :
                session['Name'] = data[0][0]
                session['Last'] = data[0][1]
                session['Email'] = data[0][2]
                Name_Email_found = True
        
        c.close()
        mydb.close()
             
        if Name_Email_found:
            try:
                session['login_error'] = 'none'
            
            except:
                pass
                
            return redirect('/admin')
        
        else:
            session['login_error'] = "Account Does not Exist !"
            
            return redirect('/')
        
    else:
        session['login_error'] = "Data is invalid !"
        return "Data is invalid"

if __name__ == "__main__":
    app.secret_key = "!1@2fdgabb-qmz&*aa:m_+&T%"
    app.run(debug=True)
    