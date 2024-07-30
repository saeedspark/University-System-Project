from source.interface.dashboard import Dashboard
import json
import tkinter

with open("data\\variables.json", "r") as f:
    var = json.load(f)

def dashboard():
    global dashboard
    dashboard = Dashboard()
    dashboard.title("Saeid")
    dashboard.resizable(False, False)
    dashboard.size(900, 500) #844 #677
    dashboard.center_window()
    dashboard.header() # Created (display_time, display_university_name)
    dashboard.information()
    # ...
    dashboard.hide_window()
    
def show():
    dashboard.show_window()
    
def close():
    dashboard.destroy()



    
