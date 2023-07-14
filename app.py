from flask import Flask , redirect,url_for,render_template , request , session,flash,g
from flask_sqlalchemy import SQLAlchemy
import os
import base64
import io
from pathlib import Path
import threading
sem = threading.Semaphore()
import subprocess
import sqlite3
import time

current_dir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///"+os.path.join(current_dir,"database.sqlite3")
db = SQLAlchemy()
db.init_app(app)
# Session
app.secret_key = os.urandom(34)

from model import *
db.init_app(app)
app.app_context().push()

# ADMIN Functions
@app.route('/admin')
def admin():
    return render_template('admin_login.html')

@app.route('/admin_login' ,methods=['post'])
def admin_login():
    if request.method == 'POST':
        Adminusername = request.form.get('adminUserName')
        Adminpassword = request.form.get('AdminPassword')
        conn = sqlite3.connect('database.sqlite3')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Admin WHERE username=? AND password=?", (Adminusername, Adminpassword))
        result = cursor.fetchone()
        print (result)
        if result:
            session['admin'] = Adminusername
            print(">>>" , session['admin'])
            print("login successful")
            conn.close()
            return redirect(url_for('AdminControl1'))
        else:
            print("invalid login")
            conn.close()
            return redirect(url_for('admin'))
    else:
        return render_template('admin_login.html')

@app.route('/AdminControl1')
def AdminControl1():
    if "admin" in session:
        conn = sqlite3.connect('database.sqlite3')
        cursor = conn.cursor()
        cursor.execute('select * from user')
        data = cursor.fetchall()
        conn.close()
        return render_template('AdminReviewUsers.html',data=data)
    else:
        return render_template('admin_login.html')
    
@app.route('/AdminControl2')
def AdminControl2():
    if "admin" in session:
        return render_template('AdminRemoveUserBlock.html')
    else:
        return render_template('admin_login.html')

@app.route('/search',methods=['GET', 'POST'])
def search():
    query = request.args.get('query')
    conn = sqlite3.connect('database.sqlite3')
    cursor = conn.cursor()
    cursor.execute(f"select username,isBlocked from user where ID = '{query}'")
    results = cursor.fetchall()
    conn.close()
    return render_template('AdminRemoveUserBlock.html', query=query, results=results)

@app.route('/RemoveBlock',methods=['GET', 'POST'])
def RemoveBlock():
    query = request.args.get('query2')
    conn = sqlite3.connect('database.sqlite3')
    cursor = conn.cursor()
    cursor.execute(f"update user set isBlocked = 0 where ID = '{query}'")
    conn.commit()
    print("Block Removed")
    conn.close()
    return render_template('AdminRemoveUserBlock.html', query=query)

#################################################################

# USER Functions

# Home Page
@app.route('/')
def home():
    session.clear()
    return render_template('Home.html')

# login Page
@app.route('/login')
def Login():
    session.clear()
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('username',None)
    return render_template('login.html')
    
@app.route('/logoutAdmin')
def logoutAdmin():
    session.pop('admin',None)
    return render_template('admin_login.html')

# Authenticate login
@app.route('/login_user' , methods=['post'])

def login_user():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        users = User.query.filter_by(username=username, password=password)
        usersName = User.query.filter_by(username=username)
        checkUsName=[userN for userN in usersName]
        check = [user for user in users]
        conn  = sqlite3.connect('database.sqlite3')
        cursor = conn.cursor()
        if check:
                session['username'] = check[0].username
                isBlocked = cursor.execute("select isBlocked from user where username = '" + str(session["username"]) + "'").fetchone()[0]
                if isBlocked >= 3:
                    conn.close()
                    session.clear()
                    flash('Your Account Is Blocked. Review Customer Service')
                    return render_template('login.html')
                else:
                    conn.close()
                    return redirect(url_for("faceAuth"))
        else:
            print("LOGIN FAILED!!!!!!")
            flash('* Invalid Username or password')
            if checkUsName:
                cursor.execute("UPDATE user SET isBlocked = isBlocked + 1 WHERE UserName = '"+username+"'")
                conn.commit()
                print("Incremeanted")
                conn.close()
                return render_template('login.html')
            return render_template('login.html')
    else:
        return render_template('login.html')

