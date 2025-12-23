 PART 1/5: Medicine Dataset & UI
import pandas as pd
import numpy as np
import ipywidgets as widgets
from IPython.display import display, clear_output
from google.colab import files

print("Upload medicines11.csv:")
uploaded = files.upload()
csv_file = list(uploaded.keys())[0]
med_df = pd.read_csv(csv_file)

if 'category' not in med_df.columns:
    def assign_category(name):
        name_lower = str(name).lower()
        if 'paracetamol' in name_lower: return 'Analgesic/Antipyretic'
        elif 'ibuprofen' in name_lower: return 'NSAID'
        elif any(word in name_lower for word in ['amoxicillin','azithromycin','ciprofloxacin']): return 'Antibiotic'
        elif 'metformin' in name_lower: return 'Antidiabetic'
        elif any(word in name_lower for word in ['cetirizine','fexofenadine']): return 'Antihistamine'
        else: return 'General Medicine'
    med_df['category'] = med_df['medicine_name'].apply(assign_category)

first_aid = pd.DataFrame([
    {'medicine_id':101,'medicine_name':'Soframycin','brand':'Soframycin','manufacturer':'Sanofi','composition':'Framycetin','price':65.0,'dosage_form':'Ointment','strength':'1%','indications':'Wounds','side_effects':'Irritation','prescription_required':'No','category':'First Aid'},
    {'medicine_id':102,'medicine_name':'Betadine','brand':'Betadine','manufacturer':'Win-Medicare','composition':'Povidone-Iodine','price':45.5,'dosage_form':'Solution','strength':'5%','indications':'Disinfection','side_effects':'Staining','prescription_required':'No','category':'First Aid'},
    {'medicine_id':103,'medicine_name':'Volini','brand':'Volini','manufacturer':'Ranbaxy','composition':'Diclofenac','price':95.0,'dosage_form':'Gel','strength':'1.16%','indications':'Pain relief','side_effects':'Irritation','prescription_required':'No','category':'First Aid'}
])
med_df = pd.concat([med_df, first_aid], ignore_index=True)

class SuggestionBox:
    def __init__(self, df):
        self.df = df
        self.input = widgets.Text(placeholder='Paracetamol, Soframycin...', layout=widgets.Layout(width='60%'))
        self.suggestions = widgets.SelectMultiple(rows=4, layout=widgets.Layout(width='60%'))
        self.btn = widgets.Button(description='Track', button_style='success')
        self.output = widgets.Output()
        self.input.observe(self.update_suggestions, 'value')
        self.btn.on_click(self.search)

    def update_suggestions(self, change):
        q = change['new'].lower() if change['new'] else ''
        if len(q) > 1:
            matches = self.df[
                self.df['medicine_name'].str.lower().str.contains(q) |
                self.df['brand'].str.lower().str.contains(q)
            ][['medicine_name', 'brand']].head(10)
            self.suggestions.options = [f"{r['medicine_name']} ({r['brand']})" for _, r in matches.iterrows()]

    def search(self, b):
        with self.output:
            clear_output()
            print(f"Ready to track '{self.input.value}' shipments...")

    def display(self):
        display(widgets.VBox([self.input, self.suggestions, self.btn, self.output]))

suggestion_box = SuggestionBox(med_df)
global_med_df = med_df
suggestion_box.display()
# PART 2/5: Shipment Generation
import numpy as np
from datetime import datetime, timedelta
import pandas as pd

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

np.random.seed(42)
N_SHIPMENTS = 500
shipments = []
now = datetime.utcnow()

for idx in range(N_SHIPMENTS):
    med_probs = np.ones(len(global_med_df))
    med_probs[global_med_df['category'] == 'First Aid'] *= 1.5
    med_row = global_med_df.sample(1, weights=med_probs).iloc[0]

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

    cost_per_km = mode_params['cost_per_km']
    transport_cost = distance_completed * cost_per_km

    shipments.append({
        'shipment_id': f'SHP{1000+idx:06d}',
        'route_id': route_id, 'route_from': route['from'], 'route_to': route['to'],
        'transport_mode': mode, 'status': status,
        'medicine_id': med_row['medicine_id'], 'medicine_name': med_row['medicine_name'],
        'brand': med_row['brand'], 'manufacturer': med_row['manufacturer'],
        'composition': med_row['composition'], 'dosage_form': med_row['dosage_form'],
        'strength': med_row['strength'], 'category': med_row['category'],
        'start_timestamp_utc': start_time.isoformat(), 'current_timestamp_utc': now.isoformat(),
        'elapsed_hours': round(elapsed_hours, 1), 'eta_hours_remaining': round(eta_remaining, 1),
        'total_distance_km': total_distance, 'distance_completed_km': round(distance_completed, 1),
        'distance_remaining_km': round(distance_remaining, 1), 'progress_pct': round(progress_ratio * 100, 1),
        'current_temperature_c': round(current_temp, 2), 'temp_min_target_c': profile['temp_min'],
        'temp_max_target_c': profile['temp_max'], 'current_humidity_pct': round(humidity, 1),
        'current_vibration_idx': round(mode_params['cost_per_km'] * 0.1, 2),
        'temperature_alert': int(temp_alert), 'humidity_alert': int(humidity_alert),
        'long_distance_alert': int(long_distance_alert), 'long_eta_alert': int(long_eta_alert),
        'delayed_alert': int(delayed_alert), 'overall_alert': int(overall_alert),
        'transport_cost_inr': round(transport_cost, 2), 'speed_kmph': round(speed, 1)
    })

