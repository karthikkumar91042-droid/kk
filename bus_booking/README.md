# 🚌 BusGo – Online Bus Booking System

A full-stack online bus ticket booking system built with **Python Flask**, **MySQL**, and a premium dark-mode UI.

## Tech Stack
- Frontend: HTML5, CSS3, JavaScript
- Backend: Python 3 + Flask
- Database: MySQL (via SQLAlchemy ORM)
- Auth: Flask-Login

## Quick Start

### 1. Setup MySQL
```bash
mysql -u root -p < database.sql
```

### 2. Configure `.env`
Update your MySQL password in `.env`:
```
DATABASE_URL=mysql+pymysql://root:YOUR_PASSWORD@localhost/bus_booking_db
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Run
```bash
python app.py
```
Open http://127.0.0.1:5000

## Default Admin Login
- Email: admin@busbook.com
- Password: admin123
