# -*- coding: utf-8 -*-
"""Receipt forms."""
from flask_wtf import FlaskForm
from wtforms import IntegerField, StringField, FieldList
from wtforms.validators import DataRequired, NumberRange

from flask_cash_receipts.receipts.models import Receipt


class RetailItemForm(FlaskForm):
    """Form for a single retail item."""

    count = IntegerField(
        "Item Count",
        validators=[
            NumberRange(
                min=0, max=1000, message="You must select between 0 and 1000 items."
            )
        ],
    )


class ReceiptForm(FlaskForm):
    """Form for a receipt."""

    username = StringField("Username", validators=[DataRequired()])
    pin = StringField("Pin", validators=[DataRequired()])
    items = FieldList(RetailItemForm, label="Item Name", validators=[DataRequired()])

    def __init__(self, retail_items: list, *args, **kwargs):
        """Create an instance of a receipt."""
        super(ReceiptForm, self).__init__(*args, **kwargs)

        self.items.min_entries = len(retail_items)
