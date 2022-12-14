from flask import (
    Blueprint,
    render_template,
    session,
    request,
    redirect,
    url_for,
)
from modules.auth.auth_bearer import security
from modules.schemas.responses.base_response import BaseResponse
from modules.schemas.responses.product import GetProductsDealsResponse
from flask_pydantic import validate
from modules.schemas.requests.order import CreateOrder
from modules.schemas.responses.order import CreateOrderResponse


pages_bp = Blueprint(
    "pages_bp",
    __name__,
    template_folder="templates",
    static_folder="static",
    static_url_path="assets",
)


@pages_bp.route("/")
def index():
    list_products = handler_prod.get_all_products()
    if not session.get("user"):
        return render_template("index.html", products=list_products)
    user_info = session.get("user")
    return render_template(
        "index.html", username=user_info["username"], products=list_products
    )


@pages_bp.route("/<pid>/<price>/", methods=["GET"])
@validate()
def product(pid: str, price: str):
    details = handler_prod.get_product_details(pid)
    if not session.get("user"):
        return render_template("product.html", details=details, price=price)
    user_info = session.get("user")
    return render_template(
        "product.html",
        username=user_info["username"],
        details=details,
        price=price,
    )


# Create order
@pages_bp.route("/create_order", methods=["POST"])
@validate()
def create_order(form: CreateOrder) -> CreateOrderResponse:
    res = handler_order._create_order(
        CreateOrder(pid=form.pid, volume=form.volume, unit_price=form.unit_price)
    )
    if not session.get("user"):
        return render_template("order.html", order=res)
    user_info = session.get("user")
    return render_template("order.html", order=res, username=user_info["username"])


@pages_bp.route("/login")
def login():
    return render_template("login.html")


# Special deals
@pages_bp.route("/deals")
@validate()
def special_deals() -> GetProductsDealsResponse:
    deals = handler_prod._special_deals()
    if "user" in session:
        user_info = session.get("user")
        return render_template(
            "deals.html", products=deals, username=user_info["username"]
        )
    return render_template("deals.html", products=deals)


# Admin Module to be completed
@pages_bp.route("/admin")
def admin_module():
    if not session.get("user") and request.endpoint != "login":
        return redirect(url_for("pages_bp.login"))
    user_info = session.get("user")
    return render_template("admin.html", username=user_info["username"])


@pages_bp.route("/logout")
@validate()
def logout():
    session.clear()
    return BaseResponse(message="You are logged out!")
