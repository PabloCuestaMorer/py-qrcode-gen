from flask import Flask, render_template, request
import qrcode
from io import BytesIO
from base64 import b64encode

app = Flask(__name__, static_url_path="/static", static_folder="static")


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/", methods=["POST"])
def generateQR():
    data = request.form.get("qrInput")

    # Input validation
    if not data:
        return render_template("index.html", error="ERROR: Please enter a valid input.")

    try:
        qrImg = qrcode.make(data)
    except Exception as e:
        return render_template(
            "index.html", error="Failed to generate QR code. Please try again later."
        )

    memory = BytesIO()
    qrImg.save(memory)
    memory.seek(0)
    b64EncodeQrImg = "data:image/png;base64," + b64encode(memory.getvalue()).decode(
        "ascii"
    )
    return render_template("index.html", data=b64EncodeQrImg)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8080)
