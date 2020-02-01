import tkinter as tk
from os import system, getcwd
import pymysql as psql

back_color = '#CAE1F4'
fore_color = '#7ABDE4'


def getdbdata():
    """Fetch database configuration data"""
    try:
        with open('db.vf', 'r') as fl:
            data = fl.readlines()
        return data
    except FileNotFoundError:
        print('Use DB Settings and enter Database Credentials first')
        exit()


def menu():
    """Main Menu - Database Setup"""

    def submit(r, a, b):
        """Destroy Window and return values"""
        nonlocal d, s
        d = a.get()
        s = b.get().split(',')
        r.destroy()
        return 0
    
    
    d = ''
    s = ''
    root = tk.Tk()
    root.title('DB Initializer')
    root.geometry('325x100')
    root.config(background=back_color)
    l1 = tk.Label(root, text='No. of Divisions (Enter a whole number) -', bg=back_color)
    l2 = tk.Label(root, text='Sections (separated by comma) -', bg=back_color)
    e1 = tk.Entry(root, width=5, highlightthickness=0)
    e2 = tk.Entry(root, width=5, highlightthickness=0)
    b1 = tk.Button(root, text='Initialize', command=lambda: submit(root, e1, e2), width=15, bg=fore_color)
    l1.place(x=10, y=10)
    l2.place(x=10, y=40)
    e1.place(x=270, y=10)
    e2.place(x=270, y=40)
    b1.place(x=90, y=70)
    root.protocol('WM_DELETE_WINDOW',lambda: exit())
    root.mainloop()
    return d, s


def askbox():
    """Asks to upload data to DB"""
    
    res = 0
    
    def yes(a):
        """Returns True and destroys window"""
        nonlocal res
        res = True
        a.destroy()

    def no(a):
        """Returns False and destroys window"""
        nonlocal res
        res = False
        a.destroy()
        exit()

    root = tk.Tk()
    root.title('DB Initialize')
    root.geometry('200x100')
    root.config(background=back_color)
    l1 = tk.Label(root, text='Do you want to \n upload data to the new Database', bg=back_color)
    b1 = tk.Button(root, text='Yes', width=5, command=lambda: yes(root), bg=fore_color)
    b2 = tk.Button(root, text='No', width=5, command=lambda: no(root), bg=fore_color)
    l1.place(x=50, y=10)
    b1.place(x=20, y=40)
    b2.place(x=60, y=40)
    root.protocol('WM_DELETE_WINDOW',lambda: exit())
    root.mainloop()


cwd = getcwd()
# Fetch database credentials from configuration file
dbdat = getdbdata()
dbhost = dbdat[0].rstrip('\n')
dbuser = dbdat[1].rstrip('\n')
dbpas = dbdat[2].rstrip('\n')

clas, sec = menu()
print(int(clas),sec)
# Main databases
dbs = ['info','users', 'exam', 'class']
# Connect to database
with psql.connect(dbhost, dbuser, dbpas, autocommit=True) as db:
    for i in dbs:
        # Create databases
        db.execute('DROP DATABASE IF EXISTS %s' % i)
        print(f'Created Database: {i}')
        db.execute('create database %s' % i)
    for i in ['info', 'exam', 'users']:
        # Execute from pre-written file
        with open("DBSetup/" + i + ".sql", "r") as fl:
            x = fl.readlines()
            print(f'Executing: {i}.sql')
            for i in x:
                db.execute(i.rstrip())
    db.execute('use class')
    for i in range(1,int(clas)+1):
        for j in sec:
            db.execute('create table %s (admno int(11),name varchar(30),rollno int(11),subjects varchar(100))' % (str(
                i) + "_" + j))
            print(f'Created Table: {str(i)+"_"+j}')
print('Database Set-up complete')
"""if askbox():
    system('python3 "db set-up.py"')"""
