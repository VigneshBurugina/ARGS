from guis import *
from defs import *

# Socket object to establish connection
x = sc.socket()
x.settimeout(5)
try:
    x.connect((host, port))
except:
    msgbox(f'Host {host}:{port} is Down\nCheck Server Config. or try later', c='310x100', d=(110, 60))
    exit()
# Login GUI
username, epas, pas, here = login()
sleep(1)
x.send(username.encode())
sleep(1)
x.send(epas.encode())
rep = msg(x.recv(1024))
x.settimeout(13)
# Repeat if invalid credentials
while rep == "INVALID":
    msgbox('Invalid Login')
    username, epas, pas, here = login()
    x.send(username.encode())
    sleep(1)
    x.send(epas.encode())
    sleep(1)
    rep = msg(x.recv(1024))
msgbox("Successful", 'Login')
if here == 1:
    pc, cc = Pipe()
    p = Process(target=store, args=(username, pas))
    p.start()
    p.join()

sleep(1)
typ = msg(x.recv(1024))
for i in login_gen(typ):
    x.send(i.encode())
    sleep(1)
    rep = msg(x.recv(1024))
    if rep != i:
        msgbox("Try Again")
        pass
    # Handle Requests
    elif rep == 'VIEW INFO':
        # Student - View info
        sleep(1)
        info = msg(x.recv(1024))[1:-1].split(',')
        info_win(info)
    elif rep == "VIEW MARKS":
        # Student - View Marks
        sleep(1)
        ex = msg(x.recv(1024))
        ex = str_to_list(ex)
        repex = choose_exam(ex)
        x.send(repex.encode())
        sleep(1)
        mks = str_to_list(msg(x.recv(1024)))
        mks_win(mks)
    elif rep == "VIEW CLASS INFO":
        # Teacher - View Class Info
        sleep(1)
        cl = msg(x.recv(1024))
        with open(cwd + '/downloads/%s.xlsx' % cl, 'wb') as fl:
            data_size = int(msg(x.recv(1024)))
            data = x.recv(data_size)
            fl.write(data)
        msgbox('File Recieved', 'MySkool')
    elif rep == "DOWNLOAD TEMP":
        # Teacher - Download data template
        exam = choose_exam(['active', 'active', 'active', 'active'])
        sleep(1)
        x.send(exam.encode())
        sleep(1)
        fname = msg(x.recv(1024))
        with open(cwd + '/downloads/%s.xlsx' % fname, 'wb') as fl:
            data_size = int(msg(x.recv(1024)))
            data = x.recv(data_size)
            fl.write(data)
        msgbox('File Recieved', 'MySkool')
    elif rep == "UPLOAD TEMP":
        # Teacher - upload filled template
        fname = file_dialog2(f'{cwd}/uploads').split('/')[-1] # Handle here
        if fname == ():
            pass
        x.send(fname.encode())
        sleep(1)
        with open(f'{cwd}/uploads/{fname}', 'rb') as fl:
            data = fl.read()
            data_size = len(data)
            x.send(str(data_size).encode())
            sleep(1)
            x.send(data)
    elif rep == "GENERATE REPORT TCH":
        # Generate report cards
        cou = 0
        exam = choose_exam(['active', 'active', 'active', 'active'])
        x.send(exam.encode())
        sleep(1)
        lst = int(msg(x.recv(1024)))
        for i in range(lst):
            flnm = msg(x.recv(1024))
            sleep(1)
            data_size = int(msg(x.recv(1024)))
            with open(f'{cwd}/downloads/{flnm}', 'wb') as fl:
                data = x.recv(data_size)
                fl.write(data)
            cou += 1
        msgbox('File Recieved', 'MySkool')
    elif rep == "GET REPORT STU":
        # Generate student report
        ex = msg(x.recv(1024))
        ex = str_to_list(ex)
        repex = choose_exam(ex)
        x.send(repex.encode())
        sleep(1)
        fl = msg(x.recv(1024))
        sleep(1)
        with open(f'{cwd}/downloads/{fl}', 'wb') as fl:
            dl = msg(x.recv(1024))
            sleep(1)
            data = x.recv(int(dl))
            fl.write(data)
        msgbox('File Recieved', 'MySkool')
    elif rep == 'CLOSE':
        # Closed
        sys.exit()
