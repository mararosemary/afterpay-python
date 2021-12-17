import afterpay
import os
from dotenv import load_dotenv


load_dotenv()

test_params = {
    "amount": {
        "amount": "25.00",
        "currency": "USD"
    },
    "consumer": {
        "givenNames": "Joe",
        "surname": "Consumer",
        "email": "test@example.com"
    },
    "billing": {
        "name": "Joe Consumer",
        "line1": "155 S Seward St",
        "postcode": "99801",
        "area1": "Juneau",
        "region": "Alaska",
        "countryCode": "US"
    },
    "shipping": {
        "name": "Joe Consumer",
        "line1": "155 S Seward St",
        "postcode": "99801",
        "area1": "Juneau",
        "region": "Alaska",
        "countryCode": "US"
    },
    "merchant": {
        "redirectConfirmUrl": "https://example.com/checkout/confirm",
        "redirectCancelUrl": "https://example.com/checkout/cancel"
    },
}

cfg = afterpay.Configuration(environment=afterpay.Environment.Sandbox_NA, merchant_id=os.environ.get("MERCHANT_ID"), secret_key=os.environ.get("SECRET_KEY"))
gateway = afterpay.AfterpayGateway(config=cfg)

print(gateway.client_token.generate(test_params))
