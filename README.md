# Officer - Unified Office Management Dashboard

<p align="center">
  <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" />
  <img src="https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white" />
  <img src="https://img.shields.io/badge/MongoDB-47A248?style=for-the-badge&logo=mongodb&logoColor=white" />
  <img src="https://img.shields.io/badge/React-20232A?style=for-the-badge&logo=react&logoColor=61DAFB" />
  <img src="https://img.shields.io/badge/Tailwind_CSS-38B2AC?style=for-the-badge&logo=tailwind-css&logoColor=white" />
</p>

A cyberpunk-themed dashboard to control various office systems from a single, unified interface. This project combines multiple backend modules into one sleek frontend, demonstrating a full-stack application architecture with a futuristic aesthetic.

## 📸 Screenshot

![Uploading image.png…]()



## ✨ Features

The "Officer" dashboard integrates multiple control panels into a single, cohesive command center.

### 👤 User & Access Control
- **Secure Login & Permissions**: Role-based access control with `user` and `admin` levels.
- **User Management (Admin-Only)**:
    - Create, delete, and manage all user accounts.
    - Change user passwords.
    - Promote users to admins or demote them.

### 🌡️ Environmental Control
- **Live Status Monitoring**: View real-time office temperature, HVAC mode, and lighting status with an instantly updating status bar.
- **Manual Override**:
    - Set a target temperature.
    - Change HVAC mode (Heat, Cool, Off).
    - Toggle lights On/Off.

### 🅿️ Parking Management
- **Visual Parking Lot**: An interactive grid displays the real-time status of all parking spots (Available, Reserved, Occupied).
- **Interactive Reservations**: Click an available spot to reserve it, or un-reserve a spot you no longer need.
- **Personalized View**:
    - See your current reservations highlighted.
    - Check-in to a reserved spot.
- **Admin Override**: Administrators can manually clear any spot that is reserved or occupied.

### 🤖 Automation Hub
- **Dynamic Rule Engine**: Administrators can create complex, event-driven rules from the UI.
    - **Triggers**: `User Login`, `Parking Check-in`, `Motion Detected`.
    - **Actions**: `Turn Lights On/Off`, `Turn HVAC Off`.
- **Energy Savings**: Monitor estimated energy savings achieved through automation.

---

## 🏛️ Architecture

This project follows a monolithic backend architecture with a modular design, serving a single-page application (SPA) frontend.

-   **Backend (Flask)**: The core application is a Flask server that acts as a unified API gateway. Functionality is broken down into distinct modules using **Flask Blueprints** (`auth`, `climate`, `parking`, `automation`), promoting separation of concerns and maintainability.
-   **Frontend (React)**: The user interface is a single `index.html` file powered by React (using JSX transpiled in the browser via Babel). This creates a dynamic and responsive dashboard without requiring a separate frontend build step, making it simple to run.
-   **Database (MongoDB)**: A single MongoDB database (`office_app_db`) persists all application state, from user credentials to parking spot status and automation rules.
-   **Communication**: The frontend communicates with the backend via a RESTful API. All API endpoints are consolidated under the `/api/` prefix.

---

## 📂 Project Structure

The repository is organized to keep the frontend, backend modules, and configuration separate and easy to navigate.

```
OfficeApp/
├── .env                # Local environment variables (e.g., MONGO_URI) - (You create this)
├── README.md           # This file
├── requirements.txt    # Python backend dependencies
├── index.html          # The single-page React frontend
├── main.py             # Main Flask application entry point and initializer
├── database.py         # MongoDB connection and setup
├── auth.py             # Handles user authentication and management API
├── climate.py          # Handles environmental controls API
├── parking.py          # Handles parking management API
└── automation.py       # Handles automation rules and events API
```

## 🛠️ Tech Stack

- **Frontend:**
    - **React**: For building the dynamic user interface.
    - **Tailwind CSS**: For rapid, utility-first styling.
    - **HTML/CSS/JavaScript (ES6+)**: The core web technologies.
- **Backend:**
    - **Python**: The language for our backend services.
    - **Flask**: A lightweight micro-framework for creating the REST APIs.
    - **MongoDB**: The primary database for storing all application data.
    - **PyMongo**: Python driver for MongoDB.
    - **Werkzeug**: For secure password hashing.

---

## 🚀 Getting Started

### Prerequisites

- Python 3.x installed.
- MongoDB instance (local or a cloud service like MongoDB Atlas).
- A modern web browser (e.g., Chrome, Firefox, Edge).

### Installation & Setup

1.  **Configure the Database**:
    - In the root of the `OfficeApp` directory, create a file named `.env`.
    - Inside the `.env` file, add your MongoDB connection string like this:
      ```
      MONGO_URI="mongodb+srv://<username>:<password>@<cluster-address>/<database-name>?retryWrites=true&w=majority"
      ```
    - Replace the placeholders with your actual database credentials.
2.  **Set up the Backend**:
    - Open a terminal in the `OfficeApp` root directory.
    *   **Install Dependencies**:
        ```sh
        pip install -r requirements.txt 
        ```
    *   **Run the Server**:
        ```sh
        python main.py
        ```
    This will start the unified server on `http://127.0.0.1:5000`. On the first run, it will automatically initialize the database with default users, parking spots, and automation rules.

3.  **Launch the Frontend**:
    - Open the `index.html` file directly in your web browser.

You should now see the "Officer" login screen. You can log in with one of the default accounts (e.g., `admin1`/`adminpass1` or `user1`/`userpass1`).
