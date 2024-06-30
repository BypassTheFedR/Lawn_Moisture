from fastapi import FastAPI, Request, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from pydantic import BaseModel
from database import SessionLocal, SensorData
from fastapi.staticfiles import StaticFiles
from pathlib import Path

app = FastAPI()
tempaltes = Jinja2Templates(directory="Templates")



class SensorDataInput(BaseModel):
    temperature: float
    soil_moisture: float

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Assuming 'static' folder is in the same directory as your main.py
app.mount("/static", StaticFiles(directory=Path(__file__).parent.absolute() / "static"), name="static")

@app.post("/data/")
def create_data(data: SensorDataInput, db: Session = Depends(get_db)):
    db_data = SensorData(
        temperature=data.temperature,
        soil_moisture=data.soil_moisture,
    )
    db.add(db_data)
    db.commit()
    db.refresh(db_data)
    return db_data

@app.get("/", response_class=HTMLResponse)
def read_root(request: Request, db: Session = Depends(get_db)):
    data = db.query(SensorData).order_by(SensorData.timestamp.desc()).all()
    return tempaltes.TemplateResponse("index.html", {"request": request, "data": data})