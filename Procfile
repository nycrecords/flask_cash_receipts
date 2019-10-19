release: flask db upgrade
web: gunicorn flask_cash_receipts.app:create_app\(\) -b 0.0.0.0:$PORT -w 3
