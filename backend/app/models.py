"""
Database models for ShowUp application
"""

from sqlalchemy import Column, Integer, String, DateTime, Boolean, Float, ForeignKey, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base

class Provider(Base):
    """
    Medical provider/practice using the system.
    """
    __tablename__ = "providers"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False)
    email = Column(String(200), unique=True, nullable=False)
    phone = Column(String(20))
    practice_type = Column(String(100))  # dental, medical, therapy, etc.
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    patients = relationship("Patient", back_populates="provider")
    appointments = relationship("Appointment", back_populates="provider")

class Patient(Base):
    """
    Patient information (anonymized).
    """
    __tablename__ = "patients"
    
    id = Column(Integer, primary_key=True, index=True)
    provider_id = Column(Integer, ForeignKey("providers.id"))
    
    # Anonymized identifier (don't store real names)
    patient_code = Column(String(50), unique=True, nullable=False, index=True)
    
    # Contact information for reminders
    phone = Column(String(20))
    email = Column(String(200))
    preferred_contact = Column(String(20))  # 'sms', 'email', or 'both'
    
    # Patient history stats
    total_appointments = Column(Integer, default=0)
    total_noshow = Column(Integer, default=0)
    total_cancelled = Column(Integer, default=0)
    noshow_rate = Column(Float, default=0.0)
    
    # Metadata
    is_new_patient = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    last_appointment = Column(DateTime, nullable=True)
    
    # Relationships
    provider = relationship("Provider", back_populates="patients")
    appointments = relationship("Appointment", back_populates="patient")

class Appointment(Base):
    """
    Appointment records and outcomes.
    """
    __tablename__ = "appointments"
    
    id = Column(Integer, primary_key=True, index=True)
    provider_id = Column(Integer, ForeignKey("providers.id"))
    patient_id = Column(Integer, ForeignKey("patients.id"))
    
    # Appointment details
    appointment_datetime = Column(DateTime, nullable=False, index=True)
    duration_minutes = Column(Integer, default=30)
    appointment_type = Column(String(100))  # cleaning, checkup, procedure, etc.
    
    # Scheduling info
    scheduled_at = Column(DateTime, default=datetime.utcnow)  # When they booked it
    days_in_advance = Column(Integer)  # Calculated: days between booking and appointment
    
    # Outcome
    status = Column(String(50), default="scheduled")  # scheduled, confirmed, completed, noshow, cancelled
    actual_status = Column(String(50), nullable=True)  # The actual outcome after appointment time
    did_noshow = Column(Boolean, nullable=True)  # True = no-show, False = showed up, None = hasn't happened yet
    
    # Reminders sent
    reminder_sent_count = Column(Integer, default=0)
    last_reminder_sent = Column(DateTime, nullable=True)
    patient_confirmed = Column(Boolean, default=False)
    confirmed_at = Column(DateTime, nullable=True)
    
    # Metadata
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    provider = relationship("Provider", back_populates="appointments")
    patient = relationship("Patient", back_populates="appointments")
    prediction = relationship("Prediction", back_populates="appointment", uselist=False)
    reminders = relationship("Reminder", back_populates="appointment")

class Prediction(Base):
    """
    ML predictions for no-show risk.
    """
    __tablename__ = "predictions"
    
    id = Column(Integer, primary_key=True, index=True)
    appointment_id = Column(Integer, ForeignKey("appointments.id"), unique=True)
    
    # Prediction results
    risk_score = Column(Float, nullable=False)  # 0-100 scale
    probability = Column(Float, nullable=False)  # 0-1 probability of no-show
    risk_level = Column(String(20), nullable=False)  # 'low', 'medium', 'high'
    
    # Model information
    model_version = Column(String(50))
    features_used = Column(Text)  # JSON string of features
    
    # Outcome tracking
    was_correct = Column(Boolean, nullable=True)  # Did prediction match reality?
    
    # Metadata
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    appointment = relationship("Appointment", back_populates="prediction")

class Reminder(Base):
    """
    Reminder messages sent to patients.
    """
    __tablename__ = "reminders"
    
    id = Column(Integer, primary_key=True, index=True)
    appointment_id = Column(Integer, ForeignKey("appointments.id"))
    
    # Reminder details
    reminder_type = Column(String(20), nullable=False)  # 'sms' or 'email'
    sent_at = Column(DateTime, nullable=False)
    scheduled_for = Column(DateTime, nullable=False)  # When it was supposed to be sent
    
    # Message content
    message_template = Column(String(100))  # Which template was used
    message_content = Column(Text)  # Actual message sent
    
    # Delivery status
    delivery_status = Column(String(50), default="pending")  # pending, sent, delivered, failed
    provider_response = Column(Text, nullable=True)  # Response from Twilio/SendGrid
    
    # Outcome
    patient_responded = Column(Boolean, default=False)
    response_content = Column(Text, nullable=True)
    
    # Metadata
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    appointment = relationship("Appointment", back_populates="reminders")

class ModelMetrics(Base):
    """
    Track ML model performance over time.
    """
    __tablename__ = "model_metrics"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # Model information
    model_version = Column(String(50), nullable=False)
    model_type = Column(String(50))  # logistic_regression, random_forest, etc.
    
    # Training info
    training_samples = Column(Integer)
    training_date = Column(DateTime, default=datetime.utcnow)
    
    # Performance metrics
    accuracy = Column(Float)
    precision = Column(Float)
    recall = Column(Float)
    f1_score = Column(Float)
    auc_roc = Column(Float)
    
    # Feature importance (JSON string)
    feature_importance = Column(Text)
    
    # Metadata
    created_at = Column(DateTime, default=datetime.utcnow)
