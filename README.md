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

<img width="2314" height="1568" alt="image" src="https://github.com/user-attachments/assets/45336409-ac27-42e3-9b18-6a715a9bc5e6" />




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
├── automation.py       # Handles automation rules and events API
└── meeting_rooms.py    # Handles meeting room booking API
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

- For local development: Python 3.x installed.
- For Docker: Docker Desktop installed and running.
- MongoDB instance (local or a cloud service like MongoDB Atlas).
- A modern web browser (e.g., Chrome, Firefox, Edge).

### 1. Configure the Database

No matter how you run the application, you first need to configure your database connection.

1.  In the root of the `OfficeApp` directory, create a file named `.env`.
2.  Inside the `.env` file, add your MongoDB connection string. **Do not include quotes.**
    ```env
    MONGO_URI=mongodb+srv://<username>:<password>@<cluster-address>/<database-name>?retryWrites=true&w=majority
    ```
3.  Replace the placeholders with your actual database credentials.

### 2. Running the Application

You can run the application either locally using Python or containerized with Docker.

#### Option A: Running with Docker (Recommended)

This is the easiest and most consistent way to run the application.

1.  **Build the Docker image:**
    ```sh
    docker build -t officer-app .
    ```

2.  **Run the container:**
    This command maps port 5000 and securely passes your `.env` file to the container.
    ```sh
    docker run -p 5000:5000 --env-file ./.env officer-app
    ```

##### Development with Docker
To avoid rebuilding the image on every code change, you can use a bind mount to sync your local code into the container. This allows you to see updates by simply restarting the container.

###### Using the Command Line (CLI)
1.  **Start the container with a bind mount:**
    ```sh
    # We give it a name for easy restarts
    docker run --name officer-dev -p 5000:5000 --env-file ./.env -v .:/app officer-app
    ```
2.  **Make code changes** on your local machine.
3.  **Restart the container** to apply the changes (this is much faster than rebuilding):
    ```sh
    docker restart officer-dev
    ```

###### Using the Docker Desktop GUI
1.  Go to the **Images** tab in Docker Desktop.
2.  Find your `officer-app` image and click the **Run** button.
3.  In the "Create new container" screen, click **Optional settings**.
4.  Configure the following:
    - **Container name**: Give it a memorable name, like `officer-dev-gui`.
    - **Ports**: Set the "Host port" to `5000`.
    - **Volumes**: For "Host path", browse to your project folder. For "Container path", enter `/app`.
    - **Environment variables**: Browse and select your `.env` file. Which contains the `MONGO_URI`. Copy and paste it in the Value box and the Variable should be `MONGO_URI`.
5.  Click **Run**.
6.  To apply code changes, go to the **Containers** tab and click the **Restart** button on your running container.

#### Option B: Running Locally (without Docker)

1.  **Install Dependencies**:
    ```sh
    pip install -r requirements.txt 
    ```

2.  **Run the Server**:
    ```sh
    python main.py
    ```
    This will start the server on `http://localhost:5000`.

### 3. Access and Login

Once the application is running, open your browser and navigate to **`http://localhost:5000`**.

You should see the "Officer" login screen. You can log in with one of the default accounts:
-   **Admin**: `admin1` / `adminpass1`
-   **User**: `user1` / `userpass1`
