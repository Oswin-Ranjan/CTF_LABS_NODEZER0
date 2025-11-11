from flask import Flask, render_template, request, redirect, url_for, session
import os

app = Flask(__name__, template_folder="templates", static_folder="static")
app.secret_key = "demo_secret"

PRODUCTS = [
    {"id": 1, "name": "Girls Top", "price": 299, "desc": "Cute Top for girls.", "img": "top.webp"},
    {"id": 2, "name": "Men's Shirt", "price": 249, "desc": "Dashing shirt for men.", "img": "shirt.jpg"},
    {"id": 3, "name": "Phone", "price": 12999, "desc": "Cool phone.", "img": "phone.jpg"},
    {"id": 4, "name": "Bedsheet", "price": 999, "desc": "Good quality bedsheet.", "img": "bedsheet.jpg"},
    {"id": 5, "name": "PS5", "price": 54999, "desc": "For the players.", "img": "ps5.jpg"},
    {"id": 6, "name": "Wrist Watch", "price": 1999, "desc": "Stylish wrist watch.", "img": "watch.jpg"},
    {"id": 7, "name": "Small Tree", "price": 799, "desc": "Cute little tree.", "img": "tree.jpg"},
    {"id": 8, "name": "Washing Machine", "price": 18999, "desc": "Perfect for every wash.", "img": "washing_machine.webp"}
]

def get_cart():
    """Return cart stored in session."""
    return session.get("cart", [])

@app.route("/")
def home():
    return render_template("home.html", title="Home")

@app.route("/products")
def products():
    return render_template("products.html", title="Products", products=PRODUCTS)

@app.route("/product/<int:pid>")
def product(pid):
    product = next((p for p in PRODUCTS if p["id"] == pid), None)
    if not product:
        return render_template("404.html", title="Not Found"), 404
    return render_template("product.html", title=product["name"], product=product)

@app.route("/add-to-cart/<int:pid>")
def add_to_cart(pid):
    product = next((p for p in PRODUCTS if p["id"] == pid), None)
    if not product:
        return redirect(url_for("products"))
    cart = get_cart()
    cart.append({"id": product["id"], "name": product["name"], "price": product["price"]})
    session["cart"] = cart
    return redirect(url_for("cart"))

@app.route("/cart")
def cart():
    cart = get_cart()
    total = sum(item["price"] for item in cart)
    return render_template("cart.html", title="Cart", cart=cart, total=total)

@app.route("/checkout", methods=["GET", "POST"])
def checkout():
    cart = get_cart()
    total = sum(item["price"] for item in cart)
    if request.method == "POST":
        name = request.form.get("name", "Customer")
        session.pop("cart", None)
        return render_template("checkout.html", title="Order Complete", done=True, name=name, total=total)
    return render_template("checkout.html", title="Checkout", done=False, total=total)

@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        name = request.form.get("name", "Guest")
        return f"<h2>Thanks, {name}!</h2><p>Your message has been received.</p><a href='/'>Return home</a>"
    return render_template("contact.html", title="Contact")

@app.errorhandler(404)
def not_found(e):
    return render_template("404.html", title="Not Found"), 404

if __name__ == "__main__":
    app.run(debug=True)