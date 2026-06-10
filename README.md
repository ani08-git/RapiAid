# 🚑 RapidAid

## Problem Statement

In emergency situations, people often waste valuable time searching for nearby hospitals, finding the fastest route, and estimating travel time. During critical moments, even a few minutes can make a significant difference.

## Solution

RapidAid is a real-time emergency assistance platform that helps users quickly locate nearby hospitals, identify the fastest route, estimate travel time, and make informed decisions during emergencies using live map and routing data.

---

## Features

* 📍 Convert user location into coordinates
* 🏥 Find nearby hospitals in real time
* 🛣️ Calculate distance and route information
* ⏱️ Estimate travel time (ETA)
* 🚦 Display traffic status
* 🌍 Uses live map data instead of stored datasets

---

## Project Workflow

User Location
↓
Geocoding (Geopy + Nominatim)
↓
Latitude & Longitude
↓
OpenStreetMap Overpass API
↓
Nearby Hospitals
↓
OpenRouteService API
↓
Distance & ETA
↓
Traffic Status
↓
Results Displayed to User

---

## Technologies Used

| Component       | Technology                 |
| --------------- | -------------------------- |
| Frontend        | Streamlit                  |
| Backend         | Python                     |
| Geocoding       | Geopy + Nominatim          |
| Hospital Search | OpenStreetMap Overpass API |
| Routing         | OpenRouteService API       |
| Version Control | Git & GitLab               |

---

## APIs Used

### 1. Nominatim (OpenStreetMap)

Used for converting city names and addresses into geographical coordinates.

Example:

Hyderabad → (17.3850, 78.4867)

### 2. Overpass API

Used to retrieve nearby hospitals around the user's location using real-time OpenStreetMap data.

### 3. OpenRouteService API

Used to calculate:

* Distance
* Estimated travel time (ETA)
* Route information

---

## Backend Services

### Location Service

File:

services/location.py

Function:

get_coordinates(address)

Purpose:

Converts a user-entered location into latitude and longitude coordinates.

### Hospital Search Service

File:

services/hospitals.py

Function:

get_nearby_hospitals(lat, lon)

Purpose:

Returns nearby hospitals around a given location.

### Routing Service

File:

services/routes.py

Function:

get_route(start_lat, start_lon, end_lat, end_lon)

Purpose:

Calculates travel distance and ETA.

### Traffic Status Service

Function:

traffic_status(eta)

Purpose:

Provides a simple traffic indicator based on estimated travel time.

---

## Installation

Clone the repository:

git clone <repository-url>

Navigate into the project:

cd RapidAid

Create virtual environment:

python -m venv venv

Activate virtual environment:

Windows:

venv\Scripts\activate

Install dependencies:

pip install -r requirements.txt

Run the application:

streamlit run app.py

---

## Future Enhancements

* Live ambulance tracking
* Emergency contact integration
* Hospital specialization filtering
* AI-powered emergency recommendations
* Real-time traffic analysis

---

## Team

RapidAid
Hackathon Team - 1.Pandhare Shivani
                 2.M.Anila Cyble

Built to provide faster access to emergency healthcare information using real-time location and routing services.
