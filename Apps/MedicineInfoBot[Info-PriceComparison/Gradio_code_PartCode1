import pandas as pd
import numpy as np
import re
import matplotlib.pyplot as plt
import seaborn as sns
import gradio as gr
from io import BytesIO
from PIL import Image


class MedicineChatbot:
    def __init__(self, data=None):
        """Initialize the chatbot with an optional medicine dataset."""
        if data is not None:
            self.df = data
            self.dataset_status = f"Dataset loaded successfully with {len(self.df)} medicines."
        else:
            self.create_sample_dataset()
            self.dataset_status = f"Sample dataset created with {len(self.df)} medicines."

    def create_sample_dataset(self):
        """Create a default sample dataset with basic medicine information."""
        data = {
            "medicine_id": list(range(1, 11)),
            "medicine_name": [
                "Paracetamol", "Paracetamol", "Ibuprofen", "Amoxicillin", "Cetirizine",
                "Metformin", "Atorvastatin", "Losartan", "Ciprofloxacin", "Omeprazole"
            ],
            "brand": [
                "Crocin", "Dolo", "Brufen", "Novamox", "Alerid",
                "Glycomet", "Atorva", "Losar", "Ciprobay", "Omez"
            ],
            "manufacturer": [
                "GSK", "Micro Labs", "Abbott", "Cipla", "Cipla",
                "USV", "Zydus", "Unichem", "Bayer", "Dr. Reddy's"
            ],
            "composition": [
                "Paracetamol", "Paracetamol", "Ibuprofen", "Amoxicillin",
                "Cetirizine Hydrochloride", "Metformin Hydrochloride",
                "Atorvastatin Calcium", "Losartan Potassium",
                "Ciprofloxacin Hydrochloride", "Omeprazole"
            ],
            "price": [
                15.50, 20.25, 45.00, 85.30, 35.75,
                42.50, 120.00, 35.25, 65.80, 85.40
            ],
            "dosage_form": [
                "Tablet", "Tablet", "Tablet", "Capsule", "Tablet",
                "Tablet", "Tablet", "Tablet", "Tablet", "Capsule"
            ],
            "strength": [
                "500 mg", "650 mg", "400 mg", "500 mg", "10 mg",
                "500 mg", "10 mg", "50 mg", "500 mg", "20 mg"
            ],
            "indications": [
                "Fever and mild to moderate pain",
                "Fever and mild to moderate pain",
                "Pain fever inflammation",
                "Bacterial infections",
                "Allergies and hay fever",
                "Type 2 diabetes",
                "High cholesterol",
                "Hypertension",
                "Bacterial infections",
                "Acid reflux and ulcers"
            ],
            "side_effects": [
                "Nausea and skin rash",
                "Nausea and skin rash",
                "Stomach upset and dizziness",
                "Diarrhea and rash",
                "Drowsiness and dry mouth",
                "Nausea and diarrhea",
                "Muscle pain and headache",
                "Dizziness and fatigue",
                "Nausea and diarrhea",
                "Headache and diarrhea"
            ],
            "prescription_required": [
                "No", "No", "No", "Yes", "No",
                "Yes", "Yes", "Yes", "Yes", "No"
            ],
        }
        self.df = pd.DataFrame(data)

    def search_medicine(self, query: str) -> pd.DataFrame:
        """Search for medicines that match a free-text query."""
        query = query.lower()
        mask = (
            self.df["medicine_name"].str.lower().str.contains(query) |
            self.df["brand"].str.lower().str.contains(query) |
            self.df["composition"].str.lower().str.contains(query) |
            self.df["indications"].str.lower().str.contains(query)
        )
        return self.df[mask].head(5)

    def find_by_composition(self, composition: str) -> pd.DataFrame:
        """Find medicines matching a given composition."""
        composition = composition.lower()
        return self.df[self.df["composition"].str.lower().str.contains(composition)]

    def find_by_brand(self, brand: str) -> pd.DataFrame:
        """Find medicines from a specific brand."""
        brand = brand.lower()
        return self.df[self.df["brand"].str.lower().str.contains(brand)]

    def find_by_indication(self, indication: str) -> pd.DataFrame:
        """Find medicines for a specific indication."""
        indication = indication.lower()
        return self.df[self.df["indications"].str.lower().str.contains(indication)]

    def compare_prices(self, medicine_name: str) -> pd.DataFrame:
        """Compare prices of different brands for the same medicine."""
        medicine_name = medicine_name.lower()
        matches = self.df[self.df["medicine_name"].str.lower() == medicine_name]
        if len(matches) > 1:
            return matches.sort_values("price")
        return matches

    def process_query(self, query: str):
        """Process a user query and route it to the appropriate search."""
        query = query.lower()

        # Composition-based queries
        if any(word in query for word in ["composition", "contain", "ingredient"]):
            composition_match = re.search(
                r"(?:composition|contain|ingredient)[s\s]*(of|in|for)?\s*([a-zA-Z\s]+)", query
            )
            if composition_match:
                composition = composition_match.group(2).strip()
                return (
                    f"Showing medicines with composition '{composition}':",
                    self.find_by_composition(composition),
                )

        # Brand-based queries
        if any(word in query for word in ["brand", "company", "manufacturer"]):
            brand_match = re.search(
                r"(?:brand|company|manufacturer)[s\s]*(of|from|by)?\s*([a-zA-Z\s]+)", query
            )
            if brand_match:
                brand = brand_match.group(2).strip()
                return (
                    f"Showing medicines from brand '{brand}':",
                    self.find_by_brand(brand),
                )

        # Indication-based queries
        if any(word in query for word in ["treat", "cure", "for", "indication"]):
            indication_match = re.search(
                r"(?:treat|cure|for|indication)[s\s]*(of|like|such as)?\s*([a-zA-Z\s,]+)",
                query,
            )
            if indication_match:
                indication = indication_match.group(2).strip()
                return (
                    f"Showing medicines for treating '{indication}':",
                    self.find_by_indication(indication),
                )

        # Price/compare queries
        if any(word in query for word in ["price", "cost", "cheap", "expensive", "compare"]):
            medicine_match = re.search(
                r"(?:price|cost|cheap|expensive|compare)[s\s]*(of|for)?\s*([a-zA-Z\s]+)",
                query,
            )
            if medicine_match:
                medicine = medicine_match.group(2).strip()
                return (
                    f"Comparing prices for '{medicine}':",
                    self.compare_prices(medicine),
                )

        # Fallback: general text search
        return "Showing relevant medicines for your query:", self.search_medicine(query)

    def format_results(self, results: pd.DataFrame) -> str:
        """Format search results as HTML with better colors and contrast."""
        if len(results) == 0:
            return "<div style='background: #ffe6e6; padding: 20px; border-radius: 10px; border: 2px solid #ff4444;'><h3 style='color: #cc0000; margin:0;'>❌ No medicines found matching your query.</h3></div>"

        formatted_results = []
        for idx, (_, med) in enumerate(results.iterrows(), 1):
            formatted_med = f"""
            <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                        padding: 20px; margin: 15px 0; border-radius: 12px; 
                        box-shadow: 0 4px 6px rgba(0,0,0,0.1); color: white;'>
                <h2 style='margin-top: 0; color: #ffffff; font-size: 24px; border-bottom: 2px solid white; padding-bottom: 10px;'>
                    {idx}. {med['medicine_name'].title()} ({med['brand']})
                </h2>
                <div style='background: rgba(255,255,255,0.2); padding: 15px; border-radius: 8px; margin-top: 10px;'>
                    <p style='font-size: 16px; margin: 8px 0;'><strong>🏭 Manufacturer:</strong> {med['manufacturer']}</p>
                    <p style='font-size: 16px; margin: 8px 0;'><strong>💊 Composition:</strong> {med['composition']}</p>
                    <p style='font-size: 16px; margin: 8px 0;'><strong>📋 Form:</strong> {med['dosage_form']} - {med['strength']}</p>
                    <p style='font-size: 18px; margin: 8px 0; background: #ffd700; color: #000; padding: 8px; border-radius: 5px; display: inline-block;'>
                        <strong>💰 Price: ₹{med['price']:.2f}</strong>
                    </p>
                    <p style='font-size: 16px; margin: 8px 0;'><strong>🎯 For:</strong> {med['indications']}</p>
                    <p style='font-size: 16px; margin: 8px 0;'><strong>⚠️ Side Effects:</strong> {med['side_effects']}</p>
                    <p style='font-size: 16px; margin: 8px 0;'><strong>📝 Prescription Required:</strong> {med['prescription_required']}</p>
                </div>
            </div>
            """
            formatted_results.append(formatted_med)

        # Summary: cheapest in the result set
        if len(results) > 0:
            cheapest = results.loc[results["price"].idxmin()]
            cheapest_text = f"""
            <div style='background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%); 
                        padding: 20px; margin: 15px 0; border-radius: 12px; 
                        box-shadow: 0 6px 12px rgba(0,0,0,0.2); color: white;'>
                <h2 style='margin-top: 0; color: #ffffff; font-size: 22px;'>
                    🏆 Cheapest Medicine in Results
                </h2>
                <p style='font-size: 20px; margin: 10px 0; background: rgba(255,255,255,0.3); padding: 15px; border-radius: 8px;'>
                    <strong>{cheapest['medicine_name'].title()} ({cheapest['brand']})</strong><br>
                    <span style='font-size: 24px; color: #ffff00;'>₹{cheapest['price']:.2f}</span>
                </p>
            </div>
            """
            formatted_results.append(cheapest_text)

        return "".join(formatted_results)

    def visualize_price_comparison(self, medicine_name: str):
        """Display a bar chart comparing prices of different brands of a medicine."""
        medicine_name = medicine_name.lower()
        matches = self.df[self.df["medicine_name"].str.lower() == medicine_name]

        if len(matches) > 1:
            # Set style and create figure
            plt.style.use('seaborn-v0_8-darkgrid')
            fig, ax = plt.subplots(figsize=(12, 7))
            
            # Create bar plot with better colors
            bars = ax.bar(matches['brand'], matches['price'], 
                         color=['#667eea', '#764ba2', '#f093fb', '#4facfe', '#00f2fe'],
                         edgecolor='black', linewidth=2)
            
            # Add value labels on bars
            for bar in bars:
                height = bar.get_height()
                ax.text(bar.get_x() + bar.get_width()/2., height,
                       f'₹{height:.2f}',
                       ha='center', va='bottom', fontsize=12, fontweight='bold')
            
            # Styling
            ax.set_title(f"Price Comparison for {medicine_name.title()}", 
                        fontsize=18, fontweight='bold', pad=20)
            ax.set_xlabel("Brand", fontsize=14, fontweight='bold')
            ax.set_ylabel("Price (₹)", fontsize=14, fontweight='bold')
            ax.tick_params(axis='both', labelsize=12)
            plt.xticks(rotation=45, ha='right')
            
            # Add grid
            ax.grid(True, alpha=0.3, linestyle='--')
            ax.set_axisbelow(True)
            
            plt.tight_layout()
            
            # Save to BytesIO and return as PIL Image
            buf = BytesIO()
            plt.savefig(buf, format='png', dpi=150, bbox_inches='tight', 
                       facecolor='white', edgecolor='none')
            buf.seek(0)
            img = Image.open(buf)
            plt.close(fig)
            return img
        else:
            return None


# Initialize chatbot with sample data
chatbot = MedicineChatbot()


def upload_dataset(file):
    """Handle dataset upload."""
    global chatbot
    if file is not None:
        try:
            df = pd.read_csv(file.name)
            chatbot = MedicineChatbot(df)
            return f"<div style='background: #d4edda; padding: 15px; border-radius: 8px; border: 2px solid #28a745;'><h3 style='color: #155724; margin:0;'>✅ Dataset loaded successfully with {len(df)} medicines!</h3></div>"
        except Exception as e:
            return f"<div style='background: #f8d7da; padding: 15px; border-radius: 8px; border: 2px solid #dc3545;'><h3 style='color: #721c24; margin:0;'>❌ Error loading dataset: {str(e)}</h3></div>"
    return "<div style='background: #fff3cd; padding: 15px; border-radius: 8px; border: 2px solid #ffc107;'><h3 style='color: #856404; margin:0;'>⚠️ No file uploaded. Using sample dataset.</h3></div>"


def search_medicines(query):
    """Handle search query."""
    if not query.strip():
        return "<div style='background: #ffe6e6; padding: 20px; border-radius: 10px; border: 2px solid #ff4444;'><h3 style='color: #cc0000; margin:0;'>⚠️ Please enter a query.</h3></div>", None
    
    message, results = chatbot.process_query(query)
    header = f"<div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 20px; border-radius: 10px; margin-bottom: 20px;'><h2 style='color: white; margin:0; font-size: 24px;'>🔍 {message}</h2></div>"
    formatted_output = header + chatbot.format_results(results)
    
    # Generate chart if it's a price comparison
    chart = None
    if len(results) > 1 and "price" in query.lower():
        medicine_name = results.iloc[0]["medicine_name"]
        chart = chatbot.visualize_price_comparison(medicine_name)
    
    return formatted_output, chart


# Create Gradio interface with custom CSS
custom_css = """
.gradio-container {
    font-family: 'Arial', sans-serif;
}
"""

with gr.Blocks(title="Medicine Information Chatbot", theme=gr.themes.Soft(), css=custom_css) as demo:
    gr.Markdown(
        """
        <div style='text-align: center; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                    padding: 30px; border-radius: 15px; margin-bottom: 20px;'>
            <h1 style='color: white; font-size: 42px; margin: 0;'>💊 Medicine Information Chatbot</h1>
            <p style='color: white; font-size: 18px; margin-top: 10px;'>
                Ask questions about medicines, compare prices, and find alternatives!
            </p>
        </div>
        """
    )
    
    with gr.Row():
        with gr.Column(scale=1):
            gr.Markdown("### 📤 Upload Custom Dataset (Optional)")
            file_input = gr.File(label="Upload CSV File", file_types=[".csv"])
            upload_btn = gr.Button("📥 Load Dataset", variant="primary", size="lg")
            upload_status = gr.HTML("<div style='background: #d1ecf1; padding: 15px; border-radius: 8px; border: 2px solid #0c5460;'><p style='color: #0c5460; margin:0;'>ℹ️ Using sample dataset with 10 medicines.</p></div>")
    
    gr.Markdown("---")
    
    gr.Markdown(
        """
        <div style='background: #e7f3ff; padding: 20px; border-radius: 10px; border-left: 5px solid #2196F3;'>
            <h3 style='color: #1976D2; margin-top: 0;'>🔍 Example Queries:</h3>
            <ul style='font-size: 16px; color: #333;'>
                <li>What medicines contain paracetamol?</li>
                <li>Show me medicines for fever</li>
                <li>Compare prices of Paracetamol</li>
                <li>What medicines are made by Cipla?</li>
            </ul>
        </div>
        """
    )
    
    gr.Markdown("<br>")
    
    with gr.Row():
        query_input = gr.Textbox(
            label="Enter your query",
            placeholder="e.g., medicines for fever",
            lines=2,
            scale=4
        )
        search_btn = gr.Button("🔍 Search", variant="primary", scale=1, size="lg")
    
    gr.Markdown("<br>")
    
    with gr.Row():
        with gr.Column(scale=2):
            output_html = gr.HTML(label="Search Results")
        with gr.Column(scale=1):
            output_chart = gr.Image(label="Price Comparison Chart", type="pil")
    
    # Event handlers
    upload_btn.click(
        fn=upload_dataset,
        inputs=[file_input],
        outputs=[upload_status]
    )
    
    search_btn.click(
        fn=search_medicines,
        inputs=[query_input],
        outputs=[output_html, output_chart]
    )
    
    query_input.submit(
        fn=search_medicines,
        inputs=[query_input],
        outputs=[output_html, output_chart]
    )

# Launch the app with share=True to generate a public link
if __name__ == "__main__":
    demo.launch(share=True, debug=True)
