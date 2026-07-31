# 🎓 Student Course Registration System - Backend

A RESTful API built with **Flask** for managing a Student Course Registration System. The API provides authentication, user management, departments, courses, and enrollments using JWT authentication.

---

## 🚀 Live API

https://student-course-registration-backend-2mbs.onrender.com

---

## 📌 Features

- User Registration
- User Login with JWT Authentication
- User Profile Management
- Department Management
- Course Management
- Student Enrollment
- Secure Password Hashing
- RESTful API
- PostgreSQL Database
- Flask Migrations

---

## 🛠 Tech Stack

- Python
- Flask
- Flask SQLAlchemy
- Flask JWT Extended
- Flask Migrate
- Flask Bcrypt
- PostgreSQL
- Gunicorn
- Render

---

## 📂 Project Structure

```
student-course-registration-backend/
│
├── app/
│   ├── models/
│   ├── routes/
│   ├── schemas/
│   ├── extensions.py
│   ├── config.py
│   └── __init__.py
│
├── migrations/
├── requirements.txt
├── run.py
├── seed.py
└── README.md
```

---

## ⚙ Installation

Clone the repository

```bash
git clone https://github.com/HexCipher224/student-course-registration-backend.git
```

Navigate into the project

```bash
cd student-course-registration-backend
```

Create a virtual environment

```bash
python -m venv venv
```

Activate the environment

### Windows

```bash
venv\Scripts\activate
```

### macOS/Linux

```bash
source venv/bin/activate
```

Install dependencies

```bash
pip install -r requirements.txt
```

---

## 🔐 Environment Variables

Create a `.env` file in the root directory.

```env
SECRET_KEY=your_secret_key

JWT_SECRET_KEY=your_jwt_secret

DATABASE_URL=your_postgresql_database_url
```

---

## 🗄 Database Migration

Initialize migrations

```bash
flask db init
```

Create migration

```bash
flask db migrate -m "Initial migration"
```

Apply migration

```bash
flask db upgrade
```

---

## ▶ Running the Server

```bash
python run.py
```

Server runs at

```
http://127.0.0.1:5000
```

---

## 🔑 Authentication Endpoints

| Method | Endpoint | Description |
|---------|----------|-------------|
| POST | /api/auth/register | Register User |
| POST | /api/auth/login | Login |
| GET | /api/auth/profile | Get Profile |
| PUT | /api/auth/profile | Update Profile |

---

## 📚 Department Endpoints

| Method | Endpoint |
|---------|----------|
| GET | /api/departments |
| POST | /api/departments |
| PUT | /api/departments/<id> |
| DELETE | /api/departments/<id> |

---

## 📖 Course Endpoints

| Method | Endpoint |
|---------|----------|
| GET | /api/courses |
| POST | /api/courses |
| PUT | /api/courses/<id> |
| DELETE | /api/courses/<id> |

---

## 🎓 Enrollment Endpoints

| Method | Endpoint |
|---------|----------|
| GET | /api/enrollments |
| POST | /api/enrollments |
| PUT | /api/enrollments/<id> |
| DELETE | /api/enrollments/<id> |

---

## 🔒 Authentication

Protected routes require a JWT token.

Example

```
Authorization: Bearer YOUR_ACCESS_TOKEN
```

---

## 🚀 Deployment

Backend deployed using **Render**

Live URL

https://student-course-registration-backend-2mbs.onrender.com

---

## 👨‍💻 Author

**Duncan Munene**

GitHub:
https://github.com/HexCipher224

---

## 📄 License

This project is licensed under the MIT License.