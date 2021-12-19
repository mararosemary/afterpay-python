import afterpay
import os
from dotenv import load_dotenv


load_dotenv()

test_params = {
    "merchantReference": os.environ.get("TEST_ORDER_MERCHANT_REF")
}

cfg = afterpay.Configuration(environment=afterpay.Environment.Sandbox_NA, merchant_id=os.environ.get("MERCHANT_ID"), secret_key=os.environ.get("SECRET_KEY"))
gateway = afterpay.AfterpayGateway(config=cfg)
payment = afterpay.Payment(gateway)

print(payment.reverse(token=os.environ.get("TEST_TOKEN"), params=test_params))
