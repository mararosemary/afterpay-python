import afterpay
import os
from dotenv import load_dotenv


load_dotenv()

cfg = afterpay.Configuration(environment=afterpay.Environment.Sandbox_NA, merchant_id=os.environ.get("MERCHANT_ID"), secret_key=os.environ.get("SECRET_KEY"))
gateway = afterpay.AfterpayGateway(config=cfg)
payment = afterpay.Payment(gateway)

print(payment.list())
