import json
from unittest import result
from flask import Flask, jsonify, redirect, render_template, request, url_for
from requests import Response

from math_parser import MathParser
from examples import examples

app = Flask(__name__)



@app.get("/")
def index():
    return render_template('index.html')

@app.post("/solve")
def solve():
    hypo = request.form["hypo"]
    question = request.form["question"]
    parser = MathParser(hypo, question)
    answers = parser.solve()
    return jsonify(answers)
    
@app.get("/example/<id>")
def example(id):
    id = int(id)
    ex = examples[id]
    return jsonify(ex)

if __name__ == '__main__':
    app.jinja_env.auto_reload = True
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.run(debug=True, host='0.0.0.0')