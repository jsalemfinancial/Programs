from flask import Flask, request, render_template, redirect, url_for, flash
from loginUtils import loginPortal
import mysql.connector

app = Flask(__name__.split(".")[0])
dbconfig = {"host": "flaskdb-001.cmtvzzpoedvj.us-east-2.rds.amazonaws.com", "port": "5050", "user": "flaskadmin", "password": "flasklover"}
conn = mysql.connector.connect(**dbconfig)
cursor = conn.cursor()
cursor.execute("""SHOW DATABASES""")
print(cursor.fetchall())

app.config["SECRET_KEY"] = "BiGGiEsmaLLz555313555baCKaTiTaGaIN"

@app.route("/", methods=["GET", "POST"])
def landing(title: str = "Joe's Web App") -> "html":
    clientAddress = request.environ.get("REMOTE_ADDR")
    serverAddress = request.environ.get("SERVER_NAME")
    requestHost = request.environ.get("HTTP_HOST")
    
    return render_template("landing.html", the_title = title,
                                            the_client_address = clientAddress, 
                                            the_server_address = serverAddress, 
                                            the_host = requestHost)

@app.route("/login", methods=["GET", "POST"])
def login(title: str = "Login Portal") -> "html":
    LoginForm = loginPortal()

    if (LoginForm.validate_on_submit()):
        if (str(LoginForm.userEmail.data) == "Jamal@gmail.com"):
            flash("Submitted Successfully, " + str(LoginForm.userEmail.data).split("@")[0], "success")
            return redirect(url_for("landing"))
        else:
            flash("Submission Failed", "fail")
            return redirect(url_for("login"))

    return render_template("login.html", the_title = title, form=LoginForm)

if __name__ == "__main__":
    app.run(debug=True)