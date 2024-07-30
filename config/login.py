from source.interface.login import LoginForm
import json

with open("data\\variables.json", "r") as f:
    var = json.load(f)
    
def login():
    login = LoginForm()
    login.title("Login")
    login.resizable(False, False)
    login.size(925, 500)
    login.configure(bg="white")
    login.center_window()
    login.background('images\\login.png')
    login.create_frame() # Created (heading, username, password, submit_button)