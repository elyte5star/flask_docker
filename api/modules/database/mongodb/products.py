from flask import render_template
from modules.schemas.responses.product import (
    GetProductsDetailsResponse,
    GetProductsResponse,
    GetSortResponse,
    CreateProductResponse,
)
from modules.schemas.requests.product import (
    GetSortRequest,
    CreateProductRequest,
)
from bson.objectid import ObjectId
from flask_pydantic import validate
from modules.database.mongodb.orders import Discount


class Product(Discount):
    @validate()
    def get_all_products(self) -> GetProductsResponse:
        cursor = self.admin_db.products.find({}, {"created_at": 0, "details": 0})
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

    def _special_deals(self):
        discount = 0.05  #### Five percent discount
        res = self.get_all_products()
        product_list = res["data"]
        if product_list:
            product_list_deals = []
            for product in product_list:
                # You can add and if statement here to select the category of product that should have discount
                product["price"] = self.calculate_discount(product["price"], discount)
                product_list_deals.append(product)
            return product_list_deals
        return self.bad_request("No deals!")

    def _sort_items(self, criteria: GetSortRequest) -> GetSortResponse:
        response_dict = self.get_all_products()
        response_list, message = (None for x in range(2))
        if criteria:
            if criteria.key == "deals":
                response_list = self._special_deals()
                message = criteria.key
            elif criteria.key == "numeric_asc":
                message = criteria.key
                response_list = sorted(
                    response_dict["data"], key=lambda x: x["price"], reverse=False
                )
            elif criteria.key == "numeric_desc":
                message = criteria.key
                response_list = sorted(
                    response_dict["data"], key=lambda x: x["price"], reverse=True
                )
            elif criteria.key == "name_asc":
                message = criteria.key
                response_list = sorted(
                    response_dict["data"], key=lambda x: x["name"], reverse=False
                )

            elif criteria.key == "name_desc":
                message = criteria.key
                response_list = sorted(
                    response_dict["data"], key=lambda x: x["name"], reverse=True
                )
            else:
                return self.bad_request("Unknown search criteria !")
            return GetSortResponse(data=response_list, message=message)
        return self.bad_request("Unknown search!")

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