global_ship_df = pd.DataFrame(shipments)
print(f"Generated {len(global_ship_df)} shipments")
# PART 2.5 FIXED: Clean Enterprise Data Scaling (Run ONCE between Part 2 & 3)
import numpy as np
import pandas as pd
from datetime import datetime, timezone, timedelta

print("🔄 Scaling dataset (run ONCE)...")

# Fix deprecation warning
def utc_now():
    return datetime.now(timezone.utc)

# Enhanced configs
ROUTES_NETWORK.update({
    'R011': {'from': 'Vadodara', 'to': 'Guwahati', 'distance': 2560, 'hubs': 7},
    'R012': {'from': 'Surat', 'to': 'Patna', 'distance': 1634, 'hubs': 5},
    'R013': {'from': 'Nashik', 'to': 'Bhubaneswar', 'distance': 1425, 'hubs': 4},
    'R014': {'from': 'Aurangabad', 'to': 'Raipur', 'distance': 725, 'hubs': 2},
    'R015': {'from': 'Amravati', 'to': 'Jamshedpur', 'distance': 985, 'hubs': 3}
})

TRANSPORT_MODES['Express Air'] = {'speed': (700, 950), 'cost_per_km': 18.0}

# Generate ONLY 2000 additional shipments (total ~2500)
N_ADDITIONAL = 2000
additional_shipments = []

print(f"Generating {N_ADDITIONAL} additional shipments...")
np.random.seed(123)  # Fixed seed for consistency

for idx in range(N_ADDITIONAL):
    # Medicine selection
    med_probs = np.ones(len(global_med_df))
    med_probs[global_med_df['category'].str.contains('First Aid', na=False)] *= 2.0
    med_row = global_med_df.sample(1, weights=med_probs).iloc[0]

    route_id = np.random.choice(list(ROUTES_NETWORK.keys()))
    route = ROUTES_NETWORK[route_id]
    total_distance = route['distance']

    progress_ratio = np.random.beta(2, 1.5)
    distance_completed = total_distance * progress_ratio
    distance_remaining = total_distance - distance_completed

    mode = np.random.choice(list(TRANSPORT_MODES.keys()), p=[0.3,0.15,0.2,0.08,0.12,0.05,0.1])
    mode_params = TRANSPORT_MODES[mode]
    speed = np.random.uniform(*mode_params['speed'])

    total_duration = np.random.gamma(24, 2)
    elapsed_hours = total_duration * progress_ratio
    start_time = utc_now() - timedelta(hours=elapsed_hours)
    eta_remaining = distance_remaining / speed if distance_remaining > 0 else 0

    # Simplified profiles
    category = med_row['category']
    if 'First Aid' in str(category):
        profile = {'temp_min': 10, 'temp_max': 30}
    elif 'Antidiabetic' in str(category):
        profile = {'temp_min': 2, 'temp_max': 8}
    else:
        profile = {'temp_min': 15, 'temp_max': 25}

    base_temp = np.random.uniform(profile['temp_min'], profile['temp_max'])
    current_temp = base_temp + np.random.normal(0, 1.2)
    humidity = np.random.normal(55, 15)

    # Status
    if progress_ratio >= 0.95:
        status = np.random.choice(['Delivered', 'At Hub'], p=[0.7, 0.3])
    elif progress_ratio > 0.7:
        status = np.random.choice(['In Transit', 'Delayed'], p=[0.8, 0.2])
    else:
        status = 'In Transit'

    temp_alert = current_temp < profile['temp_min']-2 or current_temp > profile['temp_max']+2
    long_distance_alert = distance_remaining > total_distance * 0.6
    overall_alert = temp_alert or long_distance_alert or (status == 'Delayed')

    transport_cost = distance_completed * mode_params['cost_per_km']

    additional_shipments.append({
        'shipment_id': f'SHP{2000+idx:06d}',
        'route_id': route_id, 'route_from': route['from'], 'route_to': route['to'],
        'transport_mode': mode, 'status': status,
        'medicine_id': med_row['medicine_id'], 'medicine_name': med_row['medicine_name'],
        'brand': med_row['brand'], 'manufacturer': med_row['manufacturer'],
        'composition': med_row['composition'], 'dosage_form': med_row['dosage_form'],
        'strength': med_row['strength'], 'category': med_row['category'],
        'start_timestamp_utc': start_time.isoformat(), 'current_timestamp_utc': utc_now().isoformat(),
        'elapsed_hours': round(elapsed_hours, 1), 'eta_hours_remaining': round(eta_remaining, 1),
        'total_distance_km': total_distance, 'distance_completed_km': round(distance_completed, 1),
        'distance_remaining_km': round(distance_remaining, 1), 'progress_pct': round(progress_ratio * 100, 1),
        'current_temperature_c': round(current_temp, 2), 'temp_min_target_c': profile['temp_min'],
        'temp_max_target_c': profile['temp_max'], 'current_humidity_pct': round(humidity, 1),
        'current_vibration_idx': round(mode_params['cost_per_km'] * 0.1, 2),
        'temperature_alert': int(temp_alert), 'humidity_alert': 0,
        'long_distance_alert': int(long_distance_alert), 'long_eta_alert': 0,
        'delayed_alert': int(status == 'Delayed'), 'overall_alert': int(overall_alert),
        'transport_cost_inr': round(transport_cost, 2), 'speed_kmph': round(speed, 1)
    })

