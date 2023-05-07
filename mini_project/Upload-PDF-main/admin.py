import pickle
from sklearn.feature_extraction.text import TfidfVectorizer

from flask import Flask, render_template, redirect, url_for, session, request, flash
import psycopg2

import contentEctraction
import resumeclassification
from comparison import obj_jd_profile_comparison
# from skill_extraction import resumeExtraction, resumeExtractor
from contentEctraction import pdfextract,cleanResume
# import sqlite3
import os
# import fitz

app=Flask(__name__)
app.secret_key = 'Kollayikode@98'

app.config['UPLOAD_FOLDER_EMP'] = r"static\PDF\emp"
app.config['UPLOAD_FOLDER_CAN'] = r"static\PDF\can"
# # create a connection to the database
# conn = sqlite3.connect('database.db')
#
# # create a cursor object to execute SQL statements
# cur = conn.cursor()
# print('hiii')
# # check if the table exists
# cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='users'")
# table_exists = cur.fetchone()
#
# # if the table does not exist, create it
# if not table_exists:
#     cur.execute("CREATE TABLE users (id INTEGER PRIMARY KEY AUTOINCREMENT,username TEXT UNIQUE NOT NULL,email TEXT UNIQUE NOT NULL,password TEXT NOT NULL,usertype TEXT NOT NULL);")
#     conn.commit()
#
# # close the cursor and database connection
# cur.close()
# conn.close()
conn = psycopg2.connect(database="postgres", user="postgres",
						password="safvan", host="localhost", port="5432")

# create a cursor
cur = conn.cursor()
conn.commit()

# close the cursor and connection
cur.close()
conn.close()



@app.route('/register', methods=['GET', 'POST'])
def register():
    conn = psycopg2.connect(database="postgres",
                            user="postgres",
                            password="safvan",
                            host="localhost", port="5432")

    cur = conn.cursor()

    if request.method == 'POST':
        # get the form data
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        usertype = request.form['usertype']
        cur.execute("""INSERT INTO user_master (user_name,email,password,user_type) VALUES ('{name}','{email}','{password}','{usertype}');""".format(name=username,email=email,password=password,usertype=usertype))

        # commit the changes
        conn.commit()

        # close the cursor and connection
        cur.close()
        conn.close()

        # redirect to the login page
        return redirect(url_for('login'))
    else:
        # display the registration form
        return render_template('register.html')




@app.route('/login', methods=['GET', 'POST'])
def login():
    conn = psycopg2.connect(database="postgres",
                            user="postgres",
                            password="safvan",
                            host="localhost", port="5432")

    cur = conn.cursor()

    if request.method == 'POST':
        # get the form data
        email = request.form['email']
        password = request.form['password']
        usertype = request.form['usertype']

        # check if the user exists in the database
        cur.execute(f"""select * from user_master where email='{email}' and password = '{password}' and user_type = '{usertype}'; """.format(email=email,password=password,usertype=usertype))
        conn.commit()
        user=cur.fetchone()
        # close the cursor and connection
        print(user)

        # if the user exists, create a session and redirect to the dashboard
        if user:
            username = user[2]
            uid = user[0]
            cur.execute(f"""update user_master set active_status = 1 where id = {uid}; """.format(uid=uid))
            conn.commit()

            cur.close()

            conn.close()
            print(usertype)
            if usertype == 'recruiter':
                return redirect(url_for('employer_upload',username=user[0],user_type=usertype))
                # return render_template('employer.html',username=user[0])

            else:
                # return render_template('employee.html',username=user[0])
                username=user[0]
                return redirect(url_for('employee_upload',username=user[0],user_type=usertype))

        else:
            # if the user doesn't exist, display an error message
            error = 'Invalid email or password'
            return render_template('login.html', error=error)
    else:
        # display the login form
        return render_template('login.html')


@app.route('/logout/<int:username>', methods=['GET', 'POST'])
def logout(username):
    conn = psycopg2.connect(database="postgres",
                            user="postgres",
                            password="safvan",
                            host="localhost", port="5432")

    cur = conn.cursor()


    # get the form data
    uid = username

    # email = request.form['email']
    # password = request.form['password']
    # usertype = request.form['usertype']

    # check if the user exists in the database


    cur.execute(f"update user_master set active_status = 0 where id = {uid};".format(uid=uid))
    conn.commit()

    cur.close()

    conn.close()


    # display the login form
    return render_template('login.html')


