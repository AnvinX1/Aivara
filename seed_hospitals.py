"""
Seed script to populate database with major Indian hospitals and sample doctors.
Run this script to add initial data for testing the doctor-hospital workflow.
"""

import os
import sys

# Add project root to path
_current_dir = os.path.dirname(os.path.abspath(__file__))
_project_root = _current_dir
if _project_root not in sys.path:
    sys.path.insert(0, _project_root)

from db.database import SessionLocal, create_db_tables
from models.hospital import Hospital
from models.doctor import Doctor
from dependencies import get_password_hash

def seed_hospitals_and_doctors():
    """Seed database with hospitals and doctors from major Indian cities."""
    
    # Create tables first
    create_db_tables()
    
    db = SessionLocal()
    
    try:
        # Check if hospitals already exist
        existing_hospitals = db.query(Hospital).count()
        if existing_hospitals > 0:
            print(f"Found {existing_hospitals} existing hospitals. Skipping seed.")
            return
        
        # Hospitals data - Major Indian cities
        hospitals_data = [
            # Mumbai
            {
                "name": "Tata Memorial Hospital",
                "address": "Dr. E Borges Marg, Parel",
                "city": "Mumbai",
                "state": "Maharashtra",
                "pincode": "400012",
                "phone": "+91-22-24177000",
                "email": "contact@tmc.gov.in",
                "doctors": [
                    {"full_name": "Dr. Rajesh Kumar", "email": "rajesh.kumar@tmc.gov.in", "specialization": "Oncology", "phone": "+91-9876543210", "registration_number": "MCI-12345"},
                    {"full_name": "Dr. Priya Sharma", "email": "priya.sharma@tmc.gov.in", "specialization": "Pathology", "phone": "+91-9876543211", "registration_number": "MCI-12346"},
                ]
            },
            {
                "name": "Apollo Hospital Mumbai",
                "address": "Bandra Kurla Complex, Bandra East",
                "city": "Mumbai",
                "state": "Maharashtra",
                "pincode": "400051",
                "phone": "+91-22-62826282",
                "email": "mumbai@apollohospitals.com",
                "doctors": [
                    {"full_name": "Dr. Amit Patel", "email": "amit.patel@apollo.in", "specialization": "Cardiology", "phone": "+91-9876543212", "registration_number": "MCI-12347"},
                    {"full_name": "Dr. Sneha Desai", "email": "sneha.desai@apollo.in", "specialization": "General Medicine", "phone": "+91-9876543213", "registration_number": "MCI-12348"},
                ]
            },
            {
                "name": "Kokilaben Dhirubhai Ambani Hospital",
                "address": "Rao Saheb Achutrao Patwardhan Marg, Andheri West",
                "city": "Mumbai",
                "state": "Maharashtra",
                "pincode": "400053",
                "phone": "+91-22-30999999",
                "email": "info@kokilabenhospital.com",
                "doctors": [
                    {"full_name": "Dr. Vikram Singh", "email": "vikram.singh@kokilaben.in", "specialization": "Nephrology", "phone": "+91-9876543214", "registration_number": "MCI-12349"},
                ]
            },
            
            # Delhi
            {
                "name": "All India Institute of Medical Sciences (AIIMS)",
                "address": "Ansari Nagar, New Delhi",
                "city": "Delhi",
                "state": "Delhi",
                "pincode": "110029",
                "phone": "+91-11-26588500",
                "email": "info@aiims.edu",
                "doctors": [
                    {"full_name": "Dr. Anil Gupta", "email": "anil.gupta@aiims.edu", "specialization": "General Medicine", "phone": "+91-9876543215", "registration_number": "MCI-12350"},
                    {"full_name": "Dr. Meera Joshi", "email": "meera.joshi@aiims.edu", "specialization": "Hematology", "phone": "+91-9876543216", "registration_number": "MCI-12351"},
                ]
            },
            {
                "name": "Sir Ganga Ram Hospital",
                "address": "Rajinder Nagar, New Delhi",
                "city": "Delhi",
                "state": "Delhi",
                "pincode": "110060",
                "phone": "+91-11-25750000",
                "email": "info@sgrh.com",
                "doctors": [
                    {"full_name": "Dr. Rohit Malhotra", "email": "rohit.malhotra@sgrh.com", "specialization": "Internal Medicine", "phone": "+91-9876543217", "registration_number": "MCI-12352"},
                ]
            },
            {
                "name": "Apollo Hospital Delhi",
                "address": "Sarita Vihar, New Delhi",
                "city": "Delhi",
                "state": "Delhi",
                "pincode": "110076",
                "phone": "+91-11-71791090",
                "email": "delhi@apollohospitals.com",
                "doctors": [
                    {"full_name": "Dr. Kavita Reddy", "email": "kavita.reddy@apollo.in", "specialization": "Endocrinology", "phone": "+91-9876543218", "registration_number": "MCI-12353"},
                ]
            },
            
            # Bangalore
            {
                "name": "Narayana Health City",
                "address": "Bommasandra Industrial Area, Hosur Road",
                "city": "Bangalore",
                "state": "Karnataka",
                "pincode": "560099",
                "phone": "+91-80-27835000",
                "email": "info@narayanahealth.org",
                "doctors": [
                    {"full_name": "Dr. Suresh Rao", "email": "suresh.rao@narayanahealth.org", "specialization": "Cardiology", "phone": "+91-9876543219", "registration_number": "KMC-12354"},
                    {"full_name": "Dr. Ananya Iyer", "email": "ananya.iyer@narayanahealth.org", "specialization": "General Medicine", "phone": "+91-9876543220", "registration_number": "KMC-12355"},
                ]
            },
            {
                "name": "Manipal Hospital",
                "address": "98, HAL Old Airport Road, Kodihalli",
                "city": "Bangalore",
                "state": "Karnataka",
                "pincode": "560017",
                "phone": "+91-80-25024444",
                "email": "info@manipalhospitals.com",
                "doctors": [
                    {"full_name": "Dr. Pradeep Kumar", "email": "pradeep.kumar@manipal.com", "specialization": "Oncology", "phone": "+91-9876543221", "registration_number": "KMC-12356"},
                ]
            },
            
            # Chennai
            {
                "name": "Apollo Hospital Chennai",
                "address": "21 Greams Lane, Off Greams Road",
                "city": "Chennai",
                "state": "Tamil Nadu",
                "pincode": "600006",
                "phone": "+91-44-28290200",
                "email": "chennai@apollohospitals.com",
                "doctors": [
                    {"full_name": "Dr. Ramesh Venkatesan", "email": "ramesh.venkatesan@apollo.in", "specialization": "General Medicine", "phone": "+91-9876543222", "registration_number": "TMC-12357"},
                    {"full_name": "Dr. Lakshmi Nair", "email": "lakshmi.nair@apollo.in", "specialization": "Hematology", "phone": "+91-9876543223", "registration_number": "TMC-12358"},
                ]
            },
            
            # Hyderabad
            {
                "name": "Apollo Hospital Hyderabad",
                "address": "Jubilee Hills, Road No. 72",
                "city": "Hyderabad",
                "state": "Telangana",
                "pincode": "500033",
                "phone": "+91-40-23607777",
                "email": "hyderabad@apollohospitals.com",
                "doctors": [
                    {"full_name": "Dr. Srinivas Reddy", "email": "srinivas.reddy@apollo.in", "specialization": "Internal Medicine", "phone": "+91-9876543224", "registration_number": "TMC-12359"},
                ]
            },
            {
                "name": "Yashoda Hospitals",
                "address": "Rajbhavan Road, Somajiguda",
                "city": "Hyderabad",
                "state": "Telangana",
                "pincode": "500082",
                "phone": "+91-40-24555555",
                "email": "info@yashodahospitals.com",
                "doctors": [
                    {"full_name": "Dr. Madhavi Rao", "email": "madhavi.rao@yashoda.com", "specialization": "General Medicine", "phone": "+91-9876543225", "registration_number": "TMC-12360"},
                ]
            },
            
            # Kolkata
            {
                "name": "Apollo Gleneagles Hospitals",
                "address": "58, Canal Circular Road",
                "city": "Kolkata",
                "state": "West Bengal",
                "pincode": "700054",
                "phone": "+91-33-23203030",
                "email": "kolkata@apollohospitals.com",
                "doctors": [
                    {"full_name": "Dr. Subhash Mukherjee", "email": "subhash.mukherjee@apollo.in", "specialization": "General Medicine", "phone": "+91-9876543226", "registration_number": "WMC-12361"},
                ]
            },
            
            # Coimbatore - KMCH
            {
                "name": "KMCH - Kovai Medical Center and Hospital",
                "address": "Avinashi Road, Coimbatore",
                "city": "Coimbatore",
                "state": "Tamil Nadu",
                "pincode": "641014",
                "phone": "+91-422-4323800",
                "email": "info@kmchhospitals.com",
                "doctors": [
                    {"full_name": "Dr. Ravi Kumar", "email": "ravi.kumar@kmchhospitals.com", "specialization": "Cardiology", "phone": "+91-9876543227", "registration_number": "TMC-12362"},
                    {"full_name": "Dr. Deepa Nair", "email": "deepa.nair@kmchhospitals.com", "specialization": "General Medicine", "phone": "+91-9876543228", "registration_number": "TMC-12363"},
                    {"full_name": "Dr. Senthil Kumar", "email": "senthil.kumar@kmchhospitals.com", "specialization": "Orthopedics", "phone": "+91-9876543229", "registration_number": "TMC-12364"},
                ]
            },
        ]
        
        # Create hospitals and doctors
        for hospital_data in hospitals_data:
            doctors_list = hospital_data.pop("doctors", [])
            
            hospital = Hospital(**hospital_data)
            db.add(hospital)
            db.flush()  # Get hospital ID
            
            # Create doctors for this hospital
            for doctor_data in doctors_list:
                # Generate a default password (in production, doctors should set their own)
                default_password = "Doctor@123"  # Should be changed on first login
                hashed_password = get_password_hash(default_password)
                
                doctor = Doctor(
                    email=doctor_data["email"],
                    hashed_password=hashed_password,
                    full_name=doctor_data["full_name"],
                    specialization=doctor_data["specialization"],
                    hospital_id=hospital.id,
                    phone=doctor_data.get("phone"),
                    registration_number=doctor_data.get("registration_number"),
                    is_active=True
                )
                db.add(doctor)
        
        db.commit()
        print(f"Successfully seeded {len(hospitals_data)} hospitals with doctors!")
        print("Default doctor password: Doctor@123 (should be changed on first login)")
        
    except Exception as e:
        db.rollback()
        print(f"Error seeding database: {e}")
        raise
    finally:
        db.close()

if __name__ == "__main__":
    seed_hospitals_and_doctors()

