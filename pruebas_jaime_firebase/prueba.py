import pyrebase

config = {
    "apiKey": "AIzaSyBV6mvRXNxEFQSN9yM9ANcWPHkKG3QAR10",
    "authDomain": "prueba01-2a133.firebaseapp.com",
    "projectId": "prueba01-2a133",
    "databaseURL": "https://prueba01-2a133-default-rtdb.europe-west1.firebasedatabase.app/",
    "storageBucket": "prueba01-2a133.firebasestorage.app",
    "messagingSenderId": "853595247603",
    "appId": "1:853595247603:web:ec104003b6186badc03886"
}

firebase = pyrebase.initialize_app(config)
auth = firebase.auth()

user = auth.create_user_with_email_and_password("test@test.com", "password123")
print("Usuario creado:", user['email'])
