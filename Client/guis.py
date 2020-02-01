import hashlib
import platform
import sys
import tkinter as tk
import webbrowser
from multiprocessing import Process, Pipe
from os import system, getcwd
from tkinter import filedialog
from tkinter import ttk
from defs import *
from pwdman import get, store
from time import sleep
import socket as sc


cwd = getcwd()
back_color = '#CAE1F4'
fore_color = '#7ABDE4'


def ex():
    """Exit Program"""
    sys.exit()


def get_store(a=None, b=None):
    """Store & Fetch password"""
    if a is None and b is None:
        parent_conn, child_conn = Pipe()
        p = Process(target=get, args=(child_conn,))
        p.start()
        usn = parent_conn.recv()
        pas = parent_conn.recv()
        p.join()
        return usn, pas
    elif a is not None and b is not None:
        p = Process(target=store, args=(a, b))
        p.start()
        p.join()


def login():
    """Login Window"""

    def submit(u, p, v, r):
        """Login - return entered credentials"""
        nonlocal username
        nonlocal pas
        nonlocal here
        nonlocal epas
        here = v.get()
        username = u.get()
        pas = p.get()
        epas = hashlib.blake2b(pas.encode()).hexdigest()
        r.destroy()
        return 0

    here = ''
    epas = ''
    username, pas = get_store()
    root = tk.Tk()
    root.title("Login")
    root.geometry('280x125')
    root.config(background=back_color)
    var = tk.IntVar()
    ulabel = tk.Label(root, text="Name:", bg=back_color)
    plabel = tk.Label(root, text="Password:", bg=back_color)
    uentry = tk.Entry(root, highlightthickness=0)
    pentry = tk.Entry(root, show="*", highlightthickness=0)
    uentry.insert(tk.END, username)
    pentry.insert(tk.END, pas)
    cbutton = tk.Button(root, text="Cancel", command=lambda: ex(), width=10, bg=fore_color, highlightthickness=0)
    sbutton = tk.Button(root, text="Login", command=lambda: submit(uentry, pentry, var, root), width=10,
                        bg=fore_color, highlightthickness=0)
    chk = tk.Checkbutton(root, text="Remember Password", variable=var, onvalue=1, offvalue=0, height=1, width=20,
                         bg=back_color, highlightthickness=0)
    ulabel.place(x=10, y=10)
    plabel.place(x=10, y=40)
    uentry.place(x=80, y=10)
    pentry.place(x=80, y=40)
    cbutton.place(x=20, y=90)
    sbutton.place(x=150, y=90)
    chk.place(x=70, y=60)
    root.mainloop()
    return username, epas, pas, here


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


def file_dialog1(a=""):
    """File Dialog"""

    def cls(a):
        a.destroy()
        return

    root = tk.Tk()
    root.geometry('1x2')
    root.config(background=back_color)
    root.protocol("WM_DELETE_WINDOW", lambda: cls(root))
    root.filename = filedialog.askopenfilename(initialdir=a, title="", filetypes=(
        ("excel files", "*.xlsx"), ("Portable Document Format (PDF)", "*.pdf"),
        ("all files", "*.*")))  # Change Initial Dir
    if root.filename == () or root.filename == "":
        return ''
    if '.xlsx' in root.filename[0].split('/')[-1]:
        if platform.system() == "Linux":
            # Easter Egg
            msgbox("You'r Awesome")
            system(f"libreoffice -o '{root.filename}'")
        elif platform.system() == "Windows":
            system(f"open {root.filename}'")
    elif '.pdf' in root.filename[0].split('/')[-1]:
        if platform.system() == "Linux":
            system(f"libreoffice -o '{root.filename}'")
        elif platform.system() == 'Windows':
            system(f'start "" /max "{root.filename}"')
    root.destroy()


def file_dialog2(a=""):
    """File Dialog"""

    def cls(a):
        a.destroy()
        return

    root = tk.Tk()
    root.geometry('1x2')
    root.config(background=back_color)
    root.title("Choose File")
    root.protocol("WM_DELETE_WINDOW", lambda: cls(root))
    root.filename = filedialog.askopenfilename(initialdir=a, title="", filetypes=(
        ("excel files", "*.xlsx"), ("Portable Document Format (PDF)", "*.pdf"),
        ("all files", "*.*")))  # Change Initial Dir
    x = root.filename
    root.destroy()
    return x


