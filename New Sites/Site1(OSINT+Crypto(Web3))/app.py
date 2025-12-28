from flask import Flask, render_template, session, jsonify, request, abort
import random, string, time
from collections import defaultdict

app = Flask(__name__)
app.secret_key = "ctf_secret_key"

# ------------------ UTILITIES ------------------

def gen_wallet():
    return "0x" + ''.join(random.choices("abcdef0123456789", k=40))

def gen_ens():
    return "user" + str(random.randint(1000,9999)) + ".eth"

def gen_flag():
    return "FLAG{" + ''.join(random.choices(string.ascii_lowercase, k=10)) + "}"

# ------------------ RATE LIMITER ------------------

visits = defaultdict(list)

def rate_limit(ip, limit=20, window=30):
    now = time.time()
    visits[ip] = [t for t in visits[ip] if now - t < window]
    if len(visits[ip]) >= limit:
        abort(429)
    visits[ip].append(now)

@app.before_request
def guard():
    ip = request.remote_addr
    rate_limit(ip)

# ------------------ CORE ROUTES ------------------

@app.route("/")
def index():
    if "wallet" not in session:
        session["wallet"] = gen_wallet()
        session["ens"] = gen_ens()
        session["flag"] = gen_flag()
    return render_template("index.html")

# REAL PATHS (not obvious)
@app.route("/lookup")
def wallet():
    return render_template("wallet.html")

@app.route("/name")
def ens():
    return render_template("ens.html")

# ------------------ API ------------------

@app.route("/api/profile")
def profile_api():
    return jsonify({
        "username": "kai_dev",
        "bio": "frontend dev • learning web3 🚀\nbuilding identity layer stuff lately",
        "wallet": session["wallet"]
    })

@app.route("/api/wallet")
def wallet_api():
    return jsonify({
        "wallet": session["wallet"],
        "balance": "3.42 ETH",
        "ens": session["ens"],
        "nfts": 1
    })

@app.route("/api/ens")
def ens_api():
    return jsonify({
        "ens": session["ens"],
        "records": {
            "email": "kai@web3.dev",
            "github": "kai_dev",
            "description": "identity experiments",
            "note": session["flag"]
        }
    })

# ------------------ DECOY ROUTES ------------------

@app.route("/explorer")
def fake1():
    return "<h3>Explorer temporarily unavailable.</h3>"

@app.route("/wallet")
def fake2():
    return "<h3>Invalid wallet format.</h3>"

@app.route("/ens")
def fake3():
    return "<h3>No ENS found.</h3>"

@app.route("/identity")
def fake4():
    return "<h3>Identity service offline.</h3>"

# ------------------ FAKE API ENDPOINTS ------------------

@app.route("/api/tx")
def fake_tx():
    return jsonify({"error":"transaction not found"})

@app.route("/api/address")
def fake_addr():
    return jsonify({"status":"unknown address"})

# ------------------ FLAG SUBMISSION ------------------

@app.route("/api/submit", methods=["POST"])
def submit_flag():
    if request.json.get("flag") == session["flag"]:
        return jsonify({"status":"correct"})
    return jsonify({"status":"wrong"})

# ------------------ ERROR HANDLER ------------------

@app.errorhandler(429)
def ratelimited(e):
    return "<h3>Too many requests. Slow down, detective.</h3>", 429

# ------------------ RUN ------------------

if __name__ == "__main__":
    app.run(debug=True)
