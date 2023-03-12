import keyboard
import pyautogui
from time import sleep
import sqlite3
import customtkinter as CTk
from tkinter import StringVar

class Bind:

    def __init__(self, hotkey, id, name, text=""):
        keyboard.add_hotkey(hotkey, self.Write)
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

    def delete(self, window):
        cur.execute("DELETE FROM `binds` WHERE `id` = (?)", (self.id,))
        con.commit()
        App.all_binds.remove(self)
        window.destroy()




class App(CTk.CTk):
    all_binds = []

    def __init__(self):
        super().__init__()
        self.geometry('350x250')
        self.title('Minecraft Binds')
        self.resizable(False, False)

        self.var_bind_name = StringVar()
        self.var_bind_command = StringVar()
        self.var_bind_hotkey = StringVar()

        # name
        self.label_name_bind = CTk.CTkLabel(master=self, text='Name: ', font=('calibri', 20))
        self.label_name_bind.grid(row=0, column=0, padx=(20, 10), pady=(30, 20))

        self.name_bind_entry = CTk.CTkEntry(master=self, width=160, textvariable=self.var_bind_name)
        self.name_bind_entry.grid(row=0, column=1, padx=(10, 10), pady=(30, 20))

        # command
        self.label_command_bind = CTk.CTkLabel(master=self, text='Command: ', font=('calibri', 20))
        self.label_command_bind.grid(row=1, column=0, padx=(20, 10), pady=(0, 30))

        self.command_bind_entry = CTk.CTkEntry(master=self, width=160, textvariable=self.var_bind_command)
        self.command_bind_entry.grid(row=1, column=1, padx=(10, 10), pady=(0, 30))

        # hot-key
        self.label_command_bind = CTk.CTkLabel(master=self, text='Hot-key: ', font=('calibri', 20))
        self.label_command_bind.grid(row=2, column=0, padx=(20, 10), pady=(0, 30))

        self.command_bind_entry = CTk.CTkEntry(master=self, width=160, textvariable=self.var_bind_hotkey)
        self.command_bind_entry.grid(row=2, column=1, padx=(10, 10), pady=(0, 30))


        # buttons
        self.btn_add_bind = CTk.CTkButton(master=self, text='Add', width=100,command=self.add_bind, font=('calibri', 20))
        self.btn_add_bind.grid(row=3, column=0)

        self.btn_all_bind = CTk.CTkButton(master=self, text='All binds', width=100, command=self.view_binds,font=('calibri', 20))
        self.btn_all_bind.grid(row=3, column=1)


        for i in cur.execute("SELECT * from binds"):
            App.all_binds.append(Bind(hotkey=i[3], id=i[0], name=i[1], text=i[2]))


    def add_bind(self):
        args = [self.var_bind_name.get(), self.var_bind_command.get(), self.var_bind_hotkey.get()]
        self.var_bind_name.set('')
        self.var_bind_command.set('')
        self.var_bind_hotkey.set('')

        cur.execute("INSERT INTO binds ('name', 'command', hotkey) VALUES (?, ?, ?);", args)
        con.commit()
        pk = cur.execute("SELECT id from binds WHERE command=(?);", (args[1],))

        App.all_binds.append(Bind(hotkey=args[2], id=pk, name=args[0], text=args[1]))


    def view_binds(self):
        BindsView(self)


class BindsView(CTk.CTkToplevel):
    def __init__(self, parant):
        super().__init__(parant)
        self.geometry('500x320')
        self.resizable(False, False)
        self.title('Binds')

        CTk.CTkLabel(master=self, text='Name', font=('calibri', 20)).grid(row=0, column=0, padx=(20, 10), pady=(10, 20))

        CTk.CTkLabel(master=self, text='Command', font=('calibri', 20)).grid(row=0, column=1, padx=(20, 10), pady=(10, 20))

        CTk.CTkLabel(master=self, text='Hot-key', font=('calibri', 20)).grid(row=0, column=2, padx=(20, 10), pady=(10, 20))


        CTk.CTkLabel(master=self, text='Delete', font=('calibri', 20)).grid(row=0, column=3, padx=(20, 10), pady=(10, 20))



        for i, bind in enumerate(App.all_binds):
            command = bind.text
            if len(command) > 14:
                command = bind.text[0:13] + '..'

            CTk.CTkLabel(master=self, text=bind.name, font=('calibri', 20)).grid(row=i+1, column=0, padx=(20, 10), pady=(10, 20))

            CTk.CTkLabel(master=self, text=command, font=('calibri', 20)).grid(row=i+1, column=1, padx=(20, 10), pady=(10, 20))

            CTk.CTkLabel(master=self, text=bind.hotkey, font=('calibri', 20)).grid(row=i+1, column=2, padx=(20, 10),pady=(10, 20))

            CTk.CTkButton(master=self, text='Del', width=50, command=lambda:bind.delete(self), font=('calibri', 20)).grid(row=i+1, column=3, padx=(20, 10), pady=(10, 20))




if __name__ == '__main__':
    with sqlite3.connect("BindsDB.db") as con:
        cur = con.cursor()
    app = App()

    app.mainloop()



