import tkinter as tk
import pymysql


def getdbdata():
    """Fetch database configuration data"""
    try:
        with open('db.vf', 'r') as fl:
            data = fl.readlines()
        return data
    except FileNotFoundError:  # Solve This!
        print('Use DB Settings First and enter Database Credentials')
        exit()

def dest():
    l = ['users','class','exam','info']
    global dbhost,dbuser,dbpas
    with pymysql.connect(dbhost,dbuser,dbpas) as db:
        for i in l:
            db.execute(f'DROP DATABASE {i}')
    root = tk.Tk()
    root.geometry('200x100')
    root.title('DB Remove')
    root.config(background=back_color)
    l1 = tk.Label(root,text='Data removed successfully',bg=back_color)
    b1 = tk.Button(root,text='Ok!',command=lambda: exit(),bg=fore_color, highlightthickness=0)
    l1.pack(side='top')
    b1.pack(side='bottom')
    root.protocol('WM_DELETE_WINDOW',lambda: exit())
    root.mainloop()
    
back_color = '#CAE1F4'
fore_color = '#7ABDE4'
dbdat = getdbdata()
dbhost = dbdat[0].rstrip('\n')
dbuser = dbdat[1].rstrip('\n')
dbpas = dbdat[2].rstrip('\n')
root = tk.Tk()
root.geometry('200x100')
root.title('DB Remove')
root.config(background=back_color)
l1 = tk.Label(root,text='Delete Data?',bg=back_color)
b1 = tk.Button(root,text='YES',command=lambda: dest(),bg='red', highlightthickness=0)
b2 = tk.Button(root,text='NO',command=lambda: exit(),bg='green', highlightthickness=0)
l1.place(x=60,y=20)
b1.place(x=120,y=50)
b2.place(x=30,y=50)
root.protocol('WM_DELETE_WINDOW',lambda: exit())
root.mainloop()