# Append without duplicates or overwrites
new_df = pd.DataFrame(additional_shipments)
global_ship_df = pd.concat([global_ship_df, new_df], ignore_index=True)

# Remove any potential duplicates
global_ship_df = global_ship_df.drop_duplicates(subset=['shipment_id']).reset_index(drop=True)

print(f"✅ DATASET SCALED: {len(global_ship_df):,} TOTAL SHIPMENTS")
print(f"• Alerts: {global_ship_df['overall_alert'].sum():,}")
print(f"• In Transit: {len(global_ship_df[global_ship_df['status']=='In Transit']):,}")
print("\n🚀 Continue with Part 3 → 4 → 5 (NO REPEATS!)")


# PART 3/5: Search & Dashboard
import ipywidgets as widgets
from IPython.display import display, clear_output
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots

def find_shipments_multi_query(query, ship_df=global_ship_df):
    query_lower = query.lower().strip()
    if not query_lower:
        return ship_df.head(10)

    conditions = [
        ship_df['medicine_name'].str.lower().str.contains(query_lower, na=False),
        ship_df['brand'].str.lower().str.contains(query_lower, na=False),
        ship_df['shipment_id'].str.contains(query_lower.upper(), na=False),
        ship_df['route_id'].str.contains(query_lower.upper(), na=False),
        ship_df['medicine_id'].astype(str).str.contains(query_lower, na=False),
        ship_df['status'].str.lower().str.contains(query_lower, na=False),
        ship_df['transport_mode'].str.lower().str.contains(query_lower, na=False),
        ship_df['category'].str.lower().str.contains(query_lower, na=False)
    ]

    mask = conditions[0]
    for cond in conditions[1:]:
        mask = mask | cond

    return ship_df[mask].sort_values('overall_alert', ascending=False).head(50)

def get_alert_summary(ship_df=global_ship_df):
    return {
        'total_shipments': len(ship_df),
        'active_alerts': ship_df['overall_alert'].sum(),
        'temp_alerts': ship_df['temperature_alert'].sum(),
        'humidity_alerts': ship_df['humidity_alert'].sum(),
        'long_distance': ship_df['long_distance_alert'].sum(),
        'delayed': ship_df['delayed_alert'].sum(),
        'in_transit': len(ship_df[ship_df['status'] == 'In Transit']),
        'high_risk_routes': len(ship_df[ship_df['route_id'].isin(['R007', 'R010'])])
    }

