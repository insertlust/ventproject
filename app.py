from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/recommendations", methods=["POST"])
def recommendations():
    # Get data from the form
    data = request.json
    weight = data.get("weight")
    age = data.get("age")
    sex = data.get("sex")
    ph = data.get("ph")
    pao2 = data.get("pao2")
    paco2 = data.get("paco2")
    bicarb = data.get("bicarb")
    base_excess = data.get("base_excess")
    cao2 = data.get("cao2")

    # Simulated recommendation logic (replace with your real logic)
    recommendations = {
        "mode": "PCSIMVPS",
        "rate": 30,
        "pip": 20,
        "peep": 5,
        "pressure_support": 10,
        "itime": 0.6,
        "fio2": 0.4
    }

    return jsonify(recommendations)

if __name__ == "__main__":
    app.run(debug=True)
