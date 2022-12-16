from flask import render_template
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
from modules.database.mongodb.orders import Discount


class Product(Discount):
    @validate()
    def get_all_products(self) -> GetProductsResponse:
        cursor = self.admin_db.products.find({}, {"created_at": 0, "description": 0})
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

    def get_product_details(self, product_id: str) -> GetProductsDetailsResponse:
        product_dict = self.admin_db.products.find_one({"_id": ObjectId(product_id)})
        if product_dict:
            product_dict["pid"] = str(product_dict.pop("_id"))
            model = GetProductsDetailsResponse(data=product_dict)
            return model.dict()
        return self.bad_request("No product details found!")

    # ==========================================#
    # Special deals based on season for everyone#
    # ===========================================#

    def _special_deals(self) -> GetProductsDealsResponse:
        discount = 0.05  #### Five percent discount
        res = self.get_all_products()
        product_list = res["data"]
        if product_list:
            product_list_deals = []
            for product in product_list:
                # You can add and if statement here to select the category of product that should have discount
                product["price"] = self.calculate_discount(product["price"], discount)
                product_list_deals.append(product)
                model = GetProductsDealsResponse(
                    data=product_list_deals,
                    message=f"Total number of Xmas special deals: {len(product_list_deals)}",
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
