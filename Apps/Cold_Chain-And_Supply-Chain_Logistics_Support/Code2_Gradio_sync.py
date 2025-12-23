import gradio as gr
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.express as px
from datetime import datetime, timedelta, timezone

# ==================== DATA GENERATION ====================

def generate_medicine_data():
    """Generate sample medicine dataset"""
    medicines = [
        {'medicine_id': 1, 'medicine_name': 'Paracetamol 500mg', 'brand': 'Crocin', 'manufacturer': 'GSK', 
         'composition': 'Paracetamol', 'price': 25.5, 'dosage_form': 'Tablet', 'strength': '500mg', 
         'indications': 'Fever, Pain', 'side_effects': 'Nausea', 'prescription_required': 'No', 'category': 'Analgesic/Antipyretic'},
        {'medicine_id': 2, 'medicine_name': 'Ibuprofen 400mg', 'brand': 'Brufen', 'manufacturer': 'Abbott', 
         'composition': 'Ibuprofen', 'price': 45.0, 'dosage_form': 'Tablet', 'strength': '400mg', 
         'indications': 'Pain, Inflammation', 'side_effects': 'Gastritis', 'prescription_required': 'No', 'category': 'NSAID'},
        {'medicine_id': 3, 'medicine_name': 'Amoxicillin 500mg', 'brand': 'Novamox', 'manufacturer': 'Cipla', 
         'composition': 'Amoxicillin', 'price': 85.0, 'dosage_form': 'Capsule', 'strength': '500mg', 
         'indications': 'Bacterial Infections', 'side_effects': 'Diarrhea', 'prescription_required': 'Yes', 'category': 'Antibiotic'},
        {'medicine_id': 4, 'medicine_name': 'Metformin 500mg', 'brand': 'Glycomet', 'manufacturer': 'USV', 
         'composition': 'Metformin', 'price': 35.0, 'dosage_form': 'Tablet', 'strength': '500mg', 
         'indications': 'Diabetes', 'side_effects': 'GI upset', 'prescription_required': 'Yes', 'category': 'Antidiabetic'},
        {'medicine_id': 5, 'medicine_name': 'Cetirizine 10mg', 'brand': 'Alerid', 'manufacturer': 'Cipla', 
         'composition': 'Cetirizine', 'price': 18.5, 'dosage_form': 'Tablet', 'strength': '10mg', 
         'indications': 'Allergy', 'side_effects': 'Drowsiness', 'prescription_required': 'No', 'category': 'Antihistamine'},
        {'medicine_id': 101, 'medicine_name': 'Soframycin', 'brand': 'Soframycin', 'manufacturer': 'Sanofi', 
         'composition': 'Framycetin', 'price': 65.0, 'dosage_form': 'Ointment', 'strength': '1%', 
         'indications': 'Wounds', 'side_effects': 'Irritation', 'prescription_required': 'No', 'category': 'First Aid'},
        {'medicine_id': 102, 'medicine_name': 'Betadine', 'brand': 'Betadine', 'manufacturer': 'Win-Medicare', 
         'composition': 'Povidone-Iodine', 'price': 45.5, 'dosage_form': 'Solution', 'strength': '5%', 
         'indications': 'Disinfection', 'side_effects': 'Staining', 'prescription_required': 'No', 'category': 'First Aid'},
        {'medicine_id': 103, 'medicine_name': 'Volini', 'brand': 'Volini', 'manufacturer': 'Ranbaxy', 
         'composition': 'Diclofenac', 'price': 95.0, 'dosage_form': 'Gel', 'strength': '1.16%', 
         'indications': 'Pain relief', 'side_effects': 'Irritation', 'prescription_required': 'No', 'category': 'First Aid'}
    ]
    return pd.DataFrame(medicines)

