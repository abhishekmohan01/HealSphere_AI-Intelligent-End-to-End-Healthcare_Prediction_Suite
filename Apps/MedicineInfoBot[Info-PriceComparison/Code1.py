import pandas as pd
import numpy as np
import re
from google.colab import files
import matplotlib.pyplot as plt
import seaborn as sns
from IPython.display import display, HTML, clear_output
import ipywidgets as widgets


class MedicineChatbot:
    def __init__(self, data=None):
        """Initialize the chatbot with an optional medicine dataset."""
        if data is not None:
            self.df = data
            print(f"Dataset loaded successfully with {len(self.df)} medicines.")
        else:
            self.create_sample_dataset()

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
        print(f"Sample dataset created with {len(self.df)} medicines.")

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
        """Format search results as HTML."""
        if len(results) == 0:
            return "No medicines found matching your query."

        formatted_results = []
        for _, med in results.iterrows():
            formatted_med = (
                f"<b>{med['medicine_name'].title()} ({med['brand']})</b><br>"
                f"• Manufacturer: {med['manufacturer']}<br>"
                f"• Composition: {med['composition']}<br>"
                f"• Form: {med['dosage_form']} - {med['strength']}<br>"
                f"• Price: ₹{med['price']:.2f}<br>"
                f"• For: {med['indications']}<br>"
                f"• Side Effects: {med['side_effects']}<br>"
                f"• Prescription Required: {med['prescription_required']}<br>"
            )
            formatted_results.append(formatted_med)

        # Summary: cheapest in the result set
        if len(results) > 0:
            cheapest = results.loc[results["price"].idxmin()]
            cheapest_text = (
                "<br><b>Cheapest medicine in these results:</b> "
                f"{cheapest['medicine_name']} ({cheapest['brand']}) - ₹{cheapest['price']:.2f}"
            )
            formatted_results.append(cheapest_text)

        return "<hr>".join(formatted_results)

    def visualize_price_comparison(self, medicine_name: str) -> None:
        """Display a bar chart comparing prices of different brands of a medicine."""
        medicine_name = medicine_name.lower()
        matches = self.df[self.df["medicine_name"].str.lower() == medicine_name]

        if len(matches) > 1:
            plt.figure(figsize=(10, 6))
            sns.barplot(x="brand", y="price", data=matches)
            plt.title(f"Price Comparison for {medicine_name.title()}")
            plt.xlabel("Brand")
            plt.ylabel("Price (₹)")
            plt.xticks(rotation=45)
            plt.tight_layout()
            plt.show()
        else:
            print(f"Not enough data to compare prices for {medicine_name.title()}")


def upload_dataset():
    """Upload a CSV dataset from Colab."""
    uploaded = files.upload()
    if uploaded:
        file_name = next(iter(uploaded.keys()))
        try:
            df = pd.read_csv(file_name)
            print(f"Dataset loaded successfully with {len(df)} medicines.")
            return df
        except Exception as exc:
            print(f"Error loading dataset: {exc}")
            return None
    return None


def create_chatbot_interface():
    """Text-only chatbot interface (console input/output)."""
    print("Would you like to upload a custom medicine dataset? (If not, a sample dataset will be used)")
    choice = input("Enter 'yes' to upload or any key to continue with sample: ")

    if choice.lower() == "yes":
        print("Please upload your CSV file:")
        data = upload_dataset()
        chatbot = MedicineChatbot(data)
    else:
        chatbot = MedicineChatbot()

    print("\n--- Medicine Information Chatbot ---")
    print("You can ask questions like:")
    print("1. What medicines contain paracetamol?")
    print("2. Show me medicines for fever")
    print("3. Compare prices of Paracetamol")
    print("4. What medicines are made by Cipla?")
    print("5. Type 'exit' to quit\n")

    while True:
        query = input("\nEnter your query: ")
        if query.lower() == "exit":
            print("Thank you for using the Medicine Information Chatbot. Goodbye!")
            break

        message, results = chatbot.process_query(query)
        print(f"\n{message}")

        if len(results) > 0:
            for _, med in results.iterrows():
                print("\n" + "=" * 50)
                print(f"{med['medicine_name']} ({med['brand']})")
                print(f"Manufacturer: {med['manufacturer']}")
                print(f"Composition: {med['composition']}")
                print(f"Form: {med['dosage_form']} - {med['strength']}")
                print(f"Price: ₹{med['price']:.2f}")
                print(f"For: {med['indications']}")
                print(f"Side Effects: {med['side_effects']}")
                print(f"Prescription Required: {med['prescription_required']}")

            # Summary: only cheapest (least side-effect part removed as requested)
            cheapest = results.loc[results["price"].idxmin()]
            print("\nCheapest medicine in these results:")
            print(f"- {cheapest['medicine_name']} ({cheapest['brand']}) at ₹{cheapest['price']:.2f}")

            if "price" in query.lower() and len(results) > 1:
                viz_choice = input("\nWould you like to see a price comparison chart? (yes/no): ")
                if viz_choice.lower() == "yes":
                    medicine_name = results.iloc[0]["medicine_name"]
                    chatbot.visualize_price_comparison(medicine_name)
        else:
            print("No medicines found matching your query.")


def create_colab_ui():
    """Widget-based UI for Colab."""
    output = widgets.Output()
    chatbot = MedicineChatbot()

    text_input = widgets.Text(
        description="Query:",
        placeholder="Ask about a medicine...",
        layout=widgets.Layout(width="70%"),
    )

    search_button = widgets.Button(
        description="Search",
        button_style="primary",
        layout=widgets.Layout(width="20%"),
    )

    upload_button = widgets.Button(
        description="Upload Dataset",
        button_style="info",
        layout=widgets.Layout(width="20%"),
    )

    instructions = widgets.HTML(
        value="""
        <h3>Medicine Information Chatbot</h3>
        <p>You can ask questions like:</p>
        <ul>
            <li>What medicines contain paracetamol?</li>
            <li>Show me medicines for fever</li>
            <li>Compare prices of Paracetamol</li>
            <li>What medicines are made by Cipla?</li>
        </ul>
        """
    )

    def on_search_button_clicked(_):
        with output:
            clear_output()
            message, results = chatbot.process_query(text_input.value)
            print(message)
            display(HTML(chatbot.format_results(results)))
            if "price" in text_input.value.lower() and len(results) > 1:
                medicine_name = results.iloc[0]["medicine_name"]
                chatbot.visualize_price_comparison(medicine_name)

    def on_upload_button_clicked(_):
        nonlocal chatbot
        with output:
            clear_output()
            print("Please upload your CSV file:")
            data = upload_dataset()
            if data is not None:
                chatbot = MedicineChatbot(data)

    search_button.on_click(on_search_button_clicked)
    upload_button.on_click(on_upload_button_clicked)

    display(instructions)
    display(widgets.HBox([upload_button]))
    display(widgets.HBox([text_input, search_button]))
    display(output)


print("Running Medicine Information Chatbot...")
try:
    create_colab_ui()
except Exception as exc:
    print(f"Could not create graphical interface: {exc}")
    print("Falling back to text interface...")
    create_chatbot_interface()
