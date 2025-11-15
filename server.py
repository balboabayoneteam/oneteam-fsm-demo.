import uuid
from datetime import datetime
from typing import List, Optional
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(title="OneTeam FSM Demo API", version="0.1.0")

REQUESTS, VENDORS, BIDS, JOBS = {}, {}, {}, {}

class MaintenanceRequest(BaseModel):
    property_id: str
    unit: str
    category: str
    urgency: str
    description: str
    photos: Optional[List[str]] = None

class Vendor(BaseModel):
    name: str
    category: List[str]
    max_cap: float = 500.0
    emergency_cap: float = 1000.0

class Bid(BaseModel):
    vendor_id: str
    request_id: str
    amount: float
    response: str

class DispatchDecision(BaseModel):
    bid_id: str
    decision: str
    bill_to: str

@app.post("/intake")
def intake(req: MaintenanceRequest):
    req_id = str(uuid.uuid4())
    REQUESTS[req_id] = req.dict() | {"id": req_id, "created_at": datetime.utcnow().isoformat()}
    return {"request_id": req_id}

@app.post("/vendors")
def register_vendor(vendor: Vendor):
    vid = str(uuid.uuid4())
    VENDORS[vid] = vendor.dict() | {"id": vid}
    return {"vendor_id": vid}

@app.get("/vet/{request_id}")
def vet(request_id: str):
    if request_id not in REQUESTS:
        raise HTTPException(status_code=404, detail="Request not found")
    req = REQUESTS[request_id]
    vetted = [{"vendor_id": vid, "name": v["name"]} for vid, v in VENDORS.items() if req["category"] in v["category"]]
    return {"request_id": request_id, "vetted_vendors": vetted}

@app.post("/bid")
def bid(bid: Bid):
    if bid.request_id not in REQUESTS or bid.vendor_id not in VENDORS:
        raise HTTPException(status_code=404, detail="Request or Vendor not found")
    bid_id = str(uuid.uuid4())
    BIDS[bid_id] = bid.dict() | {"id": bid_id}
    return {"bid_id": bid_id}

@app.post("/dispatch")
def dispatch(decision: DispatchDecision):
    if decision.bid_id not in BIDS:
        raise HTTPException(status_code=404, detail="Bid not found")
    bid = BIDS[decision.bid_id]
    job_id = str(uuid.uuid4())
    JOBS[job_id] = {"job_id": job_id, "request_id": bid["request_id"], "vendor_id": bid["vendor_id"], "amount": bid["amount"], "bill_to": decision.bill_to, "status": "dispatched"}
    return {"status": "approved", "job": JOBS[job_id]}

@app.get("/jobs/{job_id}")
def job_status(job_id: str):
    if job_id not in JOBS:
        raise HTTPException(status_code=404, detail="Job not found")
    return JOBS[job_id]
