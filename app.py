from flask import Flask,abort, render_template, request, jsonify
from jinja2 import TemplateNotFound

app = Flask(__name__)

patterns = {"rainbow", "solid", "blink", "fade", "matrix"}
DEFAULT_COLOR = (131,10,210)

@app.route("/send_rgb", methods=["POST"])
def get_color():
    data = request.form
    print(f"Form data: {data}")
    return jsonify({"response":"OK", "data":data})


@app.route("/", methods=["GET"])
def index():
    try:
        return render_template("index.html", patterns=patterns, red=DEFAULT_COLOR[0], green=DEFAULT_COLOR[1], blue=DEFAULT_COLOR[2])
    except TemplateNotFound:
        abort(404)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
