from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/results", methods=["POST"])
def results():
    address = request.form.get("address")
    return render_template("results.html", address=address)

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/donations")
def donations():
    return render_template("donations.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
