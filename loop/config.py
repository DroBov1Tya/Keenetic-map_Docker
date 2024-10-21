import os
from src.keenetic import Router

x_api_key = os.getenv("FASTAPI_KEY")
keenetic_ip = os.getenv("KEENETIC_IP")
keenetic_user = os.getenv("KEENETIC_USER")
keenetic_pass = os.getenv("KEENETIC_PASSWD")

headers = {
    "X-API-Key": x_api_key
}

router = Router(
    username=keenetic_user, 
    password=keenetic_pass, 
    host=keenetic_ip
    )