import os

from pypulse import Window, Aplication
from pypulse.Template import Template
from pypulse.Controller import Controller, BackendInstance

# Specifying application Route
Aplication.Vars.APLICATION_PATH = os.path.dirname(os.path.abspath(__file__))

# Defining the locations for templates and static files.
Template.TEMPLATE_PATH = os.path.join(Aplication.Vars.APLICATION_PATH, "templates")
Template.STATIC_PATH = os.path.join(Aplication.Vars.APLICATION_PATH, "static")


# Configuring applications
# If you create a new application, make sure to include it here.
Aplication.SetAplication("baseapp")

# Application window settings
APP_SETTINGS = {
    "title": "Talk with Cletus Spuckler",
    "debug": False,
    "debug_file_name": "debug.log",
    "window_size_x": 500,
    "window_size_y": 900,
    "icon_path": os.path.join(Aplication.Vars.APLICATION_PATH, "window_logo.ico"),
}

# Active Backend Controller
Controller.BACKEND_CONTROLLER = True

# Setting Backend Type
Controller.BACKEND_TYPE = "api-restful"

# Backend Controller
Controller.BACKEND_AUTH = {
    "type": "basic",
    "bearer": True,
    "bearer_header": "Authorization",
    "bearer_key": "Bearer",
    "url": "https://api.openai.com/v1/",
}

Controller.CHECK_AUTH_URL = "completions"

# Instancing backend
BackendInstance()

# Initializing window
browser = Window.LoadBrowser(**APP_SETTINGS)
