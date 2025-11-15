
"""
Notification service for doctor and patient notifications.
Currently uses database flags. In the future, this can be extended with email/SMS.
"""

import os
import sys
from datetime import datetime
from typing import Optional

_current_dir = os.path.dirname(os.path.abspath(__file__))
_project_root = os.path.dirname(_current_dir)
if _project_root not in sys.path:
    sys.path.insert(0, _project_root)

from db.database import SessionLocal

def notify_doctor_new_report(report_id: int, doctor_id: int):
    """
    Notify a doctor that a new report has been shared with them.
    Currently: Just logs the notification. In future: Send email/SMS.
    
    Args:
        report_id: ID of the report shared
        doctor_id: ID of the doctor to notify
    """
    try:
        print(f"📧 Notification: Doctor {doctor_id} has received a new report {report_id} for review")
        # TODO: Implement email/SMS notification
        # Example future implementation:
        # send_email(doctor.email, f"New report #{report_id} requires your review")
        # send_sms(doctor.phone, f"New report #{report_id} shared with you")
    except Exception as e:
        print(f"Error sending notification to doctor: {e}")

def notify_patient_doctor_review(report_id: int, patient_id: int):
    """
    Notify a patient that a doctor has reviewed their report.
    Currently: Just logs the notification. In future: Send email/SMS.
    
    Args:
        report_id: ID of the reviewed report
        patient_id: ID of the patient to notify
    """
    try:
        print(f"📧 Notification: Patient {patient_id} has received a doctor review for report {report_id}")
        # TODO: Implement email/SMS notification
        # Example future implementation:
        # send_email(patient.email, f"Doctor has reviewed your report #{report_id}")
        # send_sms(patient.phone, f"Your report #{report_id} has been reviewed")
    except Exception as e:
        print(f"Error sending notification to patient: {e}")

def notify_forecast_generated(report_id: int, patient_id: int):
    """
    Notify a patient that a health forecast has been generated for their report.
    
    Args:
        report_id: ID of the report
        patient_id: ID of the patient
    """
    try:
        print(f"📧 Notification: Health forecast generated for patient {patient_id}, report {report_id}")
        # TODO: Implement email/SMS notification
    except Exception as e:
        print(f"Error sending forecast notification: {e}")

