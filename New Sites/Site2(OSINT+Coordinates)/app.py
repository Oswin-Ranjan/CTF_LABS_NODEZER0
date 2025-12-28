from flask import Flask, render_template, session, request
import random, string, os
from tools.make_image import make_image_with_exif

app = Flask(__name__)
app.secret_key = "geo_ctf_secret"

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
STATIC_DIR = os.path.join(BASE_DIR, "static")
GEN_DIR = os.path.join(STATIC_DIR, "generated")

os.makedirs(GEN_DIR, exist_ok=True)

@app.route("/")
def index():
    if "challenge" not in session:
        lat = random.uniform(-60, 60)
        lon = random.uniform(-180, 180)

        token = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
        filename = f"{token}.jpg"
        filepath = os.path.join(GEN_DIR, filename)

        make_image_with_exif(filepath, lat, lon, random.randint(10, 4000))

        if not os.path.exists(filepath):
            raise Exception("IMAGE GENERATION FAILED")

        flag = f"FLAG{{{round(lat,3)}_{round(lon,3)}}}"

        session["challenge"] = {
            "image": filename,
            "flag": flag
        }

    return render_template("index.html")

@app.route("/view")
def view():
    return render_template("viewer.html", image=session["challenge"]["image"])

if __name__ == "__main__":
    app.run(debug=True)