class ColdChainSearchWidget:
    def __init__(self, ship_df, med_df):
        self.ship_df = ship_df
        self.med_df = med_df

        self.search_input = widgets.Text(
            value='', placeholder='Paracetamol, SHP100123, R005, In Transit...',
            description='Search:', style={'description_width': '60px'},
            layout=widgets.Layout(width='70%')
        )

        self.status_filter = widgets.Dropdown(
            options=['All'] + sorted(self.ship_df['status'].unique().tolist()),
            value='All', description='Status:'
        )

        self.alert_filter = widgets.Dropdown(
            options=['All', 'Alert Only', 'No Alerts'], value='All', description='Alerts:'
        )

        self.mode_filter = widgets.Dropdown(
            options=['All'] + sorted(self.ship_df['transport_mode'].unique().tolist()),
            value='All', description='Mode:'
        )

        self.search_btn = widgets.Button(description='Search', button_style='success', icon='search')
        self.alert_dashboard_btn = widgets.Button(description='Alert Dashboard', button_style='warning', icon='exclamation-triangle')

        self.results_table = widgets.Output()
        self.summary_output = widgets.Output()

        self.search_btn.on_click(self.on_search)
        self.alert_dashboard_btn.on_click(self.show_alert_dashboard)
        self.search_input.observe(self.on_search_input_change, names='value')

    def on_search_input_change(self, change):
        if len(change['new']) > 2:
            self.on_search(None)

    def on_search(self, b):
        with self.results_table:
            clear_output()

            query = self.search_input.value
            df_filtered = self.ship_df.copy()

            if self.status_filter.value != 'All':
                df_filtered = df_filtered[df_filtered['status'] == self.status_filter.value]

            if self.alert_filter.value == 'Alert Only':
                df_filtered = df_filtered[df_filtered['overall_alert'] == 1]
            elif self.alert_filter.value == 'No Alerts':
                df_filtered = df_filtered[df_filtered['overall_alert'] == 0]

            if self.mode_filter.value != 'All':
                df_filtered = df_filtered[df_filtered['transport_mode'] == self.mode_filter.value]

            if query.strip():
                df_filtered = find_shipments_multi_query(query, df_filtered)

            if len(df_filtered) == 0:
                print("No shipments found matching your criteria.")
                return

            display_cols = ['shipment_id', 'medicine_name', 'brand', 'route_id',
                          'transport_mode', 'status', 'distance_remaining_km',
                          'eta_hours_remaining', 'current_temperature_c', 'overall_alert']

            styled_df = df_filtered[display_cols].head(20).style\
                .format({'distance_remaining_km': '{:.1f}', 'eta_hours_remaining': '{:.1f}',
                        'current_temperature_c': '{:.1f}'})\
                .background_gradient(subset=['overall_alert'], cmap='RdYlGn_r')

            print(f"Found {len(df_filtered)} shipments")
            display(styled_df)

    def show_alert_dashboard(self, b):
        with self.summary_output:
            clear_output()

            alerts = get_alert_summary(self.ship_df)

            print("ALERT DASHBOARD")
            print("=" * 50)
            print(f"Total Shipments: {alerts['total_shipments']:,}")
            print(f"Active Alerts: {alerts['active_alerts']:,} ({alerts['active_alerts']/alerts['total_shipments']*100:.1f}%)")
            print(f"Temp Alerts: {alerts['temp_alerts']:,}")
            print(f"Humidity Alerts: {alerts['humidity_alerts']:,}")
            print(f"Long Distance: {alerts['long_distance']:,}")
            print(f"Delayed: {alerts['delayed']:,}")

            fig = make_subplots(rows=1, cols=2, subplot_titles=('Alert Types', 'Status Distribution'))

            alert_types = ['Temp', 'Humidity', 'Distance', 'Delayed']
            alert_counts = [alerts['temp_alerts'], alerts['humidity_alerts'],
                          alerts['long_distance'], alerts['delayed']]
            fig.add_trace(go.Pie(labels=alert_types, values=alert_counts), row=1, col=1)

            status_counts = self.ship_df['status'].value_counts()
            fig.add_trace(go.Pie(labels=status_counts.index, values=status_counts.values), row=1, col=2)

            fig.update_layout(height=400, showlegend=True, title_text="Cold Chain Risk Dashboard")
            fig.show()

    def display(self):
        controls = widgets.VBox([
            widgets.HTML("<h3>Cold Chain Shipment Tracker</h3>"),
            widgets.HBox([self.search_input, self.search_btn]),
            widgets.GridBox([self.status_filter, self.alert_filter, self.mode_filter, self.alert_dashboard_btn],
                          layout=widgets.Layout(grid_template_columns="repeat(4, 200px)"))
        ])

        display(widgets.VBox([controls, self.results_table, self.summary_output]))

print("Quick Status Overview:")
alerts = get_alert_summary()
print(f"Total: {alerts['total_shipments']:,} | Alerts: {alerts['active_alerts']:,}")

search_widget = ColdChainSearchWidget(global_ship_df, global_med_df)
search_widget.display()
# PART 4/5: Detailed Viewer & Historical Tracking
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np
from IPython.display import display, clear_output
import ipywidgets as widgets

