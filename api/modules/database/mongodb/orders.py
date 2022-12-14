from typing import Tuple
from modules.database.mongodb.base import Database
from modules.schemas.requests.order import ConfirmOrderRequest, CreateOrder
from modules.schemas.responses.order import ConfirmOrderResponse, CreateOrderResponse
from flask_pydantic import validate
from flask import session
from bson.objectid import ObjectId

# ===================================#
# Discount by volume and by sales-amount#
# ====================================#
class Discount(Database):
    def low_discount_volume(self, volume: str, sale_amount: float) -> float:
        if volume <= 1500:
            return self.calculate_discount(sale_amount, 0.1)  # 10% discount
        return sale_amount

    def high_discount_volume(self, volume: str, sale_amount: float) -> float:
        volume = int(volume)
        if volume <= 10000:
            return self.calculate_discount(sale_amount, 0.3)  # 30% discount
        return sale_amount

    def low_discount_sale_amount(self, sale_amount: float) -> float:
        if sale_amount <= 1000:
            return self.calculate_discount(sale_amount, 0.1)  # 10% discount
        return sale_amount

    def high_discount_sale_amount(self, sale_amount: float) -> float:
        if sale_amount <= 100000:
            return self.calculate_discount(sale_amount, 0.3)  # 30% discount
        return sale_amount

    def calculate_discount(self, amount: float, percentage: float) -> float:
        discount = amount * percentage
        sale_price = amount - discount
        return str(round(sale_price, 2))


# ==============================#
# Inheriting the Discount class#
# ==============================#
class Order(Discount):
    def _create_order(self, form_data: CreateOrder) -> CreateOrderResponse:
        total_price = 0.0
        volume = form_data.volume
        unit_price = form_data.unit_price
        if form_data:
            # check if the client is logged in and get the discount and not admin
            if "user" in session and session["user"]["discount"]:
                user_dict = session.get("user")
                print(user_dict)
                discount = user_dict["discount"]
                _total_price = unit_price * int(volume)
                total_price = self.calculate_discount(_total_price, discount)
                model = CreateOrderResponse(
                    created_at=self.time_now(),
                    sale_price=total_price,
                    volume=volume,
                    userid=user_dict["userid"],
                    pid=form_data.pid,
                )
                self.admin_db.orders.insert_one(model.dict())
                return model.dict()

            # ordinary customers with non registered account
            total_price = unit_price * int(volume)
            model = CreateOrderResponse(
                created_at=self.time_now(),
                sale_price=total_price,
                volume=volume,
                userid=self.get_indent(),
                pid=form_data.pid,
            )
            self.admin_db.orders.insert_one(model.dict())
            return model.dict()

        return self.bad_request("Product does not exist!")

    def _confirm_order(self, confirm_oder: ConfirmOrderRequest) -> ConfirmOrderResponse:
        if confirm_oder:
            # Clients not logged in
            if not session.get("user"):
                self.admin_db.orders.update_one(
                    {"userid": confirm_oder.userid},
                    {
                        "$set": {
                            "email": confirm_oder.email,
                            "telephone": confirm_oder.telephone,
                        }
                    },
                )

                model = ConfirmOrderResponse(message="Order Registered!")
                return model.dict()
            else:
                # Logged in clients
                model = ConfirmOrderResponse(message="Order Already Registered!")
                return model.dict()

        return self.bad_request("Can't confirm the order!")
