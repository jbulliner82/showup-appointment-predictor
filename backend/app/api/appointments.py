"""
Appointments API endpoints
"""

from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import csv
import io
from datetime import datetime

from app.database import get_db
from app.models import Provider, Patient, Appointment

router = APIRouter()

@router.post("/import-csv")
async def import_appointments_csv(
    file: UploadFile = File(...),
    provider_id: int = 1,
    db: Session = Depends(get_db)
):
    """
    Import appointments from CSV file.
    
    CSV should have columns:
    - patient_code: Unique patient identifier
    - appointment_datetime: YYYY-MM-DD HH:MM:SS format
    - showed_up: true/false or 1/0
    - appointment_type: (optional) cleaning, checkup, etc.
    """
    
    contents = await file.read()
    csv_text = contents.decode('utf-8')
    csv_reader = csv.DictReader(io.StringIO(csv_text))
    
    imported_count = 0
    patients_created = 0
    errors = []
    
    provider = db.query(Provider).filter(Provider.id == provider_id).first()
    if not provider:
        provider = Provider(
            id=provider_id,
            name="Default Provider",
            email="provider@example.com",
            practice_type="dental"
        )
        db.add(provider)
        db.commit()
    
    for row_num, row in enumerate(csv_reader, start=2):
        try:
            patient_code = row.get('patient_code', '').strip()
            appointment_datetime_str = row.get('appointment_datetime', '').strip()
            showed_up_str = row.get('showed_up', '').strip().lower()
            appointment_type = row.get('appointment_type', 'general').strip()
            
            if not patient_code or not appointment_datetime_str:
                errors.append(f"Row {row_num}: Missing patient_code or appointment_datetime")
                continue
            
            try:
                appointment_datetime = datetime.strptime(appointment_datetime_str, '%Y-%m-%d %H:%M:%S')
            except ValueError:
                try:
                    appointment_datetime = datetime.strptime(appointment_datetime_str, '%Y-%m-%d %H:%M')
                except ValueError:
                    errors.append(f"Row {row_num}: Invalid datetime format: {appointment_datetime_str}")
                    continue
            
            showed_up = showed_up_str in ['true', '1', 'yes', 'y']
            did_noshow = not showed_up
            
            patient = db.query(Patient).filter(
                Patient.patient_code == patient_code,
                Patient.provider_id == provider_id
            ).first()
            
            if not patient:
                patient = Patient(
                    provider_id=provider_id,
                    patient_code=patient_code,
                    total_appointments=0,
                    total_noshow=0,
                    noshow_rate=0.0,
                    is_new_patient=True
                )
                db.add(patient)
                db.flush()
                patients_created += 1
            
            appointment = Appointment(
                provider_id=provider_id,
                patient_id=patient.id,
                appointment_datetime=appointment_datetime,
                appointment_type=appointment_type,
                scheduled_at=appointment_datetime,
                status="completed",
                actual_status="showed" if showed_up else "noshow",
                did_noshow=did_noshow
            )
            db.add(appointment)
            
            patient.total_appointments += 1
            if did_noshow:
                patient.total_noshow += 1
            patient.noshow_rate = patient.total_noshow / patient.total_appointments if patient.total_appointments > 0 else 0
            patient.last_appointment = appointment_datetime
            patient.is_new_patient = False
            
            imported_count += 1
            
        except Exception as e:
            errors.append(f"Row {row_num}: {str(e)}")
            continue
    
    db.commit()
    
    return {
        "success": True,
        "message": f"Successfully imported {imported_count} appointments",
        "appointments_imported": imported_count,
        "patients_created": patients_created,
        "errors": errors if errors else None
    }