def generate_historical_data(shipment_row, n_points=50):
    duration_hours = float(shipment_row['elapsed_hours'])
    time_points = np.linspace(0, duration_hours, n_points)

    base_temp = float(shipment_row['current_temperature_c'])
    temp_min = float(shipment_row['temp_min_target_c'])
    temp_max = float(shipment_row['temp_max_target_c'])

    historical_data = []

    for t in time_points:
        temp_drift = np.sin(t / 6) * 2
        temp_noise = np.random.normal(0, 0.8)
        hist_temp = base_temp + temp_drift + temp_noise

        hist_humidity = 45 + 0.4 * hist_temp + np.random.normal(0, 8)
        base_vibration = float(shipment_row['current_vibration_idx'])
        vibration_spikes = [4, 12, 24, 36]
        hist_vibration = base_vibration + (0.3 if any(abs(t - spike) < 1 for spike in vibration_spikes) else 0)

        historical_data.append({
            'timestamp_hours': round(t, 1),
            'temperature_c': round(hist_temp, 2),
            'humidity_pct': round(hist_humidity, 1),
            'vibration_idx': round(hist_vibration, 3),
            'temp_alert': 1 if hist_temp < temp_min or hist_temp > temp_max else 0
        })

    return pd.DataFrame(historical_data)

class DetailedShipmentViewer:
    def __init__(self, ship_df):
        self.ship_df = ship_df

        self.shipment_id_input = widgets.Text(
            value='', placeholder='SHP100123',
            description='Shipment ID:', style={'description_width': '100px'}
        )

        self.view_btn = widgets.Button(description='View Details', button_style='primary', icon='eye')
        self.history_btn = widgets.Button(description='History Graph', button_style='success')
        self.risk_btn = widgets.Button(description='Risk Analysis', button_style='warning')
        self.export_btn = widgets.Button(description='Export Report', button_style='info')

        self.output = widgets.Output()

        self.view_btn.on_click(self.view_shipment)
        self.history_btn.on_click(self.show_history)
        self.risk_btn.on_click(self.show_risk_analysis)
        self.export_btn.on_click(self.export_report)
        self.shipment_id_input.observe(self.on_id_change, names='value')

    def on_id_change(self, change):
        if len(change['new']) > 6:
            self.view_shipment(None)

    def view_shipment(self, b):
        with self.output:
            clear_output()

            shipment_id = self.shipment_id_input.value.strip().upper()
            if not shipment_id.startswith('SHP'):
                print("Enter valid Shipment ID (SHPxxxxx)")
                return

            shipment = self.ship_df[self.ship_df['shipment_id'] == shipment_id]
            if shipment.empty:
                print(f"Shipment {shipment_id} not found.")
                return

            row = shipment.iloc[0]

            print("=" * 80)
            print(f"SHIPMENT DETAILS: {shipment_id}")
            print("=" * 80)

            print("\nBASIC INFORMATION")
            print("-" * 40)
            print(f"Route: {row['route_from']} → {row['route_to']} ({row['route_id']})")
            print(f"Medicine: {row['medicine_name']} ({row['brand']})")
            print(f"Transport: {row['transport_mode']} | Speed: {row['speed_kmph']:.1f} km/h")
            print(f"Status: {row['status']}")

            print("\nPROGRESS TRACKING")
            print("-" * 40)
            print(f"Total: {row['total_distance_km']:.0f} km")
            print(f"Completed: {row['distance_completed_km']:.0f} km ({row['progress_pct']:.1f}%)")
            print(f"Remaining: {row['distance_remaining_km']:.0f} km")
            print(f"ETA: {row['eta_hours_remaining']:.1f} hours")

            print("\nCOLD CHAIN MONITORING")
            print("-" * 40)
            print(f"Target: {row['temp_min_target_c']:.1f}°C - {row['temp_max_target_c']:.1f}°C")
            print(f"Current Temp: {row['current_temperature_c']:.1f}°C")
            print(f"Humidity: {row['current_humidity_pct']:.1f}%")

            print("\nALERT STATUS")
            print("-" * 40)
            alerts_active = sum([
                row['temperature_alert'], row['humidity_alert'],
                row['long_distance_alert'], row['long_eta_alert'], row['delayed_alert']
            ])

            if alerts_active > 0:
                print(f"ACTIVE ALERTS ({alerts_active}):")
                if row['temperature_alert']: print("  • Temperature excursion")
                if row['long_distance_alert']: print("  • Long distance remaining")
                if row['delayed_alert']: print("  • Delayed status")
            else:
                print("All systems nominal")

            print("\nCOST SUMMARY")
            print("-" * 40)
            print(f"Transport Cost: ₹{row['transport_cost_inr']:,.2f}")
            print("=" * 80)

    def show_history(self, b):
        with self.output:
            clear_output()

            shipment_id = self.shipment_id_input.value.strip().upper()
            shipment = self.ship_df[self.ship_df['shipment_id'] == shipment_id]

            if shipment.empty:
                print("Shipment not found.")
                return

            hist_df = generate_historical_data(shipment.iloc[0])

            fig = make_subplots(rows=2, cols=2, subplot_titles=('Temperature', 'Humidity', 'Vibration', 'Alerts'))

            fig.add_trace(go.Scatter(x=hist_df['timestamp_hours'], y=hist_df['temperature_c'],
                                   mode='lines+markers', name='Temperature', line=dict(color='orange')), row=1, col=1)
            fig.add_hline(y=float(shipment.iloc[0]['temp_min_target_c']), line_dash="dash", line_color="green", row=1, col=1)
            fig.add_hline(y=float(shipment.iloc[0]['temp_max_target_c']), line_dash="dash", line_color="red", row=1, col=1)

            fig.add_trace(go.Scatter(x=hist_df['timestamp_hours'], y=hist_df['humidity_pct'],
                                   mode='lines', name='Humidity', line=dict(color='blue')), row=1, col=2)

            fig.add_trace(go.Scatter(x=hist_df['timestamp_hours'], y=hist_df['vibration_idx'],
                                   mode='lines+markers', name='Vibration', line=dict(color='purple')), row=2, col=1)

            alert_times = hist_df[hist_df['temp_alert'] == 1]['timestamp_hours']
            fig.add_trace(go.Scatter(x=alert_times, y=np.ones(len(alert_times))*0.8, mode='markers',
                                   name='Temp Alerts', marker=dict(color='red', size=10, symbol='x')), row=2, col=2)

            fig.update_layout(height=600, title=f"Sensor History - {shipment_id}")
            fig.show()

    def show_risk_analysis(self, b):
        with self.output:
            clear_output()

            shipment_id = self.shipment_id_input.value.strip().upper()
            shipment = self.ship_df[self.ship_df['shipment_id'] == shipment_id]

            if shipment.empty:
                print("Shipment not found.")
                return

            row = shipment.iloc[0]

            print("RISK ANALYSIS REPORT")
            print("=" * 50)

            temp_risk = min(abs(row['current_temperature_c'] - row['temp_min_target_c']) * 10, 50)
            distance_risk = min(row['distance_remaining_km'] / row['total_distance_km'] * 100, 50)
            eta_risk = min(row['eta_hours_remaining'] / 24 * 50, 50)
            vibration_risk = row['current_vibration_idx'] * 100

            total_risk = (temp_risk + distance_risk + eta_risk + vibration_risk) / 4

            print(f"Temperature Risk:  {temp_risk:.0f}/100")
            print(f"Distance Risk:     {distance_risk:.0f}/100")
            print(f"ETA Risk:          {eta_risk:.0f}/100")
            print(f"Vibration Risk:    {vibration_risk:.0f}/100")
            print(f"TOTAL RISK SCORE:  {total_risk:.0f}/100")

            print("\nRECOMMENDATIONS:")
            if temp_risk > 30: print("• Immediate temperature stabilization required")
            if distance_risk > 40: print("• Consider air transport upgrade")
            if eta_risk > 40: print("• Expedite delivery - ETA critical")
            if row['overall_alert']: print("• ACTION REQUIRED - Multiple alerts active")

    def export_report(self, b):
        shipment_id = self.shipment_id_input.value.strip().upper()
        shipment = self.ship_df[self.ship_df['shipment_id'] == shipment_id]

        if shipment.empty:
            print("No shipment to export.")
            return

        report_df = shipment[['shipment_id', 'medicine_name', 'brand', 'route_id',
                            'route_from', 'route_to', 'transport_mode', 'status',
                            'distance_remaining_km', 'eta_hours_remaining',
                            'current_temperature_c', 'overall_alert']].copy()

        filename = f"shipment_report_{shipment_id.lower()}.csv"
        report_df.to_csv(filename, index=False)
        files.download(filename)
        print(f"Report exported: {filename}")

    def display(self):
        controls = widgets.VBox([
            widgets.HTML("<h3>Detailed Shipment Viewer</h3>"),
            widgets.HBox([self.shipment_id_input, self.view_btn]),
            widgets.HBox([self.history_btn, self.risk_btn, self.export_btn])
        ])
        display(controls, self.output)

