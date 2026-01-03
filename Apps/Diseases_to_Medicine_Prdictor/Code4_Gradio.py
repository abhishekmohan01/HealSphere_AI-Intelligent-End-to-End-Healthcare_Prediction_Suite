"""
Comprehensive Medicine Recommendation System with Gradio Interface
==================================================================
A medical recommendation system with an interactive web interface that provides 
detailed drug information, safety data, pricing analysis, and alternative options.

Author: Medical AI Assistant
Date: January 2026
"""

# ============================================================================
# DEPENDENCIES & SETUP
# ============================================================================

import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from collections import Counter
import warnings
import gradio as gr

warnings.filterwarnings('ignore')


# ============================================================================
# DATA LOADING & PREPARATION
# ============================================================================

def clean_datasets(disease_drug_df, drug_details_df, pharma_price_df):
    """Clean and standardize all datasets for consistent processing."""
    # Remove unnamed columns
    for df in [disease_drug_df, drug_details_df, pharma_price_df]:
        df.columns = df.columns.str.strip()
        unnamed_cols = [col for col in df.columns if 'Unnamed' in col]
        df.drop(columns=unnamed_cols, inplace=True, errors='ignore')
    
    # Standardize disease and drug names to lowercase
    disease_drug_df['disease'] = disease_drug_df['disease'].str.strip().str.lower()
    disease_drug_df['drug'] = disease_drug_df['drug'].str.strip().str.lower()
    
    # Extract and standardize disease names in pharma dataset
    pharma_price_df['disease_name'] = (
        pharma_price_df['disease_name']
        .str.extract(r'([A-Za-z\s]+)')[0]
        .str.strip()
        .str.lower()
    )
    
    # Standardize drug details
    drug_details_df['drug_name'] = drug_details_df['drug_name'].str.strip().str.lower()
    drug_details_df['medical_condition'] = drug_details_df['medical_condition'].str.strip().str.lower()
    
    return disease_drug_df, drug_details_df, pharma_price_df


# ============================================================================
# MEDICINE RECOMMENDER CLASS
# ============================================================================

