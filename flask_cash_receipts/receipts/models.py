# -*- coding: utf-8 -*-
"""Receipt models."""
import datetime as dt
import json

from flask_cash_receipts.database import (
    Column,
    Model,
    SurrogatePK,
    db,
    reference_col,
    relationship,
)
from flask_cash_receipts.extensions import bcrypt


class RetailItem(SurrogatePK, Model):
    """An item for sale in a retail store."""

    __tablename__ = "retail_items"
    id = Column(db.String(32), nullable=False, primary_key=True, unique=True)
    name = Column(db.String(250), nullable=False)
    price = Column(db.Float, nullable=False, default=0.00)
    tax = Column(db.Float, nullable=False, default=0.00)
    event_name = Column(db.String(32), nullable=False)
    custom_attributes = Column(db.Text, nullable=True, default="")

    def __init__(self, id, name, price, tax, event_name, custom_attributes=""):
        """Create a retail item."""
        db.Model.__init__(
            self,
            id=id,
            name=name,
            price=price,
            tax=tax,
            event_name=event_name,
            custom_attributes=custom_attributes,
        )


class Receipt(SurrogatePK, Model):
    """A receipt."""

    ___tablename__ = "receipts"
    id = Column(db.String(32), nullable=False, primary_key=True)
    username = Column(db.String(32), nullable=False)
    pin = Column(db.String(32), nullable=False)
    transaction_time = Column(db.DateTime, nullable=False, default=dt.datetime.utcnow)
    subtotal = Column(db.Float, nullable=False)
    tax = Column(db.Float, nullable=False)
    total = Column(db.Float, nullable=False)
    items = Column(db.Text, nullable=False)

    def __init__(self, id, username, pin, transaction_time, subtotal, tax, total, items):
        """Create a receipt."""
        db.Model.__init__(
            self,
            id=id,
            username=username,
            pin=pin,
            transaction_time=transaction_time,
            subtotal=subtotal,
            total=total,
            tax=tax,
            items=items
        )

    def _pack_items(items: dict) -> str:
        return json.dumps(items)

    def _unpack_items(items: str) -> dict:
        return json.loads(items)
