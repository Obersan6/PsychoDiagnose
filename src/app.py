"""Flask app for dsm-diagnosis tool."""

import os
from flask import Flask, request, jsonify, render_template, redirect, url_for, flash, session
from src.secret_keys import SQLALCHEMY_DATABASE_URI, SECRET_KEY
from flask_debugtoolbar import DebugToolbarExtension
from src.models import db, connect_db, User

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['DEBUG_TB_INTERCEPT_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = SECRET_KEY

debug = DebugToolbarExtension(app)

connect_db(app)

# ROUTES







