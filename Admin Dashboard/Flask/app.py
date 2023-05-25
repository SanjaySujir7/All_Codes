
from hmac import new
from flask import Flask, jsonify,render_template,request,session,redirect
import mysql.connector
import csv


app = Flask(__name__)


@app.route('/update-students-table',methods=['POST'])
def Update_Students_Data():
    details = request.get_json()
    
    if details:
        
        new_list = []
        
        for sublist in details:
            if not new_list:
                new_list.append(sublist)
            else:
                got = False
                
                for x in new_list:
                    if x[0] == sublist[0] and x[1] == sublist[1]:
                        got = True
                        
                if not got :
                    new_list.append(sublist)
        
    
        
        Mydb = mysql.connector.connect(
        host = "localhost",
        user = "root",
        password = "admin",
        database = 'sis'
        )
        
        cursor = Mydb.cursor()
        
        for each_user in new_list:
            Phone = each_user[0]
            Email = each_user[1]
            Course = each_user[2]
            Total = each_user[3]
            Payment_Status = each_user[4]
            
            cursor.execute("UPDATE students SET Course_Name = %s , Total = %s , Payment_Status = %s WHERE Phone = %s AND Email = %s;",
                           (Course,Total,Payment_Status,Phone,Email,))
            
        
        Mydb.commit()
        cursor.close()
        Mydb.close()
        
    
        return jsonify({'result':True})
    
    else:
        return jsonify({'result': False})
    

@app.route('/get-data-csv',methods=['GET'])
def Get_Csv_Data ():
    
    Mydb = mysql.connector.connect(
        host = "localhost",
        user = "root",
        password = "admin",
        database = 'sis'
        )
        
    cursor = Mydb.cursor()
    
    cursor.execute("SELECT * FROM students;")
    data = cursor.fetchall()
    
    if data:
        Students = [{'exist' : True}]
        
        for Each_User in data:

            Name = Each_User[0]
            Last = Each_User[1]
            Phone = Each_User[2]
            Email = Each_User[3]
            Register_Number= Each_User[4]
            Institution_Name = Each_User[5]
            Course_Name = Each_User[6]
            Total = Each_User[7]
            Entry_Date = Each_User[8]
            Payment_Status = Each_User[9]
            
            
            Students.append(
                {
                    'Name' : Name,
                    'Last' : Last,
                    'Phone' :  Phone,   
                    'Email' : Email,
                    'Register_Number' :  Register_Number,
                    'Institution_Name' : Institution_Name,
                    'Course_Name' :  Course_Name,
                    'Total' :  Total,
                    'Entry_Date' : Entry_Date,
                    'Payment_Status' : Payment_Status
                }
                
            )
            
    else:
        Students = {'exist' : False}

    cursor.close()
    Mydb.close()
    return jsonify(Students)



@app.route('/students')
def Students_DashBoard():

    return render_template('Students.html')



@app.route('/import-file',methods=['POST'])
def Import_File ():
    filename = request.files["File"]
    
    if '.csv' in filename.filename:
        
        file_text = filename.read().decode('utf-8')
        Reader = csv.DictReader(file_text.splitlines())
        
        data = []

        for each_user in Reader:
            data.append(each_user)

        if data:
                
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
                
                cursor.execute("SELECT First_Name FROM students WHERE Phone = %s AND Register_Number = %s;",(Phone,Register_Number,))
                if_data_exist = cursor.fetchall()
                
                if if_data_exist :
                    pass
                
                else:
                
                    cursor.execute("""INSERT INTO students (First_Name, Last_Name, Phone,
                        Email , Register_Number, Institution_Name, Course_Name,
                        Total, Entry_Date,Payment_Status) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);""",(Name,Last,Phone,Email,Register_Number,Institution_Name,
                        Course_Name,Total,Entry_Date,Payment_Status,))
            
            Mydb.commit()
            cursor.close()
            Mydb.close()
            
            return redirect('/students')
        
        else:
            return redirect("/students")
        
    else:
        
        return redirect('/students')


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
    