"""Paymob Accept helpers. Keys stay on the server; success is confirmed ONLY by the signed webhook."""
import hashlib, hmac
import requests
from django.conf import settings

BASE = "https://accept.paymob.com/api"
HMAC_FIELDS = ["amount_cents", "created_at", "currency", "error_occured", "has_parent_transaction", "id",
               "integration_id", "is_3d_secure", "is_auth", "is_capture", "is_refunded",
               "is_standalone_payment", "is_voided", "order.id", "owner", "pending",
               "source_data.pan", "source_data.sub_type", "source_data.type", "success"]

def _post(path, payload):
    r = requests.post(f"{BASE}/{path}", json=payload, timeout=20)
    r.raise_for_status()
    return r.json()

def checkout_url(payment, user):
    cfg = settings.PAYMOB
    token = _post("auth/tokens", {"api_key": cfg["API_KEY"]})["token"]
    order = _post("ecommerce/orders", {"auth_token": token, "delivery_needed": False,
        "amount_cents": payment.amount_cents, "currency": "EGP",
        "merchant_order_id": payment.merchant_order_id, "items": []})
    key = _post("acceptance/payment_keys", {"auth_token": token, "amount_cents": payment.amount_cents,
        "expiration": 3600, "order_id": order["id"], "currency": "EGP",
        "integration_id": int(cfg["INTEGRATION_ID"]),
        "billing_data": {"first_name": user.first_name or "NA", "last_name": "NA", "email": user.email,
            "phone_number": user.phone or "NA", "apartment": "NA", "floor": "NA", "street": "NA",
            "building": "NA", "shipping_method": "NA", "postal_code": "NA", "city": "NA",
            "country": "EG", "state": "NA"}})["token"]
    return f"{BASE}/acceptance/iframes/{cfg['IFRAME_ID']}?payment_token={key}"

def _get(obj, dotted):
    for part in dotted.split("."):
        obj = obj.get(part, "") if isinstance(obj, dict) else ""
    return str(obj).lower() if isinstance(obj, bool) else str(obj)

def valid_signature(obj, received):
    msg = "".join(_get(obj, f) for f in HMAC_FIELDS)
    calc = hmac.new(settings.PAYMOB["HMAC_SECRET"].encode(), msg.encode(), hashlib.sha512).hexdigest()
    return hmac.compare_digest(calc, received or "")
