from flask import render_template
from typing import Tuple
from modules.database.mongodb.base import Database
from modules.schemas.responses.product import (
    GetProductsDetailsResponse,
    GetProductsResponse,
    GetProductsDealsResponse,
    CreateProductResponse,
)
from modules.schemas.requests.product import (
    GetProductDetailsRequest,
    CreateProductRequest,
)
from bson.objectid import ObjectId
from flask_pydantic import validate


class Product(Database):
    @validate()
    def get_all_products(self) -> GetProductsResponse:
        cursor = self.admin_db.products.find(
            {}, {"created_at": 0, "description": 0, "details": 0}
        )
        if cursor:
            product_list = []
            for product in cursor:
                product["pid"] = str(product.pop("_id"))
                product_list.append(product)
            model = GetProductsResponse(
                data=product_list, message=f"num_products {len(product_list)}"
            )
            return model.dict()
        return self.bad_request("No products found!")

    def get_product_details(self, product_id: str):
        product_dict = self.admin_db.products.find_one({"_id": ObjectId(product_id)})
        if product_dict:
            product_dict["pid"] = str(product_dict.pop("_id"))
            return product_dict
        return self.bad_request("No product details found!")

    # ==========================================#
    # Special deals based on season for everyone#
    # ===========================================#

    @validate()
    def _special_deals(self) -> GetProductsDealsResponse:
        discount = 0.05  #### Five percent discount
        cursor = self.admin_db.products.find(
            {}, {"created_at": 0, "location": 0, "description": 0, "details": 0}
        )
        if cursor:
            product_list = []
            for product in cursor:
                product["pid"] = str(
                    product.pop("_id")
                )  # You can add and if statement here to select the category of product that should have discount
                disc = product["price"] * discount
                discount_price = product["price"] - disc
                product["price"] = str(round(discount_price, 2))
                product_list.append(product)
                model = GetProductsDealsResponse(
                    data=product_list,
                    message=f"Total number of Xmas special deals: {len(product_list)}",
                )
            return model.dict()
        return self.bad_request("No deals!")

    @validate()
    def create_product(
        self, product_data: CreateProductRequest
    ) -> CreateProductResponse:
        if product_data:
            product_data["created_at"] = self.time_now()
            result = self.admin_db.products.insert_one(product_data.dict(by_alias=True))
            model = CreateProductResponse(
                pid=str(result.inserted_id), message="A new product created!"
            )
            return model
        return self.bad_request("Couldnt create a product!")