detailed_viewer = DetailedShipmentViewer(global_ship_df)
print("Sample shipment IDs: SHP100123, SHP100456")
detailed_viewer.display()
# PART 5/5 FIXED: Enterprise Dashboard & Alerts
# PART 5/5: Enterprise Dashboard with Matplotlib
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd
import ipywidgets as widgets
from IPython.display import display, clear_output
from google.colab import files

plt.style.use('default')
sns.set_palette("husl")

def generate_historical_data(shipment_row, n_points=50):
    duration_hours = float(shipment_row['elapsed_hours'])
    time_points = np.linspace(0, duration_hours, n_points)
    temp_min = float(shipment_row['temp_min_target_c'])
    temp_max = float(shipment_row['temp_max_target_c'])
    base_temp = float(shipment_row['current_temperature_c'])

    historical_data = []
    for t in time_points:
        temp_drift = np.sin(t / 6) * 2
        temp_noise = np.random.normal(0, 0.8)
        hist_temp = base_temp + temp_drift + temp_noise
        humidity = 45 + 0.4 * hist_temp + np.random.normal(0, 8)
        vibration_spikes = [4, 12, 24, 36]
        base_vibration = 0.3
        hist_vibration = base_vibration + (0.3 if any(abs(t - spike) < 1 for spike in vibration_spikes) else 0)

        historical_data.append({
            'timestamp_hours': round(t, 1),
            'temperature_c': round(hist_temp, 2),
            'humidity_pct': round(humidity, 1),
            'vibration_idx': round(hist_vibration, 3),
            'temp_alert': 1 if hist_temp < temp_min or hist_temp > temp_max else 0
        })
    return pd.DataFrame(historical_data)

