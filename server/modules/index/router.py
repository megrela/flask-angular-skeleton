from . import module

from flask import render_template


@module.route('/', methods=("GET", "POST"))
def index():
    return render_template("index.html")
