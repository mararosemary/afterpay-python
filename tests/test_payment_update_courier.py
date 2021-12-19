import afterpay
import os
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

tracking = afterpay.Payment.generate_uuid()

test_params = {
    "shippedAt": datetime.now().isoformat(),
    "name": "UPS",
    "tracking": tracking,
    "priority": "STANDARD"
}

cfg = afterpay.Configuration(environment=afterpay.Environment.Sandbox_NA, merchant_id=os.environ.get("MERCHANT_ID"), secret_key=os.environ.get("SECRET_KEY"))
gateway = afterpay.AfterpayGateway(config=cfg)
payment = afterpay.Payment(gateway)

print("Before: " + payment.get(order_id=os.environ.get("TEST_ORDER_ID")))
print("Update: " + payment.update_courier(order_id=os.environ.get("TEST_ORDER_ID"), params=test_params))
print("After: " + payment.get(order_id=os.environ.get("TEST_ORDER_ID")))
