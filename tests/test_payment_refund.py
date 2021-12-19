import afterpay
import os
from dotenv import load_dotenv


load_dotenv()

test_params = {
    "amount": {
        "amount": os.environ.get("TEST_ORDER_AMOUNT"),
        "currency": os.environ.get("TEST_ORDER_CURRENCY")
    },
    "merchantReference": afterpay.Payment.generate_uuid()
}

cfg = afterpay.Configuration(environment=afterpay.Environment.Sandbox_NA, merchant_id=os.environ.get("MERCHANT_ID"), secret_key=os.environ.get("SECRET_KEY"))
gateway = afterpay.AfterpayGateway(config=cfg)
payment = afterpay.Payment(gateway)

print("Before: " + payment.get(order_id=os.environ.get("TEST_ORDER_ID")))
print("Refund: " + payment.refund(order_id=os.environ.get("TEST_ORDER_ID"), params=test_params))
print("After: " + payment.get(order_id=os.environ.get("TEST_ORDER_ID")))
