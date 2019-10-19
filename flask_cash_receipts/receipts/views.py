# -*- coding: utf-8 -*-
"""Receipt section."""
from flask import (
    Blueprint,
    current_app,
    flash,
    redirect,
    render_template,
    request,
    url_for,
)
from flask_cash_receipts.receipts.forms import ReceiptForm
from flask_cash_receipts.receipts.models import Receipt, RetailItem
from flask_cash_receipts.utils import flash_errors
from flask_cash_receipts.receipts.constants import ITEM_ROW
from flask_cash_receipts.database import db

from functools import reduce
from operator import add
from sys import maxsize
from json import dumps

import datetime as dt

blueprint = Blueprint(
    "receipt", __name__, url_prefix="/retail", static_folder="../static"
)


@blueprint.route("/generate", methods=["GET", "POST"])
def generate():
    """Generate a receipt."""
    event_name = request.args.get("event_name", "default")
    event_id = request.args.get("event_id", "")
    if event_name:
        retail_items = RetailItem.query.filter_by(event_name=event_name).all()

    if request.method == "POST":
        username = request.form.get("username", None)
        pin = request.form.get("pin", None)

        if not username or not pin:
            flash_errors("Username and Pin are required.")

        retail_items_dict = {
            item.id: {
                "name": item.name,
                "price": item.price,
                "tax": item.tax,
                "custom_attributes": item.custom_attributes,
            }
            for item in retail_items
        }

        receipt_items = []
        for key, value in enumerate(request.form.to_dict(flat=True)):
            if value in retail_items_dict.keys():
                if request.form.get(value) == "0":
                    continue
                item_id = value
                item_name = retail_items_dict[value]["name"]
                quantity = int(request.form.get(value))
                if retail_items_dict[value]["custom_attributes"] is not None:
                    item_name += "({attribute}: {attribute_value})".format(
                        attribute=retail_items_dict[value]["custom_attributes"],
                        attribute_value=request.form.get(
                            value + retail_items_dict[value]["custom_attributes"]
                        ),
                    )
                price = retail_items_dict[value]["price"]
                tax = retail_items_dict[value]["tax"]
                receipt_items.append(
                    {
                        "id": value,
                        "name": item_name,
                        "price": price,
                        "quantity": quantity,
                        "total": quantity * price,
                        "total_tax": quantity * tax,
                        "subtotal": (quantity * tax) + (quantity * price)
                    }
                )
        
        subtotal = reduce(add, [i["total"] for i in receipt_items])
        total_tax = reduce(add, [i["total_tax"] for i in receipt_items])
        total = subtotal + total_tax
        timestamp = dt.datetime.now()
        receipt_id = "{timestamp}-{userhash}".format(timestamp=timestamp.strftime('%Y%m%d%H%M'), userhash=str((hash((username, pin, timestamp)) & maxsize))[:5])

        receipt = Receipt(
            id=receipt_id,
            username=username,
            pin=pin,
            transaction_time = timestamp,
            subtotal=subtotal,
            tax=total_tax,
            total=total,
            items=dumps(receipt_items)
        )
        db.session.add(receipt)
        db.session.commit()

        return render_template("receipts/receipt.html", receipt=receipt, receipt_items=receipt_items, event_name=event_name)

    return render_template("receipts/register.html", items=retail_items)
