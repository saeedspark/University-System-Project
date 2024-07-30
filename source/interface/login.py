import sqlite3
import ast
import json
from tkinter import *
from tkinter import messagebox
from source.database.database import University
from source.interface.dashboard import Dashboard
from config import database, dashboard, login


class LoginForm(Toplevel, University, Dashboard):
    def __init__(self, database="data\\university.db"):
        super().__init__()
        self.database = database
        self.conn = sqlite3.connect(database)
        self.cur = self.conn.cursor()
        print('LoginForm is created')
    
        
    def clear_username(self, event):
        if self.username.get() == 'Username':
            self.username.delete(0, END)
            
    def fill_username(self, event):
        if self.username.get() == '':
            self.username.insert(0, 'Username')
        
    def username(self):
        self.username = Entry(self.frame, width=25, fg='black', border=0, bg='white', font=('Arial', 11))
        self.username.insert(0, 'Username')
        self.username.place(x=140, y=80)
        Frame(self.frame, width=300, height=2, bg='black').place(x=25, y=107)
        self.username.bind('<FocusIn>', self.clear_username)
        self.username.bind('<FocusOut>', self.fill_username)
        
    def clear_password(self, event):
        if self.password.get() == 'Password':
            self.password.delete(0, END)
            self.password.config(show='*')
            
    def fill_password(self, event):
        if self.password.get() == '':
            self.password.insert(0, 'Password')
            self.password.config(show='')
        
    def password(self):
        self.password = Entry(self.frame, width=25, fg='black', border=0, bg='white', font=('Arial', 11))
        self.password.insert(0, 'Password')
        self.password.place(x=140, y=150)
        Frame(self.frame, width=300, height=2, bg='black').place(x=25, y=177)
        self.password.bind('<FocusIn>', self.clear_password)
        self.password.bind('<FocusOut>', self.fill_password)

    def submit(self):
        self.username_get = self.username.get()
        self.password_get = self.password.get()
        with self.conn:
            self.cur.execute("SELECT username, password FROM Login WHERE username=?", (self.username_get,))
            self.result = self.cur.fetchone()
            if self.result != None:
                if self.result[0] == self.username_get and self.result[1] == self.password_get:
                    messagebox.showinfo('Success', 'Login Successfully')
                    self.destroy()
                    with open("data\\variables.json", "w") as data:
                        # python object to be appended
                        obj = {"username":f"{self.result[0]}"}
                        json.dump(obj, data)
                        
                    dashboard.show()

                else:
                    messagebox.showerror('Oops!', 'Password is incorrect.')
            
            else:
                messagebox.showerror('Oops!', 'Username Not Found.')
                
    def enter(self, event):
        self.submit()
            
    def submit_button(self):
        self.submit_btn = Button(self.frame, text='Submit', width=25, height=2, bg='green',cursor='hand2', fg='white', border=0, pady=5, command=self.submit, font=('Arial', 11, 'bold'))
        self.submit_btn.place(x=60, y=204)
        
    def background(self, source):
        self.img = PhotoImage(file=source)
        Label(self, image=self.img, border=0, bg='white').place(x=50, y=90)
        
        self.frame = Frame(self, width=350, height=390, bg='#fff')
        self.frame.place(x=480, y=50)
        
    def heading(self):
        self.head = Label(self.frame, text='Login', fg="blue", font=('Arial', 23, 'bold'), bg='white')
        self.head.place(x=123, y=5)
    
    def create_frame(self):
        self.frame = Frame(self, width=350, height=350, bg='white')
        self.frame.place(x=480, y=70)
        # Add login form elements to the frame
        self.heading()
        self.username()
        self.password()
        self.submit_button()

        
    
            
    