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

<img width="2439" height="1613" alt="image" src="https://github.com/user-attachments/assets/cb47c75a-d531-497a-a914-7098133d745a" />





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

### 🤝 Meeting Room Management
- **Visual Calendar**: A weekly calendar (Sunday-Thursday) displays all bookings with respect to the user's local timezone.
- **Color-Coded Rooms**: Each meeting room is assigned a unique color for easy identification on the calendar.
- **Flexible Booking**: Users can book any available room for a specific date, time, and duration.
- **Live Availability**: The main status bar shows a real-time count of currently available rooms.
- **Conflict Handling**: The system prevents double-booking and provides clear error messages.

###  Automation Hub
- **Dynamic Rule Engine**: Administrators can create complex, event-driven rules from the UI.
    - **Triggers**: `User Login`, `Parking Check-in`, `Motion Detected`, `Time of Day`.
    - **Actions**: `Turn Lights On/Off`, `Turn HVAC Off`.
- **Energy Savings**: Monitor estimated energy savings achieved through automation.

### ❤️ Wellness Hub
- **Daily Check-in**: Users can log their daily mood, energy, and stress levels using an interactive UI.
- **Intelligent Feedback**: The system analyzes check-ins to provide immediate, contextual advice. For high stress or low mood/energy, it discreetly suggests support resources by logging them to the browser console for privacy.
- **Office Vitals**: Monitor real-time office vitals like Air Quality (CO₂, Temperature, Humidity) and Noise Levels. The vitals auto-refresh periodically.
- **Ergonomics & Breaks**: Get on-demand ergonomic tips or set reminders to take a break.
- **Confidential Support**: A dedicated button provides discreet access to mental health support resources.

---

## 🏛️ Architecture

This project follows a monolithic backend architecture with a modular design, serving a single-page application (SPA) frontend.

-   **Backend (Flask)**: The core application is a Flask server that acts as a unified API gateway. Functionality is broken down into distinct modules using **Flask Blueprints** (`auth`, `climate`, `parking`, `automation`), promoting separation of concerns and maintainability.
-   **Frontend (React + Vite)**: The user interface is a modern Single-Page Application built with React and Vite. Vite compiles and bundles all frontend assets into highly optimized static files, which are then served by the Flask backend. This provides a fast, efficient user experience and a powerful development environment with Hot Module Replacement (HMR).
-   **Security**: Authentication is handled via JSON Web Tokens (JWT). The backend issues a signed token on login, which the frontend then includes in the `Authorization` header for all subsequent API requests. This ensures every protected endpoint verifies the user's identity and role on the server.
-   **Database (MongoDB)**: A single MongoDB database (`office_app_db`) persists all application state, from user credentials to parking spot status and automation rules.
-   **Communication**: The frontend communicates with the backend via a RESTful API. All API endpoints are consolidated under the `/api/` prefix.

---

## 📂 Project Structure

The repository is organized to keep the frontend, backend modules, and configuration separate and easy to navigate.

```
OfficeApp/ 
├── .env # Local environment variables (You create this) 
├── README.md # This file 
├── compose.yaml # Docker Compose configuration 
├── requirements.txt # Python backend dependencies 
├── main.py # Main Flask application entry point

├── backend/ # Flask backend modules
├── database.py # MongoDB connection setup 
├── auth.py # Auth module (Blueprint) 
├── climate.py # Climate module (Blueprint) 
├── parking.py # Parking module (Blueprint) 
├── automation.py # Automation module (Blueprint) 
├── meeting_rooms.py # Meeting Rooms module (Blueprint) 
├── wellness.py # Wellness module (Blueprint) 

├── frontend/ # React + Vite Single-Page Application
├── index.html # HTML entry point for Vite
├── package.json # Frontend dependencies and scripts
└── src/ # React source code (components, hooks, etc.)
```

## 🛠️ Tech Stack