# Profile Page
@app.route('/profile')
def profile():
    if "username" in session:
        
        conn  = sqlite3.connect('database.sqlite3')
        cursor = conn.cursor()
        usID = cursor.execute("select id from user where username = '" + str(session["username"]) + "'").fetchone()[0]
        uspass = cursor.execute("select password from user where username = '" + str(session["username"]) + "'").fetchone()[0]
        usFirstName = cursor.execute("select FirstName from user where username = '" + str(session["username"]) + "'").fetchone()[0]
        usLastName = cursor.execute("select LastName from user where username = '" + str(session["username"]) + "'").fetchone()[0]
        usEmail = cursor.execute("select Email from user where username = '" + str(session["username"]) + "'").fetchone()[0]
        usPhone = cursor.execute("select phone from user where username = '" + str(session["username"]) + "'").fetchone()[0]
        usBalance = cursor.execute("select Balance from user where username = '" + str(session["username"]) + "'").fetchone()[0]
        usphoto = cursor.execute("select photo from user where username = '" + str(session["username"]) + "'").fetchone()[0]
        isBlocked = cursor.execute("select isBlocked from user where username = '" + str(session["username"]) + "'").fetchone()[0]
        FullName = cursor.execute("select fullName from user where username = '" + str(session["username"]) + "'").fetchone()[0]
        encoded_image = base64.b64encode(usphoto).decode('utf-8')
        base64_encoded_photo = 'data:image/png;base64,'+encoded_image
        conn.close()
        return render_template('profile.html' , userID = usID , userpass = uspass , usFName = usFirstName , 
                                            usLName = usLastName ,usEmail = usEmail , usPhone=usPhone ,
                                            usBalance=usBalance ,usphoto = base64_encoded_photo,
                                            isBlocked=isBlocked,FullName=FullName)
    else:
        return render_template('login.html')

# FaceRecognition Page
@app.route('/faceAuth')
def faceAuth():
    if "username" in session :
        print(session["username"])
        g.accVoice = True
        print("********************************")
        return render_template('faceAuth.html')
    else:
        g.accVoice = False
        print("Login First")
        return render_template('login.html')

# VoiceRecognition Page
@app.route('/voiceAuth')
def voiceAuth():
    if "username" in session:
        print(session["username"])
        return render_template('voiceAuth.html')
    else:
        print("User Not loged in")
    return render_template('login.html')

# Method That Save Image From base64 To png
@app.route('/uploadimage',methods=['POST'])
def uploadimage():
    if "username" in session:
        start_Time = time.time()
        sem.acquire()
        user_name = session["username"]
        global userAccss
        data = request.get_json() #Requist with all data

        # User Images List
        userImagesData =[]
        position=[]
        # Append User First Image In List
        userImagesData.append(data['USER_CAP1'])
        # Append User Second Image In List
        userImagesData.append(data['USER_CAP2'])
        # Append User Third Image In List
        userImagesData.append(data['USER_CAP3'])

        position.append(data['pos1'])
        position.append(data['pos2'])
        position.append(data['pos3'])
        
        prefix = 'data:image/png;base64,'
        positionsList=[position[0],position[1],position[2]]

        for i in range(0,3):
            userImagesData[i] = userImagesData[i][len(prefix):]
            userImagesData[i] = base64.b64decode(userImagesData[i])     
            input_folder = Path(f'face_Recognition_Utilities/SVC_Testimgs/Users_Photos/{user_name}/{positionsList[i]}.png')
            input_folder.parent.mkdir(exist_ok=True, parents=True)
            input_folder_path = str(input_folder)
            # Write images
            with open (input_folder_path,'wb') as f:
                f.write(userImagesData[i])

        print("identifying png images By Face Model ...")
        # Call Python File
        from Face_Recognition import FaceRec_Model
        userAccss = FaceRec_Model(user_name,positionsList)
        print("userAccess is : ", userAccss)
        
        if userAccss == True:
            sem.release()
            end_time = time.time()
            execution_time = end_time - start_Time
            print(f"Execution Time Is {execution_time}")
            return str(userAccss)
        else:
            sem.release()
            end_time = time.time()
            execution_time = end_time - start_Time
            print(f"Execution Time Is {execution_time}")
            return str(userAccss)

