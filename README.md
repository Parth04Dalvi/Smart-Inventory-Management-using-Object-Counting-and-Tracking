# Smart-Inventory-Management-using-Object-Counting-and-Tracking
Create a computer vision system that monitors and tracks inventory items in a simulated warehouse or retail setting to automate stock counts.   Technologies: Python, PyTorch/TensorFlow (for model training ), OpenCV, Flask/FastAPI (for serving the video stream and results), Graph Databases (for storing relationship data between items

🤖 Smart Inventory Management using Computer Vision

Project Overview

This project implements a scalable, real-time inventory tracking system leveraging Computer Vision (specifically Object Detection and Tracking) to automate stock auditing in a simulated warehouse or retail shelf environment. The system continuously monitors video feeds to detect stock movements, automatically updates inventory counts, and issues alerts for low stock levels.

This project demonstrates strong skills in Applied Machine Learning (YOLO/DeepSORT), FastAPI/REST API Development, Data Wrangling, and Full Stack Visualization.

🚀 Key Features

Real-Time Object Tracking: Utilizes simulated YOLOv8 for detection and a DeepSORT/ByteTrack-like algorithm for persistent object tracking across video frames.

Automated Stock Auditing: Compares tracked objects in the current frame against the previous state to accurately calculate stock changes (ADD or REMOVE).

Low Stock Alerting: Implements business logic to change an item's status to LOW or CRITICAL when stock drops below predefined minimum thresholds.

RESTful API: A high-performance FastAPI backend serves real-time inventory status and transaction history.

Responsive Dashboard: A simple, interactive HTML/JavaScript frontend that consumes the API data and displays stock levels and alerts with a robust polling mechanism (using exponential backoff).

💡 Architecture

The application is structured into three main components that typically run independently and communicate via persistent storage (simulated with JSON for simplicity):

Vision Processor (vision_processor.py): The core ML component. It simulates video ingestion, runs detection and tracking, and calculates stock differences. It then updates the shared data layer (JSON/DB).

API Backend (app_api.py): Built with FastAPI. It handles API requests, retrieves the current inventory state from the data layer, and provides JSON responses to the frontend.

Frontend Dashboard (index.html): A single-file HTML/JS/Tailwind application that constantly polls the FastAPI endpoints to present a real-time, user-friendly view of the inventory.

🛠️ Technology Stack

The project utilizes the following technologies across the stack:

Backend API: Python, FastAPI (High-performance, async REST API server).

Vision Logic: Python, Simulated YOLOv8, DeepSORT Logic (Detection, Tracking, and Stock Change Calculation).

Data Simulation: Python (JSON File) (Placeholder for a scalable database, e.g., PostgreSQL or MongoDB).

Frontend: HTML, Tailwind CSS, JavaScript (Real-time dashboard visualization and polling client).

⚙️ Setup and Running Locally

Prerequisites

You need Python 3.8+ and pip installed.

Create a Virtual Environment:

python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate



Install Dependencies:
This project requires FastAPI to run the API backend and Uvicorn as the ASGI server.

pip install fastapi uvicorn



Execution

The Vision Processor and the API server are combined for demonstration simplicity, but the logic in vision_processor.py is the core ML execution loop.

Start the FastAPI Server:
Run the application using Uvicorn. This will start the server and load the app_api.py module.

uvicorn app_api:app --reload



The server will be running at http://127.0.0.1:8000.

View the Dashboard:
Open the index.html file in your web browser. The dashboard will automatically start polling the API endpoints (/inventory/status and /inventory/transactions) every 3 seconds to display the simulated, real-time updates.

📁 File Structure

app_api.py: Contains the FastAPI server setup and the in-memory simulation of the core vision logic and database updates.

vision_processor.py: Contains the detailed, commented logic for the detection, tracking, and stock change calculation.

index.html: The full, responsive client-side dashboard with Tailwind CSS and JavaScript polling logic.

inventory_state.json: (Generated upon first run) The file used to persist the inventory state between simulated "frames."