@app.route('/')

def index():
    return render_template('index.html')

@app.route('/profile/<user>')
def profile(user):
    return render_template('profile.html',user=user,isActive=True)

@app.route('/books')
def book():
    books = [{'name':'book1','author':'safvan','cover':'https://images.template.net/wp-content/uploads/2015/12/Free-Sample-Vintage-Book-Cover-Template.jpg'},{'name':'book3','author':'saf','cover':'https://damonza.com/wp-content/uploads/portfolio/fiction/Frost9.jpg'},{'name':'book2','author':'safvanck','cover':'https://th.bing.com/th/id/R.427d176de4c401f8e8bdb6047713189e?rik=iL1Bt5%2fVT%2faSrA&riu=http%3a%2f%2fwww.creativindiecovers.com%2fwp-content%2fgallery%2fportfolio%2f10.11B.jpg&ehk=eyk9%2bWG49ICkX3Ja82Ge7G3KyfhZCFgV%2b12eRbbkSWI%3d&risl=&pid=ImgRaw&r=0'},]
    return render_template('books.html',books=books)
#
# @app.route("/employer", methods=["GET", "POST"])
# def employer_upload():
#     conn = psycopg2.connect(database="postgres",
#                             user="postgres",
#                             password="safvan",
#                             host="localhost", port="5432")
#
#     cur = conn.cursor()
#
#     if request.method == 'POST':
#         upload_pdf = request.files['upload_PDF']
#         title = request.form['title']
#         uid = request.form['user_id']
#         if upload_pdf.filename != '':
#             filepath = os.path.join(app.config['UPLOAD_FOLDER_EMP'], upload_pdf.filename)
#             print(filepath)
#             print(upload_pdf.filename)
#             upload_pdf.save(filepath)
#
#
#             # result = resumeExtractor.extractorData(fitz.open(filepath), "pdf")
#             # skills = list(result['skills'])
#             # text = str(result['text'])
#             # skill_list = []
#             # for i in skills:
#             #     skill = i.upper()
#             #     skill_list.append(skill)
#             #
#             # skillss = set(skill_list)
#             # skills = str(skillss)
#             # # print(skills)
#             # # file = pdfextract(filepath)
#             # cleaned_file = skills
#             cur.execute(f"insert into employer_master (ref_user_id,title,file_path) values ({uid},'{title}','{filepath}') ".format(
#                     uid=uid, title=title, filepath=filepath), (upload_pdf.filename,))
#             conn.commit()
#
#             cur.close()
#
#             conn.close()
#
#             # print(cleaned_file)
#             flash("File Upload Successfully", "success")
#
#             return render_template("employer.html")
#     return render_template("employer.html")