# Method That Save Image From base 64 to wav
@app.route('/uploadwav', methods=['POST'])
def uploadwav():
    if "username" in session:
        sem.acquire()
        user_name = session["username"]
        data = request.get_json() #Requist with all data
        wav_data  = data['soundwav'] # image
        prefix = 'data:audio/wav;base64,'
        cuttedbase64 = wav_data[len(prefix):]
        # print("Base 64 Voice is " , cuttedbase64)
        wav_recovered = base64.b64decode(cuttedbase64)
        input_folder = Path('Voice_Recognition_Utilities/AuthenticationWaves/' + user_name +'/' +'oriSound.wav')
        input_folder2 = Path('Voice_Recognition_Utilities/AuthenticationWaves/' + user_name +'/' + user_name +'.wav')
        input_folder.parent.mkdir(exist_ok=True, parents=True)
        with open (str(input_folder),'wb') as f:
            f.write(wav_recovered)
            subprocess.call(['ffmpeg','-y','-i',str(input_folder),str(input_folder2)])
        print("Identifying WAV file By Voice Model ...")
        print("userName is " , user_name)
        
        from Voice_Recognition_new import VoiceRec_Model
        print("MODEL Imported !!")
        FinaluserAccss = VoiceRec_Model(user_name)
        print("FinaluserAccss :::" , FinaluserAccss)
        if FinaluserAccss == True:
            sem.release()
            return str(FinaluserAccss)
        else:
            sem.release()
            return str(FinaluserAccss)

# Help
@app.route('/userhelp')
def userhelp():
    return render_template('Help.html')

# OTP
@app.route('/otpSend' , methods=['POST','GET'])
def otpSend():
    if "username" in session:
        print(session['username'])
        conn = sqlite3.connect('database.sqlite3')
        cursor = conn.cursor()
        cursor.execute(f"select Email From user where username = '{session['username']}'")
        UserEmail = cursor.fetchone()[0]
        conn.close()
        from SendMail import send_Mail
        OTP_Result = send_Mail(UserEmail , session['username'])
        conn = sqlite3.connect('database.sqlite3')
        cursor = conn.cursor()
        cursor.execute(f"UPDATE user SET OTP ={OTP_Result} WHERE UserName ='{session['username']}'")
        conn.commit()
        conn.close()
        return render_template('otp.html')
    else:
        return render_template('login.html')

@app.route('/otpVerify',methods=['POST','GET'])
def otpVerify():
    if "username" in session:
        FormOTP = request.form.get('userOTP')
        conn = sqlite3.connect('database.sqlite3')
        curser = conn.cursor()
        curser.execute(f"select OTP from user WHERE UserName ='{session['username']}'")
        OTP = curser.fetchone()[0]
        conn.close()
        OTP = int(OTP)
        FormOTP = int(FormOTP)
        if (OTP == FormOTP):
            return redirect(url_for('profile'))
        else:
            flash('* Invalid OTP')
            return render_template('otp.html')
    else:
        return render_template('login.html')





if __name__ == '__main__':
    # app.run(debug=True,host='192.168.10.55',ssl_context=("cert.pem","key.pem"))s
    app.run(debug=False,host='192.168.1.5')