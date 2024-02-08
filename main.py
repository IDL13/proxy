import time
from fastapi import FastAPI, Request, Header, HTTPException
from fastapi.responses import RedirectResponse
from pydantic import BaseModel

class Setting(BaseModel):
    time_lock: int
    request_limit: int

app = FastAPI()

time_lock = 120
request_limit = 100

users = {}
blocked = {}

@app.get("/")
async def root():
    return {"msg": "Server started"}

@app.post("/setting/")
async def setting(setting: Setting):
    global time_lock 
    global request_limit
    
    time_lock = setting.time_lock
    request_limit = setting.request_limit
    
    return {"time_lock": time_lock, "request_limit": request_limit}

@app.get("/redirect/{site}")
async def status(site: str, x_forwarded_for: str = Header(None, alias = "X-Forwarded-For")):
    
    site = "/".join(site.split("_"))
    
    x_forwarded_for = ".".join(x_forwarded_for.split(".")[:-1])

    if x_forwarded_for in blocked and time.time() - blocked.get(x_forwarded_for, 0) < time_lock:
        raise HTTPException(status_code = 429, detail = "The request limit from one IP has been exceeded")
    else:
        if blocked.get(x_forwarded_for, 0) > 0:
            del blocked[x_forwarded_for]
        
        if users.get(x_forwarded_for, 0) == request_limit:
            users[x_forwarded_for] = 0
            blocked[x_forwarded_for] = time.time()
            raise HTTPException(status_code = 429, detail = "The request limit from one IP has been exceeded")
    
        users[x_forwarded_for] = users.get(x_forwarded_for, 0) + 1
    
    return RedirectResponse("https://" + site)

@app.get("/rm/{ip}")
async def remove(ip: str):
    
    if ip in blocked:
        del blocked[ip]
        
    return {"msg": "Ip addres unlock"}