@app.route("/employee/<int:username>", methods=["GET", "POST"])
def employee_upload(username):
    conn = psycopg2.connect(database="postgres",
                            user="postgres",
                            password="safvan",
                            host="localhost", port="5432")
    uid = username
    cur = conn.cursor()
    cur.execute(f"select * from candidate_master where ref_user_id={uid}".format(uid=uid))
    data = cur.fetchall()
    conn.close()


    if request.method == 'POST':
        upload_pdf = request.files['upload_PDF']
        title = request.form['title']
        uid = request.form['user_id']

        if upload_pdf.filename != '':
            filepath = os.path.join(app.config['UPLOAD_FOLDER_CAN'], upload_pdf.filename)
            print(filepath)
            print(upload_pdf.filename)
            upload_pdf.save(filepath)

            file = pdfextract(filepath)
            str_file = str(file)
            print("type :",type(str_file))
            text = cleanResume(str_file)

            in_text = contentEctraction.final_resumes
            in_text.append(text)

            vect = TfidfVectorizer(
                sublinear_tf=True,
                stop_words='english',
                max_features=400)

            vect.fit(in_text)

            in_Word_feature = vect.transform(in_text)

            loaded_model = pickle.load(open('final_model.pkl', 'rb'))
            prd1 = loaded_model.predict(in_Word_feature)
            print(prd1)
            leng = len(prd1)
            d = resumeclassification.d
            fields = []
            for i in d:
                x = d.get(i)
                for j in range(leng):
                    if x == prd1[j]:
                        fields.append(i)

            print(fields)
            prediction = fields[-1]
            # result = resumeExtractor.extractorData(fitz.open(filepath), "pdf")
            # skills = list(result['skills'])
            # text = str(result['text'])
            # skill_list = []
            # for i in skills:
            #     skill = i.upper()
            #     skill_list.append(skill)
            #
            # skillss = set(skill_list)
            # skills = str(skillss)
            # # print(skills)
            # cleaned_file = skills
            conn = psycopg2.connect(database="postgres",
                                    user="postgres",
                                    password="safvan",
                                    host="localhost", port="5432")

            cur = conn.cursor()
            cur.execute(f"insert into candidate_master (ref_user_id,title,file_path,text,prediction) values ({uid},'{title}','{filepath}','{text}','{prediction}') ".format(
                    uid=uid, title=title, filepath=filepath,text=text,prediction=prediction), (upload_pdf.filename,))
            conn.commit()

            cur.close()

            conn.close()
            conn = psycopg2.connect(database="postgres",
                                    user="postgres",
                                    password="safvan",
                                    host="localhost", port="5432")

            cur = conn.cursor()
            cur.execute(f"select * from candidate_master where ref_user_id={uid}".format(uid=uid))
            data = cur.fetchall()
            conn.close()

            # print(cleaned_file)
            flash("File Upload Successfully", "success")

            return render_template("employee.html",data=data,username=username)
    return render_template("employee.html",data=data,username=username)


@app.route("/employer/<int:username>", methods=["GET", "POST"])
def employer_upload(username):
    conn = psycopg2.connect(database="postgres",
                            user="postgres",
                            password="safvan",
                            host="localhost", port="5432")
    uid = username
    cur = conn.cursor()
    cur.execute(f"select * from employerr_master where ref_user_id={uid}".format(uid=uid))
    data = cur.fetchall()
    conn.close()


    if request.method == 'POST':
        upload_pdf = request.files['upload_PDF']
        title = request.form['title']
        uid = request.form['user_id']

        if upload_pdf.filename != '':
            filepath = os.path.join(app.config['UPLOAD_FOLDER_CAN'], upload_pdf.filename)
            print(filepath)
            print(upload_pdf.filename)
            upload_pdf.save(filepath)
            file = pdfextract(filepath)
            str_file = str(file)
            print("type :",type(str_file))
            text = cleanResume(str_file)

            in_text = contentEctraction.final_resumes
            in_text.append(text)

            vect = TfidfVectorizer(
                sublinear_tf=True,
                stop_words='english',
                max_features=400)

            vect.fit(in_text)

            in_Word_feature = vect.transform(in_text)

            loaded_model = pickle.load(open('final_model.pkl', 'rb'))
            prd1 = loaded_model.predict(in_Word_feature)
            print(prd1)
            leng = len(prd1)
            d = resumeclassification.d
            fields = []
            for i in d:
                x = d.get(i)
                for j in range(leng):
                    if x == prd1[j]:
                        fields.append(i)

            print(fields)
            prediction = fields[-1]

            # result = resumeExtractor.extractorData(fitz.open(filepath), "pdf")
            # skills = list(result['skills'])
            # text = str(result['text'])
            # skill_list = []
            # for i in skills:
            #     skill = i.upper()
            #     skill_list.append(skill)
            #
            # skillss = set(skill_list)
            # skills = str(skillss)
            # # print(skills)
            # # file = pdfextract(filepath)
            # cleaned_file = skills
            conn = psycopg2.connect(database="postgres",
                                    user="postgres",
                                    password="safvan",
                                    host="localhost", port="5432")

            cur = conn.cursor()
            cur.execute(f"insert into employerr_master (ref_user_id,title,file_path,text,prediction) values ({uid},'{title}','{filepath}','{text}','{prediction}') ".format(
                    uid=uid, title=title, filepath=filepath,text=text,prediction=prediction), (upload_pdf.filename,))
            conn.commit()

            cur.close()

            conn.close()
            conn = psycopg2.connect(database="postgres",
                                    user="postgres",
                                    password="safvan",
                                    host="localhost", port="5432")

            cur = conn.cursor()
            cur.execute(f"select * from employerr_master where ref_user_id={uid}".format(uid=uid))
            data = cur.fetchall()
            conn.close()

            # print(cleaned_file)
            flash("File Upload Successfully", "success")

            return render_template("employer.html",data=data,username=username)
    return render_template("employer.html",data=data,username=username)



