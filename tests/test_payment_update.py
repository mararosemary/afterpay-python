import afterpay
import os
from dotenv import load_dotenv


load_dotenv()

new_ref = afterpay.Payment.generate_uuid()

test_params = {
    "merchantReference": new_ref
}

cfg = afterpay.Configuration(environment=afterpay.Environment.Sandbox_NA, merchant_id=os.environ.get("MERCHANT_ID"), secret_key=os.environ.get("SECRET_KEY"))
gateway = afterpay.AfterpayGateway(config=cfg)
payment = afterpay.Payment(gateway)

print("Before: " + payment.get(order_id=os.environ.get("TEST_ORDER_ID")))
print("Update: " + payment.update(order_id=os.environ.get("TEST_ORDER_ID"), params=test_params))
print("After: " + payment.get(order_id=os.environ.get("TEST_ORDER_ID")))
