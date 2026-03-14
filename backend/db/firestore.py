import os
import firebase_admin
from firebase_admin import credentials, firestore

_db = None


def get_db():
    global _db
    if _db is None:
        if not firebase_admin._apps:
            from config import settings
            service_account_path = settings.firebase_service_account_path
            if os.path.exists(service_account_path):
                cred = credentials.Certificate(service_account_path)
                firebase_admin.initialize_app(cred)
            else:
                # Initialize without credentials (for local dev without Firebase)
                raise RuntimeError(
                    f"Firebase service account file not found at: {service_account_path}\n"
                    "Please set FIREBASE_SERVICE_ACCOUNT_PATH in your .env file."
                )
        _db = firestore.client()
    return _db