@app.route('/update_record/<int:id>', methods=['GET', 'POST'])
def update_record_candidate(id):
    conn = psycopg2.connect(database="postgres",
                            user="postgres",
                            password="safvan",
                            host="localhost", port="5432")
    uid = id
    # username=username
    cur = conn.cursor()
    cur.execute(f"select * from candidate_master where id={uid}".format(uid=uid))
    data = cur.fetchall()
    print(data)
    user_id = data[0][1]
    print(user_id)
    conn.close()
    conn = psycopg2.connect(database="postgres",
                            user="postgres",
                            password="safvan",
                            host="localhost", port="5432")
    # uid = id
    # username=username
    cur = conn.cursor()
    cur.execute(f"select * from candidate_master where ref_user_id={user_id}".format(user_id=user_id))
    data1 = cur.fetchall()
    print(data1)
    conn.close()



    if request.method == 'POST':
        try:
            title = request.form['title']
            upload_pdf = request.files['upload_PDF']
            # print(upload_pdf)
            status = request.form['status']
            print(status)
            filepath = os.path.join(app.config['UPLOAD_FOLDER_EMP'], upload_pdf.filename)
            x = str(filepath)
            print(x)
            if filepath == x :
                filepath = data[0][3]
            print(filepath)
            upload_pdf.save(filepath)
            conn = psycopg2.connect(database="postgres",
                                    user="postgres",
                                    password="safvan",
                                    host="localhost", port="5432")

            cur = conn.cursor()

            cur.execute(
                f"update candidate_master set title='{title}',file_path= '{filepath}',active_status = '{status}' where id = {uid} ".format(status=status,
                    uid=uid, title=title, filepath=filepath), (upload_pdf.filename,))

            conn.commit()

            cur.close()


            flash("Record Update Successfully", "success")
        except:
            flash("Record Update Failed", "danger")
        finally:
            # return render_template("update.html", data=data, id=uid)
            return redirect(url_for("employee_upload",username=user_id,data=data1))
            # return render_template('employee.html',username=u)

            conn.close()
    return render_template("update.html", data=data,id=uid)

@app.route('/delete_record/<int:id>', methods=['GET', 'POST'])
def delete_record(id):
    conn = psycopg2.connect(database="postgres",
                            user="postgres",
                            password="safvan",
                            host="localhost", port="5432")
    uid = id
    # username=username
    cur = conn.cursor()
    cur.execute(f"select * from candidate_master where id={uid}".format(uid=uid))
    data = cur.fetchall()
    print(data)
    user_id = data[0][1]
    print(user_id)
    conn.close()
    conn = psycopg2.connect(database="postgres",
                            user="postgres",
                            password="safvan",
                            host="localhost", port="5432")
    # uid = id
    # username=username
    cur = conn.cursor()
    cur.execute(f"select * from candidate_master where ref_user_id={user_id}".format(user_id=user_id))
    data1 = cur.fetchall()
    print(data1)
    conn.close()
    print(uid)


    try:

        conn = psycopg2.connect(database="postgres",
                                user="postgres",
                                password="safvan",
                                host="localhost", port="5432")

        cur = conn.cursor()
        cur.execute(
            f"delete from candidate_master where id = {uid} ".format(uid=uid))
        conn.commit()

        cur.close()
        print(uid)

        flash("Record Deleted Successfully", "success")
    except:
        flash("Record Deletion Failed", "danger")
    finally:
        # return render_template("update.html", data=data, id=uid)
        return redirect(url_for("employee_upload",username=user_id,data=data1))
        # return render_template('employee.html',username=u)

        conn.close()
    return redirect(url_for("employee_upload", username=user_id, data=data1))


