import os
import datetime
import webbrowser

from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from fpdf import FPDF

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


@app.route("/")
#@login_required
def index():
    #Template to create a PDF File
    #pdf = FPDF()
    #pdf.add_page()
    #pdf.set_xy(0, 0)
    #pdf.set_font('arial', 'B', 13.0)
    #pdf.cell(ln=0, h=5.0, align='L', w=0, txt="Hello", border=0)
    #pdf.output('test.pdf', 'F')

    return render_template("calculate.html")


@app.route("/calculate", methods=["GET", "POST"])
def calculate():
    if request.method == "GET":
      return render_template("calculate.html")

    #else:
        #return apology("400", "400")