@router.get("/stats")
async def get_appointment_stats(db: Session = Depends(get_db)):
    """
    Get basic statistics about appointments in the database.
    """
    total_appointments = db.query(Appointment).count()
    total_patients = db.query(Patient).count()
    total_noshows = db.query(Appointment).filter(Appointment.did_noshow == True).count()
    
    noshow_rate = (total_noshows / total_appointments * 100) if total_appointments > 0 else 0
    
    return {
        "total_appointments": total_appointments,
        "total_patients": total_patients,
        "total_noshows": total_noshows,
        "noshow_rate": f"{noshow_rate:.1f}%"
    }

@router.post("/train-model")
async def train_prediction_model(db: Session = Depends(get_db)):
    """
    Train the ML model on current appointment data.
    """
    from app.ml.predictor import NoShowPredictor
    import pandas as pd
    
    # Get all appointments and patients
    appointments = db.query(Appointment).all()
    patients = db.query(Patient).all()
    
    if len(appointments) < 10:
        raise HTTPException(
            status_code=400, 
            detail="Need at least 10 appointments to train model"
        )
    
    # Convert to DataFrames
    apt_data = [{
        'patient_id': a.patient_id,
        'appointment_datetime': a.appointment_datetime,
        'did_noshow': a.did_noshow
    } for a in appointments]
    
    pat_data = [{
        'id': p.id,
        'noshow_rate': p.noshow_rate,
        'total_appointments': p.total_appointments,
        'is_new_patient': p.is_new_patient
    } for p in patients]
    
    apt_df = pd.DataFrame(apt_data)
    pat_df = pd.DataFrame(pat_data)
    
    # Train model
    predictor = NoShowPredictor()
    metrics = predictor.train(apt_df, pat_df)
    
    return {
        "success": True,
        "message": "Model trained successfully",
        "metrics": metrics,
        "training_samples": len(appointments)
    }	

@router.post("/predict-risk")
async def predict_noshow_risk(
    patient_code: str,
    appointment_datetime: str,
    appointment_type: str = "general",
    db: Session = Depends(get_db)
):
    """
    Predict no-show risk for a future appointment.
    
    Parameters:
    - patient_code: Patient identifier
    - appointment_datetime: Future appointment time (YYYY-MM-DD HH:MM:SS)
    - appointment_type: Type of appointment (optional)
    """
    from app.ml.predictor import NoShowPredictor
    
    # Get or create patient
    patient = db.query(Patient).filter(
        Patient.patient_code == patient_code
    ).first()
    
    if not patient:
        # New patient - use defaults
        patient_data = {
            'id': 0,
            'noshow_rate': 0.0,
            'total_appointments': 0,
            'is_new_patient': True
        }
    else:
        patient_data = {
            'id': patient.id,
            'noshow_rate': patient.noshow_rate,
            'total_appointments': patient.total_appointments,
            'is_new_patient': patient.is_new_patient
        }
    
    # Parse appointment datetime
    try:
        apt_datetime = datetime.strptime(appointment_datetime, '%Y-%m-%d %H:%M:%S')
    except ValueError:
        apt_datetime = datetime.strptime(appointment_datetime, '%Y-%m-%d %H:%M')
    
    # Prepare appointment data
    appointment_data = {
        'patient_id': patient_data['id'],
        'appointment_datetime': apt_datetime,
        'appointment_type': appointment_type
    }
    
    # Make prediction
    try:
        predictor = NoShowPredictor()
        prediction = predictor.predict(appointment_data, patient_data)
        
        return {
            "success": True,
            "patient_code": patient_code,
            "appointment_datetime": appointment_datetime,
            "prediction": prediction,
            "recommendation": get_recommendation(prediction['risk_level'])
        }
    except FileNotFoundError:
        raise HTTPException(
            status_code=400,
            detail="Model not trained yet. Please train the model first using /train-model"
        )

def get_recommendation(risk_level: str) -> str:
    """Get recommendation based on risk level."""
    if risk_level == "high":
        return "Send 3 reminders: 7 days, 3 days, and 1 day before. Consider phone call confirmation."
    elif risk_level == "medium":
        return "Send 2 reminders: 3 days and 1 day before appointment."
    else:
        return "Send 1 reminder: 1 day before appointment."
		