- **Frontend:**
    - **React & Vite**: For a modern, fast, and scalable user interface.
    - **Tailwind CSS**: For rapid, utility-first styling.
    - **HTML/CSS/JavaScript (ES6+)**: The core web technologies.
- **Backend:**
    - **Python**: The language for our backend services.
    - **Flask**: A lightweight micro-framework for creating the REST APIs.
    - **MongoDB**: The primary database for storing all application data.
    - **PyMongo**: Python driver for MongoDB.
    - **PyJWT**: For generating and validating JSON Web Tokens.
    - **APScheduler**: For running scheduled background tasks (e.g., time-based automation).
    - **Werkzeug**: For password hashing and other web utilities.

---

## 🚀 Getting Started

### Prerequisites

- For local development: Python 3.x and Node.js (with npm) installed.
- For Docker: Docker Desktop installed and running.
- MongoDB instance (local or a cloud service like MongoDB Atlas).
- A modern web browser (e.g., Chrome, Firefox, Edge).

### 1. Configure the Database

No matter how you run the application, you first need to configure your database connection.

1.  In the root of the `OfficeApp` directory, create a file named `.env`.
2.  Inside the `.env` file, add your MongoDB connection string and a secret key for signing JWTs. **Do not include quotes.**

    You can generate a strong secret key by running this in a Python shell:
    ```python
    import secrets
    secrets.token_hex(24)
    ```

    ```env
    MONGO_URI=mongodb+srv://<username>:<password>@<cluster-address>/<database-name>?retryWrites=true&w=majority
    SECRET_KEY=your_super_secret_randomly_generated_key_here
    ```
3.  Replace the placeholders with your actual database credentials and generated secret key.

### 2. Running the Application

You can run the application either locally using Python or containerized with Docker.

#### Option A: Running with Docker for Production (Recommended)

This method builds the optimized frontend and serves it from the Python backend, simulating a production environment.

1.  **Build and run the services:**
    This single command performs a multi-stage build: it builds the frontend assets and then copies them into the final Python image.
    ```sh
    docker compose up --build
    ```
2.  To stop the services, press `Ctrl+C` and then run:
    ```sh
    docker compose down
    ```

#### Option B: Running Locally for Development

This is the recommended workflow for active development, as it provides hot-reloading for the frontend. You will run two separate processes in two separate terminals.

1.  **Terminal 1: Start the Backend Server**
    From the project root (`OfficeApp/`):
    ```sh
    # Install Python dependencies
    pip install -r requirements.txt
    # Run the Flask server
    python main.py
    ```
    The backend will be running on `http://localhost:5000`.

2.  **Terminal 2: Start the Frontend Dev Server**
    Navigate into the new `frontend` directory:
    ```sh
    cd frontend
    # Install Node.js dependencies
    npm install
    # Run the Vite dev server
    npm run dev
    ```
    The frontend dev server will start, likely on `http://localhost:5173`.

### 3. Access and Login

Once the application is running (using either Docker or the local dev setup), open your browser and navigate to the appropriate URL:
-   **Docker/Production**: `http://localhost:5000`
-   **Local Development**: `http://localhost:5173` (or whatever URL your Vite server indicates)

You should see the "Officer" login screen. You can log in with one of the default accounts:
-   **Admin**: `admin1` / `adminpass1`
-   **User**: `user1` / `userpass1`

### 🤔 Troubleshooting

- **Error: `MONGO_URI environment variable not set`**

  This is the most common startup error. It means the application container could not find the database connection string.

  1.  **Check the `.env` file name**: Ensure the file is named exactly `.env` (with the leading dot) and not `.env.txt`.
  2.  **Check the file location**: The `.env` file must be in the root of the `OfficeApp` project directory, next to `compose.yaml`.
  3.  **Check the file content**: The file must contain the `MONGO_URI` and `SECRET_KEY` variables, with no extra spaces or quotes. Copy the example from step 1 exactly.
  4.  **Restart Docker Compose**: If you made changes, stop the containers with `docker compose down` and start them again with `docker compose up --build`.