@app.route('/update_record_emp/<int:id>', methods=['GET', 'POST'])
def update_record_employer(id):
    conn = psycopg2.connect(database="postgres",
                            user="postgres",
                            password="safvan",
                            host="localhost", port="5432")
    uid = id
    # username=username
    cur = conn.cursor()
    cur.execute(f"select * from employerr_master where id={uid}".format(uid=uid))
    data = cur.fetchall()
    print(data)
    user_id = data[0][1]
    print(user_id)
    conn.close()
    conn = psycopg2.connect(database="postgres",
                            user="postgres",
                            password="safvan",
                            host="localhost", port="5432")
    # uid = id
    # username=username
    cur = conn.cursor()
    cur.execute(f"select * from employerr_master where ref_user_id={user_id}".format(user_id=user_id))
    data1 = cur.fetchall()
    print(data1)
    conn.close()



    if request.method == 'POST':
        try:
            title = request.form['title']
            upload_pdf = request.files['upload_PDF']
            # print(upload_pdf)
            status = request.form['status']
            print(status)
            filepath = os.path.join(app.config['UPLOAD_FOLDER_EMP'], upload_pdf.filename)
            x = str(filepath)
            print(x)
            if filepath == x :
                filepath = data[0][3]
            print(filepath)
            upload_pdf.save(filepath)
            conn = psycopg2.connect(database="postgres",
                                    user="postgres",
                                    password="safvan",
                                    host="localhost", port="5432")

            cur = conn.cursor()

            cur.execute(
                f"update employerr_master set title='{title}',file_path= '{filepath}',active_status = '{status}' where id = {uid} ".format(status=status,
                    uid=uid, title=title, filepath=filepath), (upload_pdf.filename,))

            conn.commit()

            cur.close()


            flash("Record Update Successfully", "success")
        except:
            flash("Record Update Failed", "danger")
        finally:
            # return render_template("update.html", data=data, id=uid)
            return redirect(url_for("employer_upload",username=user_id,data=data1))
            # return render_template('employee.html',username=u)

            conn.close()
    return render_template("emp_update.html", data=data,id=uid)


@app.route('/delete_record_emp/<int:id>', methods=['GET', 'POST'])
def delete_record_emp(id):
    conn = psycopg2.connect(database="postgres",
                            user="postgres",
                            password="safvan",
                            host="localhost", port="5432")
    uid = id
    # username=username
    cur = conn.cursor()
    cur.execute(f"select * from employerr_master where id={uid}".format(uid=uid))
    data = cur.fetchall()
    print(data)
    user_id = data[0][1]
    print(user_id)
    conn.close()
    conn = psycopg2.connect(database="postgres",
                            user="postgres",
                            password="safvan",
                            host="localhost", port="5432")
    # uid = id
    # username=username
    cur = conn.cursor()
    cur.execute(f"select * from employerr_master where ref_user_id={user_id}".format(user_id=user_id))
    data1 = cur.fetchall()
    print(data1)
    conn.close()
    print(uid)


    try:

        conn = psycopg2.connect(database="postgres",
                                user="postgres",
                                password="safvan",
                                host="localhost", port="5432")

        cur = conn.cursor()
        cur.execute(
            f"delete from employerr_master where id = {uid} ".format(uid=uid))
        conn.commit()

        cur.close()
        print(uid)

        flash("Record Deleted Successfully", "success")
    except:
        flash("Record Deletion Failed", "danger")
    finally:
        # return render_template("update.html", data=data, id=uid)
        return redirect(url_for("employer_upload",username=user_id,data=data1))
        # return render_template('employee.html',username=u)

        conn.close()
    return redirect(url_for("employer_upload", username=user_id, data=data1))

