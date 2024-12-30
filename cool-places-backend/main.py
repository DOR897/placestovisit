
from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from typing import List, Optional

app = FastAPI()

# Define the base model
Base = declarative_base()

# Define the Location model
class Location(Base):
    __tablename__ = "locations"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    description = Column(String(255), nullable=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)

# Create the database engine
engine = create_engine("sqlite:///your_database.db")

# Create the tables
Base.metadata.create_all(bind=engine)

# Create a session
Session = sessionmaker(bind=engine)

# Pydantic models for request and response
class LocationCreate(BaseModel):
    name: str
    description: str
    latitude: float
    longitude: float

class LocationUpdate(BaseModel):
    name: Optional[str]
    description: Optional[str]
    latitude: Optional[float]
    longitude: Optional[float]

class LocationResponse(BaseModel):
    id: int
    name: str
    description: str
    latitude: float
    longitude: float

    class Config:
        orm_mode = True

# Dependency to get the database session
def get_db():
    db = Session()
    try:
        yield db
    finally:
        db.close()

# API Endpoints
@app.get("/locations", response_model=List[LocationResponse])
async def get_all_locations(db: Session = Depends(get_db)):
    locations = db.query(Location).all()
    return locations

@app.get("/locations/{location_id}", response_model=LocationResponse)
async def get_location(location_id: int, db: Session = Depends(get_db)):
    location = db.query(Location).filter(Location.id == location_id).first()
    if not location:
        raise HTTPException(status_code=404, detail="Location not found")
    return location

@app.post("/locations", response_model=LocationResponse)
async def create_location(location: LocationCreate, db: Session = Depends(get_db)):
    db_location = 'Location'(
        name=location.name,
        description=location.description,
        latitude=location.latitude,
        longitude=location.longitude
    )
    db.add(db_location)
    db.commit()
    db.refresh(db_location)
    return db_location

@app.put("/locations/{location_id}", response_model=LocationResponse)
async def update_location(location_id: int, location: LocationUpdate, db: Session = Depends(get_db)):
    db_location = db.query(Location).filter(Location.id == location_id).first()
    if not db_location:
        raise HTTPException(status_code=404, detail="Location not found")
    if location.name is not None:
        db_location.name = location.name
    if location.description is not None:
        db_location.description = location.description
    if location.latitude is not None:
        db_location.latitude = location.latitude
    if location.longitude is not None:
        db_location.longitude = location.longitude
    db.commit()
    db.refresh(db_location)
    return db_location

@app.delete("/locations/{location_id}")
async def delete_location(location_id: int, db: Session = Depends(get_db)):
    db_location = db.query(Location).filter(Location.id == location_id).first()
    if not db_location:
        raise HTTPException(status_code=404, detail="Location not found")
    db.delete(db_location)
    db.commit()
    return {"message": "Location deleted successfully."}
