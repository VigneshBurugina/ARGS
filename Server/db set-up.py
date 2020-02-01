import hashlib
import tkinter as tk
from os import getcwd
from tkinter import filedialog
import pymysql
import xlrd
import xlsxwriter as xw

back_color = '#CAE1F4'
fore_color = '#7ABDE4'

def getdbdata():
    """Fetch database configuration data"""
    try:
        with open('db.vf', 'r') as fl:
            data = fl.readlines()
        return data
    except FileNotFoundError:  # Solve This!
        print('Use DB Settings First and enter Database Credentials')
        exit()


def generate_input_template():
    """Generates input template"""
    headers = ['Admission No.', 'Name', 'Class', 'Date of Birth', "Father`s Name", "Mother`s Name", "Phone Number",
               'Address', 'E-mail']
    lst = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I']
    c_f = {'bold': True, 'border': True, 'font_size': 14, 'align': 'center'}
    with xw.Workbook('Data.xlsx') as wb:
        ws1 = wb.add_worksheet('Students')
        c_format = wb.add_format(c_f)
        for i in range(0, len(headers)):
            ws1.set_column(f'{lst[i - 1]}:{lst[i - 1]}', 20)
            ws1.write(lst[i] + "1", headers[i], c_format)
        headers1 = ['Employee ID', 'Name', 'Class', 'Phone Number', "E-mail"]
        lst1 = ['A', 'B', 'C', 'D', 'E']
        c_f = {'bold': True, 'border': True, 'font_size': 14, 'align': 'center'}
        ws2 = wb.add_worksheet('Teachers')
        c_format = wb.add_format(c_f)
        for i in range(0, len(headers1)):
            ws2.set_column(f'{lst1[i - 1]}:{lst1[i - 1]}', 20)
            ws2.write(lst[i] + "1", headers1[i], c_format)


def update_input_form(fname):
    """updates database with filled template data"""
    global dbhost, dbuser, dbpas
    main_l = []
    hdrs = ['Admission No.', 'Name', 'Class', 'Date of Birth', "Father`s Name", "Mother`s Name", "Phone Number",
            'Address', 'E-mail']
    dd = {}
    lst = []
    wb = xlrd.open_workbook(fname)
    ws = wb.sheet_by_name('Students')
    x = ws.nrows
    for i in range(1, x):
        for j in range(len(hdrs)):
            val = ws.cell_value(i, j)
            if "/" in str(val):
                tp1 = str(val).split('/')
                val = tp1[0] + "-" + tp1[1] + "-" + tp1[2]
            lst.append(val)
        for k in range(len(hdrs)):
            dd[hdrs[k]] = lst[k]
        main_l.append(dd)
        lst = []
        dd = {}
    with pymysql.connect(dbhost, dbuser, dbpas, 'info', autocommit=True) as db:
        for i in range(len(main_l)):  # Unterminated String
            x = f"""INSERT INTO student (admno,name,class,dob,fathername,mothername,phone,address,email) VALUES ({int(main_l[i]["Admission No."])},'{main_l[i]["Name"]}','{main_l[i]["Class"]}','{main_l[i]["Date of Birth"]}','{main_l[i]["Father`s Name"]}','{main_l[i]["Mother`s Name"]}','{int(main_l[i]["Phone Number"])}','{main_l[i]["Address"]}','{main_l[i]["E-mail"]}')"""
            db.execute(x)
            for j in ['pa1','pa2','hy','fy']:
                y = f"""INSERT INTO exam.{j} (admno,name) values ({int(main_l[i]["Admission No."])},'{main_l[i]["Name"]}')"""
                db.execute(y)
            passhash = hashlib.blake2b(main_l[i]["Name"].encode()).hexdigest()
            db.execute(f"""INSERT INTO class.{main_l[i]["Class"]} values ({int(main_l[i]["Admission No."])},'{main_l[i]["Name"]}',{i+1},'English,Science,Math,Social Studies')""")
            db.execute(f"""INSERT INTO users.users values ('{main_l[i]["Name"]}','{passhash}','STU')""")
            db.execute(f"""INSERT INTO users.user_admno values ('{main_l[i]["Name"]}',{int(main_l[i]["Admission No."])})""")
            print(f'Created Student Record: {main_l[i]["Name"]} {main_l[i]["Class"]}')
    hdrs = ['Employee ID', 'Name', 'Class', 'Phone Number', "E-mail"]
    dd = {}
    main_l = []
    lst = []
    wb = xlrd.open_workbook(fname)
    ws = wb.sheet_by_name('Teachers')
    x = ws.nrows
    for i in range(1, x):
        for j in range(len(hdrs)):
            val = ws.cell_value(i, j)
            if "/" in str(val):
                tp1 = str(val).split('/')
                val = tp1[0] + "-" + tp1[1] + "-" + tp1[2]
            lst.append(val)
        for k in range(len(hdrs)):
            dd[hdrs[k]] = lst[k]
        main_l.append(dd)
        lst = []
        dd = {}
    with pymysql.connect(dbhost, dbuser, dbpas, 'info', autocommit=True) as db:
        for i in range(len(main_l)):
            passhash = hashlib.blake2b(main_l[i]["Name"].encode()).hexdigest()
            x = f"""INSERT INTO teacher (empid,name,class,phone,email) VALUES ({int(main_l[i]["Employee ID"])},'{main_l[i]["Name"]}','{main_l[i]["Class"]}','{main_l[i]["Phone Number"]}','{main_l[i]["E-mail"]}')"""
            db.execute(x)
            db.execute(f"""INSERT INTO users.users values ('{main_l[i]["Name"]}','{passhash}','TCH')""")
            print(f'Created Teacher Record: {main_l[i]["Name"]} {main_l[i]["Class"]}')
    return