#
# @app.route('/match_record_can/<int:id>', methods=['GET', 'POST'])
# def match_record_can(id):
#     conn = psycopg2.connect(database="postgres",
#                             user="postgres",
#                             password="safvan",
#                             host="localhost", port="5432")
#     uid = id
#     # username=username
#     cur = conn.cursor()
#     cur.execute(f"select * from candidate_master where id={uid}".format(uid=uid))
#     data = cur.fetchall()
#     print(data)
#     user_id = data[0][1]
#     path = data[0][3]
#     print(path)
#     resume_row = pdfextract(path)
#     resume_cleaned = cleanResume(str(resume_row))
#     print(resume_cleaned)
#     conn.close()
#     conn = psycopg2.connect(database="postgres",
#                             user="postgres",
#                             password="safvan",
#                             host="localhost", port="5432")
#     cur = conn.cursor()
#     cur.execute(f"select text from candidate_master ")
#     data1 = cur.fetchall()
#     print(data1)
#     conn.close()
#     pers = []
#     pickle.dump(obj_jd_profile_comparison, open("jd_profile_comparison.pkl", "wb"))
#
#     for row in data1:
#         # Extract the text data from the row
#         resume_text = row[0]
#         if resume_text is None:
#             resume_text = 'empty'
#
#         result = obj_jd_profile_comparison.match(resume_text, resume_cleaned)
#         pers.append(result)
#     print(pers)
#
#     conn = psycopg2.connect(database="postgres",
#                             user="postgres",
#                             password="safvan",
#                             host="localhost", port="5432")
#     cur = conn.cursor()
#     cur.execute(f"select * from candidate_master ")
#     final_data = cur.fetchall()
#     # for i in final_data:
#     #     i['match'] =
#     conn.close()
#
#
#     return render_template("match.html", data=final_data)

@app.route('/match_record_can/<int:id>', methods=['GET', 'POST'])
def match_record_can(id):
    main_title = 'Job Description'
    conn = psycopg2.connect(database="postgres", user="postgres", password="safvan", host="localhost", port="5432")
    uid = id
    # username=username
    cur = conn.cursor()
    cur.execute(f"SELECT * FROM candidate_master WHERE id={uid}")
    data = cur.fetchall()
    user_id = data[0][1]
    path = data[0][3]
    resume_row = pdfextract(path)
    resume_cleaned = cleanResume(str(resume_row))
    conn.close()

    # Retrieve all the candidate data from the database
    conn = psycopg2.connect(database="postgres", user="postgres", password="safvan", host="localhost", port="5432")
    cur = conn.cursor()
    cur.execute(f"SELECT * FROM employerr_master")
    final_data = cur.fetchall()

    # Compute match percentage for each candidate
    for i in range(len(final_data)):
        resume_text = final_data[i][4] # Assuming the resume text is stored in the second column
        match_percentage = obj_jd_profile_comparison.match(resume_text, resume_cleaned)
        final_data[i] = final_data[i] + (match_percentage,) # Append match percentage to the data tuple
    final_data = sorted(final_data, key=lambda x: x[8], reverse=True)
    conn.close()

    return render_template("match.html", data=final_data,title=main_title)


@app.route('/match_record_emp/<int:id>', methods=['GET', 'POST'])
def match_record_emp(id):
    main_title = 'Resumes'
    conn = psycopg2.connect(database="postgres", user="postgres", password="safvan", host="localhost", port="5432")
    uid = id
    # username=username
    cur = conn.cursor()
    cur.execute(f"SELECT * FROM employerr_master WHERE id={uid}")
    data = cur.fetchall()
    # user_id = data[0][1]
    path = data[0][3]
    resume_row = pdfextract(path)
    resume_cleaned = cleanResume(str(resume_row))
    conn.close()

    # Retrieve all the candidate data from the database
    conn = psycopg2.connect(database="postgres", user="postgres", password="safvan", host="localhost", port="5432")
    cur = conn.cursor()
    cur.execute(f"SELECT * FROM candidate_master")
    final_data = cur.fetchall()

    # Compute match percentage for each candidate
    for i in range(len(final_data)):
        resume_text = final_data[i][4] # Assuming the resume text is stored in the second column
        match_percentage = obj_jd_profile_comparison.match(resume_text, resume_cleaned)
        final_data[i] = final_data[i] + (match_percentage,) # Append match percentage to the data tuple
    final_data = sorted(final_data, key=lambda x: x[8], reverse=True)
    conn.close()

    return render_template("match.html", data=final_data,title=main_title)

app.run(debug=True)