ROUTES_NETWORK = {
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

TRANSPORT_MODES = {
    'Reefer Truck': {'speed': (40, 65), 'cost_per_km': 2.5},
    'Air Cargo': {'speed': (500, 900), 'cost_per_km': 15.0},
    'Rail': {'speed': (60, 120), 'cost_per_km': 1.8},
    'Sea Container': {'speed': (20, 35), 'cost_per_km': 0.8},
    'Insulated Van': {'speed': (35, 55), 'cost_per_km': 3.2},
    'Courier': {'speed': (30, 50), 'cost_per_km': 5.0}
}

COLD_CHAIN_PROFILES = {
    'Analgesic/Antipyretic': {'temp_min': 15, 'temp_max': 25},
    'Antibiotic': {'temp_min': 15, 'temp_max': 25},
    'Antidiabetic': {'temp_min': 2, 'temp_max': 8},
    'First Aid': {'temp_min': 10, 'temp_max': 30},
    'NSAID': {'temp_min': 15, 'temp_max': 25},
    'Antihistamine': {'temp_min': 15, 'temp_max': 25},
    'General Medicine': {'temp_min': 15, 'temp_max': 25}
}

def generate_shipments(n_shipments=500):
    """Generate shipment data"""
    np.random.seed(42)
    shipments = []
    now = datetime.now(timezone.utc)
    med_df = generate_medicine_data()
    
    for idx in range(n_shipments):
        med_row = med_df.sample(1).iloc[0]
        route_id = np.random.choice(list(ROUTES_NETWORK.keys()))
        route = ROUTES_NETWORK[route_id]
        total_distance = route['distance']
        
        progress_ratio = np.random.beta(2, 1.2)
        distance_completed = total_distance * progress_ratio
        distance_remaining = total_distance - distance_completed
        
        mode = np.random.choice(list(TRANSPORT_MODES.keys()), p=[0.35,0.20,0.15,0.10,0.15,0.05])
        mode_params = TRANSPORT_MODES[mode]
        speed = np.random.uniform(*mode_params['speed'])
        
        total_duration = np.random.gamma(24, 1.5)
        elapsed_hours = total_duration * progress_ratio
        start_time = now - timedelta(hours=elapsed_hours)
        eta_remaining = distance_remaining / speed if distance_remaining > 0 else 0
        
        category = med_row['category']
        profile = COLD_CHAIN_PROFILES.get(category, {'temp_min': 15, 'temp_max': 25})
        
        base_temp = np.random.uniform(profile['temp_min'], profile['temp_max'])
        current_temp = base_temp + np.random.normal(0, 1.2)
        humidity = np.random.normal(55, 15)
        
        if progress_ratio >= 0.95:
            status = np.random.choice(['Delivered', 'At Hub'], p=[0.7, 0.3])
        elif progress_ratio > 0.7:
            status = np.random.choice(['In Transit', 'At Hub', 'Delayed'], p=[0.6, 0.3, 0.1])
        else:
            status = 'In Transit'
        
        temp_alert = current_temp < profile['temp_min']-2 or current_temp > profile['temp_max']+2
        humidity_alert = humidity > 70
        long_distance_alert = distance_remaining > total_distance * 0.6
        long_eta_alert = eta_remaining > 24
        delayed_alert = status == 'Delayed'
        overall_alert = temp_alert or humidity_alert or long_distance_alert or long_eta_alert or delayed_alert
        
        transport_cost = distance_completed * mode_params['cost_per_km']
        
        shipments.append({
            'shipment_id': f'SHP{1000+idx:06d}',
            'route_id': route_id, 'route_from': route['from'], 'route_to': route['to'],
            'transport_mode': mode, 'status': status,
            'medicine_id': med_row['medicine_id'], 'medicine_name': med_row['medicine_name'],
            'brand': med_row['brand'], 'manufacturer': med_row['manufacturer'],
            'category': med_row['category'],
            'start_timestamp_utc': start_time.isoformat(), 'current_timestamp_utc': now.isoformat(),
            'elapsed_hours': round(elapsed_hours, 1), 'eta_hours_remaining': round(eta_remaining, 1),
            'total_distance_km': total_distance, 'distance_completed_km': round(distance_completed, 1),
            'distance_remaining_km': round(distance_remaining, 1), 'progress_pct': round(progress_ratio * 100, 1),
            'current_temperature_c': round(current_temp, 2), 'temp_min_target_c': profile['temp_min'],
            'temp_max_target_c': profile['temp_max'], 'current_humidity_pct': round(humidity, 1),
            'temperature_alert': int(temp_alert), 'humidity_alert': int(humidity_alert),
            'long_distance_alert': int(long_distance_alert), 'long_eta_alert': int(long_eta_alert),
            'delayed_alert': int(delayed_alert), 'overall_alert': int(overall_alert),
            'transport_cost_inr': round(transport_cost, 2), 'speed_kmph': round(speed, 1)
        })
    
    return pd.DataFrame(shipments)

# Initialize data
global_ship_df = generate_shipments(500)
global_med_df = generate_medicine_data()

# ==================== VISUALIZATION FUNCTIONS ====================

def create_overview_dashboard():
    """Create main dashboard with KPIs and charts"""
    df = global_ship_df
    
    # Calculate KPIs
    total_shipments = len(df)
    active_alerts = df['overall_alert'].sum()
    in_transit = len(df[df['status'] == 'In Transit'])
    avg_temp = df['current_temperature_c'].mean()
    total_cost = df['transport_cost_inr'].sum()
    
    # Create subplots
    fig = make_subplots(
        rows=3, cols=3,
        subplot_titles=('Status Distribution', 'Alert Types Breakdown', 'Transport Mode Usage',
                       'Temperature Distribution', 'Route Traffic', 'Progress Overview',
                       'Cost Analysis', 'Alert Timeline', 'Medicine Categories'),
        specs=[[{'type': 'pie'}, {'type': 'bar'}, {'type': 'pie'}],
               [{'type': 'histogram'}, {'type': 'bar'}, {'type': 'scatter'}],
               [{'type': 'bar'}, {'type': 'scatter'}, {'type': 'pie'}]],
        vertical_spacing=0.12,
        horizontal_spacing=0.1
    )
    
    # 1. Status Distribution (Pie)
    status_counts = df['status'].value_counts()
    fig.add_trace(go.Pie(labels=status_counts.index, values=status_counts.values, 
                         marker=dict(colors=['#2ecc71', '#f39c12', '#e74c3c', '#3498db'])),
                  row=1, col=1)
    
    # 2. Alert Types (Bar)
    alert_types = ['Temperature', 'Humidity', 'Distance', 'ETA', 'Delayed']
    alert_counts = [df['temperature_alert'].sum(), df['humidity_alert'].sum(),
                   df['long_distance_alert'].sum(), df['long_eta_alert'].sum(), df['delayed_alert'].sum()]
    fig.add_trace(go.Bar(x=alert_types, y=alert_counts, marker_color='#e74c3c',
                         text=alert_counts, textposition='auto'), row=1, col=2)
    
    # 3. Transport Mode (Pie)
    mode_counts = df['transport_mode'].value_counts()
    fig.add_trace(go.Pie(labels=mode_counts.index, values=mode_counts.values,
                         hole=0.3), row=1, col=3)
    
    # 4. Temperature Distribution (Histogram)
    fig.add_trace(go.Histogram(x=df['current_temperature_c'], nbinsx=30,
                               marker_color='#3498db', name='Temperature'), row=2, col=1)
    
    # 5. Route Traffic (Bar)
    route_counts = df['route_id'].value_counts().head(10)
    fig.add_trace(go.Bar(x=route_counts.index, y=route_counts.values,
                         marker_color='#9b59b6'), row=2, col=2)
    
    # 6. Progress Overview (Scatter)
    fig.add_trace(go.Scatter(x=df['distance_completed_km'], y=df['distance_remaining_km'],
                            mode='markers', marker=dict(size=5, color=df['overall_alert'],
                            colorscale='RdYlGn_r', showscale=True), name='Progress'), row=2, col=3)
    
    # 7. Cost Analysis (Bar)
    mode_costs = df.groupby('transport_mode')['transport_cost_inr'].sum().sort_values(ascending=False)
    fig.add_trace(go.Bar(x=mode_costs.index, y=mode_costs.values,
                         marker_color='#16a085', text=[f'₹{x:,.0f}' for x in mode_costs.values],
                         textposition='auto'), row=3, col=1)
    
    # 8. Alert Timeline (Scatter)
    alert_df = df[df['overall_alert'] == 1]
    fig.add_trace(go.Scatter(x=alert_df['elapsed_hours'], y=alert_df['current_temperature_c'],
                            mode='markers', marker=dict(size=8, color='red'),
                            name='Alerts'), row=3, col=2)
    
    # 9. Medicine Categories (Pie)
    cat_counts = df['category'].value_counts()
    fig.add_trace(go.Pie(labels=cat_counts.index, values=cat_counts.values), row=3, col=3)
    
    # Update layout
    fig.update_layout(
        height=1200,
        showlegend=False,
        title_text=f"<b>Cold Chain Dashboard Overview</b><br><sup>Total: {total_shipments:,} | Alerts: {active_alerts:,} | In Transit: {in_transit:,} | Avg Temp: {avg_temp:.1f}°C | Total Cost: ₹{total_cost:,.0f}</sup>",
        title_font_size=20
    )
    
    return fig

def search_shipments(query, status_filter, alert_filter, mode_filter):
    """Search and filter shipments"""
    df = global_ship_df.copy()
    
    # Apply filters
    if status_filter != 'All':
        df = df[df['status'] == status_filter]
    
    if alert_filter == 'Alert Only':
        df = df[df['overall_alert'] == 1]
    elif alert_filter == 'No Alerts':
        df = df[df['overall_alert'] == 0]
    
    if mode_filter != 'All':
        df = df[df['transport_mode'] == mode_filter]
    
    # Search query
    if query.strip():
        query_lower = query.lower()
        mask = (
            df['medicine_name'].str.lower().str.contains(query_lower, na=False) |
            df['brand'].str.lower().str.contains(query_lower, na=False) |
            df['shipment_id'].str.contains(query.upper(), na=False) |
            df['route_id'].str.contains(query.upper(), na=False) |
            df['status'].str.lower().str.contains(query_lower, na=False) |
            df['category'].str.lower().str.contains(query_lower, na=False)
        )
        df = df[mask]
    
    df = df.sort_values('overall_alert', ascending=False).head(50)
    
    # Create summary
    summary = f"""
### Search Results
- **Total Found:** {len(df):,} shipments
- **Alerts:** {df['overall_alert'].sum():,}
- **In Transit:** {len(df[df['status']=='In Transit']):,}
- **Average Progress:** {df['progress_pct'].mean():.1f}%
    """
    
    # Display columns
    display_df = df[['shipment_id', 'medicine_name', 'brand', 'route_from', 'route_to',
                     'transport_mode', 'status', 'progress_pct', 'eta_hours_remaining',
                     'current_temperature_c', 'overall_alert']].copy()
    
    display_df.columns = ['ID', 'Medicine', 'Brand', 'From', 'To', 'Mode', 'Status', 
                          'Progress %', 'ETA (hrs)', 'Temp °C', 'Alert']
    
    return summary, display_df

def get_shipment_details(shipment_id):
    """Get detailed shipment information"""
    if not shipment_id:
        return "Please enter a shipment ID", None, None
        
    shipment = global_ship_df[global_ship_df['shipment_id'] == shipment_id.upper()]
    
    if shipment.empty:
        return "Shipment not found", None, None
    
    row = shipment.iloc[0]
    
    # Detailed info
    details = f"""
# 📦 Shipment Details: {shipment_id.upper()}

### Basic Information
- **Route:** {row['route_from']} → {row['route_to']} ({row['route_id']})
- **Medicine:** {row['medicine_name']} ({row['brand']})
- **Category:** {row['category']}
- **Transport:** {row['transport_mode']} | Speed: {row['speed_kmph']:.1f} km/h
- **Status:** {row['status']}

### Progress Tracking
- **Total Distance:** {row['total_distance_km']:.0f} km
- **Completed:** {row['distance_completed_km']:.0f} km ({row['progress_pct']:.1f}%)
- **Remaining:** {row['distance_remaining_km']:.0f} km
- **ETA:** {row['eta_hours_remaining']:.1f} hours
- **Elapsed Time:** {row['elapsed_hours']:.1f} hours

### Cold Chain Monitoring
- **Target Range:** {row['temp_min_target_c']:.1f}°C - {row['temp_max_target_c']:.1f}°C
- **Current Temperature:** {row['current_temperature_c']:.1f}°C
- **Humidity:** {row['current_humidity_pct']:.1f}%

### Alert Status
    """
    
    alerts_active = sum([row['temperature_alert'], row['humidity_alert'],
                        row['long_distance_alert'], row['long_eta_alert'], row['delayed_alert']])
    
    if alerts_active > 0:
        details += f"\n**🔴 ACTIVE ALERTS ({alerts_active}):**\n"
        if row['temperature_alert']: details += "- ⚠️ Temperature excursion\n"
        if row['humidity_alert']: details += "- ⚠️ High humidity\n"
        if row['long_distance_alert']: details += "- ⚠️ Long distance remaining\n"
        if row['long_eta_alert']: details += "- ⚠️ Extended ETA\n"
        if row['delayed_alert']: details += "- ⚠️ Delayed status\n"
    else:
        details += "\n**🟢 All systems nominal**\n"
    
    details += f"\n### Cost Summary\n- **Transport Cost:** ₹{row['transport_cost_inr']:,.2f}"
    
    # Generate historical chart
    hist_fig = generate_historical_chart(row)
    
    # Generate risk analysis
    risk_fig = generate_risk_analysis(row)
    
    return details, hist_fig, risk_fig

def generate_historical_chart(row):
    """Generate historical sensor data chart"""
    n_points = 50
    duration_hours = float(row['elapsed_hours'])
    time_points = np.linspace(0, duration_hours, n_points)
    
    base_temp = float(row['current_temperature_c'])
    temp_min = float(row['temp_min_target_c'])
    temp_max = float(row['temp_max_target_c'])
    
    temps = []
    humidities = []
    vibrations = []
    alerts = []
    
    for t in time_points:
        temp = base_temp + np.sin(t / 6) * 2 + np.random.normal(0, 0.8)
        temps.append(temp)
        humidities.append(45 + 0.4 * temp + np.random.normal(0, 8))
        vibrations.append(0.3 + (0.3 if any(abs(t - spike) < 1 for spike in [4,12,24,36]) else 0))
        alerts.append(1 if temp < temp_min or temp > temp_max else 0)
    
    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=('Temperature History', 'Humidity Levels', 'Vibration Index', 'Alert Events'),
        specs=[[{'secondary_y': False}, {'secondary_y': False}],
               [{'secondary_y': False}, {'secondary_y': False}]]
    )
    
    # Temperature
    fig.add_trace(go.Scatter(x=time_points, y=temps, mode='lines+markers',
                            name='Temperature', line=dict(color='orange', width=2)), row=1, col=1)
    fig.add_hline(y=temp_min, line_dash="dash", line_color="green", row=1, col=1)
    fig.add_hline(y=temp_max, line_dash="dash", line_color="red", row=1, col=1)
    
    # Humidity
    fig.add_trace(go.Scatter(x=time_points, y=humidities, mode='lines',
                            name='Humidity', line=dict(color='blue', width=2)), row=1, col=2)
    
    # Vibration
    fig.add_trace(go.Scatter(x=time_points, y=vibrations, mode='lines+markers',
                            name='Vibration', line=dict(color='purple', width=2)), row=2, col=1)
    
    # Alerts
    alert_times = [time_points[i] for i, a in enumerate(alerts) if a == 1]
    if alert_times:
        fig.add_trace(go.Scatter(x=alert_times, y=[0.5]*len(alert_times), mode='markers',
                                name='Alerts', marker=dict(color='red', size=12, symbol='x')), row=2, col=2)
    
    fig.update_layout(height=600, showlegend=True, title_text="Sensor History")
    fig.update_xaxes(title_text="Hours", row=2, col=1)
    fig.update_xaxes(title_text="Hours", row=2, col=2)
    
    return fig

