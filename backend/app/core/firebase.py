import firebase_admin
from firebase_admin import credentials, auth
import json
from app.core.config import settings

firebase_app = None


def init_firebase():
    global firebase_app
    
    try:
        firebase_credentials = {
            "type": "service_account",
            "project_id": settings.FIREBASE_PROJECT_ID,
            "private_key_id": settings.FIREBASE_PRIVATE_KEY_ID,
            "private_key": settings.FIREBASE_PRIVATE_KEY.replace('\\n', '\n'),
            "client_email": settings.FIREBASE_CLIENT_EMAIL,
            "client_id": settings.FIREBASE_CLIENT_ID,
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "token_uri": "https://oauth2.googleapis.com/token",
        }
        
        cred = credentials.Certificate(firebase_credentials)
        firebase_app = firebase_admin.initialize_app(cred)
        print("Firebase initialized successfully")
    except Exception as e:
        print(f"Error initializing Firebase: {e}")


def get_firebase_app():
    if firebase_app is None:
        init_firebase()
    return firebase_app


def create_firebase_user(email: str, password: str, display_name: str = None):
    try:
        user = auth.create_user(
            email=email,
            password=password,
            display_name=display_name,
            email_verified=False
        )
        return user.uid
    except firebase_admin.auth.EmailAlreadyExistsError:
        raise ValueError(f"Email {email} already registered")
    except Exception as e:
        raise ValueError(f"Error creating Firebase user: {str(e)}")


def verify_firebase_token(id_token: str):
    try:
        decoded_token = auth.verify_id_token(id_token)
        return decoded_token
    except Exception as e:
        return None


def get_firebase_user_by_email(email: str):
    try:
        user = auth.get_user_by_email(email)
        return user
    except firebase_admin.auth.UserNotFoundError:
        return None
    except Exception as e:
        return None


def send_password_reset_email(email: str):
    try:
        reset_link = auth.generate_password_reset_link(email)
        return reset_link
    except Exception as e:
        raise ValueError(f"Error generating password reset link: {str(e)}")


def send_email_verification(uid: str):
    try:
        verification_link = auth.generate_email_verification_link(uid)
        return verification_link
    except Exception as e:
        raise ValueError(f"Error generating email verification link: {str(e)}")
