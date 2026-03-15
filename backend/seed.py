"""
Seed logic — creates 2 doctors and 5 patients for each on app startup.
"""
from db.local_db import init_db, get_user_by_email, create_user, create_patient, list_user_patients
from auth.utils import hash_password
import uuid
from datetime import datetime, timezone

DOCTORS = [
    {"name": "Dr. Gregory House", "email": "dr.house@medquery.com", "password": "password123"},
    {"name": "Dr. John Watson",   "email": "dr.watson@medquery.com", "password": "password123"},
]

PATIENTS_MAP = {
    "dr.house@medquery.com": [
        {"name": "John Doe", "age": 45, "gender": "Male", "mrn": "MRN-1001"},
        {"name": "Jane Smith", "age": 32, "gender": "Female", "mrn": "MRN-1002"},
        {"name": "William Wilson", "age": 58, "gender": "Male", "mrn": "MRN-1003"},
        {"name": "Sarah Connor", "age": 29, "gender": "Female", "mrn": "MRN-1004"},
        {"name": "Peter Parker", "age": 19, "gender": "Male", "mrn": "MRN-1005"},
    ],
    "dr.watson@medquery.com": [
        {"name": "Sherlock Holmes", "age": 38, "gender": "Male", "mrn": "MRN-2001"},
        {"name": "Irene Adler", "age": 35, "gender": "Female", "mrn": "MRN-2002"},
        {"name": "Mycroft Holmes", "age": 42, "gender": "Male", "mrn": "MRN-2003"},
        {"name": "James Moriarty", "age": 40, "gender": "Male", "mrn": "MRN-2004"},
        {"name": "Mary Morstan", "age": 30, "gender": "Female", "mrn": "MRN-2005"},
    ]
}


def seed_data():
    init_db()  # Ensure tables exist
    
    for doc in DOCTORS:
        existing_user = get_user_by_email(doc["email"])
        if not existing_user:
            uid = str(uuid.uuid4())
            user_data = {
                "uid": uid,
                "name": doc["name"],
                "email": doc["email"],
                "password_hash": hash_password(doc["password"]),
                "created_at": datetime.now(timezone.utc).isoformat(),
            }
            create_user(user_data)
            print(f"  ✅ Seeded Doctor: {doc['email']}")
        else:
            uid = existing_user["uid"]

        # Seed Patients if the doctor has none
        existing_patients = list_user_patients(uid)
        if not existing_patients:
            for p in PATIENTS_MAP[doc["email"]]:
                patient_id = str(uuid.uuid4())
                patient_data = {
                    "patient_id": patient_id,
                    "user_id": uid,
                    "name": p["name"],
                    "age": p["age"],
                    "gender": p["gender"],
                    "mrn": p.get("mrn"),
                    "notes": f"Initial seed record for {p['name']}",
                    "created_at": datetime.now(timezone.utc).isoformat(),
                }
                create_patient(patient_data)
            print(f"  ✅ Seeded 5 patients for {doc['email']}")

if __name__ == "__main__":
    print("🌱 Manually seeding database...")
    seed_data()