def file_dialog(a=""):
    # Choose the template file
    root = tk.Tk()
    root.geometry('1x2')
    root.title("Choose File")
    root.config(background=back_color)
    root.filename = filedialog.askopenfilename(initialdir=a, title="", filetypes=(
        ("excel files", "*.xlsx"), ("all files", "*.*")))  # Change Initial Dir
    x = root.filename
    root.destroy()
    return x


def menu():
    """Main Menu - upload data to Database"""

    def get():
        # Generate template
        generate_input_template()
        root = tk.Tk()
        root.geometry('200x100')
        root.title('DB Set-up')
        root.config(background=back_color)
        l1 = tk.Label(root, text='Template Created - \n Data.xlsx',bg=back_color)
        l1.pack()
        root.protocol('WM_DELETE_WINDOW',lambda: exit())
        root.mainloop()
        return

    def send():
        # Upload template data
        fname = file_dialog()
        update_input_form(fname)
        root = tk.Tk()
        root.geometry('200x100')
        root.title('DB Set-up')
        root.config(background=back_color)
        l1 = tk.Label(root, text='Data uploaded', bg=back_color)
        l1.pack()
        root.protocol('WM_DELETE_WINDOW',lambda: exit())
        root.mainloop()
        return

    root = tk.Tk()
    root.geometry('200x100')
    root.title('DB Set-up')
    root.config(background=back_color)
    b1 = tk.Button(root, text='Create Template', command=lambda: get(), width=20, bg=fore_color)
    b2 = tk.Button(root, text='Use Template', command=lambda: send(), width=20, bg=fore_color)
    b1.pack()
    b2.pack()
    root.protocol('WM_DELETE_WINDOW',lambda: exit())
    root.mainloop()
    return


cwd = getcwd()
dbdat = getdbdata()
dbhost = dbdat[0].rstrip('\n')
dbuser = dbdat[1].rstrip('\n')
dbpas = dbdat[2].rstrip('\n')
menu()
