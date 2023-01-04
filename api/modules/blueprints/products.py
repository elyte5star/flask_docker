from flask import Blueprint
from modules.schemas.requests.product import (
    CreateProductRequest,
)
from modules.schemas.responses.product import (
    CreateProductResponse,
    GetProductsResponse,
)

products_bp = Blueprint(
    "products_bp",
    __name__,
    template_folder="templates",
    static_folder="static",
    static_url_path="assets",
)


@products_bp.route("/all", methods=["GET"])
def list_of_products() -> GetProductsResponse:
    return handler_prod.get_all_products()


@products_bp.route("/<product_id>", methods=["GET"])
def get_product_details(product_id: str):
    return handler_prod.get_product_details(product_id)


@products_bp.route("/create", methods=["POST"])
def create_product(body: CreateProductRequest) -> CreateProductResponse:
    return handler_prod.create_product(body)
