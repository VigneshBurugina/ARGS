#!/usr/bin/env python3
import os
import random
import shutil
import smtplib
import socket as sc
import ssl
from multiprocessing import Process
import PyPDF2
import logger as lg
import pymysql
import xlrd
import xlsxwriter as xw
from PyPDF2.generic import BooleanObject, NameObject, IndirectObject, NumberObject
import hashlib
import pypdftk
from time import sleep
import sys

def msg(a):
    return str(a)[2:-1]


def getdbdata():
    with open(f'{cwd}/db.vf', 'r') as fl:
        data = fl.readlines()
    return data


def get_actual_ip():
    try:
        s = sc.socket(sc.AF_INET, sc.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        x = s.getsockname()[0]
        s.close()
        return x
    except OSError:
        print('Server is not connected to the Internet', 'Connect & try again', sep='\n')
        exit()


def authenticate(u, p):
    global dbhost, dbuser, dbpas
    with pymysql.connect(dbhost, dbuser, dbpas, 'users') as db:
        db.execute('SELECT username,type FROM users WHERE passhash = "%s"' % p)
        res = db.fetchall()
    if res == () or res[0][0] != u:
        return [False, ""]
    elif res[0][0] == u:
        return [True, res[0][1]]


def send_info(a):
    global dbhost, dbuser, dbpas
    with pymysql.connect(dbhost, dbuser, dbpas, 'users') as db:
        db.execute("SELECT admno FROM user_admno WHERE username = '%s'" % a)
        res = db.fetchall()
        try:
            res = res[0][0]
            db.execute('SELECT * FROM info.student WHERE admno = %d' % res)
            res = list(db.fetchall()[0])
            res[3] = str(res[3])
            return res
        except:
            return 'NO RECORD'


def get_exam(a):
    global dbhost, dbuser, dbpas
    lst = []
    exams = ['pa1', 'pa2', 'hy', 'fy']
    with pymysql.connect(dbhost, dbuser, dbpas, 'exam') as db:
        for i in exams:
            db.execute('SELECT * FROM %s WHERE name="%s"' % (i, a))
            res = db.fetchall()
            if res == ():
                lst.append('disabled')
            else:
                lst.append('normal')
            pass
    return lst


def checkexam(a):
    if a == 'Periodic Assessment - 1':
        return 'pa1'
    elif a == 'Periodic Assessment - 2':
        return 'pa2'
    elif a == 'Mid-Term Exam':
        return 'hy'
    elif a == 'Final Exam':
        return 'fy'


def get_marks(a, b):
    global dbhost, dbuser, dbpas
    with pymysql.connect(dbhost, dbuser, dbpas, 'exam') as db:
        db.execute('SELECT * FROM %s WHERE name= "%s"' % (b, a))
        res = db.fetchall()
    return list(res[0])


def get_class(a):
    global dbhost, dbuser, dbpas
    with pymysql.connect(dbhost, dbuser, dbpas, 'info') as db:
        db.execute('SELECT class FROM teacher WHERE name="%s"' % a)
        res = db.fetchall()
    return res[0][0]


def get_class_student(a):
    global dbhost, dbuser, dbpas
    with pymysql.connect(dbhost, dbuser, dbpas, 'info') as db:
        db.execute(f"SELECT class FROM student WHERE name='{a}'")
        res = db.fetchall()
    return res[0][0]


def get_class_info(a):
    global dbhost, dbuser, dbpas
    with pymysql.connect(dbhost, dbuser, dbpas, 'class') as db:
        db.execute('SELECT * FROM %s' % a)
        res = db.fetchall()
    return res


def generate_class_template(fl, cl):
    headers = ['Admission No.', 'Name', 'Roll Number', 'Subjects']
    lst = ['A', 'B', 'C', 'D']
    c_f = {'bold': True, 'border': True, 'font_size': 14, 'align': 'center'}
    with xw.Workbook(cwd + '/uploads/%s.xlsx' % cl) as wb:  # Change This
        ws = wb.add_worksheet('Marks')
        c_format = wb.add_format(c_f)
        bold = wb.add_format({'bold': True})
        for i in range(0, len(headers)):
            if headers[i] == 'Subjects':
                ws.set_column('%s:%s' % (lst[i], lst[i]), 30)
            else:
                ws.set_column('%s:%s' % (lst[i], lst[i]), 20)
            ws.write(lst[i] + "1", headers[i], c_format)
        tmp = 1
        for i in range(len(fl)):
            tmp += 1
            for j in range(len(fl[i])):
                ws.write(lst[j] + "%d" % tmp, fl[i][j])


def generate_template(c, t, exam, cwd):
    global dbhost, dbuser, dbpas
    with pymysql.connect(dbhost, dbuser, dbpas, 'class') as db:
        db.execute(f'select admno,name from {c}')
        cdb = db.fetchall()
    headers = ['Admission No.', 'Name', 'English', 'English Max', 'Science', 'Science Max', 'Math', 'Math Max',
               'Social Studies', 'Social St. Max', 'Marks Obtained', 'Total', 'Percentage']
    lst = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M']
    c_f = {'bold': True, 'border': True, 'font_size': 14, 'align': 'center'}
    fname = c + " " + rev_get_exam(exam)
    wb = xw.Workbook(f'{cwd}/uploads/{fname}.xlsx')
    ws = wb.add_worksheet('Marks')
    c_format = wb.add_format(c_f)
    bold = wb.add_format({'bold': True})
    ws.write(lst[0] + '1', "Class:", bold)
    ws.write(lst[0] + '2', "Teacher:", bold)
    ws.write(lst[1] + '1', c, bold)
    ws.write(lst[1] + '2', t, bold)
    ws.write(lst[2] + '1', 'Exam:', bold)
    ws.write(lst[3] + '1', rev_get_exam(exam), bold)
    for i in range(1, len(headers) + 1):
        if i in [1, 2]:
            ws.set_column(f'{lst[i - 1]}:{lst[i - 1]}', 25)
        else:
            ws.set_column(f'{lst[i - 1]}:{lst[i - 1]}', 20)
        ws.write(lst[i - 1] + '3', headers[i - 1], c_format)
    for i in range(len(cdb)):
        ws.write(lst[0] + str(i + 4), cdb[i][0])
        ws.write(lst[1] + str(i + 4), cdb[i][1])
        ws.write(lst[10] + str(i + 4),
                 f'=SUM({lst[2] + str(i + 4)},{lst[4] + str(i + 4)},{lst[6] + str(i + 4)},{lst[8] + str(i + 4)})')
        ws.write(lst[11] + str(i + 4),
                 f'=SUM({lst[3] + str(i + 4)},{lst[5] + str(i + 4)},{lst[7] + str(i + 4)},{lst[9] + str(i + 4)})')
        ws.write(lst[12] + str(i + 4), f'=ROUND({lst[10] + str(i + 4)}/{lst[11] + str(i + 4)}*100,1)')
    wb.close()
    return fname


def update_entry_form(fname):
    global dbhost, dbuser, dbpas
    main_l = []
    hdrs = ['Admission No.', 'Name', 'English', 'English Max', 'Science', 'Science Max', 'Math', 'Math Max',
            'Social Studies', 'Social St. Max', 'Marks Obtained', 'Total', 'Percentage']
    dd = {}
    lst = []
    wb = xlrd.open_workbook(fname)
    ws = wb.sheet_by_name('Marks')
    x = ws.nrows
    exam = checkexam(ws.cell_value(0, 3))
    for i in range(3, x):
        for j in range(len(hdrs)):
            lst.append(ws.cell_value(i, j))
        for k in range(len(hdrs)):
            dd[hdrs[k]] = lst[k]
        main_l.append(dd)
        lst = []
        dd = {}
    with pymysql.connect(dbhost, dbuser, dbpas, 'exam', autocommit=True) as db:
        for i in range(len(main_l)):
            x = f"UPDATE {exam} SET science={main_l[i]['Science']}, science_max={main_l[i]['Science Max']}, math={main_l[i]['Math']}, math_max={main_l[i]['Math Max']}, social={main_l[i]['Social Studies']}, social_max={main_l[i]['Social St. Max']}, english={main_l[i]['English']}, english_max={main_l[i]['English Max']}, total={main_l[i]['Total']}, marks_obtained={main_l[i]['Marks Obtained']}, percent={main_l[i]['Percentage']} WHERE admno={int(main_l[i]['Admission No.'])}"
            db.execute(x)
    return 1


def generatereport(field_dictionary, cl):
    def set_need_appearances_writer(writer):
        try:
            catalog = writer._root_object
            if "/AcroForm" not in catalog:
                writer._root_object.update({
                    NameObject("/AcroForm"): IndirectObject(len(writer._objects), 0, writer)})

            need_appearances = NameObject("/NeedAppearances")
            writer._root_object["/AcroForm"][need_appearances] = BooleanObject(True)
            return writer

        except Exception as e:
            print('set_need_appearances_writer() catch : ', repr(e))
            return writer

    outfile = cl + ".pdf"
    infile = cwd + '/templates/report.pdf'
    inputStream = open(infile, "rb")
    pdf_reader = PyPDF2.PdfFileReader(inputStream, strict=False)
    if "/AcroForm" in pdf_reader.trailer["/Root"]:
        pdf_reader.trailer["/Root"]["/AcroForm"].update(
            {NameObject("/NeedAppearances"): BooleanObject(True)})

    pdf_writer = PyPDF2.PdfFileWriter()
    set_need_appearances_writer(pdf_writer)
    if "/AcroForm" in pdf_writer._root_object:
        pdf_writer._root_object["/AcroForm"].update(
            {NameObject("/NeedAppearances"): BooleanObject(True)})

    pdf_writer.addPage(pdf_reader.getPage(0))
    pdf_writer.updatePageFormFieldValues(pdf_writer.getPage(0), field_dictionary)
    page = pdf_writer.getPage(0)
    for j in range(0, len(page['/Annots'])):
        writer_annot = page['/Annots'][j].getObject()
        for field in field_dictionary:
            if writer_annot.get('/T') == field:
                writer_annot.update({
                    NameObject("/Ff"): NumberObject(1)  # make ReadOnly
                })
    outputStream = open(outfile, "wb")
    pdf_writer.write(outputStream)
    inputStream.close()
    outputStream.close()

def generate_student_report(a, b):
    def student_data(a, b):
        global dbhost, dbuser, dbpas
        with pymysql.connect(dbhost, dbuser, dbpas, 'exam') as db:
            db.execute(f"SELECT * FROM {b} WHERE name = '{a}'")
            res = db.fetchone()
        return res

    def set_need_appearances_writer(writer):
        try:
            catalog = writer._root_object
            if "/AcroForm" not in catalog:
                writer._root_object.update({
                    NameObject("/AcroForm"): IndirectObject(len(writer._objects), 0, writer)})

            need_appearances = NameObject("/NeedAppearances")
            writer._root_object["/AcroForm"][need_appearances] = BooleanObject(True)
            return writer

        except Exception as e:
            print('set_need_appearances_writer() catch : ', repr(e))
            return writer

    def create_dict(a):  # Check totals
        data_dict['name'] = a[1]
        data_dict['class'] = get_class_student(a[1])
        data_dict['exam'] = rev_get_exam(b)
        data_dict['english_obt'] = a[2]
        data_dict['english_total'] = a[3]
        data_dict['english_percent'] = str((int(a[2]) / int(a[3])) * 100)[:4]
        data_dict['english_api'] = getapi(data_dict['english_percent'])
        data_dict['science_obt'] = a[4]
        data_dict['science_total'] = a[5]
        data_dict['science_percent'] = str((int(a[4]) / int(a[5])) * 100)[:4]
        data_dict['science_api'] = getapi(data_dict['science_percent'])
        data_dict['math_obt'] = a[6]
        data_dict['math_total'] = a[7]
        data_dict['math_percent'] = str((int(a[6]) / int(a[7])) * 100)[:4]
        data_dict['math_api'] = getapi(data_dict['math_percent'])
        data_dict['social_obt'] = a[8]
        data_dict['social_total'] = a[9]
        data_dict['social_percent'] = str((int(a[8]) / int(a[9])) * 100)[:4]
        data_dict['social_api'] = getapi(data_dict['social_percent'])
        data_dict['obt_total'] = a[-3]
        data_dict['total_total'] = a[-2]
        data_dict['percentage'] = a[-1]
        data_dict['total_api'] = data_dict['english_api'] + data_dict['science_api'] + \
                                 data_dict['math_api'] + data_dict['social_api']
        return data_dict

    x = student_data(a, b)
    data_dict = {}
    outfile = f'{cwd}/uploads/{a}.pdf'
    infile = f'{cwd}/templates/report2.pdf'
    data = create_dict(x)
    input_stream = open(infile, "rb")
    pdf_reader = PyPDF2.PdfFileReader(input_stream, strict=False)
    if "/AcroForm" in pdf_reader.trailer["/Root"]:
        pdf_reader.trailer["/Root"]["/AcroForm"].update(
            {NameObject("/NeedAppearances"): BooleanObject(True)})

    pdf_writer = PyPDF2.PdfFileWriter()
    set_need_appearances_writer(pdf_writer)
    if "/AcroForm" in pdf_writer._root_object:
        pdf_writer._root_object["/AcroForm"].update(
            {NameObject("/NeedAppearances"): BooleanObject(True)})

    pdf_writer.addPage(pdf_reader.getPage(0))
    pdf_writer.updatePageFormFieldValues(pdf_writer.getPage(0), data)
    page = pdf_writer.getPage(0)
    for j in range(0, len(page['/Annots'])):
        writer_annot = page['/Annots'][j].getObject()
        for field in data_dict:
            if writer_annot.get('/T') == field:
                writer_annot.update({
                    NameObject("/Ff"): NumberObject(1)  # make ReadOnly
                })
    output_stream = open(outfile, "wb")
    pdf_writer.write(output_stream)
    input_stream.close()
    output_stream.close()
    outfile = outfile.split('/')[-1]
    return outfile

def get_class_exam_data(adml, exam):
    global dbhost, dbuser, dbpas
    data_list = []
    with pymysql.connect(dbhost, dbuser, dbpas, 'exam') as db:
        for i in adml:
            db.execute(f'SELECT * FROM {exam} WHERE admno = {i}')
            rep = db.fetchone()
            data_list.append(rep)
    return data_list


def rev_get_exam(a):
    if a == 'pa1':
        return 'Periodic Assessment - 1'
    elif a == 'pa2':
        return 'Periodic Assessment - 2'
    elif a == 'hy':
        return 'Mid-Term Exam'
    elif a == 'fy':
        return 'Final Exam'


def getapi(a):
    a = float(a)
    if 95.00 <= a <= 100.00:
        return 6
    elif 90.00 <= a < 95.00:
        return 4
    elif 80.00 <= a < 90.00:
        return 3
    elif 70.00 <= a < 80.00:
        return 2
    elif 60.00 <= a < 70.00:
        return 1
    elif 33.00 <= a < 60.00:
        return 0
    elif 0 <= a < 33.00:
        return -1
    else:
        return -999


def random_genie():
    lst = [65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83,
           84, 85, 86, 87, 88, 89, 90, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106,
           107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121]
    st = ''
    iq = ''
    for i in range(1, 31):
        st = st + chr(lst[random.randint(0, len(lst) - 1)])
        if i in range(1, 6):
            iq = iq + str(random.randint(0, 9))
    return st, iq


def get_email(a):
    global dbhost, dbuser, dbpas
    with pymysql.connect(dbhost, dbuser, dbpas, 'users') as db:
        db.execute(f'SELECT email FROM emails WHERE id = {a}')
        rep = db.fetchone()
        if rep == ():
            return -1
    return rep[0]


def send_email(a, b, c):
    global host, port, email, email_pass
    message = f'''\
    Subject:Password Reset


    Hello,click on the below link to reset your password: \n
    http://{host}:{port + 2}/{a} \n
    Please enter this pin : {b} \n
    This Link will expire after 1 hour. \n

    This is a computer generated email.'''
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", ssl_port, context=context) as server:
        server.login(email, email_pass)
        server.sendmail(email, c, message)


def start_django_server():
    def start():
        global host, port
        os.chdir(f'{cwd}/webserver/webserver')
        os.system(f'python3 manage.py runserver {host}:{port + 1}')

    p = Process(target=start, args=())
    p.start()
    return p.pid


def create_django_pass_server(lnk, pin):
    global host, port
    cwd = os.getcwd()
    os.chdir(f'{cwd}')
    s_cwd = os.getcwd()
    os.system(f'django-admin startapp {lnk}')
    cpr(f'{s_cwd}/default/change_settings.py', f'{s_cwd}/pass_server/settings.py', '~' * 30, lnk)
    cpr(f'{s_cwd}/default/change_urls.py', f'{s_cwd}/pass_server/urls.py', '~' * 30, lnk)
    cpr(f'{s_cwd}/default/app_urls.py', f'{s_cwd}/{lnk}/urls.py', '~' * 30, lnk)
    cpr(f'{s_cwd}/default/app_views.py', f'{s_cwd}/{lnk}/views.py', '~' * 30, lnk)
    cpr(f'{s_cwd}/default/change_submit_views.py', f'{s_cwd}/submit/views.py', '+' * 5, pin)
    os.system(f'python3 manage.py runserver {host}:{port+2}')


def pass_server_reset():
    pass_server_wd = f'{os.getcwd()}/webserver/pass_server'
    dirs = ['pass_server', 'default', 'error' , 'submit', 'templates']
    os.chdir(pass_server_wd)
    for i in os.listdir():
        if i not in dirs:
            try:
                shutil.rmtree(os.path.join(pass_server_wd, i))
            except NotADirectoryError:
                pass
    cpr(f'{pass_server_wd}/default/default_settings.py',f'{pass_server_wd}/pass_server/settings.py')
    cpr(f'{pass_server_wd}/default/default_urls.py',f'{pass_server_wd}/pass_server/urls.py')
    cpr(f'{pass_server_wd}/default/change_submit_views.py',f'{pass_server_wd}/submit/views.py')
    return


def cpr(path1,path2,pat="",rep=""):
    with open(path1,'r') as fl:
        data = fl.read()
    if pat != rep:
        data = data.replace(pat,rep)
    with open(path2, 'w') as fl:
        fl.write(data)
    return


def change_pass(a,b):
    global dbhost, dbuser, dbpas
    hp = hashlib.blake2d(b.encode()).hexdigest()
    with pymysql.connect(dbhost,dbuser, dbpas, 'users') as db:
        db.execute(f'UPDATE users SET password = {hp} WHERE username = {a}')
    return


cwd = os.getcwd()
dbdat = getdbdata()
dbhost = dbdat[0].rstrip('\n')
dbuser = dbdat[1].rstrip('\n')
dbpas = dbdat[2].rstrip('\n')

email = 'noreply.args@gmail.com'
email_pass = 'KVExA3amqMbcbpE'
ssl_port = 465

# Network
host = get_actual_ip()
print(host)
port = 8080

# Logger
logpath = cwd + '/logs/'
lg.begin()
lg.startlogfile(logpath)

#Clear Ports
print("Clearing Ports")
os.system(f'fuser -k {port}/tcp')
os.system(f'fuser -k {port+1}/tcp')

x = sc.socket()
x.setsockopt(sc.SOL_SOCKET, sc.SO_REUSEADDR, 1)
x.bind((host, port))
x.listen(5)
pass_server_reset()
spid = start_django_server()

print("Server Started")
lg.log('Server Started')

while True:
    c, caddr = x.accept()
    lg.log(f"Client Connected: {caddr}")
    print(f"Client Connected: {caddr}")
    username = msg(c.recv(1024))
    if username == 'pwdmgr':
        adm = msg(c.recv(1024))
        x = get_email(adm)
        if x == -1:
            c.send('NOT FOUND'.encode())
            pass
        else:
            c.send('OK'.encode())
            lnk, pin = random_genie()
            send_email(lnk, pin, x)
            p = Process(target=create_django_pass_server, args=(lnk, pin))
            p.start()
            sleep(3600)
            os.system(f'kill -9 {p.pid}')
            pass_server_reset()
            if os.isfile('web.info'):
                with open('web.info','r') as fl:
                    username = fl.readline().rstrip('\n')
                    pas = fl.readline().rstrip('\n')
                change_pass(username, pas)

    pas = msg(c.recv(1024))
    lg.log(f'Client Credentials: {username}')
    x = authenticate(username, pas)
    while not x[0]:
        lg.log(f'{username}: Login Failed')
        x = authenticate(username, pas)
        c.send('INVALID'.encode())
        sleep(2)
        username = msg(c.recv(1024))
        sleep(1)
        pas = msg(c.recv(1024))
    else:
        c.send('CORRECT'.encode())
        sleep(1)
        c.send(x[1].encode())
    lg.log(f'{username}: Login Successful')
    while True:
        try:
            req = msg(c.recv(1024))
            if req in ['VIEW INFO', 'VIEW MARKS', 'GET REPORT', 'VIEW CLASS INFO', 'GENERATE REPORT TCH',
                       'GET REPORT STU', 'UPLOAD TEMP', 'DOWNLOAD TEMP', 'CLOSE']:
                c.send(req.encode())
                sleep(1)
                lg.log(f'{username}: Request -> {req}')
                print(req)
                if req == 'VIEW INFO':
                    c.send(str(send_info(username)).encode())
                elif req == 'VIEW MARKS':
                    c.send(str(get_exam(username)).encode())
                    sleep(1)
                    repex = msg(c.recv(1024))
                    mks = get_marks(username, repex)
                    c.send(str(mks).encode())
                elif req == 'VIEW CLASS INFO':
                    cl = get_class(username)
                    clas_info = get_class_info(cl)
                    generate_class_template(clas_info, cl)
                    lg.log(f'{username}: File: Generated - {cwd + "/uploads/%s.xlsx" % cl}')
                    c.send(cl.encode())
                    with open(cwd + '/uploads/%s.xlsx' % cl, 'rb') as fl:
                        data = fl.read()
                    sleep(1)
                    c.send(str(len(data)).encode())
                    sleep(1)
                    c.send(data)
                    lg.log(f"{username}: File: Sent - {cwd + '/uploads/%s.xlsx' % cl}")
                    for f in os.listdir(f'{cwd}/uploads'):
                        os.remove(os.path.join(f'{cwd}/uploads', f))
                elif req == "DOWNLOAD TEMP":
                    exam = msg(c.recv(1024))
                    sleep(1)
                    cl = get_class(username)
                    clas_info = get_class_info(cl)
                    fname = generate_template(cl, username, exam, cwd)
                    lg.log(f"{username}: File: Generated - {fname}")
                    c.send(fname.encode())
                    with open(cwd + '/uploads/%s.xlsx' % fname, 'rb') as fl:
                        data = fl.read()
                    sleep(1)
                    c.send(str(len(data)).encode())
                    sleep(1)
                    c.send(data)
                    lg.log(f"{username}: File: Sent - {fname}")
                    for f in os.listdir(f'{cwd}/uploads'):
                        os.remove(os.path.join(f'{cwd}/uploads', f))
                elif req == "UPLOAD TEMP":
                    fname = msg(c.recv(1024))
                    with open(f'{cwd}/downloads/{fname}', 'wb') as fl:
                        data_size = int(msg(c.recv(1024)))
                        data = c.recv(data_size)
                        fl.write(data)
                    update_entry_form(f'{cwd}/downloads/{fname}')
                    lg.log(f'{username}: File: Received - {cwd}/downloads/{fname}')
                elif req == 'GENERATE REPORT TCH':
                    exam = msg(c.recv(1024))
                    cl = get_class(username)
                    clas_info = get_class_info(cl)
                    admno_list = []
                    for i in clas_info:
                        admno_list.append(i[0])
                    data = get_class_exam_data(admno_list, exam)
                    cl_a = cl.split('_')
                    exam = rev_get_exam(exam)
                    data_dict = {}
                    for i in data:
                        data_dict['name'] = i[1]
                        data_dict['class'] = cl_a[0]
                        data_dict['section'] = cl_a[1]
                        data_dict['exam'] = exam
                        data_dict['teacher'] = username
                        data_dict['percentage'] = i[-1]
                        data_dict['english_obt'] = i[2]
                        data_dict['english_total'] = i[3]
                        data_dict['english_percent'] = str(
                            (data_dict['english_obt'] / data_dict['english_total']) * 100)[:4]
                        data_dict['english_api'] = getapi(data_dict['english_percent'])
                        data_dict['science_obt'] = i[4]
                        data_dict['science_total'] = i[5]
                        data_dict['science_percent'] = str(
                            (data_dict['science_obt'] / data_dict['science_total']) * 100)[:4]
                        data_dict['science_api'] = getapi(data_dict['science_percent'])
                        data_dict['math_obt'] = i[6]
                        data_dict['math_total'] = i[7]
                        data_dict['math_percent'] = str((data_dict['math_obt'] / data_dict['math_total']) * 100)[:4]
                        data_dict['math_api'] = getapi(data_dict['math_percent'])
                        data_dict['social_obt'] = i[8]
                        data_dict['social_total'] = i[9]
                        data_dict['social_percent'] = str((data_dict['social_obt'] / data_dict['social_total']) * 100)[:4]
                        data_dict['social_api'] = getapi(data_dict['social_percent'])
                        data_dict['obt_total'] = i[10]
                        data_dict['total_total'] = i[11]
                        data_dict['total_percent'] = data_dict['percentage']
                        data_dict['total_api'] = data_dict['english_api'] + data_dict['science_api'] + \
                                                 data_dict['math_api'] + data_dict['social_api']
                        generatereport(data_dict, f'{cwd}/uploads/{data_dict["name"]} - {cl[0]} {cl[1]}')
                        lg.log(
                            f'{username}: File: Generated Report - {cwd}/uploads/{data_dict["name"]} - {cl_a[0]}{cl_a[1]}.pdf')
                    ldir = os.listdir(f'{cwd}/uploads')
                    c.send(str(len(ldir)).encode())
                    sleep(1)
                    for i in ldir:
                        c.send(i.encode())
                        sleep(1)
                        with open(f'{cwd}/uploads/{i}', 'br') as fl:
                            data = fl.read()
                            data_size = len(data)
                        c.send(str(data_size).encode())
                        sleep(1)
                        c.send(data)
                    for f in ldir:
                        os.remove(os.path.join(f'{cwd}/uploads', f))
                elif req == 'GET REPORT STU':
                    c.send(str(get_exam(username)).encode())
                    sleep(1)
                    exam = msg(c.recv(1024))
                    fl = generate_student_report(username, exam)
                    c.send(fl.encode())
                    sleep(1)
                    with open(f'{cwd}/uploads/{fl}', 'rb') as fl:
                        data = fl.read()
                        c.send(str(len(data)).encode())
                        sleep(1)
                        c.send(data)
                elif req == 'CLOSE':
                    os.chdir(cwd)
                    os.system(f'kill -9 {spid}')
                    sleep(1)
                    os.execv(f'/files/Vignesh/Server/Server.py', sys.argv)
                    #os.system('./Server.py')
                
        except OSError:
            os.chdir(cwd)
            os.system(f'kill -9 {spid}')
            os.execv(f'/files/Vignesh/Server/Server.py', sys.argv)
            #os.system('./Server.py')
            
        
        except:
            os.chdir(cwd)
            print('ERROR: 404')
            os.system(f'kill -9 {spid}')
            sleep(1)
            os.execv(f'/files/Vignesh/Server/Server.py', sys.argv)
            #os.system('./Server.py')
        
lg.end()
lg.endlogfile()
