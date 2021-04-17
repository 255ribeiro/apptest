STEP 2 - Install virtualenv
Install virtualenv if you don’t already have it by typing pip install virtualenv at your terminal. Virtualenv allows you to create virtual environments for your app that house Python and all the dependencies your app requires. This includes specific version of plotly, dash, and other libraries that you know will work. 
As new updates become available, they won’t break your app until you’ve had a chance to test them first!


STEP 3 - Create a Development Folder
Create a new folder for your project. This will house the “development” copy of your app:
C:\>mkdir my_dash_app
C:\>cd my_dash_app


STEP 4 - Initialize Git
Initialize an empty git repository:
C:\my_dash_app>git init
Initialized empty Git repository in C:/my_dash_app/.git/

STEP 5 (WINDOWS) - Create, Activate and Populate a virtualenv
see below for macOS/Linux instructions!
Create a virtual environment. We’re calling ours “venv” but you can use any name you want:
C:\my_dash_app>python -m virtualenv venv
Activate the virtual environment:
C:\my_dash_app>.\venv\Scripts\activate 
Install dash and any desired dependencies into your virtual environment
(venv) C:\my_dash_app>pip install dash
(venv) C:\my_dash_app>pip install dash-auth
(venv) C:\my_dash_app>pip install dash-renderer
(venv) C:\my_dash_app>pip install dash-core-components
(venv) C:\my_dash_app>pip install dash-html-components
(venv) C:\my_dash_app>pip install plotly (requirement may be satisfied, see below)
