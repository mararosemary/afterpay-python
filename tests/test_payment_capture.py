import afterpay
import os
from dotenv import load_dotenv


load_dotenv()

test_capture_request = {
    "token": os.environ.get("TEST_TOKEN"),
    "merchantReference": "1"
}

cfg = afterpay.Configuration(environment=afterpay.Environment.Sandbox_NA, merchant_id=os.environ.get("MERCHANT_ID"), secret_key=os.environ.get("SECRET_KEY"))
gateway = afterpay.AfterpayGateway(config=cfg)
payment = afterpay.Payment(gateway)

print(payment.capture(test_capture_request))
