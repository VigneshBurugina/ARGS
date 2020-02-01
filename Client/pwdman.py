import random
import socket
import sys
import tkinter as tk
from os import getcwd
from time import sleep
from defs import msg, first_check


back_color = '#CAE1F4'
fore_color = '#7ABDE4'


def msgbox(a, b="Error!", c='200x100', d=(60, 60)):
    """ Message Box Utility"""

    def dest(r):
        r.destroy()
        return

    root = tk.Tk()
    root.geometry(c)
    root.title(b)
    root.config(background=back_color)
    msg = tk.Label(root, text=a, font=("Courier", 10), bg=back_color, highlightthickness=0)
    butt = tk.Button(root, text="OK", width=7, command=lambda: dest(root), highlightthickness=0, bg=fore_color)
    msg.place(x=25, y=15)
    butt.place(x=d[0], y=d[1])
    root.protocol("WM_DELETE_WINDOW", ex)
    root.mainloop()
    return


def get(child_conn):
    """Establish a pipe with parent process"""
    with open('data.vf', 'r') as fl:
        usn = decrypt(fl.readline().rstrip('\n'))
        pas = decrypt(fl.readline().rstrip('\n'))
    child_conn.send(usn)
    child_conn.send(pas)
    child_conn.close()


def store(usn, pwd):
    """Store obtained password in file"""
    with open('data.vf', 'w') as fl:
        fl.write(encrypt(usn))
        fl.write('\n')
        fl.write(encrypt(pwd))
        fl.write('\n')
    return 0


def main_menu():
    """Main Menu"""

    def req():

        def yes(a):

            def yes2(a, b):
                global host, port

                def cl(a):
                    a.destroy()

                adm = a.get()
                x = socket.socket()
                x.settimeout(5)
                try:
                    x.connect((host, port))
                except TimeoutError or OSError or ConnectionRefusedError:
                    msgbox(f'Host {host}:{port} is Down\n'
                           f'Check Server Config. or try later', c='310x100', d=(110, 60))
                    exit()
                x.send('pwdmgr'.encode())
                sleep(1)
                x.send(adm.encode())
                sleep(1)
                rep = msg(x.recv(1024))
                if rep == 'NOT FOUND':
                    txt = 'No Account Found \n Re-Check your Info'
                elif rep == 'OK':
                    txt = 'A Link has been sent to \n your registered e-mail.'
                x.close()
                root = tk.Tk()
                root.title('ARGS Password')
                root.geometry('200x100')
                root.config(background=back_color)
                l1 = tk.Label(root, text=txt, bg=back_color)
                b1 = tk.Button(root, text='OK', command=lambda: cl(root), bg=fore_color)
                l1.place(x=20, y=20)
                b1.place(x=70, y=60)
                root.mainloop()
                b.destroy()
                return 0

            a.destroy()
            root = tk.Tk()
            root.title('ARGS Password')
            root.geometry('200x100')
            root.config(background=back_color)
            l2 = tk.Label(root, text='Admission No / Employee ID', bg=back_color)
            ent = tk.Entry(root, width=10)
            but = tk.Button(root, text='Change', command=lambda: yes2(ent, root), bg=fore_color)
            l2.place(x=20, y=10)
            ent.place(x=65, y=35)
            but.place(x=65, y=70)
            root.mainloop()

        def no(a):
            a.destroy()

        root = tk.Tk()
        root.geometry('200x100')
        root.title('ARGS Password')
        root.config(background=back_color)
        l1 = tk.Label(root, text='Request New Password?', bg=back_color)
        b1 = tk.Button(root, text='YES', width=5, command=lambda: yes(root), bg=fore_color)
        b2 = tk.Button(root, text='NO', width=5, command=lambda: no(root), bg=fore_color)
        l1.place(x=35, y=20)
        b1.place(x=20, y=50)
        b2.place(x=120, y=50)
        root.mainloop()

    def view():
        """View Saved Password"""

        def reveal(a, b, c):
            """Reveal hidden password"""
            nonlocal vc
            if vc == 0:
                a.config(text=c)
                b.update()
                vc = 1
            elif vc == 1:
                a.config(text=chr(215) * len(c))
                b.update()
                vc = 0

        def noent():
            """Shows no entry found"""
            nonlocal vc
            root = tk.Tk()
            root.geometry('150x100')
            root.title('ARGS Password')
            root.config(background=back_color)
            l1 = tk.Label(root, text='No Account Found!', bg=back_color)
            b1 = tk.Button(root, text='Ok', width=10, command=lambda: root.destroy(), bg=fore_color)
            l1.place(x=20, y=20)
            b1.place(x=25, y=50)
            root.mainloop()
            vc = 1
            return False

        # open password file and decrypt it
        with open(cwd + '/data.vf', 'r') as fl:
            if len(fl.read()) != 0:
                fl.seek(0)
                fld = fl.readlines()
                usn = (str(fld[0])).rstrip("\n")
                pas = (str(fld[1])).rstrip("\n")
                pas = decrypt(pas)
            else:
                # if not entry of found
                noent()
        vc = 0
        if vc == 0:
            root = tk.Tk()
            root.title('ARGS Password')
            root.geometry('200x100')
            root.config(background=back_color)
            l1 = tk.Label(root, text="Username:", bg=back_color)
            usl = tk.Label(root, text=decrypt(usn), bg=back_color)
            l2 = tk.Label(root, text="Password:", bg=back_color)
            pwl = tk.Label(root, text=chr(215) * len(pas), bg=back_color)
            b1 = tk.Button(root, text='Show', width=6, command=lambda: reveal(pwl, root, pas), bg=fore_color)
            l1.place(x=20, y=10)
            usl.place(x=100, y=10)
            l2.place(x=20, y=40)
            pwl.place(x=100, y=40)
            b1.place(x=100, y=60)
            root.mainloop()

    # Main Menu
    root = tk.Tk()
    root.geometry('200x100')
    root.title('ARGS Password')
    root.config(background=back_color)
    req_button = tk.Button(root, text='Request New Password', width=20, command=lambda: req(), bg=fore_color)
    view_button = tk.Button(root, text='View Saved Password', width=20, command=lambda: view(), bg=fore_color)
    req_button.place(x=17, y=20)
    view_button.place(x=17, y=60)
    root.protocol("WM_DELETE_WINDOW", lambda: sys.exit())
    root.mainloop()


def encrypt(a):
    # Password Encryption
    ri = int(random.randint(10, 500))
    rs = int(random.randint(10, 50))
    r = str(ri) + "`"
    for i in a:
        r = r + chr(ord(i) + (ri + rs + ri * 2 + rs * 3))
    r = r + '`' + str(rs)
    return r


def decrypt(a):
    # Password Decryption
    a = a.split('`')
    ri = int(a[0])
    rs = int(a[2])
    r = ""
    a = a[1]
    for i in a:
        r = r + chr(ord(i) - (ri + rs + ri * 2 + rs * 3))
    return r


cwd = getcwd()

if __name__ == '__main__':
    # If launched as standalone

    # Perform startup checks
    fc = first_check()
    if fc == -1:
        msgbox('Server IP not found \n Use Configurator')
        exit()
    # Network configuration data
    with open('config.vf', 'r') as fl:
        data = fl.readlines()
    host = data[0].rstrip('\n')
    port = int(data[1].rstrip('\n'))
    main_menu()
