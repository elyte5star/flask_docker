from modules.schemas.requests.order import ConfirmOrderRequest, CreateOrder
from modules.schemas.responses.order import (
    ConfirmOrderResponse,
    CreateOrderResponse,
    GetOrderResponse,
)
from flask_pydantic import validate
from flask import Blueprint
from modules.auth.auth_bearer import security

order_bp = Blueprint(
    "order_bp",
    __name__,
    template_folder="templates",
    static_folder="static",
    static_url_path="assets",
)

# Create Order
@order_bp.route("/create_order", methods=["POST"])
@validate()
def create_order(form: CreateOrder) -> CreateOrderResponse:
    return handler._create_order(CreateOrder(pid=form.pid, volume=form.volume))


# Confirm Order
@order_bp.route("/confirm", methods=["POST"])
@validate()
def confirm_order(body: ConfirmOrderRequest) -> ConfirmOrderResponse:
    return handler._confirm_order(
        ConfirmOrderRequest(
            pid=body.pid, userid=body.userid, email=body.email, telephone=body.telephone
        )
    )


# Get Orders
@order_bp.route("/all", methods=["GET"])
@validate()
def get_orders() -> GetOrderResponse:
    return handler._get_orders()
