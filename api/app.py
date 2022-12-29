from os import path
from flask import Flask, send_file
from modules.blueprints import auth, users, products, pages, orders
from modules.database.mongodb.users import Users
from modules.database.mongodb.orders import Order
from modules.auth.handler import Auth
from modules.database.mongodb.products import Product
from flask_session import Session
from modules.config.config import Config
from modules.blueprints.auth import auth_bp
from modules.blueprints.products import products_bp
from modules.blueprints.orders import order_bp
from modules.blueprints.pages import pages_bp
from modules.blueprints.users import users_bp
from dateutil.parser import parse


cfg = (
    Config().from_toml_file()
)  # Config().from_toml_file().from_env_file() to use env file


# create a Flask app
app = Flask(__name__)
app.secret_key = cfg.secret_key
app.config["SESSION_TYPE"] = "filesystem"


# register blueprints
app.register_blueprint(users_bp, url_prefix="/users")
app.register_blueprint(auth_bp, url_prefix="/auth")
app.register_blueprint(products_bp, url_prefix="/products")
app.register_blueprint(order_bp, url_prefix="/orders")
app.register_blueprint(pages_bp, url_prefix="/")
Session(app)

# Infering one class to another
users.handler_user = Users(cfg)
auth.handler_auth = Auth(cfg)
pages.handler_prod = Product(cfg)
products.handler_prod = Product(cfg)
pages.handler_order = Order(cfg)
orders.handler = Order(cfg)


@app.route("/favicon.ico")
def favicon():
    fav_path = path.join(app.static_folder, "favicon.ico")
    return send_file(fav_path)


# custom date filter
@app.template_filter()
def format_datetime(value):
    dt = parse(value)
    return str(dt.date()) + " " + str(dt.time().replace(microsecond=0))


app.threaded = cfg.debug
app.use_reloader = app.debug = cfg.debug


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=cfg.host_port)
