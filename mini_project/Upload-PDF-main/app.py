from fitz import fitz
from flask import Flask, render_template, request, flash, redirect, url_for
import os
import sqlite3
import pandas as pd
from skill_extraction import resumeExtraction, resumeExtractor

# from comparison import *
# import contentEctraction
# from contentEctraction import file
# from sklearn.feature_extraction.text import TfidfVectorizer

app = Flask(__name__)
app.secret_key = "123"
app.config['UPLOAD_FOLDER_EMP'] = r"static\PDF\emp"
app.config['UPLOAD_FOLDER_CAN'] = r"static\PDF\can"

# jd = contentEctraction.cleaned_jd
# score = jd_profile_comparison.match(cleaned_jd,resume)
con = sqlite3.connect("MyPDF.db")
con.execute("create table if not exists myfile(pid integer primary key,pdf TEXT)")


con.execute("CREATE TABLE if not exists musers (id INTEGER PRIMARY KEY AUTOINCREMENT,username TEXT UNIQUE NOT NULL,email TEXT UNIQUE NOT NULL,password TEXT NOT NULL,usertype TEXT NOT NULL);")
# con.execute("create table if not exists employeefile(pid integer primary key,pdf TEXT)")


@app.route("/", methods=["GET", "POST"])
def home():
    return render_template('home.html')


import re


def cleanResume(resumeText):
    resumeText = re.sub('http\S+\s*', ' ', resumeText)  # remove URLs
    resumeText = re.sub('RT|cc', ' ', resumeText)  # remove RT and cc
    resumeText = re.sub('#\S+', '', resumeText)  # remove hashtags
    resumeText = re.sub('@\S+', '  ', resumeText)  # remove mentions
    resumeText = re.sub('[%s]' % re.escape("""!"#$%&'()*+,-./:;<=>?@[\]^_`{|}~"""), ' ',
                        resumeText)  # remove punctuations
    resumeText = re.sub(r'[^\x00-\x7f]', r' ', resumeText)
    resumeText = re.sub('\s+', ' ', resumeText)  # remove extra whitespace
    return resumeText


import PyPDF2


def pdfextract(file):
    fileReader = PyPDF2.PdfFileReader(open(file, 'rb'))
    countpage = fileReader.getNumPages()
    count = 0
    text = []
    while count < countpage:
        pageObj = fileReader.getPage(count)
        count += 1
        t = pageObj.extractText()
        #         print (t)
        text.append(t)
    return text


@app.route("/employer", methods=["GET", "POST"])
def employer_upload():
    con = sqlite3.connect("MyPDF.db")
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute("select * from myfile")
    data = cur.fetchall()
    con.close()

    if request.method == 'POST':
        upload_pdf = request.files['upload_PDF']
        if upload_pdf.filename != '':
            filepath = os.path.join(app.config['UPLOAD_FOLDER_EMP'], upload_pdf.filename)
            print(filepath)
            print(upload_pdf.filename)
            upload_pdf.save(filepath)
            con = sqlite3.connect("MyPDF.db")
            cur = con.cursor()
            cur.execute("insert into myfile(pdf)values(?)", (upload_pdf.filename,))
            con.commit()
            result = resumeExtractor.extractorData(fitz.open(filepath), "pdf")
            skills = list(result['skills'])
            skill_list = []
            for i in skills:
                skill = i.upper()
                skill_list.append(skill)

            skills = set(skill_list)
            print(skills)
            # file = pdfextract(filepath)
            cleaned_file = skills

            print(cleaned_file)
            flash("File Upload Successfully", "success")

            con = sqlite3.connect("MyPDF.db")
            con.row_factory = sqlite3.Row
            cur = con.cursor()
            cur.execute("select * from myfile")
            data = cur.fetchall()
            con.close()
            return render_template("employer.html", data=data, output=output, cleaned_file=cleaned_file)
    return render_template("employer.html", data=data, output=output)


@app.route('/update_record/<string:id>', methods=['GET', 'POST'])
def update_record(id):
    con = sqlite3.connect("MyPDF.db")
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute("select * from myfile where pid=?", (id))
    data = cur.fetchall()
    # print(data[0])
    for i in data:
        print(i)
    con.close()

    if request.method == 'POST':
        try:
            upload_pdf = request.files['upload_PDF']
            filepath = os.path.join(app.config['UPLOAD_FOLDER_EMP'], upload_pdf.filename)
            upload_pdf.save(filepath)
            con = sqlite3.connect("MyPDF.db")
            cur = con.cursor()
            cur.execute("UPDATE myfile SET pdf=? where pid=?", (upload_pdf.filename, id))
            con.commit()
            flash("Record Update Successfully", "success")
        except:
            flash("Record Update Failed", "danger")
        finally:
            return redirect(url_for("upload"))
            con.close()
    return render_template("update.html", data=data)


@app.route('/delete_record/<string:id>')
def delete_record(id):
    try:
        con = sqlite3.connect("MyPDF.db")
        cur = con.cursor()
        cur.execute("delete from myfile where pid=?", [id])
        con.commit()
        flash("Record Deleted Successfully", "success")
    except:
        flash("Record Deleted Failed", "danger")
    finally:
        return redirect(url_for("upload"))
        con.close()


