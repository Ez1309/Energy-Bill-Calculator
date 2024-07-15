# CONVERT CSV/XLSX TO DATBASE FILE (.DB)
#### **This project is a web application to convert CSV or XLSX files to .DB and view them as HTML tables**
#### Project demo: <https://www.youtube.com/watch?v=oc-5kGqS-xY>

#### Definition :
In a few words, this website uses flask and pandas to get CSV or XLSX files as input and convert them to a db file. The user can download the file or view them as a HTML table

# Code explanation
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
Index.html, consists in 

