from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, EmailStr, Field
from typing import List

app = FastAPI()

# In-memory storage
doctors = []
patients = []

# Pydantic Models

class Doctor(BaseModel):
    id: int
    name: str
    specialization: str
    email: EmailStr
    is_active: bool = True


class Patient(BaseModel):
    id: int
    name: str
    age: int = Field(..., gt=0)
    phone: str


# Doctor APIs

@app.post("/doctors")
def create_doctor(doctor: Doctor):
    # check duplicate id
    for d in doctors:
        if d["id"] == doctor.id:
            raise HTTPException(status_code=400, detail="Doctor already exists")

    doctors.append(doctor.dict())
    return {"message": "Doctor created", "data": doctor}


@app.get("/doctors")
def get_doctors():
    return doctors


@app.get("/doctors/{doctor_id}")
def get_doctor(doctor_id: int):
    for d in doctors:
        if d["id"] == doctor_id:
            return d

    raise HTTPException(status_code=404, detail="Doctor not found")


# Patient APIs

@app.post("/patients")
def create_patient(patient: Patient):
    for p in patients:
        if p["id"] == patient.id:
            raise HTTPException(status_code=400, detail="Patient already exists")

    patients.append(patient.dict())
    return {"message": "Patient created", "data": patient}


@app.get("/patients")
def get_patients():
    return patients
