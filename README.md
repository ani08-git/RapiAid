# RapidAid

> Real-Time Emergency Hospital Locator & Route Navigation System

RapidAid is an AI-powered emergency navigation platform that helps users locate nearby hospitals, access emergency contacts, receive AI-assisted guidance, analyze traffic conditions, and navigate emergencies in their preferred language. The platform supports multilingual interaction, local AI inference through Ollama, and Bring Your Own Token (BYOT) integration for external AI providers.

---

# Problem Statement

In emergency situations, people often lose valuable time searching for nearby hospitals and determining the fastest route. Delays in reaching medical facilities can significantly impact patient outcomes.

RapidAid addresses this challenge by providing real-time hospital discovery, route estimation, traffic insights, and live map visualization in a single platform.

---

# Solution

RapidAid combines location services, mapping technologies, and routing APIs to help users:

- Find nearby hospitals instantly
- Calculate shortest travel routes
- Estimate travel time (ETA)
- View traffic conditions
- Navigate using an interactive live map

The system uses real-time geographic data instead of static datasets, ensuring accurate and up-to-date information.

---
# AI Features

RapidAid integrates Generative AI to provide emergency assistance and guidance.

### AI Emergency Assistant
Users can ask emergency-related questions and receive contextual guidance.

### Local AI with Ollama
The platform supports local model inference through Ollama, enabling privacy-focused and offline-capable AI responses.

### Bring Your Own Token (BYOT)
Users can connect their own API keys and use external AI providers without being locked into a single service.

### Language-Aware Responses
AI responses are automatically adapted based on the selected application language.
---

## Key Features

- 📍 Convert user locations into coordinates
- 🏥 Discover nearby hospitals in real time
- 🛣️ Calculate shortest routes
- ⏱️ Estimate travel time (ETA)
- 🚦 Display traffic status
- 🗺️ Interactive live map visualization
- 🚑 Emergency contact section
- 🤖 AI Emergency Assistant
- 🦙 Local AI inference using Ollama
- 🔑 Bring Your Own Token (BYOT) support
- 🌐 Multilingual Support (English, Hindi, Telugu)
- 📌 Hospital location markers
- 🌍 Real-time OpenStreetMap integration

---

# Application Screenshots

## Dashboard

![Dashboard](screenshots/Dashboard.png)

---

## Location Search

![Location](screenshots/Location.png)

---

## Nearby Hospitals

![Hospitals](screenshots/Hospitals.png)

---

## Hospital Route & Live Map

![Hospital Location](screenshots/Hospital-location.png)

---

# Project Workflow

```text
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
Traffic Analysis
      ↓
Interactive Map Display
```

---

# System Architecture

Frontend (Streamlit)
        │
        ▼
Localization Layer
(English / Hindi / Telugu)
        │
        ▼
Location Service
(Geopy + Nominatim)
        │
        ▼
Hospital Search Service
(Overpass API)
        │
        ▼
Route Calculation Service
(OpenRouteService API)
        │
        ▼
AI Assistant Layer
(Ollama / BYOT)
        │
        ▼
Traffic & ETA Analysis
        │
        ▼
Live Map Visualization
(Folium)

---

# Technologies Used

| Component | Technology |
|------------|------------|
| Frontend | Streamlit |
| Backend | Python |
| Mapping | Folium |
| Geocoding | Geopy |
| Hospital Search | OpenStreetMap Overpass API |
| Routing | OpenRouteService API |
| AI Assistant | Ollama |
| AI Integration | BYOT |
| Localization | Python i18n/l10n |
| Map Data | OpenStreetMap |
| Version Control | Git, GitHub, GitLab |

---

# APIs Used

## 1. Nominatim (OpenStreetMap)

Used to convert user-entered locations into geographic coordinates.

Example:

```text
Hyderabad → (17.3850, 78.4867)
```

---

## 2. Overpass API

Used to retrieve nearby hospitals from OpenStreetMap based on the user's location.

Features:

- Real-time hospital discovery
- Location-based search
- Open-source geographic data

---

## 3. OpenRouteService API

Used to calculate:

- Distance
- Travel Time (ETA)
- Route Information

---

# Project Structure

```text
RapidAid/
│
├── app.py
├── requirements.txt
├── README.md
│
├── screenshots/
│   ├── Dashboard.png
│   ├── Location.png
│   ├── Hospitals.png
│   └── Hospital-location.png
│
└── services/
    ├── location.py
    ├── hospitals.py
    └── routes.py
```

---

# Backend Services

## Location Service

**File:** `services/location.py`

**Function:**

```python
get_coordinates(address)
```

Purpose:

Converts user-entered locations into latitude and longitude coordinates.

---

## Hospital Search Service

**File:** `services/hospitals.py`

**Function:**

```python
get_nearby_hospitals(lat, lon)
```

Purpose:

Retrieves nearby hospitals around the user's location.

---

## Routing Service

**File:** `services/routes.py`

**Function:**

```python
get_route(start_lat, start_lon, end_lat, end_lon)
```

Purpose:

Calculates route distance and estimated travel time.

---

## 🚦 Traffic Status Service

**Function:**

```python
traffic_status(eta)
```

Purpose:

Provides a simple traffic indicator based on ETA.

---

# 🚀 Installation

### Clone Repository

```bash
git clone https://github.com/ani08-git/RapiAid.git
```

### Navigate to Project

```bash
cd RapiAid
```

### Create Virtual Environment

```bash
python -m venv venv
```

### Activate Environment

Windows:

```bash
venv\Scripts\activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Run Application

```bash
streamlit run app.py
```

---
# Accessibility & Localization

RapidAid is designed to improve accessibility during emergencies.

Features include:

- English language support
- Hindi language support
- Telugu language support
- Dynamic language switching
- Language-aware AI responses
- User-friendly emergency workflows

# Offline-First Design

RapidAid supports local AI inference through Ollama, allowing emergency guidance even when cloud AI services are unavailable.

Benefits:

- Reduced internet dependency
- Improved privacy
- Faster local inference
- Better reliability during emergencies

# Future Enhancements

- 🌍 Additional Indian language support
- 🗣️ Voice-based emergency assistance
- 📡 Offline map caching
- 🤖 Advanced multimodal AI assistant
- 📞 Voice calling emergency services

---

# 👥 Team

### RapidAid Hackathon Team

**Pandhare Shivani**

**M. Anila Cyble**

---

# Conclusion

RapidAid helps users make faster and smarter decisions during emergencies by combining real-time hospital discovery, route navigation, ETA estimation, and live mapping into a single easy-to-use platform.

**Built for saving time when every second matters. 🚑**
