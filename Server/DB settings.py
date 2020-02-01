import sys
import tkinter as tk
from os import getcwd
import pymysql as ps

cwd = getcwd()

back_color = '#CAE1F4'
fore_color = '#7ABDE4'

def on_entry_click(a):
    """Delete default display on entry box"""
    a.delete(0, 'end')


def close():
    """Exit Program"""
    sys.exit()


def show(a, b):
    """Unhide entered password"""
    global vc
    c = a.get()
    if vc == 0:
        a.config(show='')
        b.update()
        vc = 1
    elif vc == 1:
        a.config(show='*' * len(c))
        b.update()
        vc = 0


def save(a, b, c):
    """Save entered database credentials"""
    # Write in configuration folder
    with open('db.vf', 'w') as fl:
        fl.write(a.get() + '\n')
        fl.write(b.get() + '\n')
        fl.write(c.get() + '\n')
    root = tk.Tk()
    root.title('DB Settings')
    root.geometry('120x50')
    root.config(background=back_color)
    l1 = tk.Label(root, text='Settings Saved')
    l1.place(x=20, y=15)
    root.mainloop()
    return


def test(a, b, c):
    """Test connection with entered credentials"""
    try:
        # Try to connect
        with ps.connect(a.get(), b.get(), c.get()) as db:
            db.close()
        root = tk.Tk()
        root.title('DB Settings')
        root.geometry('140x50')
        root.config(background=back_color)
        l1 = tk.Label(root, text='Database Connected')
        l1.place(x=15, y=15)
        root.mainloop()
    except:
        # Incorrect credentials
        root = tk.Tk()
        root.title('DB Settings')
        root.geometry('120x50')
        root.config(background=back_color)
        l1 = tk.Label(root, text='Settings Incorrect')
        l1.place(x=15, y=15)
        root.mainloop()
    finally:
        return


try:
    # Try to fetch
    with open('db.vf', 'r') as fl:
        data = fl.readlines()
    # If config data exists
    host = data[0].rstrip('\n')
    user = data[1].rstrip('\n')
    pas = data[2].rstrip('\n')
except:
    # if config data does not exist
    host = ''
    user = ''
    pas = ''

vc = 0
firstclick = True

root = tk.Tk()
root.title('DB Settings')
root.geometry('260x110')
root.config(background=back_color)
eyepic = tk.PhotoImage(file=f"{cwd}/resources/eye.png")  # Icon
conpic = tk.PhotoImage(file=f"{cwd}/resources/database-connect.png")  # Icon
l1 = tk.Label(root, text='Host:', bg=back_color)
l2 = tk.Label(root, text='Username:', bg=back_color)
l3 = tk.Label(root, text='Password:', bg=back_color)
e1 = tk.Entry(root, bd=1, highlightthickness=0)
e2 = tk.Entry(root, bd=1, highlightthickness=0)
e3 = tk.Entry(root, show='*', bd=1 , highlightthickness=0)
b1 = tk.Button(root, text='Test', width=15, height=15, image=conpic, command=lambda: test(e1, e2, e3), bg=fore_color)
b2 = tk.Button(root, text='Save', width=10, command=lambda: save(e1, e2, e3), bg=fore_color)
b3 = tk.Button(root, width=15, height=15, image=eyepic, command=lambda: show(e3, root), bg=fore_color)
b4 = tk.Button(root, text='Close', width=10, command=lambda: close(), bg=fore_color)
e1.insert(0, host)
e2.insert(0, user)
e3.insert(0, pas)
e1.bind('<FocusIn>', lambda x: on_entry_click(e1))
e2.bind('<FocusIn>', lambda x: on_entry_click(e2))
e3.bind('<FocusIn>', lambda x: on_entry_click(e3))
l1.place(x=10, y=10)
l2.place(x=10, y=30)
l3.place(x=10, y=50)
e1.place(x=90, y=10)
e2.place(x=90, y=30)
e3.place(x=90, y=50)
b4.place(x=10, y=75)
b2.place(x=155, y=75)
b1.place(x=235, y=10)
b3.place(x=235, y=50)
root.protocol('WM_DELETE_WINDOW',lambda: exit())
root.mainloop()
