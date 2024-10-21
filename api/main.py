import api
import base64
import urllib.parse
from fastapi import Body, UploadFile
from config import api_init, Tags
from examples import ex
from fastapi.responses import FileResponse
# pre-config #
app = api_init()

# routes #
#|=============================[keenetic routes]=============================|
# 1. /keenetic/get_devices
@app.get("/keenetic/get_devices", tags=[Tags.keenetic], summary="Get devices")
async def get_devices():
    r = await api.get_devices()
    return r
#--------------------------------------------------------------------------

# 2. /keenetic/set_device
@app.post("/keenetic/set_device", tags=[Tags.keenetic], summary="Set device in DB")
async def set_device(data = Body(example=ex.set_device)):
    r = await api.set_device(data)
    return r
#--------------------------------------------------------------------------

# 3. /keenetic/rewrite_all
@app.get("/keenetic/rewrite_all", tags=[Tags.keenetic], summary="rewrite devices")
async def rewrite_all():
    r = await api.rewrite_all()
    return r
#--------------------------------------------------------------------------