def generate_risk_analysis(row):
    """Generate risk analysis visualization"""
    temp_risk = min(abs(row['current_temperature_c'] - row['temp_min_target_c']) * 10, 50)
    distance_risk = min(row['distance_remaining_km'] / row['total_distance_km'] * 100, 50)
    eta_risk = min(row['eta_hours_remaining'] / 24 * 50, 50)
    vibration_risk = 30
    total_risk = (temp_risk + distance_risk + eta_risk + vibration_risk) / 4
    
    fig = go.Figure()
    
    risks = ['Temperature', 'Distance', 'ETA', 'Vibration', 'TOTAL']
    values = [temp_risk, distance_risk, eta_risk, vibration_risk, total_risk]
    colors = ['red' if v > 30 else 'orange' if v > 20 else 'green' for v in values]
    
    fig.add_trace(go.Bar(x=risks, y=values, marker_color=colors,
                         text=[f'{v:.0f}' for v in values], textposition='auto'))
    
    fig.update_layout(
        title='Risk Assessment',
        yaxis_title='Risk Score (0-100)',
        height=400,
        yaxis_range=[0, 100]
    )
    
    return fig

def create_analytics_dashboard():
    """Create advanced analytics dashboard"""
    df = global_ship_df
    
    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=('Shipment Heatmap by Route', 'Cost vs Distance Analysis',
                       'Temperature Compliance', 'Real-time Status Map'),
        specs=[[{'type': 'heatmap'}, {'type': 'scatter'}],
               [{'type': 'box'}, {'type': 'scatter'}]]
    )
    
    # 1. Heatmap
    route_status = pd.crosstab(df['route_id'], df['status'])
    fig.add_trace(go.Heatmap(z=route_status.values, x=route_status.columns,
                             y=route_status.index, colorscale='Viridis'), row=1, col=1)
    
    # 2. Cost vs Distance
    fig.add_trace(go.Scatter(x=df['distance_completed_km'], y=df['transport_cost_inr'],
                            mode='markers', marker=dict(size=6, color=df['overall_alert'],
                            colorscale='RdYlGn_r'), name='Cost'), row=1, col=2)
    
    # 3. Temperature Compliance
    for category in df['category'].unique()[:5]:
        cat_df = df[df['category'] == category]
        fig.add_trace(go.Box(y=cat_df['current_temperature_c'], name=category), row=2, col=1)
    
    # 4. Status Map
    status_progress = df.groupby('status')['progress_pct'].mean()
    fig.add_trace(go.Scatter(x=status_progress.index, y=status_progress.values,
                            mode='markers+lines', marker=dict(size=15),
                            line=dict(width=3)), row=2, col=2)
    
    fig.update_layout(height=800, showlegend=False, title_text="Advanced Analytics Dashboard")
    
    return fig

