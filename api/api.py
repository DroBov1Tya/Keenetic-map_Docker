import logging
from config import PostgreSQL
from typing import Dict, Any, Union

pg = PostgreSQL()
logger = logging.getLogger(__name__)

async def handle_exception(ex: Exception) -> Dict[str, Any]:
    if isinstance(ex, ConnectionError):
        logger.error("Connection error: %s", str(ex))
        return {"Success": False, "Reason": f"Connection error: {ex}"}
    
    elif isinstance(ex, TimeoutError):
        logger.warning("Timeout occurred: %s", str(ex))
        return {"Success": False, "Reason": f"Timeout occurred: {ex}"}
    
    elif isinstance(ex, ValueError):
        logger.error("Value error: %s", str(ex))
        return {"Success": False, "Reason": f"Value error: {ex}"}
    
    else:
        logger.exception("Unexpected error occurred")
        return {"Success": False, "Reason": f"Unexpected error: {ex}"}
    
#=========================[Keenetic]=============================|
# 1. /keenetic/get_devices
async def get_devices():
    """
    """

    query = '''
    SELECT * from devices;
    '''

    try:
        r = await pg.fetchall(query)
        if r:
            return {"Success": True, "result": r}
        else:
            return {"Success": False, "result": r}
        
    except Exception as ex:
        return await handle_exception(ex)
    
#-------------------------------------------------------------------
# 2. /keenetic/set_device
async def set_device(data: Dict[str, Any]):
    """
    """

    mac = data.get("mac")
    via = data.get("via")
    ip = data.get("ip")
    hostname = data.get("hostname")
    name = data.get("name")
    interface = data.get("description")
    registered = data.get("registered")
    access = data.get("access")
    permit = data.get("permit")
    priority = data.get("priority")
    active = data.get("active")
    rxbytes = data.get("rxbytes")
    txbytes = data.get("txbytes")
    uptime = data.get("uptime")
    first_seen = data.get("first-seen")
    last_seen = data.get("last-seen")
    link = data.get("link")
    auto_negotiation = data.get("auto-negotiation")
    speed = data.get("speed")
    duplex = data.get("duplex")
    port = data.get("port")

    query = '''
    INSERT INTO devices
    (mac, via, ip, hostname, device_name, segment,
    registered, access, permit, priority, active,
    rxbytes, txbytes, uptime, first_seen, last_seen, link,
    auto_negotiation, speed, duplex, port
    )
    VALUES($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12,
        $13, $14, $15, $16, $17, $18, $19, $20, $21);
    '''

    query_history = '''
    INSERT INTO devices_history
    (mac, via, ip, hostname, device_name, segment,
    registered, access, permit, priority, active,
    rxbytes, txbytes, uptime, first_seen, last_seen, link,
    auto_negotiation, speed, duplex, port
    )
    VALUES($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12,
        $13, $14, $15, $16, $17, $18, $19, $20, $21);
    '''

    values = (
        mac, via, ip, hostname, name, interface,
        registered, access, permit, priority, active,
        rxbytes, txbytes, uptime, first_seen, last_seen, link,
        auto_negotiation, speed, duplex, int(port)
    )

    try:
        r = await pg.execute(query, values)
        if r is None:
            await pg.execute(query_history, values)
            return {"Success": True, "result": r}
        else:
            return {"Success": False, "result": r}
        
    except Exception as ex:
        return await handle_exception(ex)
#-------------------------------------------------------------------

# 3. /keenetic/rewrite_all
async def rewrite_all():
    """
    """

    query = '''
        TRUNCATE TABLE devices RESTART IDENTITY;
    '''

    try:
        r = await pg.execute(query)
        if r is None:
            return {"Success": True}
        else:
            return {"Success": False, "result": r}
        
    except Exception as ex:
        return await handle_exception(ex)
#-------------------------------------------------------------------