class MedicineRecommender:
    """A comprehensive medicine recommendation system."""
    
    PREGNANCY_SAFETY = {
        'A': '✓ Safe - No risk demonstrated',
        'B': '✓ Probably Safe - No proven risk',
        'C': '⚠️ Use with Caution - Risk cannot be ruled out',
        'D': '⚠️ Positive Evidence of Risk',
        'X': '❌ Contraindicated - Should NOT be used',
        'N': 'Not classified'
    }
    
    def __init__(self, disease_drug_df, drug_details_df, pharma_price_df):
        self.disease_drug_df = disease_drug_df
        self.drug_details_df = drug_details_df
        self.pharma_price_df = pharma_price_df
        self.all_diseases = sorted(disease_drug_df['disease'].unique())
    
    def find_similar_diseases(self, user_input, top_n=5):
        """Find diseases similar to user input using fuzzy text matching."""
        vectorizer = TfidfVectorizer()
        disease_vectors = vectorizer.fit_transform(self.all_diseases)
        input_vector = vectorizer.transform([user_input])
        
        similarities = cosine_similarity(input_vector, disease_vectors)[0]
        top_indices = similarities.argsort()[-top_n:][::-1]
        
        return [(self.all_diseases[i], similarities[i]) for i in top_indices]
    
    def get_drug_details(self, drug_name):
        """Retrieve comprehensive details for a specific drug."""
        drug_name_lower = drug_name.lower()
        matches = self.drug_details_df[
            self.drug_details_df['drug_name'].str.contains(
                drug_name_lower, na=False, case=False
            )
        ]
        return matches.iloc[0] if not matches.empty else None
    
    def get_disease_description(self, disease_name):
        """Extract detailed medical description for a disease."""
        disease_name_lower = disease_name.lower()
        matches = self.drug_details_df[
            self.drug_details_df['medical_condition'].str.contains(
                disease_name_lower, na=False, case=False
            )
        ]
        
        if matches.empty or 'medical_condition_description' not in matches.columns:
            return None
        
        description = matches.iloc[0]['medical_condition_description']
        if description and len(str(description)) > 100:
            return str(description)[:500] + "..."
        return None
    
    def get_alternative_drugs(self, disease_name, current_drugs):
        """Find alternative drug options for the same disease."""
        all_drugs = self.disease_drug_df[
            self.disease_drug_df['disease'] == disease_name
        ]['drug'].unique()
        
        alternatives = [drug for drug in all_drugs if drug not in current_drugs]
        return alternatives[:10]
    
    def calculate_price_statistics(self, medicines_info):
        """Analyze pricing data and calculate statistics."""
        if not medicines_info:
            return None
        
        prices = []
        discounts = []
        
        for medicine in medicines_info:
            price_str = medicine.get('final_price', medicine.get('price', ''))
            
            if isinstance(price_str, str):
                price_digits = ''.join(
                    filter(str.isdigit, price_str.split()[0] if price_str else '0')
                )
                if price_digits:
                    prices.append(float(price_digits))
            
            if 'Save' in str(price_str):
                discount_str = ''.join(
                    filter(str.isdigit, price_str.split('Save')[-1])
                )
                if discount_str:
                    discounts.append(int(discount_str))
        
        if not prices:
            return None
        
        return {
            'min_price': min(prices),
            'max_price': max(prices),
            'avg_price': sum(prices) / len(prices),
            'median_price': sorted(prices)[len(prices) // 2],
            'count': len(prices),
            'avg_discount': sum(discounts) / len(discounts) if discounts else 0
        }
    
    def analyze_manufacturers(self, medicines_info):
        """Identify top pharmaceutical manufacturers."""
        if not medicines_info:
            return []
        
        manufacturers = [
            medicine.get('drug_manufacturer', 'N/A')
            for medicine in medicines_info
            if medicine.get('drug_manufacturer')
        ]
        return Counter(manufacturers).most_common(5)
    
    def categorize_by_rating(self, drugs_with_details):
        """Group drugs by their effectiveness ratings."""
        if not drugs_with_details:
            return {}
        
        categories = {
            'Highly Rated (8-10)': [],
            'Good (6-7.9)': [],
            'Average (4-5.9)': [],
            'Low (<4)': []
        }
        
        for drug in drugs_with_details:
            rating = drug.get('rating', 'N/A')
            if rating == 'N/A':
                continue
            
            try:
                rating_value = float(rating)
                if rating_value >= 8.0:
                    categories['Highly Rated (8-10)'].append(drug)
                elif rating_value >= 6.0:
                    categories['Good (6-7.9)'].append(drug)
                elif rating_value >= 4.0:
                    categories['Average (4-5.9)'].append(drug)
                else:
                    categories['Low (<4)'].append(drug)
            except (ValueError, TypeError):
                continue
        
        return {category: drugs for category, drugs in categories.items() if drugs}
    
    def extract_active_ingredients(self, medicines_info):
        """Extract unique active pharmaceutical ingredients."""
        if not medicines_info:
            return []
        
        ingredients = set()
        for medicine in medicines_info:
            generic_name = medicine.get('generic_name', '')
            if not generic_name or generic_name == 'N/A':
                continue
            
            compounds = str(generic_name).split('+')[:3]
            for compound in compounds:
                cleaned = compound.strip().split()[0] if compound.strip() else None
                if cleaned and len(cleaned) > 3:
                    ingredients.add(cleaned)
        
        return sorted(list(ingredients))[:10]
    
    def get_recommendations(self, disease_name):
        """Get comprehensive medicine recommendations for a disease."""
        disease_name = disease_name.strip().lower()
        
        drugs = self.disease_drug_df[
            self.disease_drug_df['disease'] == disease_name
        ]['drug'].unique()
        
        if len(drugs) == 0:
            similar = self.find_similar_diseases(disease_name, top_n=1)
            if similar[0][1] > 0.3:
                disease_name = similar[0][0]
                drugs = self.disease_drug_df[
                    self.disease_drug_df['disease'] == disease_name
                ]['drug'].unique()
        
        if len(drugs) == 0:
            return (None,) * 9
        
        disease_description = self.get_disease_description(disease_name)
        medicines_info = []
        drugs_with_details = []
        
        for drug in drugs[:25]:
            drug_lower = drug.lower()
            drug_detail = self.get_drug_details(drug)
            
            if drug_detail is not None:
                drugs_with_details.append({
                    'name': drug,
                    'rating': drug_detail.get('rating', 'N/A'),
                    'reviews': drug_detail.get('no_of_reviews', 'N/A'),
                    'activity': drug_detail.get('activity', 'N/A'),
                    'rx_otc': drug_detail.get('rx_otc', 'N/A'),
                    'pregnancy_category': drug_detail.get('pregnancy_category', 'N/A'),
                    'alcohol': drug_detail.get('alcohol', 'N/A'),
                    'csa': drug_detail.get('csa', 'N/A')
                })
            
            matches = self.pharma_price_df[
                self.pharma_price_df['med_name'].str.lower().str.contains(
                    drug_lower, na=False
                ) |
                self.pharma_price_df['generic_name'].str.lower().str.contains(
                    drug_lower, na=False
                )
            ].head(3)
            
            if not matches.empty:
                medicines_info.extend(matches.to_dict('records'))
        
        price_stats = self.calculate_price_statistics(medicines_info)
        top_manufacturers = self.analyze_manufacturers(medicines_info)
        alternative_drugs = self.get_alternative_drugs(disease_name, drugs[:10])
        categorized_drugs = self.categorize_by_rating(drugs_with_details)
        active_ingredients = self.extract_active_ingredients(medicines_info)
        
        return (
            drugs, drugs_with_details, medicines_info, price_stats,
            top_manufacturers, alternative_drugs, categorized_drugs,
            disease_description, active_ingredients
        )
    
    def format_html_output(self, disease_name):
        """Generate formatted HTML output for Gradio interface."""
        result = self.get_recommendations(disease_name)
        
        if result[0] is None:
            similar = self.find_similar_diseases(disease_name, top_n=5)
            html = f"""
            <div style='padding: 30px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                        border-radius: 15px; color: white; text-align: center;'>
                <h2>❌ No medicines found for '{disease_name}'</h2>
                <p style='font-size: 18px; margin-top: 20px;'>🔍 Did you mean one of these?</p>
            </div>
            <div style='padding: 20px; margin-top: 20px; background: white; border-radius: 10px; 
                        box-shadow: 0 4px 6px rgba(0,0,0,0.1);'>
            """
            for i, (disease, score) in enumerate(similar, 1):
                if score > 0.1:
                    html += f"<p style='font-size: 16px; padding: 10px;'>• {disease.title()} (Match: {score:.1%})</p>"
            html += "</div>"
            return html
        
        (drugs, drugs_with_details, medicines_info, price_stats,
         top_manufacturers, alternative_drugs, categorized_drugs,
         disease_description, active_ingredients) = result
        
        # Build HTML output
        html = f"""
        <style>
            .section {{ padding: 25px; margin: 20px 0; border-radius: 12px; 
                       box-shadow: 0 4px 15px rgba(0,0,0,0.1); }}
            .header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                      color: white; padding: 30px; border-radius: 15px; text-align: center; }}
            .drug-card {{ background: #f8f9fa; padding: 15px; margin: 10px 0; 
                         border-left: 4px solid #667eea; border-radius: 8px; }}
            .stat-box {{ display: inline-block; padding: 15px 25px; margin: 10px; 
                        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                        color: white; border-radius: 10px; text-align: center; }}
            .warning {{ background: #fff3cd; border-left: 4px solid #ffc107; 
                       padding: 15px; margin: 10px 0; border-radius: 8px; }}
            .safety-good {{ color: #28a745; font-weight: bold; }}
            .safety-warn {{ color: #ffc107; font-weight: bold; }}
            .safety-bad {{ color: #dc3545; font-weight: bold; }}
        </style>
        
        <div class='header'>
            <h1>💊 {disease_name.upper()}</h1>
            <p style='font-size: 18px; margin-top: 15px;'>Comprehensive Medicine Analysis Report</p>
        </div>
        """
        
        # Disease Overview
        if disease_description:
            html += f"""
            <div class='section' style='background: white;'>
                <h2 style='color: #667eea;'>📖 Disease Overview</h2>
                <p style='font-size: 16px; line-height: 1.8;'>{disease_description}</p>
            </div>
            """
        
        # Statistics Summary
        html += f"""
        <div class='section' style='background: white; text-align: center;'>
            <h2 style='color: #667eea;'>📊 Quick Statistics</h2>
            <div class='stat-box'>
                <div style='font-size: 32px; font-weight: bold;'>{len(drugs)}</div>
                <div>Generic Drugs</div>
            </div>
            <div class='stat-box'>
                <div style='font-size: 32px; font-weight: bold;'>{len(drugs_with_details)}</div>
                <div>With Ratings</div>
            </div>
            <div class='stat-box'>
                <div style='font-size: 32px; font-weight: bold;'>{len(medicines_info)}</div>
                <div>Products Available</div>
            </div>
        </div>
        """
        
        # Categorized Ratings
        if categorized_drugs:
            html += "<div class='section' style='background: white;'><h2 style='color: #667eea;'>⭐ Drugs by Effectiveness Rating</h2>"
            for category, drug_list in categorized_drugs.items():
                html += f"<h3 style='color: #764ba2; margin-top: 20px;'>{category} ({len(drug_list)} drugs)</h3>"
                for drug in drug_list[:5]:
                    html += f"""
                    <div class='drug-card'>
                        <strong>{drug['name'].title()}</strong><br>
                        Rating: {drug['rating']}/10 ({drug['reviews']} reviews) | 
                        Activity: {drug['activity']}%
                    </div>
                    """
            html += "</div>"
        
        # Safety Information
        if drugs_with_details:
            html += "<div class='section' style='background: white;'><h2 style='color: #667eea;'>🔬 Detailed Safety Information</h2>"
            for i, drug_info in enumerate(drugs_with_details[:10], 1):
                safety_class = 'safety-good'
                if drug_info['pregnancy_category'] in ['C', 'D']:
                    safety_class = 'safety-warn'
                elif drug_info['pregnancy_category'] == 'X':
                    safety_class = 'safety-bad'
                
                html += f"""
                <div class='drug-card'>
                    <h4 style='margin: 0; color: #667eea;'>{i}. {drug_info['name'].title()}</h4>
                    <p style='margin: 5px 0;'>
                        <strong>Rating:</strong> {drug_info['rating']}/10 ({drug_info['reviews']} reviews) | 
                        <strong>Type:</strong> {drug_info['rx_otc']}
                    </p>
                """
                
                if drug_info['pregnancy_category'] != 'N/A':
                    safety_info = self.PREGNANCY_SAFETY.get(drug_info['pregnancy_category'], 'N/A')
                    html += f"<p class='{safety_class}'>Pregnancy: {drug_info['pregnancy_category']} - {safety_info}</p>"
                
                if drug_info['alcohol'] == 'X':
                    html += "<p class='safety-warn'>⚠️ Avoid alcohol consumption</p>"
                
                if drug_info['csa'] not in ['N/A', 'N']:
                    html += f"<p class='safety-warn'>⚠️ Controlled Substance: Schedule {drug_info['csa']}</p>"
                
                html += "</div>"
            html += "</div>"
        
        # Price Analysis
        if price_stats:
            html += f"""
            <div class='section' style='background: white;'>
                <h2 style='color: #667eea;'>💰 Comprehensive Cost Analysis</h2>
                <div style='display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 15px;'>
                    <div style='background: #e3f2fd; padding: 20px; border-radius: 10px; text-align: center;'>
                        <div style='font-size: 24px; font-weight: bold; color: #1976d2;'>₹{price_stats['min_price']:.2f}</div>
                        <div>Minimum Price</div>
                    </div>
                    <div style='background: #f3e5f5; padding: 20px; border-radius: 10px; text-align: center;'>
                        <div style='font-size: 24px; font-weight: bold; color: #7b1fa2;'>₹{price_stats['avg_price']:.2f}</div>
                        <div>Average Price</div>
                    </div>
                    <div style='background: #e8f5e9; padding: 20px; border-radius: 10px; text-align: center;'>
                        <div style='font-size: 24px; font-weight: bold; color: #388e3c;'>₹{price_stats['max_price']:.2f}</div>
                        <div>Maximum Price</div>
                    </div>
            """
            if price_stats['avg_discount'] > 0:
                html += f"""
                    <div style='background: #fff3e0; padding: 20px; border-radius: 10px; text-align: center;'>
                        <div style='font-size: 24px; font-weight: bold; color: #f57c00;'>{price_stats['avg_discount']:.1f}%</div>
                        <div>Avg Discount</div>
                    </div>
                """
            html += "</div></div>"
        
        # Active Ingredients
        if active_ingredients:
            html += f"""
            <div class='section' style='background: white;'>
                <h2 style='color: #667eea;'>💊 Common Active Ingredients</h2>
                <div style='display: flex; flex-wrap: wrap; gap: 10px;'>
            """
            for ingredient in active_ingredients:
                html += f"<span style='background: #667eea; color: white; padding: 8px 15px; border-radius: 20px;'>{ingredient}</span>"
            html += "</div></div>"
        
        # Top Manufacturers
        if top_manufacturers:
            html += "<div class='section' style='background: white;'><h2 style='color: #667eea;'>🏭 Top Manufacturers</h2>"
            for i, (mfr, count) in enumerate(top_manufacturers, 1):
                mfr_name = mfr.split('*')[-1].strip() if '*' in mfr else mfr
                html += f"<p style='font-size: 16px; padding: 10px;'>• <strong>{mfr_name}</strong> - {count} products</p>"
            html += "</div>"
        
        # Safety Warnings
        html += """
        <div class='section warning'>
            <h2 style='color: #856404;'>⚠️ Important Safety Information</h2>
            <ul style='line-height: 2;'>
                <li>ALWAYS consult a qualified healthcare professional before taking any medication</li>
                <li>Inform your doctor about ALL current medications and supplements</li>
                <li>Check for drug allergies and potential interactions</li>
                <li>Pregnant/breastfeeding women must consult doctor before use</li>
                <li>Follow prescribed dosage strictly - do NOT self-medicate</li>
                <li>Report any adverse reactions immediately</li>
            </ul>
        </div>
        """
        
        return html


# ============================================================================
# GRADIO INTERFACE
# ============================================================================

def create_gradio_interface(recommender):
    """Create and launch the Gradio web interface."""
    
    def search_disease(disease_input):
        if not disease_input or disease_input.strip() == "":
            return "<div style='padding: 20px; text-align: center;'>⚠️ Please enter a disease name</div>"
        return recommender.format_html_output(disease_input)
    
    def get_disease_suggestions():
        return recommender.all_diseases[:100]
    
    # Custom CSS for better styling
    custom_css = """
    .gradio-container {
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    .header-text {
        text-align: center;
        padding: 20px;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 10px;
        margin-bottom: 20px;
    }
    """
    
    with gr.Blocks(css=custom_css, title="Medicine Recommendation System", theme=gr.themes.Soft()) as demo:
        gr.HTML("""
        <div class='header-text'>
            <h1 style='margin: 0; font-size: 42px;'>💊 Comprehensive Medicine Recommendation System</h1>
            <p style='font-size: 18px; margin-top: 10px;'>Get detailed drug information, safety data, and pricing analysis</p>
        </div>
        """)
        
        with gr.Row():
            with gr.Column(scale=2):
                disease_input = gr.Textbox(
                    label="🔍 Enter Disease Name",
                    placeholder="Type a disease name (e.g., diabetes, hypertension, asthma)...",
                    lines=1
                )
            with gr.Column(scale=1):
                search_btn = gr.Button("Search Medicines", variant="primary", size="lg")
        
        gr.HTML("<p style='text-align: center; color: #666;'>💡 <strong>Tip:</strong> Try diseases like 'diabetes', 'hypertension', 'asthma', 'depression', 'migraine', etc.</p>")
        
        with gr.Accordion("📋 Browse All Available Diseases", open=False):
            disease_list = gr.Dropdown(
                choices=get_disease_suggestions(),
                label=f"Select from {len(recommender.all_diseases)} available diseases",
                interactive=True
            )
            load_btn = gr.Button("Load Selected Disease", variant="secondary")
        
        output = gr.HTML(label="Analysis Results")
        
        # Event handlers
        search_btn.click(fn=search_disease, inputs=disease_input, outputs=output)
        disease_input.submit(fn=search_disease, inputs=disease_input, outputs=output)
        load_btn.click(fn=lambda x: x, inputs=disease_list, outputs=disease_input)
        
        gr.HTML("""
        <div style='margin-top: 30px; padding: 20px; background: #f8f9fa; border-radius: 10px; text-align: center;'>
            <h3>✨ Features Included</h3>
            <div style='display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 15px; margin-top: 20px;'>
                <div>✅ Disease Overview & Description</div>
                <div>⭐ Drug Ratings & Reviews</div>
                <div>🔬 Safety Information</div>
                <div>💰 Comprehensive Cost Analysis</div>
                <div>🏭 Top Manufacturers</div>
                <div>💊 Active Ingredients</div>
                <div>🔄 Alternative Options</div>
                <div>📊 Statistical Summary</div>
            </div>
        </div>
        <div style='margin-top: 20px; text-align: center; color: #666;'>
            <p>⚕️ Remember: This is for informational purposes only. Always consult healthcare professionals for medical advice.</p>
        </div>
        """)
    
    return demo


# ============================================================================
# MAIN EXECUTION
# ============================================================================

def main():
    """Main execution function."""
    print("🚀 Starting Medicine Recommendation System...")
    print("📂 Please upload your CSV files...")
    
    # For Google Colab
    try:
        from google.colab import files
        print("\n" + "="*80)
        print("Please upload your 3 CSV files:")
        print("  1. Disease-Drug mapping (1.csv)")
        print("  2. Drug details & ratings (2.csv)")
        print("  3. Pharmaceutical prices (3.csv)")
        print("="*80 + "\n")
        
        uploaded = files.upload()
        
        disease_drug_df = pd.read_csv('1.csv')
        drug_details_df = pd.read_csv('2.csv')
        pharma_price_df = pd.read_csv('3.csv')
        
    except ImportError:
        # For local execution - modify paths as needed
        print("Running in local mode. Make sure CSV files are in the current directory.")
        disease_drug_df = pd.read_csv('1.csv')
        drug_details_df = pd.read_csv('2.csv')
        pharma_price_df = pd.read_csv('3.csv')
    
    # Clean datasets
    disease_drug_df, drug_details_df, pharma_price_df = clean_datasets(
        disease_drug_df, drug_details_df, pharma_price_df
    )
    
    print(f"\n✅ Data loaded successfully!")
    print(f"   • {len(disease_drug_df):,} disease-drug mappings")
    print(f"   • {len(drug_details_df):,} drug details")
    print(f"   • {len(pharma_price_df):,} pharmaceutical products")
    print(f"   • {disease_drug_df['disease'].nunique()} unique diseases\n")
    
    # Initialize recommender
    recommender = MedicineRecommender(
        disease_drug_df, drug_details_df, pharma_price_df
    )
    
    # Create and launch Gradio interface
    print("🌐 Launching Gradio interface...")
    demo = create_gradio_interface(recommender)
    demo.launch(share=True)  # share=True creates a public link


if __name__ == "__main__":
    main()
