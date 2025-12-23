# 🌡️ Cold Chain Tracking & Monitoring System

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue)](https://www.python.org/)
[![Gradio](https://img.shields.io/badge/Gradio-4.0%2B-orange)](https://gradio.app/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Status](https://img.shields.io/badge/Status-Active-success)](https://github.com)

> A comprehensive real-time pharmaceutical cold chain tracking system with IoT monitoring, advanced analytics, and intelligent alert management.

![Cold Chain Dashboard](https://github.com/abhishekmohan01/HealSphere_AI-Intelligent-End-to-End-Healthcare_Prediction_Suite/blob/main/Apps/Cold_Chain-And_Supply-Chain_Logistics_Support/Screenshot%202025-12-23%20093923.png)

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Installation](#installation)
- [Usage](#usage)
- [System Architecture](#system-architecture)
- [Screenshots](#screenshots)
- [Data Model](#data-model)
- [API Reference](#api-reference)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)

## 🎯 Overview

The **Cold Chain Tracking & Monitoring System** is an enterprise-grade solution designed to track and monitor pharmaceutical shipments across India's logistics network. It provides real-time IoT sensor data, predictive analytics, and automated alerts to ensure medicine quality and compliance with cold chain regulations.

### Key Highlights

- 🚚 **500+ Active Shipments** - Real-time tracking across 10 major routes
- 🌡️ **IoT Monitoring** - Temperature, humidity, and vibration sensors
- 📊 **9+ Visualizations** - Interactive Plotly charts and dashboards
- ⚠️ **Smart Alerts** - Automated risk detection and notifications
- 📈 **Predictive Analytics** - Risk scoring and ETA predictions
- 🗺️ **Pan-India Coverage** - Major cities and distribution hubs

## ✨ Features

### 1. Dashboard Overview
- **Real-time KPIs** - Total shipments, active alerts, in-transit count, average temperature
- **Status Distribution** - Pie chart showing delivery status breakdown
- **Alert Types Analysis** - Bar chart categorizing temperature, humidity, distance alerts
- **Transport Mode Usage** - Distribution across reefer trucks, air cargo, rail, etc.
- **Temperature Distribution** - Histogram showing temperature compliance
- **Route Traffic Analysis** - Top 10 busiest routes
- **Cost Analysis** - Transport cost breakdown by mode
- **Medicine Categories** - Distribution of pharmaceutical categories

### 2. Search & Track
- **Multi-field Search** - Search by medicine name, brand, shipment ID, route ID
- **Advanced Filtering**
  - Status filter (In Transit, Delivered, Delayed, At Hub)
  - Alert filter (Alert Only, No Alerts)
  - Transport mode filter
- **Dynamic Results Table** - Sortable, real-time results
- **Search Statistics** - Total found, alerts count, in-transit count

### 3. Shipment Details
- **Complete Shipment Profile**
  - Route information (origin → destination)
  - Medicine details (name, brand, category)
  - Transport mode and speed
  - Progress tracking (distance completed, remaining, ETA)
- **Cold Chain Monitoring**
  - Target temperature range
  - Current temperature and humidity
  - Alert status breakdown
- **Historical Sensor Data**
  - Temperature history with target range overlay
  - Humidity trends
  - Vibration index monitoring
  - Alert timeline visualization
- **Risk Analysis Dashboard**
  - Temperature risk score
  - Distance risk assessment
  - ETA risk calculation
  - Overall risk rating (0-100 scale)

### 4. Advanced Analytics
- **Shipment Heatmap** - Route vs Status correlation matrix
- **Cost vs Distance Analysis** - Scatter plot with alert indicators
- **Temperature Compliance** - Box plots by medicine category
- **Real-time Status Map** - Progress percentage by status

### 5. Export & Reports
- **Multiple Formats** - CSV, Excel, JSON
- **Custom Filters** - All shipments, alerts only, in-transit only
- **Automated Reports** - Timestamped file generation
- **One-click Download** - Instant file export

## 🛠️ Tech Stack

### Core Technologies
- **Python 3.8+** - Backend logic and data processing
- **Gradio 4.0+** - Web interface and UI components
- **Plotly** - Interactive visualizations
- **Pandas** - Data manipulation and analysis
- **NumPy** - Numerical computations

### Key Libraries
```python
gradio==4.0.0+
plotly==5.17.0+
pandas==2.0.0+
numpy==1.24.0+
openpyxl==3.1.0+  # For Excel export
```

## 📦 Installation

### Prerequisites
- Python 3.8 or higher
- pip package manager
- 2GB RAM minimum
- Internet connection for Gradio sharing

### Step 1: Clone Repository
```bash
git clone https://github.com/yourusername/cold-chain-tracking.git
cd cold-chain-tracking
```

### Step 2: Create Virtual Environment (Optional)
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

**requirements.txt:**
```
gradio>=4.0.0
plotly>=5.17.0
pandas>=2.0.0
numpy>=1.24.0
openpyxl>=3.1.0
```

### Step 4: Run Application
```bash
python app.py
```

The application will launch and provide:
- **Local URL:** `http://127.0.0.1:7860`
- **Public URL:** `https://xxxxxxxx.gradio.live` (shareable link)

## 🚀 Usage

### Quick Start

1. **Launch Application**
   ```bash
   python app.py
   ```

2. **Access Dashboard**
   - Open the local URL in your browser
   - Or share the public Gradio link with team members

3. **Explore Tabs**
   - Start with **Dashboard Overview** for system status
   - Use **Search & Track** to find specific shipments
   - Click **Shipment Details** to deep-dive into individual shipments
   - Review **Analytics** for insights
   - **Export** data for external analysis

### Sample Shipment IDs
Try these shipment IDs in the details viewer:
- `SHP100123`
- `SHP100456`
- `SHP100789`
- `SHP101000`

### Example Workflows

#### Workflow 1: Monitor Critical Alerts
1. Go to **Dashboard Overview**
2. Check "Active Alerts" KPI
3. Navigate to **Search & Track**
4. Set Alert Filter to "Alert Only"
5. Review flagged shipments
6. Click shipment ID for details

#### Workflow 2: Track Specific Medicine
1. Open **Search & Track** tab
2. Enter medicine name (e.g., "Paracetamol")
3. Apply filters as needed
4. View search results
5. Export filtered data

#### Workflow 3: Analyze Route Performance
1. Access **Analytics** tab
2. Review shipment heatmap by route
3. Identify bottleneck routes
4. Check cost vs distance analysis
5. Generate report

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────┐
│                  Gradio Web Interface               │
├─────────────────────────────────────────────────────┤
│  Dashboard  │  Search  │  Details  │  Analytics     │
└─────────────────────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────┐
│              Data Processing Layer                  │
├─────────────────────────────────────────────────────┤
│  • Shipment Generator                               │
│  • Search Engine                                    │
│  • Risk Calculator                                  │
│  • Historical Data Simulator                        │
└─────────────────────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────┐
│              Visualization Engine                   │
├─────────────────────────────────────────────────────┤
│  Plotly Charts │ Pandas DataFrames │ Markdown       │
└─────────────────────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────┐
│                  Data Layer                         │
├─────────────────────────────────────────────────────┤
│  • Medicine Database                                │
│  • Shipment Records                                 │
│  • Route Network                                    │
│  • Transport Modes                                  │
│  • Cold Chain Profiles                              │
└─────────────────────────────────────────────────────┘
```

## 📸 Screenshots

### Dashboard Overview
![Dashboard](https://github.com/abhishekmohan01/HealSphere_AI-Intelligent-End-to-End-Healthcare_Prediction_Suite/blob/main/Apps/Cold_Chain-And_Supply-Chain_Logistics_Support/Screenshot%202025-12-23%20093923.png)

### Search & Track
![Search](https://github.com/abhishekmohan01/HealSphere_AI-Intelligent-End-to-End-Healthcare_Prediction_Suite/blob/main/Apps/Cold_Chain-And_Supply-Chain_Logistics_Support/Screenshot%202025-12-23%20093953.png)

### Shipment Details
![Details](https://github.com/abhishekmohan01/HealSphere_AI-Intelligent-End-to-End-Healthcare_Prediction_Suite/blob/main/Apps/Cold_Chain-And_Supply-Chain_Logistics_Support/Screenshot%202025-12-23%20094021.png)

### Analytics Dashboard
![Analytics](https://via.placeholder.com/1000x600/8e44ad/ffffff?text=Advanced+Analytics+%7C+Heatmaps+%26+Insights)

## 📊 Data Model

### Shipment Schema
```python
{
    'shipment_id': 'SHP100123',              # Unique identifier
    'route_id': 'R001',                       # Route reference
    'route_from': 'Mumbai',                   # Origin city
    'route_to': 'Delhi',                      # Destination city
    'transport_mode': 'Reefer Truck',         # Transport type
    'status': 'In Transit',                   # Current status
    'medicine_id': 1,                         # Medicine reference
    'medicine_name': 'Paracetamol 500mg',     # Medicine name
    'brand': 'Crocin',                        # Brand name
    'manufacturer': 'GSK',                    # Manufacturer
    'category': 'Analgesic/Antipyretic',     # Medicine category
    'total_distance_km': 1419,                # Total route distance
    'distance_completed_km': 850.5,           # Distance covered
    'distance_remaining_km': 568.5,           # Distance remaining
    'progress_pct': 59.9,                     # Completion percentage
    'elapsed_hours': 18.5,                    # Time elapsed
    'eta_hours_remaining': 8.7,               # Estimated time remaining
    'current_temperature_c': 22.3,            # Current temperature
    'temp_min_target_c': 15.0,                # Min target temp
    'temp_max_target_c': 25.0,                # Max target temp
    'current_humidity_pct': 52.1,             # Current humidity
    'temperature_alert': 0,                   # Alert flag (0/1)
    'humidity_alert': 0,                      # Alert flag (0/1)
    'long_distance_alert': 1,                 # Alert flag (0/1)
    'long_eta_alert': 0,                      # Alert flag (0/1)
    'delayed_alert': 0,                       # Alert flag (0/1)
    'overall_alert': 1,                       # Any alert active
    'transport_cost_inr': 2126.25,            # Cost in INR
    'speed_kmph': 52.3                        # Current speed
}
```

### Medicine Categories
- **Analgesic/Antipyretic** - Pain relievers (15-25°C)
- **NSAID** - Anti-inflammatory drugs (15-25°C)
- **Antibiotic** - Bacterial infection treatment (15-25°C)
- **Antidiabetic** - Diabetes medication (2-8°C - refrigerated)
- **Antihistamine** - Allergy medication (15-25°C)
- **First Aid** - Emergency supplies (10-30°C)
- **General Medicine** - Other pharmaceuticals (15-25°C)

### Routes Network
```python
{
    'R001': {'from': 'Mumbai', 'to': 'Delhi', 'distance': 1419, 'hubs': 3},
    'R002': {'from': 'Hyderabad', 'to': 'Bangalore', 'distance': 562, 'hubs': 2},
    'R003': {'from': 'Ahmedabad', 'to': 'Chennai', 'distance': 1547, 'hubs': 4},
    'R004': {'from': 'Pune', 'to': 'Kolkata', 'distance': 1930, 'hubs': 5},
    'R005': {'from': 'Jaipur', 'to': 'Mumbai', 'distance': 1120, 'hubs': 3},
    'R006': {'from': 'Lucknow', 'to': 'Hyderabad', 'distance': 1295, 'hubs': 4},
    'R007': {'from': 'Chandigarh', 'to': 'Bengaluru', 'distance': 2400, 'hubs': 6},
    'R008': {'from': 'Indore', 'to': 'Visakhapatnam', 'distance': 1185, 'hubs': 3},
    'R009': {'from': 'Nagpur', 'to': 'Coimbatore', 'distance': 1342, 'hubs': 4},
    'R010': {'from': 'Bhopal', 'to': 'Thiruvananthapuram', 'distance': 1987, 'hubs': 5}
}
```

### Transport Modes
- **Reefer Truck** - Refrigerated trucks (40-65 km/h, ₹2.5/km)
- **Air Cargo** - Fast air transport (500-900 km/h, ₹15/km)
- **Rail** - Train transport (60-120 km/h, ₹1.8/km)
- **Sea Container** - Ocean shipping (20-35 km/h, ₹0.8/km)
- **Insulated Van** - Temperature-controlled vans (35-55 km/h, ₹3.2/km)
- **Courier** - Express delivery (30-50 km/h, ₹5/km)

## 🔧 API Reference

### Core Functions

#### `generate_shipments(n_shipments=500)`
Generate synthetic shipment data with realistic parameters.

**Parameters:**
- `n_shipments` (int): Number of shipments to generate (default: 500)

**Returns:**
- `pd.DataFrame`: Shipment data

#### `search_shipments(query, status_filter, alert_filter, mode_filter)`
Search and filter shipments based on criteria.

**Parameters:**
- `query` (str): Search query
- `status_filter` (str): Status filter value
- `alert_filter` (str): Alert filter value
- `mode_filter` (str): Transport mode filter

**Returns:**
- `tuple`: (summary_markdown, filtered_dataframe)

#### `get_shipment_details(shipment_id)`
Retrieve detailed information for a specific shipment.

**Parameters:**
- `shipment_id` (str): Shipment ID (e.g., "SHP100123")

**Returns:**
- `tuple`: (details_markdown, history_plot, risk_plot)

#### `create_overview_dashboard()`
Generate main dashboard with all visualizations.

**Returns:**
- `plotly.graph_objects.Figure`: Dashboard figure

#### `create_analytics_dashboard()`
Generate advanced analytics dashboard.

**Returns:**
- `plotly.graph_objects.Figure`: Analytics figure

#### `export_report(format_type, filter_type)`
Export data to file in specified format.

**Parameters:**
- `format_type` (str): "CSV", "Excel", or "JSON"
- `filter_type` (str): Export filter criteria

**Returns:**
- `tuple`: (status_message, file_path)

## 🤝 Contributing

We welcome contributions! Please follow these steps:

1. **Fork the Repository**
   ```bash
   git fork https://github.com/yourusername/cold-chain-tracking.git
   ```

2. **Create Feature Branch**
   ```bash
   git checkout -b feature/amazing-feature
   ```

3. **Commit Changes**
   ```bash
   git commit -m "Add amazing feature"
   ```

4. **Push to Branch**
   ```bash
   git push origin feature/amazing-feature
   ```

5. **Open Pull Request**

### Development Guidelines

- The Data with which this model is trained is synthetic [Created Randomly]
- Follow PEP 8 style guide
- Add docstrings to all functions
- Include unit tests for new features
- Update README for significant changes
- Ensure all tests pass before submitting

## 🐛 Known Issues

- The Data with which this model is trained is synthetic [Created Randomly]
- Export feature requires write permissions in current directory
- Large datasets (10,000+ shipments) may impact performance
- Historical data generation uses simulated values

## 🗺️ Roadmap

### Version 2.0 (Planned)
- [ ] Real-time database integration (PostgreSQL/MongoDB)
- [ ] User authentication and role-based access
- [ ] Email/SMS alert notifications
- [ ] Machine learning for ETA prediction
- [ ] Mobile app (React Native)
- [ ] REST API endpoints
- [ ] Multi-language support
- [ ] Dark mode theme

### Version 3.0 (Future)
- [ ] Blockchain for supply chain verification
- [ ] IoT device integration (real sensors)
- [ ] Drone delivery tracking
- [ ] AR visualization for warehouse
- [ ] Predictive maintenance alerts

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

```
MIT License

Copyright (c) 2024 Abhishek Mohan

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "HealSphere_AI-Intelligent-End-to-End-Healthcare_Prediction_Suite"), to deal
in the Software without restriction...
```

## 👥 Authors

- **Abhishek Mohan** - *Initial work* - [abhishekmohan01](https://github.com/abhishekmohan01)

## 🙏 Acknowledgments

- **Gradio Team** - For the amazing UI framework
- **Plotly** - For interactive visualization library
- **Pharmaceutical Industry** - For domain insights
- **Open Source Community** - For continuous support

## 📧 Contact

**Abhishek Mohan**
- GitHub: [@abhishekmohan01](https://github.com/abhishekmohan01)
- Email: abhishek5489@outlook.com
- LinkedIn: [Abhishek Mohan](https://www.linkedin.com/in/abhishek---mohan/)

**Project Link:** [https://github.com/abhishekmohan01/HealSphere_AI-Intelligent-End-to-End-Healthcare_Prediction_Suite]

---

<div align="center">

**⭐ Star this repo if you find it helpful!**

Made with ❤️ for the pharmaceutical supply chain industry by Abhishek Mohan

[Report Bug](https://github.com/abhishekmohan01/HealSphere_AI-Intelligent-End-to-End-Healthcare_Prediction_Suite) · [Request Feature](https://github.com/abhishekmohan01/HealSphere_AI-Intelligent-End-to-End-Healthcare_Prediction_Suite)

</div>
