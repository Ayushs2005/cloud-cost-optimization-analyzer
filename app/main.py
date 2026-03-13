from fastapi import FastAPI
from .aws_cost import fetch_cost_data
from .db import SessionLocal, engine, Base
from .models import CostData

Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.get("/")
def home():
    return {"message": "Cloud Cost Optimization Analyzer"}

@app.get("/fetch-cost")
def fetch_and_store_cost():
    db = SessionLocal()
    data = fetch_cost_data()

    for item in data:
        record = CostData(
            service=item["service"],
            cost=item["cost"],
            usage_date=item["date"]
        )
        db.add(record)

    db.commit()

    return {"message": "Cost data stored", "records": len(data)}


@app.get("/cost-summary")
def cost_summary():
    db = SessionLocal()
    rows = db.query(CostData.service, CostData.cost).all()

    summary = {}
    for service, cost in rows:
        summary[service] = summary.get(service, 0) + cost

    return summary
