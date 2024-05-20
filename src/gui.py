from generator import Bin
import error
from icon import icon
import tkinter as tk
from tkinter import messagebox, filedialog
import os
import base64


class Window:
    version = 'v1.00.00'
    author = 'Developed by EF'

    def __init__(self):
        self.window = tk.Tk()
        self.window.geometry('400x200')
        self.window.title('Easytech animation generator')
        with open('tmp.ico', 'wb+') as d:
            d.write(base64.b64decode(icon))
        self.window.iconbitmap('tmp.ico')
        self.window.lift()
        os.remove('tmp.ico')
        self.path = '.'
        self.path_var = tk.StringVar()
        self.path_var.set(os.getcwd())
        path_lbl = tk.Label(self.window, textvariable=self.path_var)
        path_lbl.pack()
        path_btn = tk.Button(self.window, text='Chose directory', command=self.update_path)
        path_btn.pack()
        frame_lbl = tk.Label(self.window, text='Frame number')
        frame_lbl.pack()
        self.frame_var = tk.IntVar()
        self.frame_var.set(10)
        frame_entry = tk.Entry(self.window, textvariable=self.frame_var)
        frame_entry.pack()
        num_lbl = tk.Label(self.window, text='Animation number')
        num_lbl.pack()
        self.num_var = tk.IntVar()
        self.num_var.set(3)
        num_entry = tk.Entry(self.window, textvariable=self.num_var)
        num_entry.pack()
        generate_btn = tk.Button(self.window, text='Generate', command=self.click)
        generate_btn.pack()
        developer_lbl = tk.Label(self.window, text=self.author)
        developer_lbl.pack(side='bottom', anchor='e')
        version_lbl = tk.Label(self.window, text=self.version)
        version_lbl.pack(side='bottom', anchor='e')
        self.window.mainloop()

    def __str__(self):
        return f'{self.version}. {self.author}'

    def update_path(self):
        self.path = filedialog.askdirectory(initialdir=os.path.normpath('./'))
        self.path_var.set(self.path)

    def click(self):
        try:
            ani = Bin(FRAME=self.frame_var.get(), NUM=self.num_var.get(), DEFAULT_PATH=self.path)
            ani.generate_ani()
            ani.generate_bin()
            ani.generate_xml()
            os.startfile(ani.main_path)
        except tk.TclError:
            messagebox.showerror(title='Error', message='Wrong input')
        except error.SizeError as ex:
            messagebox.showerror(title='Error', message=str(ex))
        except Exception as ex:
            messagebox.showerror(title='Error', message=str(ex))


if __name__ == '__main__':
    w = Window()