# @app.route('/x', methods=['GET', 'POST'])
# @app.route('/match/<string:id>')
# def match(id):
#     try:
#         con = sqlite3.connect("MyPDF.db")
#         cur = con.cursor()
#         cur.execute("delete from myfile where pid=?", [id])
#         con.commit()
#     except:
#         flash("Record Deleted Failed", "danger")
#     finally:
#         return redirect(url_for("upload"))
#         con.close()
# con = sqlite3.connect("MyPDF.db")
# con.row_factory = sqlite3.Row
# cur = con.cursor()
# cur.execute("select * from myfile ")
# data = cur.fetchall()
# con.close()
#
# refile = contentEctraction.file
# jd = pdfextract(refile)
# cleaned_jd = cleanResume(str(jd))
# final_resumes = []
#
# i = 0
# while i < len(Rfiles):
#     file = Rfiles[i]
#     #     dat = create_profile(file)
#     resumeText = str(pdfextract(file))
#     cleaned = cleanResume(resumeText)
#     final_resumes.append(cleaned)
#     i += 1
# pickle.dump(obj_jd_profile_comparison, open("jd_profile_comparison.pkl", "wb"))
# x = len(final_resumes)
# pers = []
# for i in range(x):
#     result = obj_jd_profile_comparison.match(final_resumes[i], cleaned_jd)
#     #     print(result)
#     pers.append(result)
#
# name_lis = []
# i = 0
# while i < len(Rfiles):
#     file = Rfiles[i]
#     base = os.path.basename(file)
#     filename = os.path.splitext(base)[0]
#
#     name = filename.split('_')
#     name2 = name[0]
#     name2 = name2.lower()
#     name_lis.append(name2)
#     i = i + 1
#
#     in_text = final_resumes
#     # terget=data['Category'].values
#
# vect = TfidfVectorizer(
#     sublinear_tf=True,
#     stop_words='english',
#     max_features=400)
#
# vect.fit(in_text)
#
# in_Word_feature = vect.transform(in_text)
#
# loaded_model = pickle.load(open('final_model.pkl', 'rb'))
# prd1 = loaded_model.predict(in_Word_feature)
# # print(prd1)
#
# d = {'Advocate': 0, 'Arts': 1, 'Automation Testing': 2, 'Blockchain': 3, 'Business Analyst': 4, 'Civil Engineer': 5,
#      'Data Science': 6, 'Database': 7, 'DevOps Engineer': 8, 'DotNet Developer': 9, 'ETL Developer': 10,
#      'Electrical Engineering': 11, 'HR': 12, 'Hadoop': 13, 'Health and fitness': 14, 'Java Developer': 15,
#      'Mechanical Engineer': 16, 'Network Security Engineer': 17, 'Operations Manager': 18, 'PMO': 19,
#      'Python Developer': 20, 'SAP Developer': 21, 'Sales': 22, 'Testing': 23, 'Web Designing': 24}
# leng = len(prd1)
# fields = []
# for i in d:
#     x = d.get(i)
#     for j in range(leng):
#         if x == prd1[j]:
#             fields.append(i)
#
# # df = pd.DataFrame(data, columns=['Numbers'])
# data1 = {
#     "Name": name_lis,
#     "Match_Score": pers,
#     "Predicted Feild":fields
# }
#
# output1=pd.DataFrame(data1)
# output=output1.sort_values(by=['Match_Score'], ascending=False).head(10)
#
# return render_template('output.html', tables=[output.to_html(classes='data')],titles=output.columns.values)

# @app.route('/view')
# def job_post():
#     return render_template('view.html',data=data1)

@app.route('/output', methods=("POST", "GET"))
def output():
    return render_template('output.html', tables=[output.to_html(classes='data')], titles=output.columns.values)


@app.route("/employee", methods=["GET", "POST"])
def employee_upload():
    con = sqlite3.connect("MyPDF.db")
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute("select * from myfile")
    data = cur.fetchall()
    con.close()

    if request.method == 'POST':
        upload_pdf = request.files['upload_PDF']

        if upload_pdf.filename != '':
            filepath = os.path.join(app.config['UPLOAD_FOLDER_CAN'], upload_pdf.filename)
            upload_pdf.save(filepath)
            con = sqlite3.connect("MyPDF.db")
            cur = con.cursor()
            cur.execute("insert into myfile(pdf)values(?)", (upload_pdf.filename,))
            con.commit()
            flash("File Upload Successfully", "success")

            con = sqlite3.connect("MyPDF.db")
            con.row_factory = sqlite3.Row
            cur = con.cursor()
            cur.execute("select * from myfile")
            data = cur.fetchall()
            con.close()
            return render_template("employee.html", data=data, output=output)
    return render_template("employee.html", data=data, output=output)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # get the registration information from the form
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        usertype = request.form['usertype']

        # connect to the database
        conn = sqlite3.connect('database.db')
        cur = conn.cursor()

        # check if the username already exists in the database
        cur.execute('SELECT * FROM musers WHERE username = ?', (username,))
        user = cur.fetchone()

        # if the username does not exist, insert the user's information into the database and redirect to the login page
        if not user:
            cur.execute('INSERT INTO musers (username, email, password, usertype) VALUES (?, ?, ?, ?)',
                        (username, email, password, usertype))
            conn.commit()
            return redirect(url_for('login'))

        # if the username already exists, display an error message
        else:
            error = 'Username already exists. Please choose a different username.'
            return render_template('register.html', error=error)

    # if the request method is GET, display the registration form
    else:
        return render_template('register.html')


if __name__ == '__main__':
    app.run(debug=True)
