from typing import List
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

app = FastAPI()

Base = declarative_base()

class Reminder(Base):
    __tablename__ = 'reminders'

    id = Column(Integer, primary_key=True, index=True)
    date = Column(String)
    time = Column(String)
    message = Column(String)
    reminder_method = Column(String)

DATABASE_URL = "sqlite:///reminder.db"


engine = create_engine(DATABASE_URL)
Base.metadata.create_all(engine)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

class ReminderCreate(BaseModel):
    date: str #should be in YYYY-MM-DD
    time: str #shpuld be in HH:MM
    message: str
    reminder_method: str #used to define whether message is sent through SMS or Email

class OutModel(BaseModel):
    id: int
    date: str
    time: str
    message: str
    reminder_method: str



@app.post("/create_reminder/")
async def create_reminder(reminder: ReminderCreate):
    try:
        db = SessionLocal()
        db.add(Reminder(**reminder.dict()))
        db.commit()
        db.close()
        return {"message": "Reminder created successfully"}
    except Exception as e:
        print("Error:", e)
        db.rollback()
        raise HTTPException(status_code=500, detail="Error occurred while creating reminders")
    finally:
        db.close()



@app.get("/get_reminders/",response_model=List[OutModel])
async def get_reminders():
    try:
        db = SessionLocal()
        reminders = db.query(Reminder).all()
        return reminders
    except Exception as e:
        print("Error:", e)
        raise HTTPException(status_code=500, detail="Error occurred while retrieving reminders")
    finally:
        db.close()



if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
