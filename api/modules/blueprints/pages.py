from flask import (
    Blueprint,
    render_template,
    session,
    request,
    redirect,
)
from modules.auth.auth_bearer import security
from modules.schemas.responses.base_response import BaseResponse
from modules.schemas.responses.product import GetSortResponse
from flask_pydantic import validate
from modules.schemas.requests.order import CreateOrder
from modules.schemas.responses.order import CreateOrderResponse
from modules.schemas.requests.product import GetSortRequest
from newsapi import NewsApiClient
from modules.auth.auth_bearer import cfg


# https://github.com/mattlisiv/newsapi-python
news_api = NewsApiClient(api_key=cfg.news_api_key)

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
    return render_template("index.html", userinfo=user_info, products=list_products)


# Sort Items
@pages_bp.route("/sort", methods=["GET"])
@validate()
def sort_items(query: GetSortRequest) -> GetSortResponse:
    print(query.key)
    sorted_model = handler_prod._sort_items(GetSortRequest(key=query.key))
    if "user" in session:
        user_info = session.get("user")
        return render_template(
            "sorted.html", products=sorted_model.dict(), userinfo=user_info
        )
    return render_template("sorted.html", products=sorted_model.dict())


@pages_bp.route("/<pid>/<price>/", methods=["GET"])
@validate()
def product(pid: str, price: str):
    details = handler_prod.get_product_details(pid)
    if not session.get("user"):
        return render_template("product.html", details=details["data"], price=price)
    user_info = session.get("user")
    return render_template(
        "product.html",
        userinfo=user_info,
        details=details["data"],
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
    return render_template("order.html", order=res, userinfo=user_info)


@pages_bp.route("/login")
def login():
    return render_template("login.html", google_id=cfg.google_client_id)


@pages_bp.route("/game")
def game():
    if "user" in session:
        user_info = session.get("user")
        return render_template("game.html", userinfo=user_info)
    return render_template("game.html")


@pages_bp.route("/news")
def news():
    list_articles = news_api.get_top_headlines()["articles"]
    newlist = sorted(list_articles, key=lambda x: x["title"], reverse=False)
    if "user" in session:
        user_info = session.get("user")
        return render_template("news.html", userinfo=user_info, headlines=newlist)
    return render_template("news.html", headlines=newlist)


# Map using Open layer
@pages_bp.route("/map")
def map():
    if "user" in session:
        user_info = session.get("user")
        return render_template("map.html", userinfo=user_info)
    return render_template("map.html")


# Admin Module to be completed
@pages_bp.route("/admin")
def admin_module():
    if not session.get("user") and request.endpoint != "login":
        return render_template("admin.html")  # redirect(url_for("pages_bp.login"))
    user_info = session.get("user")
    return render_template("admin.html", userinfo=user_info)


@pages_bp.route("/logout")
def logout():
    session["user"] = None
    session.clear()
    return redirect("/")  # redirect(url_for("pages_bp.login"))
