import sys
import tkinter as tk

back_color = '#CAE1F4'
fore_color = '#7ABDE4'

def ex():
    sys.exit()


def submit(e1, e2):
    ip, port = e1.get(), e2.get()
    with open('config.vf', 'w') as file:
        file.write(f"{ip}\n{port}")
    root = tk.Tk()
    root.title('Configure')
    root.geometry('100x75')
    root.configure(background=back_color)
    l1 = tk.Label(root, text='Done!',bg=back_color)
    b1 = tk.Button(root, text='Close', command=lambda: ex(),bg=fore_color, highlightthickness=0)
    l1.place(x=30, y=10)
    b1.place(x=20, y=45)
    root.mainloop()
    return 0


root = tk.Tk()
root.title("Configure")
root.geometry("200x100")
root.configure(background=back_color)
iplabel = tk.Label(root, text="Server IP:",bg=back_color)
plabel = tk.Label(root, text="Server Port:",bg=back_color)
ipentry = tk.Entry(root, text="0.0.0.0", width=11,highlightthickness=0)
pentry = tk.Entry(root, text="00000", width=11,highlightthickness=0)
sbutton = tk.Button(root, text="Configure", width=7, command=lambda: submit(ipentry, pentry),bg=fore_color, highlightthickness=0)
cbutton = tk.Button(root, text="Cancel", width=7, command=lambda: ex(),bg=fore_color, highlightthickness=0)
iplabel.place(x=10, y=10)
plabel.place(x=10, y=40)
ipentry.place(x=100, y=10)
pentry.place(x=100, y=40)
sbutton.place(x=110, y=70)
cbutton.place(x=10, y=70)
root.mainloop()
