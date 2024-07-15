
# CONVERT CSV/XLSX TO DATBASE FILE (.DB)
#### **This project is a web application to convert CSV or XLSX files to .DB and view them as HTML tables**
#### Project demo: <https://www.youtube.com/watch?v=oc-5kGqS-xY>

#### Definition :
In a few words, this website uses flask and pandas to get CSV or XLSX files as input and convert them to a db file. The user can download the file or view them as a HTML table

#### Table of contents:
1. [1. Index.html](#1-indexhtml)

# Code explanation
## App.py
>```python
> from flask import Flask, render_template, request, redirect, send_file, session
> from werkzeug.utils import secure_filename 
> from helpers import create_db, create_table, clean_files
> import os
> import uuid
> 
> # Initialize Flask app
> app = Flask(__name__)
> app.config["UPLOAD_FOLDER"] = "./files/plans/"
> app.secret_key = 'supersecretkey'
> 
> # Generate a unique ID for the session
> unique_id = uuid.uuid4()
> 
> @app.route("/", methods=["GET", "POST"])
> def index():
>     # Clean up any existing files for the session and reset the session
>     clean_files(session.get("id", None))
>     session.pop("db_name", None)
>     return redirect("/upload")
> 
> @app.route("/upload", methods=["GET", "POST"])
> def upload_file():
>     # Upload session id and db_name
>     session["id"] = unique_id
>     db_name = session.pop("db_name", None)
>     
>     if request.method == "POST":
>         file = request.files.get("file")
>         view_file = request.files.get("table_file")
>         db_name = request.form.get("db_name")
>         
>         # Create the db file from the first tab form
>         if file:
>             filename = f"{unique_id}_{secure_filename(file.filename)}"
>             file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
>             db_name = f"{unique_id}_{db_name}"
>             create_db(filename, db_name)
>             session["db_name"] = db_name
> 
>         # Create the html table data from the second tab form
>         if view_file:
>             filename = f"{unique_id}_{secure_filename(view_file.filename)}"
>             view_file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
>             data = create_table(filename)
>             if isinstance(data, list):
>                 return render_template("table.html", data=data)
>             elif isinstance(data, dict):
>                 return render_template("sheets.html", data=data)
>     
>     return render_template("index.html", db_name=db_name)
> 
> @app.route("/download/<db_name>", methods=["GET"])
> def download_file(db_name):
>     # Remove the user id from the .db file name and send it to download
>     file_name = db_name.removeprefix(f"{unique_id}_") + ".db"
>     file = f"./files/databases/{db_name}.db"
>     return send_file(file, as_attachment=True, download_name=file_name)
>
>
>```
Basically, app.py uses flask to create the routes, render html templates and send files to download, werkzeug.utils to keep the file managment more safe, uuid to create a unique id for each user session and helpers.py to get some extra functions that do the job themselves.

## Routes
### 1. Index route ("/")
>```python
> @app.route("/", methods=["GET", "POST"])
> def index():
>     # Clean up any existing files for the session and reset the session
>     clean_files(session.get("id", None))
>     session.pop("db_name", None)
>     return redirect("/upload")
>```

The index route simply cleans up any previous session data (such as ```db_name``` and ```session_id```) and redirects the user to the upload route ("/upload"). It accepts get requests when the user is acessing the website for the first time, and post requests when the user converts the file and wants to download it.

### 2. Upload route ("/upload")
>```python
> @app.route("/upload", methods=["GET", "POST"])
> def upload_file():
>     # Upload session id and db_name
>     session["id"] = unique_id
>     db_name = session.pop("db_name", None)
>     
>     if request.method == "POST":
>         file = request.files.get("file")
>         view_file = request.files.get("table_file")
>         db_name = request.form.get("db_name")
>         
>         # Create the db file from the first tab form
>         if file:
>             filename = f"{unique_id}_{secure_filename(file.filename)}"
>             file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
>             db_name = f"{unique_id}_{db_name}"
>             create_db(filename, db_name)
>             session["db_name"] = db_name
> 
>         # Create the html table data from the second tab form
>         if view_file:
>             filename = f"{unique_id}_{secure_filename(view_file.filename)}"
>             view_file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
>             data = create_table(filename)
>             if isinstance(data, list):
>                 return render_template("table.html", data=data)
>             elif isinstance(data, dict):
>                 return render_template("sheets.html", data=data)
>     
>     return render_template("index.html", db_name=db_name)
>```
Firstly, the upload function attach the ```unique_id``` to the flask session. This id will be used to identify the files that a specific user has uploaded. It also sets ```db_name``` to None, in order to avoid conflicts with previous sessions and get the name that will be used for the .db file. If the request method is get, the function renders the index.html page. When the method is post, the function gets a file from the ```"file"``` form and a file from the ```"view_file"``` form. The first one will be converted to .db and the second one will be displayed as a table. If ```file``` is found, the function gets the name of it (using werkzeug.utils ```secure_filename``` function), attach it to the user session id (```unique_id```) and assign this to a ```filename``` variable. Then, the file is saved in the upload folder ("./files/plans/"), the id is attached to the ```db_name```, the database file is created (using the ```create_db``` function from helpers.py) and a ```db_name``` is set to the session.
<br>
<br>
On the other hand, if ```view_file``` is found, it means that the user has upload a file to be displayed as a html table, so the function also attaches the filename to the session id, and saves it to the upload folder. Then, it creates a variable called data, that holds the information of the CSV or XLSX file to be displayed. If this data is a list (which means the file is a CSV file with a sigle sheet) the function renders the ```table.html``` template. If the file is a dictionary (which means the file is a XLSX with one or more sheets) the function renders the ```sheets.html``` template.

### 3. Download route ("/download/<db_name>")
>```python
> @app.route("/download/<db_name>", methods=["GET"])
> def download_file(db_name):
>     # Remove the user id from the .db file name and send it to download
>     file_name = db_name.removeprefix(f"{unique_id}_") + ".db"
>     file = f"./files/databases/{db_name}.db"
>     return send_file(file, as_attachment=True, download_name=file_name)
>
>
>```

This route basically removes the user id from the database filename and send this file to be downloaded. This file will then be acessed by the index.html in the context of download.

## HTML templates
### 1. Index.html
>```html
> <!DOCTYPE html>
> <html lang="en">
> <head>
>     <meta charset="UTF-8">
>     <meta name="viewport" content="width=device-width, initial-scale=1.0">
>     <title>Convert to DB file</title>
>     <!-- Bootstrap CSS -->
>     <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">
>     <link href="/static/styles.css" rel="stylesheet">
>     <link rel="icon" href="./static/favicon.ico" type="image/x-icon">
> </head>
> <body>
>     <main>
>         <div class="container mt-5">
>             <h1 class="text-center mb-4">Convert CSV or XLSX to DB file</h1>
>             <div class="card">
>                 <!-- Navigation Tabs -->
>                 <ul class="nav nav-pills" id="pills-tab" role="tablist">
>                     <li class="nav-item" role="presentation">
>                         <a class="nav-link active" id="convert-tab" data-bs-toggle="pill" href="#convert" role="tab" aria-controls="convert" aria-selected="true">Convert to DB</a>
>                     </li>
>                     <li class="nav-item" role="presentation">
>                         <a class="nav-link" id="table-view-tab" data-bs-toggle="pill" href="#table-view" role="tab" aria-controls="table-view" aria-selected="false">View Table</a>
>                     </li>
>                 </ul>
> 
>                 <!-- Tab Content -->
>                 <div class="tab-content" id="pills-tabContent">
>                     <!-- Convert Tab -->
>                     <div class="tab-pane fade show active" id="convert" role="tabpanel" aria-labelledby="convert-tab">
>                         <div class="card-body">
>                             <form method="POST" enctype="multipart/form-data" id="file_form">
>                                 <div class="mb-3">
>                                     <label class="mb-2">Input a CSV or XLSX file</label>
>                                     <input type="file" name="file" class="form-control form-control-lg" id="file_input">
>                                 </div>
>                                 <div class="mb-3">
>                                     <label for="db_name" class="form-label">Choose the name of the database</label>
>                                     <div class="input-group" id="db_group">
>                                         <div class="form-floating">
>                                             <input type="text" name="db_name" id="db_name" class="form-control" placeholder="File name" aria-describedby="db_description" autocomplete="off">
>                                             <label for="db_name">File name</label>
>                                         </div>
>                                         <button type="submit" class="btn btn-primary">Upload</button>
>                                     </div>
>                                     <small id="db_description" class="form-text text-muted">This will be the name of your .db file</small>
>                                 </div>
>                             </form>
>                         </div>
>                     </div>
> 
>                     <!-- Table View Tab -->
>                     <div class="tab-pane fade" id="table-view" role="tabpanel" aria-labelledby="table-view-tab">
>                         <div class="card-body">
>                             <form method="POST" enctype="multipart/form-data" id="table_view_form">
>                                 <div class="mb-3">
>                                     <label class="mb-2">Input a CSV or XLSX file</label>
>                                     <input type="file" name="table_file" class="form-control form-control-lg" id="table_input">
>                                 </div>
>                                 <button id="table_view_btn" type="submit" class="btn btn-primary">View file as table</button>
>                             </form>
>                             
>                         </div>
>                     </div>
>                 </div>
>                 <!-- Modal for Error and Download Messages -->
>                 <div class="modal fade" id="reg-modal" tabindex="-1" aria-labelledby="modal-title" aria-hidden="true">
>                     <div class="modal-dialog">
>                         <div class="modal-content">
>                             <div class="modal-header">
>                                 <h5 class="modal-title" id="modal-title">Invalid Input</h5>
>                             </div>
>                             <div class="modal-body">
>                                 <p id="modal_paragraph"></p>
>                             </div>
>                             <div class="modal-footer">
>                                 <button id="modal_button" type="button" class="btn btn-primary" data-bs-dismiss="modal" aria-label="Close">Close</button>
>                             </div>
>                         </div>
>                     </div>
>                 </div>
>             </div>
>         </div>
>     </main>
> 
>     <!-- Bootstrap JS and Custom Script -->
>     <script src="https://code.jquery.com/jquery-3.5.1.slim.min.js"></script>
>     <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js"></script>
>     <script src="/static/scripts.js"></script>
>     <script>
>         {% if db_name %}
>             showDownloadModal("{{ db_name }}");
>         {% endif %}
>     </script>
> </body>
> </html>
>```
Index.html, consists in webpage with two navigation tabs. The first one, contains the form for uploading a CSV or XLSX file and inputting the name of the database file.


<p align="center">
  <img src="https://github.com/user-attachments/assets/7e7fe876-150f-42df-92b5-ba7866921d51">
</p>

If the user don't upload a file or input the name of the database or upload a file that is not a CSV or XLSX, a modal will appear to tell the user that something went wrong:

<p align="center">
  <img src="https://github.com/user-attachments/assets/44d9178b-fc71-4484-b83c-6996f1011941">
  <img src="https://github.com/user-attachments/assets/41b61170-bc2c-4dd7-932f-949b93359d50">
  <img src="https://github.com/user-attachments/assets/7ab90713-3c37-4ad9-bb4b-566f338d161b">
</p>


Finally, if everythings goes well, a download modal will appear with a button to download the database file:

<p align="center">
  <img src="https://github.com/user-attachments/assets/a6e211ac-b695-4dbd-9228-5cbe37b0ba02">
</p>


The other nav tab will have the same input form, but this time, when the user clicks upload, the file will be displayed as a HTML table.
### 2. Table.html
>```html
> <!DOCTYPE html>
> <html lang="en">
> <head>
>     <meta charset="UTF-8">
>     <meta name="viewport" content="width=device-width, initial-scale=1.0">
>     <title>CSV Table</title>
>     <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">
>     <link href="/static/styles.css" rel="stylesheet">
>     <link rel="icon" href="./static/favicon.ico" type="image/x-icon">
> </head>
> <body class="page-body">
>     <div class="card-container">
>         <div class="table-wrapper">
>             <table class="content-table">
>                 <thead>
>                     <!-- Create table headers -->
>                     {% for key in data[0].keys() %}
>                         <th>{{ key }}</th>
>                     {% endfor %}
>                 </thead>
>                 <tbody>
>                     <!-- Create table rows -->
>                     {% for row in data %}
>                         <tr>
>                             {% for value in row.values() %}
>                                 <td>{{ value }}</td>
>                             {% endfor %}
>                         </tr>
>                     {% endfor %}
>                 </tbody>
>             </table>
>             <div class="bottom-border"></div>
>         </div>
>         <form action="/">
>             <button id="table_view_btn" type="submit" class="btn btn-primary">Back</button>
>         </form>
>     </div>
> 
>     <!-- Include scripts -->
>     <script src="https://code.jquery.com/jquery-3.5.1.slim.min.js"></script>
>     <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js"></script>
>     <script src="/static/scripts.js"></script>
> </body>
> </html>
>```
Tables.html is rendered when the user input a raw CSV file with a single sheet. It uses jinja to iterate over the data that came from helpers.py ```create_table``` function (more on that in a while) and creates a table that contains the same information of the CSV file. It is displayed as a scrollable table with sticky header:


<p align="center">
  <img src="https://github.com/user-attachments/assets/1b67ca01-42d8-4b1d-b8a4-8ad5b7c9a977">
</p>

### 3. Sheets.html
>```html
>> <!DOCTYPE html>
> <html lang="en">
> <head>
>     <meta charset="UTF-8">
>     <meta name="viewport" content="width=device-width, initial-scale=1.0">
>     <title>XLSX Table</title>
>     <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">
>     <link href="/static/styles.css" rel="stylesheet">
>     <link rel="icon" href="./static/favicon.ico" type="image/x-icon">
> </head>
> <body class="page-body">
>     <div class="card-container">
>         <!-- Tab navigation -->
>         <ul class="nav nav-pills" id="myTab" role="tablist">
>             {% for sheet_name in data.keys() %}
>                 <li class="nav-item" role="presentation">
>                     <button class="nav-link {% if loop.first %}active{% endif %}" id="tab-{{ loop.index }}-tab" data-bs-toggle="tab" data-bs-target="#tab-{{ loop.index }}" type="button" role="tab" aria-controls="tab-{{ loop.index }}" aria-selected="true">{{ sheet_name }}</button>
>                 </li>
>             {% endfor %}
>         </ul>
>         <!-- Tab content -->
>         <div class="tab-content" id="myTabContent">
>             {% for sheet_name, sheet_data in data.items() %}
>                 <div class="tab-pane fade {% if loop.first %}show active{% endif %}" id="tab-{{ loop.index }}" role="tabpanel" aria-labelledby="tab-{{ loop.index }}-tab">
>                     <div class="table-wrapper">
>                         <table class="content-table">
>                             <thead>
>                                 <!-- Create table headers -->
>                                 {% for key in sheet_data[0].keys() %}
>                                     <th>{{ key }}</th>
>                                 {% endfor %}
>                             </thead>
>                             <tbody>
>                                 <!-- Create table rows -->
>                                 {% for row in sheet_data %}
>                                     <tr>
>                                         {% for value in row.values() %}
>                                             <td>{{ value }}</td>
>                                         {% endfor %}
>                                     </tr>
>                                 {% endfor %}
>                             </tbody>
>                         </table>
>                         <div class="bottom-border"></div> 
>                     </div>
>                 </div>
>             {% endfor %}
>         </div>
>         
>         <form action="/">
>             <button id="table_view_btn" type="submit" class="btn btn-primary">Back</button>
>         </form>
>     </div>
> 
>     <!-- Include scripts -->
>     <script src="https://code.jquery.com/jquery-3.5.1.slim.min.js"></script>
>     <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js"></script>
>     <script src="/static/scripts.js"></script>
> </body>
> </html>
>```

Sheets.html is the last of the HTML template. It is rendered when the user uploads a XLSX file with one or more sheets. Similar to tables.html, this code also uses jinja and iterate over the data to create multiple tables that are displayed in different sheet tabs:

<p align="center">
  <img src="https://github.com/user-attachments/assets/235c6e62-f65f-4b47-8298-3a3dd0e0fbfd">
  <img src="https://github.com/user-attachments/assets/63a93a16-be2f-4e5c-864b-bcedb2415e8b">
  <img src="https://github.com/user-attachments/assets/179b99a6-bd7a-42c9-b3be-66391bb290ea">
  <img src="https://github.com/user-attachments/assets/ae3e2795-3130-4773-bbc1-09bd22aa157e">
</p>

The back button just redirects the user to the index route.
## Helpers.py
>```python
> import pandas as pd
> import os
> import sqlite3
> import glob
> 
> def create_db(filename, db_name):
>     """
>     Create a SQLite database from a CSV or XLSX file.
>     """
>     connection = sqlite3.connect(f"./files/databases/{db_name}.db")
>     file_path = f"./files/plans/{filename}"
>     
>     try:
>         if filename.endswith(".xlsx"):
>             frames = pd.read_excel(file_path, sheet_name=None)
>             for sheet, df in frames.items():
>                 df.to_sql(sheet, con=connection, if_exists='replace', index=False)
>                 
>         elif filename.endswith(".csv"):
>             df = pd.read_csv(file_path)
>             table_name = filename.replace(" ", "_").split(".")[0]
>             df.to_sql(table_name, con=connection, if_exists='replace', index=False)
>             
>     except ValueError as UnsupportedFileExtension:
>         print(f"Error: {UnsupportedFileExtension}\nThe uploaded file is not a CSV or XLSX file.")
>     
>     finally:
>         connection.close()
>         os.remove(file_path)
> 
> def create_table(filename):
>     """
>     Create a dictionary or list from a CSV or XLSX file for rendering in HTML templates.
>     """
>     file_path = f"./files/plans/{filename}"
>     
>     if filename.endswith(".csv"):
>         df = pd.read_csv(file_path)
>         data = df.to_dict("records")
>         
>     elif filename.endswith(".xlsx"):
>         data = pd.read_excel(file_path, sheet_name=None)
>         for sheet in data:
>             data[sheet] = data[sheet].to_dict("records")
>  
>     os.remove(file_path)
>     return data
> 
> def clean_files(session_id):
>     """
>     Remove all database files associated with a session ID.
>     """
>     if session_id is not None:
>         files = glob.glob(f"./files/databases/{session_id}*.db")
>         for file in files:
>             os.remove(file)
>```
### 1. Create_db
>```python
> def create_db(filename, db_name):
>     """
>     Create a SQLite database from a CSV or XLSX file.
>     """
>     connection = sqlite3.connect(f"./files/databases/{db_name}.db")
>     file_path = f"./files/plans/{filename}"
>     
>     try:
>         if filename.endswith(".xlsx"):
>             frames = pd.read_excel(file_path, sheet_name=None)
>             for sheet, df in frames.items():
>                 df.to_sql(sheet, con=connection, if_exists='replace', index=False)
>                 
>         elif filename.endswith(".csv"):
>             df = pd.read_csv(file_path)
>             table_name = filename.replace(" ", "_").split(".")[0]
>             df.to_sql(table_name, con=connection, if_exists='replace', index=False)
>             
>     except ValueError as UnsupportedFileExtension:
>         print(f"Error: {UnsupportedFileExtension}\nThe uploaded file is not a CSV or XLSX file.")
>     
>     finally:
>         connection.close()
>         os.remove(file_path)
>```
This fuction is called when the user uploads a file. It takes the filename and the name of the database as the two arguments. First, it uses SQLite3 to create and connect to a database  in the databases directory (./files/databases/) called ```db_name.db``` . This database name is the text typed by the user attached to his session id. Secondly, the function uses a try and except block to check if the file extension is CSV or XLSX. If it is a excel file (.XLSX), the function iterates over the data frame to get the sheets and the content of those and then calls the pandas ```to_sql``` function to open the db file and write the dataframe to it. Now, all of the data from the XLSX file is inside of a .db file
</br>
</br>
Similar to the XLSX case, when the file is a CSV, the function uses pandas to read the file content into a dataframe, and write it to the database file. The only difference is that it creates a variable called ```table_name``` that removes unwanted characters from the table name (such as white spaces or underscores) and uses it as the argument for the ```to_sql``` function.
</br>
</br>
Lastly, when the database was created and populated, the SQLite connection is closed and the file path is cleaned (to avoid keeping all of the uploaded CSV's or XLSX's in my local directory.

### 2. Create_table
>```python
> def create_table(filename):
>     """
>     Create a dictionary or list from a CSV or XLSX file for rendering in HTML templates.
>     """
>     file_path = f"./files/plans/{filename}"
>     
>     if filename.endswith(".csv"):
>         df = pd.read_csv(file_path)
>         data = df.to_dict("records")
>         
>     elif filename.endswith(".xlsx"):
>         data = pd.read_excel(file_path, sheet_name=None)
>         for sheet in data:
>             data[sheet] = data[sheet].to_dict("records")
>  
>     os.remove(file_path)
>     return data
>```

This function has the role of reading CSV or XLSX files (just like ```create_db``` does) but it converts the pandas dataframe to a dictionary, if it the file is a CSV, or to a list of dictionaries, if the file is a XLSX. Then, the function also clears the plans directory and return the data to be used in the sheets.htm or tables.html templates.

### 3. Clean_files
>```python
>  def clean_files(session_id):
>     """
>     Remove all database files associated with a session ID.
>     """
>     if session_id is not None:
>         files = glob.glob(f"./files/databases/{session_id}*.db")
>         for file in files:
>             os.remove(file)
>```

This is the function used to clean the databases directory. It is called everytime the user acesses the index route, so that any previous session files will be deleted. Basically it uses the glob module to look for any file in the databases directory (./files/databases/) that starts with the user session id and ends with .db, indicating that it is a file converted by the user in a previous session. If the file is found and the session id is not None, all of the database files are removed.














