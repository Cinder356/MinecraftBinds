import keyboard
import pyautogui
from time import sleep
import sqlite3
from tkinter import *

class Bind:

    def __init__(self, hotkey, id, name, text=""):
        self.keyboard = keyboard.add_hotkey(hotkey, self.Write)
        self.hotkey = hotkey
        self.text = text
        self.id = id
        self.name = name

    def Write(self):
        pyautogui.press("/")
        sleep(0.01)
        pyautogui.typewrite(self.text)
        sleep(0.01)
        pyautogui.press("enter")

    def delete(self, all_labels_binds):
        print(f'''
        {self}
        {id(self)}
        {App.all_binds}
        ''')

        for label in all_labels_binds[self]:
            label.destroy()
        try:
            keyboard.remove_hotkey(self.keyboard)
        except:
            pass
        cur.execute("DELETE FROM 'binds' WHERE id=(?)", (self.id,))
        con.commit()
        index = App.all_binds.index(self)
        del App.all_binds[index]

class App(Tk):
    all_binds = []

    def __init__(self):
        super().__init__()
        self.geometry('350x250')
        self.title('Minecraft Binds')
        self.resizable(False, False)

        self.var_bind_name = StringVar()
        self.var_bind_command = StringVar()
        self.var_bind_hotkey = StringVar()

        # errors
        self.label_error = Label(master=self, text='', font=('calibri', 14), foreground='red')
        self.label_error.place(x=100, y=4)

        # name
        self.label_name_bind = Label(master=self, text='Name: ', font=('calibri', 14))
        self.label_name_bind.grid(row=0, column=0, padx=(20, 10), pady=(30, 20))

        self.name_bind_entry = Entry(master=self, width=30, textvariable=self.var_bind_name)
        self.name_bind_entry.grid(row=0, column=1, padx=(10, 10), pady=(30, 20))

        # command
        self.label_command_bind = Label(master=self, text='Command: ', font=('calibri', 14))
        self.label_command_bind.grid(row=1, column=0, padx=(20, 10), pady=(0, 30))

        self.command_bind_entry = Entry(master=self, width=30, textvariable=self.var_bind_command)
        self.command_bind_entry.grid(row=1, column=1, padx=(10, 10), pady=(0, 30))

        # hot-key
        self.label_command_bind = Label(master=self, text='Hot-key: ', font=('calibri', 14))
        self.label_command_bind.grid(row=2, column=0, padx=(20, 10), pady=(0, 30))

        self.command_bind_entry = Entry(master=self, width=30, textvariable=self.var_bind_hotkey)
        self.command_bind_entry.grid(row=2, column=1, padx=(10, 10), pady=(0, 30))

        # buttons
        self.btn_add_bind = Button(master=self, text='Add', width=10,command=self.add_bind, font=('calibri', 14))
        self.btn_add_bind.grid(row=3, column=0)

        self.btn_all_bind = Button(master=self, text='All binds', width=10, command=self.view_binds,font=('calibri', 14))
        self.btn_all_bind.grid(row=3, column=1)

        for i in cur.execute("SELECT * from binds"):
            App.all_binds.append(Bind(hotkey=i[3], id=i[0], name=i[1], text=i[2]))
    def add_bind(self):
        args = [self.var_bind_name.get(), self.var_bind_command.get(), self.var_bind_hotkey.get()]
        if not '' in args:
            self.var_bind_name.set('')
            self.var_bind_command.set('')
            self.var_bind_hotkey.set('')
            self.label_error['text'] = ''
            cur.execute("INSERT INTO binds ('name', 'command', hotkey) VALUES (?, ?, ?);", args)
            con.commit()
            pk_tuple = cur.execute("SELECT id from binds WHERE command=(?)", (args[1],))
            pk = (*pk_tuple,)[0][0]
            try:
                App.all_binds.append(Bind(hotkey=args[2], id=pk, name=args[0], text=args[1]))
            except Exception:
                self.label_error['text'] = 'Hot-key is not valid'
                cur.execute("DELETE FROM 'binds' WHERE id=(?)", (pk,))
                con.commit()
        else:
            self.label_error['text'] = 'Some field is empty'

    def view_binds(self):
        BindsView(self)


class BindsView(Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.geometry('620x350')
        self.resizable(False, False)
        self.title('Binds')
        self.labels_binds = dict()
        canvas = Canvas(self, borderwidth=0, highlightthickness=0)
        canvas.pack(side=LEFT, fill=BOTH, expand=True)
        scrollbar = Scrollbar(self, orient=VERTICAL, command=canvas.yview)
        scrollbar.pack(side=RIGHT, fill=Y)

        canvas.config(yscrollcommand=scrollbar.set)
        canvas.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox('all')))

        scrollable_frame = Frame(canvas)
        canvas.create_window((0, 0), window=scrollable_frame, anchor=NW)

        Label(master=scrollable_frame,width=8, text='Name', font=('calibri', 15)).grid(row=0, column=0, padx=(20, 10), pady=(10, 20))
        Label(master=scrollable_frame,width=15, text='Command', font=('calibri', 15)).grid(row=0, column=1, padx=(20, 10), pady=(10, 20))
        Label(master=scrollable_frame,width=12, text='Hot-key', font=('calibri', 15)).grid(row=0, column=2, padx=(20, 10), pady=(10, 20))
        Label(master=scrollable_frame,width=11, text='Delete', font=('calibri', 15)).grid(row=0, column=3, padx=(20, 10), pady=(10, 20))

        for i, bind in enumerate(App.all_binds, start=1):
            name = bind.name
            command = bind.text
            hotkey = bind.hotkey
            if len(command) > 12:
                command = bind.text[0:11] + '..'
            if len(name) > 8:
                name = bind.name[0:7] + '..'
            if len(hotkey) > 10:
                hotkey = bind.hotkey[0:9] + '..'

            func = self.create_func(bind)
            labels_bind = (
                Label(master=scrollable_frame, text=name, font=('calibri', 14)),
                Label(master=scrollable_frame, text=command, font=('calibri', 14)),
                Label(master=scrollable_frame, text=hotkey, font=('calibri', 14)),
                Button(master=scrollable_frame, text='Del', width=5, command=func, font=('calibri', 14))
            )
            labels_bind[0].grid(row=i, column=0, padx=(20, 10), pady=(10, 20))
            labels_bind[1].grid(row=i, column=1, padx=(20, 10), pady=(10, 20))
            labels_bind[2].grid(row=i, column=2, padx=(20, 10),pady=(10, 20))
            labels_bind[3].grid(row=i, column=3, padx=(20, 10), pady=(10, 20))
            self.labels_binds.update({bind: labels_bind})

    def create_func(self, bind):
        def func():
            bind.delete(self.labels_binds)
        return func

if __name__ == '__main__':
    with sqlite3.connect("BindsDB.db") as con:
        cur = con.cursor()
    app = App()
    app.mainloop()