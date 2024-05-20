from generator import Bin
import error
from icon import icon
import tkinter as tk
from tkinter import messagebox, filedialog
import os
import base64


class Window:
    version = 'v1.1.0'
    author = 'Developed by EF'

    def __init__(self):
        self.window = tk.Tk()
        self.window.geometry('400x300')
        self.window.title('Easytech Animation Generator')
        with open('tmp.ico', 'wb+') as d:
            d.write(base64.b64decode(icon))
        self.window.iconbitmap('tmp.ico')
        self.window.lift()
        os.remove('tmp.ico')
        self.window.columnconfigure(0, weight=1)
        self.window.rowconfigure(tuple(range(12)), weight=1)
        self.main_layouts()
        self.window.mainloop()

    def __str__(self):
        return f'{self.version}. {self.author}'

    def main_layouts(self):
        self.path = '.'
        self.path_var = tk.StringVar()
        self.path_var.set(os.getcwd())
        path_lbl = tk.Label(self.window, textvariable=self.path_var)
        path_lbl.grid(column=0, row=0)
        path_btn = tk.Button(self.window, text='Chose path', command=self.update_path)
        path_btn.grid(column=0, row=1)
        self.frame_var = tk.IntVar()
        self.frame_var.set(10)
        frame_lbl = tk.Label(self.window, text='Frame number')
        frame_lbl.grid(column=0, row=2)
        frame_entry = tk.Entry(self.window, textvariable=self.frame_var)
        frame_entry.grid(column=0, row=3)
        self.num_var = tk.IntVar()
        self.num_var.set(3)
        num_lbl = tk.Label(self.window, text='Animation number')
        num_lbl.grid(column=0, row=4)
        num_entry = tk.Entry(self.window, textvariable=self.num_var)
        num_entry.grid(column=0, row=5)
        time_btn = tk.Button(self.window, text='Advance setting', command=self.advance_setting)
        time_btn.grid(column=0, row=6)
        self.time_var = tk.IntVar()
        self.time_var.set(4)
        self.open = False
        generate_btn = tk.Button(self.window, text='Generate', command=self.click)
        generate_btn.grid(column=0, row=9)
        info_lbl = tk.Label(self.window, text=f'{self.version}\n{self.author}')
        info_lbl.grid(column=0, row=10, sticky=tk.SE)

    def update_path(self):
        self.path = filedialog.askdirectory(initialdir=os.path.normpath('./'))
        self.path_var.set(self.path)

    def advance_setting(self):
        if not self.open:
            self.time_lbl = tk.Label(self.window, text='Animation interval time')
            self.time_entry = tk.Entry(self.window, textvariable=self.time_var)
            self.time_lbl.grid(column=0, row=7)
            self.time_entry.grid(column=0, row=8)
            self.open = True
            self.window.update()
        else:
            self.time_lbl.destroy()
            self.time_entry.destroy()
            self.open = False

    def click(self):
        try:
            ani = Bin(FRAME=self.frame_var.get(), NUM=self.num_var.get(),
                      TIME=self.time_var.get(), DEFAULT_PATH=self.path)
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