def teacher_main_menu():
    """Main Menu for teachers"""

    def on_closing(a):
        """Exit Program"""
        nonlocal req
        req = 'CLOSE'
        a.destroy()

    def download_temp(a):
        """Download data template"""
        nonlocal req
        req = 'DOWNLOAD TEMP'
        a.destroy()

    def upload_temp(a):
        """Upload data template"""
        nonlocal req  # Change
        req = 'UPLOAD TEMP'
        a.destroy()

    def gen_report(a):
        """Generate report cards"""
        nonlocal req  # Change
        req = 'GENERATE REPORT TCH'
        a.destroy()

    def view_info(a):
        """Get class list"""
        nonlocal req  # Change
        req = 'VIEW CLASS INFO'
        a.destroy()
        return

    def view_download():
        """View Download Folder"""
        file_dialog1(f'{cwd}/downloads')  # Change Dir by argument
        return

    def view_upload():
        """View Upload Folder"""
        file_dialog1(f'{cwd}/uploads')  # Change Dir by argument
        return

    def server_help():
        global host, port
        """Access server's web"""
        webbrowser.open(f'http://{host}:{port + 1}')

    req = ''
    root = tk.Tk()
    root.title("ARGS")
    root.geometry("200x150")
    root.config(background=back_color)
    get_template_icon = tk.PhotoImage(file=f"{cwd}/resources/get_template.png")
    upload_template_icon = tk.PhotoImage(file=f"{cwd}/resources/upload_template.png")
    get_report_icon = tk.PhotoImage(file=f"{cwd}/resources/get_report_tch.png")
    menubar = tk.Menu(root)
    menu1 = tk.Menu(menubar, tearoff=0)
    menu1.add_command(label="Class Info", command=lambda: view_info(root))
    menu1.add_command(label="Help", command=lambda: server_help())
    menu1.add_command(label="Exit", command=lambda: on_closing(root))
    filemenu = tk.Menu(menubar, tearoff=0)
    filemenu.add_command(label="View Downloads", command=lambda: view_download())
    filemenu.add_command(label="View Uploads", command=lambda: view_upload())
    menubar.add_cascade(label="Menu", menu=menu1)
    menubar.add_cascade(label="Files", menu=filemenu)
    get_temp_button = tk.Button(root, text="Download Template", width=17, command=lambda: download_temp(root),
                                highlightthickness=0, bg=fore_color)
    upload_temp_button = tk.Button(root, text="Upload Data Template", width=17, command=lambda: upload_temp(root),
                                   highlightthickness=0, bg=fore_color)
    generate_rep_button = tk.Button(root, text="Generate Report", width=17, command=lambda: gen_report(root),
                                    highlightthickness=0, bg=fore_color)
    get_te_icon = tk.Label(root, image=get_template_icon, width=30, height=30)
    up_te_icon = tk.Label(root, image=upload_template_icon, width=30, height=30)
    gen_re_icon = tk.Label(root, image=get_report_icon, width=30, height=30)
    get_temp_button.place(x=50, y=25)
    upload_temp_button.place(x=50, y=60)
    generate_rep_button.place(x=50, y=95)
    get_te_icon.place(x=10, y=25)
    up_te_icon.place(x=10, y=60)
    gen_re_icon.place(x=10, y=95)
    root.config(menu=menubar)
    root.protocol("WM_DELETE_WINDOW", lambda: on_closing(root))
    root.mainloop()
    return req


def student_main_menu():
    """Student Main Menu"""

    def on_closing(a):
        """Exit Program"""
        nonlocal req
        req = 'CLOSE'
        a.destroy()

    def view_marks(a):
        """View marks"""
        nonlocal req  # Change
        req = 'VIEW MARKS'
        a.destroy()

    def get_report(a):
        """Generate Student report"""
        nonlocal req  # Change
        req = 'GET REPORT STU'
        a.destroy()

    def view_info(a):
        """View info"""
        nonlocal req  # Change
        req = 'VIEW INFO'
        a.destroy()
        return

    def view_download():
        """View download folder"""
        file_dialog1(f'{cwd}/downloads')  # Change Dir by argument
        return

    def view_upload():
        """View uploads folder"""
        file_dialog1(f'{cwd}/uploads')  # Change Dir by argument
        return

    def server_help():
        global host, port
        """Access server's web"""
        webbrowser.open(f'http://{host}:{port + 1}')

    req = ''
    root = tk.Tk()
    root.title("ARGS")
    root.geometry("200x100")
    root.config(background=back_color)
    view_marks_icon = tk.PhotoImage(file=f"{cwd}/resources/view_marks.png")  # Icon
    get_report_icon = tk.PhotoImage(file=f"{cwd}/resources/get_report.png")  # Icon
    menubar = tk.Menu(root)
    menu1 = tk.Menu(menubar, tearoff=0)
    menu1.add_command(label="Info", command=lambda: view_info(root))
    menu1.add_command(label="Help", command=lambda: server_help())
    menu1.add_command(label="Exit", command=lambda: on_closing(root))
    filemenu = tk.Menu(menubar, tearoff=0)
    filemenu.add_command(label="View Downloads", command=lambda: view_download())
    filemenu.add_command(label="View Uploads", command=lambda: view_upload())
    menubar.add_cascade(label="Menu", menu=menu1)
    menubar.add_cascade(label="Files", menu=filemenu)
    view_marks_button = tk.Button(root, text="View Marks", width=17, height=1, command=lambda: view_marks(root),
                                  highlightthickness=0, bg=fore_color)
    get_report_button = tk.Button(root, text="Get Report", width=17, height=1, command=lambda: get_report(root),
                                  highlightthickness=0, bg=fore_color)
    view_icon = tk.Label(root, image=view_marks_icon, width=30, height=30)
    get_icon = tk.Label(root, image=get_report_icon, width=30, height=30)
    view_marks_button.place(x=45, y=15)
    get_report_button.place(x=45, y=50)
    view_icon.place(x=5, y=15)
    get_icon.place(x=5, y=50)
    root.config(menu=menubar)
    root.protocol("WM_DELETE_WINDOW", lambda: on_closing(root))
    root.mainloop()
    return req


