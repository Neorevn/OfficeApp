# Officer - Unified Office Management Dashboard

<p align="center">
  <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" />
  <img src="https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white" />
  <img src="https://img.shields.io/badge/React-20232A?style=for-the-badge&logo=react&logoColor=61DAFB" />
  <img src="https://img.shields.io/badge/Tailwind_CSS-38B2AC?style=for-the-badge&logo=tailwind-css&logoColor=white" />
</p>

A cyberpunk-themed dashboard to control various office systems from a single, unified interface. This project combines multiple backend microservices into one sleek frontend, demonstrating a full-stack application architecture with a futuristic aesthetic.

## 📸 Screenshot

*(A placeholder for a future screenshot of the dashboard)*

<img width="2415" height="1566" alt="image" src="https://github.com/user-attachments/assets/789ca0ab-fa71-4a80-8387-ca89882c844c" />


## ✨ Features

The "Officer" dashboard currently integrates two main control panels, displayed side-by-side for a complete command center experience.

### 🌡️ Environmental Control
- **Live Status Monitoring**: View real-time office temperature, HVAC mode, and lighting status.
- **Manual Override**:
    - Set a target temperature.
    - Change HVAC mode (Heat, Cool, Off).
    - Toggle lights On/Off.
- **Cyberpunk UI**: Glowing, pulsing interface elements for a futuristic feel.

### 🅿️ Parking Management
- **Visual Parking Lot**: An interactive grid displays the real-time status of all parking spots (Available, Reserved, Occupied).
- **Interactive Reservations**: Click on an available spot to select it for reservation.
- **Personalized View**:
    - See your current reservations highlighted.
    - Check-in to a reserved spot.
- **User-friendly**: Hover over spots for more details and enjoy a seamless reservation process.

---

## 🛠️ Tech Stack

- **Frontend**:
    - **React**: For building the dynamic user interface.
    - **Tailwind CSS**: For rapid, utility-first styling.
    - **HTML/CSS/JavaScript (ES6+)**: The core web technologies.
- **Backend**:
    - **Python**: The language for our backend services.
    - **Flask**: A lightweight micro-framework for creating the REST APIs.
    - **Flask-CORS**: To handle Cross-Origin Resource Sharing between the frontend and backends.

---

## 🚀 Getting Started

Follow these instructions to get the Officer dashboard up and running on your local machine.

### Prerequisites

- Python 3.x installed.
- A modern web browser (e.g., Chrome, Firefox, Edge).

### Installation & Setup

1.  **Set up the Backend Services**:
    You need to run two separate backend servers. Open two terminal windows for this.

    *   **Terminal 1: Environmental Control**
        ```sh
        cd Climate
        pip install Flask Flask-Cors
        python main.py
        ```
        This server will run on `http://127.0.0.1:5000`.

    *   **Terminal 2: Parking Management**
        ```sh
        cd Parking
        pip install Flask Flask-Cors
        python main.py
        ```
        This server will run on `http://127.0.0.1:5001`.

2.  **Launch the Frontend**:
    -   Navigate to the root `OfficeApp` directory.
    -   Open the `index.html` file directly in your web browser.

You should now see the "Officer" dashboard, and both panels should load their respective data from the running services.
