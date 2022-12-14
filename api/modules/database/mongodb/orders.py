from typing import Tuple
from modules.database.mongodb.base import Database
from modules.schemas.requests.order import ConfirmOrderRequest, CreateOrder
from modules.schemas.responses.order import (
    ConfirmOrderResponse,
    CreateOrderResponse,
    GetOrderResponse,
)
from flask_pydantic import validate
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
            # check if the client is logged in
            if "user" in session:
                user_dict = session.get("user")
                _total_price = unit_price * int(volume)
                total_price = self.calculate_discount(
                    _total_price, user_dict["discount"]
                )
                model = CreateOrderResponse(
                    message="Order created",
                    sale_price=total_price,
                    volume=volume,
                    userid=user_dict["userid"],
                    pid=form_data.pid,
                )
                return model.dict()

            # ordinary customers with non registered account or admin
            else:
                total_price = unit_price * int(volume)
                model = CreateOrderResponse(
                    message="Order created",
                    sale_price=total_price,
                    volume=volume,
                    userid=self.get_indent(),
                    pid=form_data.pid,
                )

                return model.dict()

        return self.bad_request("Product does not exist!")

    def _confirm_order(self, confirm_oder: ConfirmOrderRequest) -> ConfirmOrderResponse:
        if confirm_oder:
            conf_dict = confirm_oder.dict()
            conf_dict["created_at"] = self.time_now()
            result = self.admin_db.orders.insert_one(conf_dict)
            return ConfirmOrderResponse(
                message="Order Registered!", oid=str(result.inserted_id)
            )

        return self.bad_request("Can't confirm the order!")

    def _get_orders(self):
        cursor = self.admin_db.orders.find({})
        if cursor:
            order_list = []
            for order in cursor:
                order["oid"] = str(order.pop("_id"))
                order_list.append(order)
            model = GetOrderResponse(
                orders=order_list, message=f"num_orders {len(order_list)}"
            )
            return model.dict()
        return self.bad_request("No orders found!")