def login_gen(a):
    """Generator for login function"""
    while True:
        if a == "STU":
            yield student_main_menu()
        elif a == "TCH":
            yield teacher_main_menu()


def info_win(a):

    def dest(a):
        """Window Destroyer"""
        a.destroy()

    # List of fields
    b = ['Admission No.:', 'Name:', 'Class:', 'Date-of-Birth:', "Father's Name:", "Mother's Name:", "Contact No.:",
         "Address:", "E-Mail:"]
    root = tk.Tk()
    root.title('Student Info')
    root.config(background=back_color)
    but = tk.Button(root, text="OK", command=lambda: dest(root), highlightthickness=0, bg=fore_color)
    for i in range(len(a)):
        lb = tk.Label(root, text="%s %s" % (b[i], a[i]), bg=back_color)
        lb.pack(side="top")
    but.pack(side="bottom")
    root.mainloop()
    return


def choose_exam(l):
    """Choose from list of exams"""
    def ret(a, b):
        """Destroy and return value"""
        nonlocal rep
        rep = a
        b.destroy()
        return

    rep = None
    root = tk.Tk()
    root.title("Exam")
    root.geometry('167x140')
    root.config(background=back_color)
    pa1_button = tk.Button(root, text="Periodic Test - I", width=15, command=lambda: ret("pa1", root),
                           state=l[0], highlightthickness=0, bg=fore_color)
    pa2_button = tk.Button(root, text="Periodic Test - II", width=15, command=lambda: ret("pa2", root),
                           state=l[1], highlightthickness=0, bg=fore_color)
    hy_button = tk.Button(root, text="Mid-Term Exam", width=15, command=lambda: ret("hy", root),
                          state=l[2], highlightthickness=0, bg=fore_color)
    fy_button = tk.Button(root, text="Final Exam", width=15, command=lambda: ret("fy", root),
                          state=l[3], highlightthickness=0, bg=fore_color)
    pa1_button.place(x=10, y=10)
    pa2_button.place(x=10, y=40)
    hy_button.place(x=10, y=70)
    fy_button.place(x=10, y=100)
    root.mainloop()
    return rep


def mks_win(a):
    """Display Marks"""
    def dest(a):
        """Window Destroyer"""
        a.destroy()

    b = ['Admission No.:', 'Name:', 'English:', 'Maximum Marks:', "Science:", 'Maximum Marks:', "Mathematics:",
         'Maximum Marks:', "Social Studies:", 'Maximum Marks:', "Marks Obtained:", "Total Marks:", "Percentage:"]
    root = tk.Tk()
    root.title('Marks')
    root.config(background=back_color)
    but = tk.Button(root, text="OK", command=lambda: dest(root), highlightthickness=0, bg=fore_color)
    for i in range(len(a)):
        lb = tk.Label(root, text="%s %s" % (b[i], a[i]), bg=back_color)
        lb.pack(side="top")
    but.pack(side="bottom")
    root.mainloop()
    return


def counter():
    root = tk.Tk()
    root.geometry('150x100')
    pb = ttk.Progressbar(root, orient="horizontal", length=100, mode="indeterminate")
    l1 = tk.Label(root, text='Downloading...\nPlease Wait')
    l1.place(x=35, y=50)
    pb.place(x=25, y=20)
    pb.start()
    root.mainloop()


# Launch Checks
fc = first_check()

if fc == -1:
    msgbox('Server IP not found \n Use Configurator')
    exit()

# Def in config.vf - network data
with open('config.vf', 'r') as fl:
    data = fl.readlines()
host = data[0].rstrip('\n')
port = int(data[1].rstrip('\n'))
