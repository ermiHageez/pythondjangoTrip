🧳 Trip Booking App — Django Backend

A Django-based backend system for managing trip destinations, user bookings, and account authentication. This project is designed to serve as the backend API for a travel or booking service.

🚀 Features

✅ User authentication & authorization
✅ Destination management
✅ Trip booking system
✅ Organized modular Django apps
✅ REST-ready project structure for integration with frontend (React / Mobile app)

🏗️ Tech Stack
Component	Technology
Backend Framework	Django
Database	PostgreSQL 
API Architecture	Django REST Framework (if available)
Environment	Python 3.8+
📌 Project Structure
pythondjangoTrip/
│── trip_backend/       # Main Django project
│── accounts/           # User authentication and profiles
│── bookings/           # Booking-related logic
│── destinations/       # Trip destinations data
│── api/                # REST API entry points (optional)
│── manage.py
│── requirements.txt
└── README.md

⚙️ Installation & Setup
✅ 1️⃣ Clone the repository
git clone https://github.com/ermiHageez/pythondjangoTrip.git
cd pythondjangoTrip

✅ 2️⃣ Create and activate a virtual environment
python -m venv venv
source venv/bin/activate   # Mac/Linux
venv\Scripts\activate      # Windows

✅ 3️⃣ Install dependencies
pip install -r requirements.txt

✅ 4️⃣ Apply migrations
python manage.py migrate

✅ 5️⃣ Run development server
python manage.py runserver


Server runs at:
👉 http://127.0.0.1:8000/

📡 API Endpoints (Sample)
Method	Endpoint	Description
POST	/api/auth/register/	Register user
POST	/api/auth/login/	Login user
GET	/api/destinations/	List available destinations
POST	/api/bookings/	Create a booking

📧 Contact
Developer: Ermiyas Eshetu
GitHub: https://github.com/ermiHageez

Phone: 0984502134
Location: Ethiopia 🇪🇹