def export_report(format_type, filter_type):
    """Export report in selected format"""
    df = global_ship_df.copy()
    
    if filter_type == 'Alerts Only':
        df = df[df['overall_alert'] == 1]
    elif filter_type == 'In Transit Only':
        df = df[df['status'] == 'In Transit']
    
    filename = f"cold_chain_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    
    if format_type == "CSV":
        filepath = f"{filename}.csv"
        df.to_csv(filepath, index=False)
    elif format_type == "Excel":
        filepath = f"{filename}.xlsx"
        df.to_excel(filepath, index=False)
    else:  # JSON
        filepath = f"{filename}.json"
        df.to_json(filepath, orient='records', indent=2)
    
    return f"✅ Report generated: {len(df):,} records", filepath

# ==================== GRADIO INTERFACE ====================
# ==================== GRADIO INTERFACE ====================

with gr.Blocks(theme=gr.themes.Soft(), title="Cold Chain Tracking System") as app:
    gr.Markdown("""
    # 🌡️ Cold Chain Tracking & Monitoring System
    ### Real-time pharmaceutical shipment tracking with IoT monitoring
    """)
    
    with gr.Tabs():
        # Tab 1: Dashboard Overview
        with gr.Tab("📊 Dashboard Overview"):
            gr.Markdown("### Real-time System Overview")
            overview_plot = gr.Plot(label="Dashboard Metrics")
            refresh_btn = gr.Button("🔄 Refresh Dashboard", variant="primary")
            refresh_btn.click(fn=create_overview_dashboard, outputs=overview_plot)
            app.load(fn=create_overview_dashboard, outputs=overview_plot)
        
        # Tab 2: Search & Track
        with gr.Tab("🔍 Search & Track"):
            gr.Markdown("### Search Shipments")
            
            with gr.Row():
                search_query = gr.Textbox(label="Search", placeholder="Medicine name, ID, Route...", scale=3)
                search_btn = gr.Button("Search", variant="primary", scale=1)
            
            with gr.Row():
                status_filter = gr.Dropdown(
                    choices=['All', 'In Transit', 'At Hub', 'Delivered', 'Delayed'],
                    value='All', label="Status Filter"
                )
                alert_filter = gr.Dropdown(
                    choices=['All', 'Alert Only', 'No Alerts'],
                    value='All', label="Alert Filter"
                )
                mode_filter = gr.Dropdown(
                    choices=['All'] + list(TRANSPORT_MODES.keys()),
                    value='All', label="Transport Mode"
                )
            
            search_summary = gr.Markdown()
            search_results = gr.Dataframe(label="Search Results", interactive=False)
            
            search_btn.click(
                fn=search_shipments,
                inputs=[search_query, status_filter, alert_filter, mode_filter],
                outputs=[search_summary, search_results]
            )
        
        # Tab 3: Shipment Details
        with gr.Tab("📦 Shipment Details"):
            gr.Markdown("### Detailed Shipment Viewer")
            gr.Markdown("**Try:** SHP100123, SHP100456, SHP100789")
            
            with gr.Row():
                shipment_id_input = gr.Textbox(
                    label="Shipment ID",
                    placeholder="SHP100123",
                    scale=3
                )
                view_btn = gr.Button("View Details", variant="primary", scale=1)
            
            shipment_details = gr.Markdown()
            
            with gr.Row():
                with gr.Column():
                    history_chart = gr.Plot(label="Sensor History")
                with gr.Column():
                    risk_chart = gr.Plot(label="Risk Analysis")
            
            view_btn.click(
                fn=get_shipment_details,
                inputs=shipment_id_input,
                outputs=[shipment_details, history_chart, risk_chart]
            )
        
        # Tab 4: Analytics
        with gr.Tab("📈 Analytics"):
            gr.Markdown("### Advanced Analytics & Insights")
            analytics_plot = gr.Plot(label="Analytics Dashboard")
            analytics_refresh = gr.Button("🔄 Refresh Analytics", variant="primary")
            analytics_refresh.click(fn=create_analytics_dashboard, outputs=analytics_plot)
            app.load(fn=create_analytics_dashboard, outputs=analytics_plot)
        
        # Tab 5: Export & Reports
        with gr.Tab("📄 Export & Reports"):
            gr.Markdown("### Generate Reports")
            
            with gr.Row():
                export_format = gr.Radio(
                    choices=["CSV", "Excel", "JSON"],
                    value="CSV",
                    label="Export Format"
                )
                export_filter = gr.Dropdown(
                    choices=['All Shipments', 'Alerts Only', 'In Transit Only'],
                    value='All Shipments',
                    label="Export Filter"
                )
            
            export_btn = gr.Button("📥 Download Report", variant="primary")
            export_status = gr.Textbox(label="Status", interactive=False)
            export_file = gr.File(label="Download")
            
            export_btn.click(
                fn=export_report,
                inputs=[export_format, export_filter],
                outputs=[export_status, export_file]
            )
    
    gr.Markdown("""
    ---
    ### 📊 System Statistics
    - **Total Shipments:** 500+
    - **Real-time Monitoring:** IoT Sensors
    - **Coverage:** Pan-India Routes
    - **Compliance:** Cold Chain Standards
    """)

# Launch the app
if __name__ == "__main__":
    app.launch(share=True, debug=True)
