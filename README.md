# Indonesia EV Station Project

A terminal-based Python application that serves as a directory for Electric Vehicle (EV) Charging Stations across Indonesia. This project implements full CRUD (Create, Read, Update, Delete) functionality backed by geospatial analytics to discover, update, and generate driving routes to nearby charging stations.

---

## 🚀 Key Features

- **Full CRUD Database Management**: 
  - **Read**: Look up EV stations dynamically by City (e.g., *Kota ADM Jakarta Pusat*) or a specific Station ID.
  - **Create**: Add brand new stations into the system with automated Google S2 Geometry cell assignment.
  - **Update**: Safely update specific metadata attributes for existing stations.
  - **Delete**: Drop obsolete or inactive stations seamlessly from the in-memory workflow.
- **Advanced Geospatial Routing (Menu 5)**: 
  - **IP-Based Geolocation**: Automatically detect your location using your public IP address.
  - **Coordinate Parsing**: Search from custom coordinates (`latitude, longitude`).
  - **Point of Interest (POI) Search**: Look up any landmark using OpenStreetMap geocoding via `Geopy` and `Nominatim`.
- **Proximity Matrix & S2 Cells**: Filters and indexes spatial datasets rapidly utilizing regional Google S2 Cell IDs, calculates exact distances in kilometers, and automatically fires up a **Google Maps navigation route** directly inside your default web browser.

---

## 🛠️ Architecture & Tech Stack

- **Core Language**: Python 3
- **Data Engine**: `DuckDB` (Handles ultra-fast remote fetching of the data source via standard SQL and the `httpfs` extension).
- **Data Serialization**: Apache `Parquet` (Efficient columnar data storage format hosted securely on GitHub).
- **Geospatial Processing**: 
  - `s2cell`: Translates geographic coordinates into discrete spatial indexes for ultra-fast spatial querying.
  - `geocoder` & `geopy`: Handles IP tracking, reverse geocoding addresses via `Nominatim`, and calculating precise ellipsoidal geodesic distances between points.
- **UI Formatter**: `tabulate` (Translates structural matrix dictionaries into human-readable terminal table grids).

---

## 📁 Repository Structure

```text
indonesia_ev_station_crud_project/
│
├── data/
│   └── indonesia_ev_station.parquet  # Remote binary Parquet dataset
│
├── ev_station.py                      # Main Application Execution Script
├── requirements.txt                  # Application Dependencies
└── README.md                         # Project Documentation