class DetailedShipmentViewer:
    def __init__(self, ship_df):
        self.ship_df = ship_df
        self.shipment_id_input = widgets.Text(
            placeholder='SHP100123',
            description='Shipment ID:',
            layout=widgets.Layout(width='400px')
        )
        self.view_btn = widgets.Button(description='View Details', button_style='primary')
        self.history_btn = widgets.Button(description='History Graph', button_style='success')
        self.risk_btn = widgets.Button(description='Risk Analysis', button_style='warning')
        self.export_btn = widgets.Button(description='Export Report', button_style='info')
        self.output = widgets.Output()

        self.view_btn.on_click(self.view_shipment)
        self.history_btn.on_click(self.show_history)
        self.risk_btn.on_click(self.show_risk_analysis)
        self.export_btn.on_click(self.export_report)
        self.shipment_id_input.observe(self.on_id_change, names='value')

    def on_id_change(self, change):
        if len(change['new']) > 6:
            self.view_shipment(None)

    def view_shipment(self, b):
        with self.output:
            clear_output()
            shipment_id = self.shipment_id_input.value.strip().upper()
            if not shipment_id.startswith('SHP'):
                print("Enter valid Shipment ID (SHPxxxxx)")
                return

            shipment = self.ship_df[self.ship_df['shipment_id'] == shipment_id]
            if shipment.empty:
                print(f"Shipment {shipment_id} not found")
                return

            row = shipment.iloc[0]
            print("=" * 80)
            print(f"SHIPMENT DETAILS: {shipment_id}")
            print("=" * 80)
            print(f"Route: {row['route_from']} → {row['route_to']} ({row['route_id']})")
            print(f"Medicine: {row['medicine_name']} ({row['brand']})")
            print(f"Transport: {row['transport_mode']} | Status: {row['status']}")
            print(f"Progress: {row['progress_pct']:.1f}% | ETA: {row['eta_hours_remaining']:.1f}h")
            print(f"Temp: {row['current_temperature_c']:.1f}°C (Range: {row['temp_min_target_c']:.1f}-{row['temp_max_target_c']:.1f}°C)")
            print(f"Humidity: {row['current_humidity_pct']:.1f}% | Cost: ₹{row['transport_cost_inr']:,.0f}")

            alerts_active = sum([
                row['temperature_alert'], row['humidity_alert'],
                row['long_distance_alert'], row['long_eta_alert'], row['delayed_alert']
            ])
            status = "🟢 OK" if alerts_active == 0 else f"🔴 {alerts_active} ALERTS"
            print(f"\n{status}")
            print("=" * 80)

    def show_history(self, b):
        with self.output:
            clear_output()
            shipment_id = self.shipment_id_input.value.strip().upper()
            shipment = self.ship_df[self.ship_df['shipment_id'] == shipment_id]
            if shipment.empty:
                print("Shipment not found")
                return

            hist_df = generate_historical_data(shipment.iloc[0])
            row = shipment.iloc[0]

            fig, axes = plt.subplots(2, 2, figsize=(15, 10))
            fig.suptitle(f'Sensor History - Shipment {shipment_id}', fontsize=16, fontweight='bold')

            axes[0,0].plot(hist_df['timestamp_hours'], hist_df['temperature_c'],
                          'orange', linewidth=2, label='Temperature')
            axes[0,0].axhline(y=row['temp_min_target_c'], color='green', linestyle='--',
                             alpha=0.7, label='Min Target')
            axes[0,0].axhline(y=row['temp_max_target_c'], color='red', linestyle='--',
                             alpha=0.7, label='Max Target')
            axes[0,0].fill_between(hist_df['timestamp_hours'], row['temp_min_target_c'],
                                 row['temp_max_target_c'], alpha=0.2, color='green')
            axes[0,0].set_title('Temperature (°C)', fontweight='bold')
            axes[0,0].grid(True, alpha=0.3)
            axes[0,0].legend()

            axes[0,1].plot(hist_df['timestamp_hours'], hist_df['humidity_pct'],
                          'blue', linewidth=2)
            axes[0,1].set_title('Humidity (%)', fontweight='bold')
            axes[0,1].grid(True, alpha=0.3)

            axes[1,0].plot(hist_df['timestamp_hours'], hist_df['vibration_idx'],
                          'purple', linewidth=2)
            axes[1,0].set_title('Vibration Index', fontweight='bold')
            axes[1,0].grid(True, alpha=0.3)

            alert_times = hist_df[hist_df['temp_alert'] == 1]['timestamp_hours']
            if len(alert_times) > 0:
                axes[1,1].scatter(alert_times, np.ones(len(alert_times))*0.8,
                                c='red', s=100, marker='X', zorder=5)
            axes[1,1].set_title('Temperature Alerts', fontweight='bold')
            axes[1,1].set_ylim(0, 1)
            axes[1,1].set_yticks([])
            axes[1,1].grid(True, alpha=0.3)

            plt.tight_layout()
            plt.show()

    def show_risk_analysis(self, b):
        with self.output:
            clear_output()
            shipment_id = self.shipment_id_input.value.strip().upper()
            shipment = self.ship_df[self.ship_df['shipment_id'] == shipment_id]
            if shipment.empty:
                print("Shipment not found")
                return

            row = shipment.iloc[0]
            temp_risk = min(abs(row['current_temperature_c'] - row['temp_min_target_c']) * 10, 50)
            distance_risk = min(row['distance_remaining_km'] / row['total_distance_km'] * 100, 50)
            eta_risk = min(row['eta_hours_remaining'] / 24 * 50, 50)
            vibration_risk = row['current_vibration_idx'] * 100
            total_risk = (temp_risk + distance_risk + eta_risk + vibration_risk) / 4

            fig, ax = plt.subplots(1, 1, figsize=(10, 6))
            risks = ['Temperature', 'Distance', 'ETA', 'Vibration', 'Total']
            risk_values = [temp_risk, distance_risk, eta_risk, vibration_risk, total_risk]
            colors = ['red' if x > 30 else 'orange' if x > 20 else 'green' for x in risk_values]

            bars = ax.bar(risks, risk_values, color=colors, alpha=0.8, edgecolor='black')
            ax.set_title(f'Risk Analysis - Shipment {shipment_id}', fontsize=16, fontweight='bold')
            ax.set_ylabel('Risk Score (0-100)')
            ax.set_ylim(0, 100)

            for bar, value in zip(bars, risk_values):
                height = bar.get_height()
                ax.text(bar.get_x() + bar.get_width()/2., height + 1,
                       f'{value:.0f}', ha='center', va='bottom', fontweight='bold')

            plt.xticks(rotation=45)
            plt.grid(axis='y', alpha=0.3)
            plt.tight_layout()
            plt.show()

            print(f"TOTAL RISK SCORE: {total_risk:.0f}/100")
            if total_risk > 40:
                print("🚨 HIGH RISK - Immediate action required")
            elif total_risk > 20:
                print("⚠️  MEDIUM RISK - Monitor closely")
            else:
                print("🟢 LOW RISK - Normal operation")

    def export_report(self, b):
        shipment_id = self.shipment_id_input.value.strip().upper()
        shipment = self.ship_df[self.ship_df['shipment_id'] == shipment_id]
        if shipment.empty:
            print("No shipment to export")
            return

        filename = f"shipment_{shipment_id.lower()}.csv"
        shipment.to_csv(filename, index=False)
        files.download(filename)
        print(f"Report exported: {filename}")

    def display(self):
        controls = widgets.VBox([
            widgets.HTML("<h3>📦 Detailed Shipment Viewer</h3>"),
            widgets.HBox([self.shipment_id_input, self.view_btn]),
            widgets.HTML("<hr>"),
            widgets.HBox([self.history_btn, self.risk_btn, self.export_btn])
        ])
        display(controls, self.output)

def get_alert_summary(ship_df=global_ship_df):
    return {
        'total_shipments': len(ship_df),
        'active_alerts': ship_df['overall_alert'].sum(),
        'temp_alerts': ship_df['temperature_alert'].sum(),
        'in_transit': len(ship_df[ship_df['status'] == 'In Transit'])
    }

print("🏢 ENTERPRISE DASHBOARD")
print("=" * 50)
alerts = get_alert_summary()
print(f"📊 Total Shipments: {alerts['total_shipments']:,}")
print(f"🚨 Active Alerts: {alerts['active_alerts']:,} ({alerts['active_alerts']/alerts['total_shipments']*100:.1f}%)")
print(f"🚚 In Transit: {alerts['in_transit']:,}")

detailed_viewer = DetailedShipmentViewer(global_ship_df)
detailed_viewer.display()

print("\n🎉 FULL SYSTEM READY")
print("💡 Test with: SHP100123, SHP100456")
