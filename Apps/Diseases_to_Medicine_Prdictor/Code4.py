# ============================================================================
# DEPENDENCIES & SETUP
# ============================================================================

# Install required libraries
try:
    import pandas as pd
    import numpy as np
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.metrics.pairwise import cosine_similarity
    from collections import Counter
    import warnings
except ImportError:
    print("Installing required packages...")
    import subprocess
    subprocess.check_call(['pip', 'install', '-q', 'pandas', 'numpy', 
                          'scikit-learn', 'matplotlib', 'seaborn'])
    import pandas as pd
    import numpy as np
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.metrics.pairwise import cosine_similarity
    from collections import Counter
    import warnings

warnings.filterwarnings('ignore')


# ============================================================================
# DATA LOADING & PREPARATION
# ============================================================================

def load_datasets():
    """
    Upload and load the three required CSV datasets.
    
    Returns:
        tuple: (disease_drug_df, drug_details_df, pharma_price_df)
    """
    from google.colab import files
    
    print("\n" + "="*80)
    print("MEDICINE RECOMMENDATION SYSTEM - DATA UPLOAD")
    print("="*80)
    print("\nPlease upload your 3 CSV files:")
    print("  1. Disease-Drug mapping (1.csv)")
    print("  2. Drug details & ratings (2.csv)")
    print("  3. Pharmaceutical prices (3.csv)\n")
    
    uploaded = files.upload()
    
    # Load datasets
    disease_drug_df = pd.read_csv('1.csv')
    drug_details_df = pd.read_csv('2.csv')
    pharma_price_df = pd.read_csv('3.csv')
    
    return disease_drug_df, drug_details_df, pharma_price_df


def clean_datasets(disease_drug_df, drug_details_df, pharma_price_df):
    """
    Clean and standardize all datasets for consistent processing.
    
    Args:
        disease_drug_df: Disease to drug mapping dataframe
        drug_details_df: Drug ratings and details dataframe
        pharma_price_df: Pharmaceutical products and pricing dataframe
        
    Returns:
        tuple: Cleaned versions of all three dataframes
    """
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
    drug_details_df['drug_name'] = (
        drug_details_df['drug_name'].str.strip().str.lower()
    )
    drug_details_df['medical_condition'] = (
        drug_details_df['medical_condition'].str.strip().str.lower()
    )
    
    # Display loading summary
    print("\n" + "="*80)
    print("DATA LOADING SUMMARY")
    print("="*80)
    print(f"✓ Disease-drug mappings loaded: {len(disease_drug_df):,} records")
    print(f"✓ Drug ratings & details loaded: {len(drug_details_df):,} records")
    print(f"✓ Pharmaceutical products loaded: {len(pharma_price_df):,} records")
    print(f"✓ Unique diseases available: {disease_drug_df['disease'].nunique()}")
    print("="*80 + "\n")
    
    return disease_drug_df, drug_details_df, pharma_price_df


# ============================================================================
# MEDICINE RECOMMENDER CLASS
# ============================================================================

class MedicineRecommender:
    """
    A comprehensive medicine recommendation system that analyzes diseases,
    suggests drugs, provides safety information, and compares prices.
    """
    
    # Class constants
    PRICE_ANALYSIS_KEYS = [
        'min_price', 'max_price', 'avg_price', 
        'median_price', 'count', 'avg_discount'
    ]
    
    RATING_CATEGORIES = {
        'excellent': (8.0, 10.0, 'Highly Rated (8-10)'),
        'good': (6.0, 7.9, 'Good (6-7.9)'),
        'average': (4.0, 5.9, 'Average (4-5.9)'),
        'poor': (0.0, 3.9, 'Low (<4)')
    }
    
    PREGNANCY_SAFETY = {
        'A': '✓ Safe - No risk demonstrated',
        'B': '✓ Probably Safe - No proven risk',
        'C': '⚠️  Use with Caution - Risk cannot be ruled out',
        'D': '⚠️  Positive Evidence of Risk',
        'X': '❌ Contraindicated - Should NOT be used',
        'N': 'Not classified'
    }
    
    def __init__(self, disease_drug_df, drug_details_df, pharma_price_df):
        """
        Initialize the medicine recommender with cleaned datasets.
        
        Args:
            disease_drug_df: Disease to drug mapping
            drug_details_df: Drug ratings and safety information
            pharma_price_df: Pharmaceutical products and pricing
        """
        self.disease_drug_df = disease_drug_df
        self.drug_details_df = drug_details_df
        self.pharma_price_df = pharma_price_df
        self.all_diseases = sorted(disease_drug_df['disease'].unique())
    
    # ------------------------------------------------------------------------
    # DISEASE MATCHING METHODS
    # ------------------------------------------------------------------------
    
    def find_similar_diseases(self, user_input, top_n=5):
        """
        Find diseases similar to user input using fuzzy text matching.
        
        Args:
            user_input: Disease name entered by user
            top_n: Number of similar diseases to return
            
        Returns:
            list: List of tuples containing (disease_name, similarity_score)
        """
        vectorizer = TfidfVectorizer()
        disease_vectors = vectorizer.fit_transform(self.all_diseases)
        input_vector = vectorizer.transform([user_input])
        
        similarities = cosine_similarity(input_vector, disease_vectors)[0]
        top_indices = similarities.argsort()[-top_n:][::-1]
        
        return [(self.all_diseases[i], similarities[i]) for i in top_indices]
    
    # ------------------------------------------------------------------------
    # DRUG INFORMATION METHODS
    # ------------------------------------------------------------------------
    
    def get_drug_details(self, drug_name):
        """
        Retrieve comprehensive details for a specific drug.
        
        Args:
            drug_name: Name of the drug to look up
            
        Returns:
            pandas.Series or None: Drug details if found, None otherwise
        """
        drug_name_lower = drug_name.lower()
        matches = self.drug_details_df[
            self.drug_details_df['drug_name'].str.contains(
                drug_name_lower, na=False, case=False
            )
        ]
        
        return matches.iloc[0] if not matches.empty else None
    
    def get_disease_description(self, disease_name):
        """
        Extract detailed medical description for a disease.
        
        Args:
            disease_name: Name of the disease
            
        Returns:
            str or None: Disease description if available
        """
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
        """
        Find alternative drug options for the same disease.
        
        Args:
            disease_name: Name of the disease
            current_drugs: List of drugs already shown
            
        Returns:
            list: Alternative drug names
        """
        all_drugs = self.disease_drug_df[
            self.disease_drug_df['disease'] == disease_name
        ]['drug'].unique()
        
        alternatives = [
            drug for drug in all_drugs 
            if drug not in current_drugs
        ]
        
        return alternatives[:10]
    
    # ------------------------------------------------------------------------
    # ANALYSIS METHODS
    # ------------------------------------------------------------------------
    
    def calculate_price_statistics(self, medicines_info):
        """
        Analyze pricing data and calculate statistics.
        
        Args:
            medicines_info: List of medicine dictionaries with price data
            
        Returns:
            dict or None: Dictionary with price statistics
        """
        if not medicines_info:
            return None
        
        prices = []
        discounts = []
        
        for medicine in medicines_info:
            price_str = medicine.get('final_price', medicine.get('price', ''))
            
            if isinstance(price_str, str):
                # Extract numeric price value
                price_digits = ''.join(
                    filter(str.isdigit, price_str.split()[0] if price_str else '0')
                )
                if price_digits:
                    prices.append(float(price_digits))
            
            # Extract discount percentage
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
            'avg_discount': (
                sum(discounts) / len(discounts) if discounts else 0
            )
        }
    
    def analyze_manufacturers(self, medicines_info):
        """
        Identify top pharmaceutical manufacturers.
        
        Args:
            medicines_info: List of medicine dictionaries
            
        Returns:
            list: List of tuples (manufacturer_name, product_count)
        """
        if not medicines_info:
            return []
        
        manufacturers = [
            medicine.get('drug_manufacturer', 'N/A')
            for medicine in medicines_info
            if medicine.get('drug_manufacturer')
        ]
        
        return Counter(manufacturers).most_common(5)
    
    def categorize_by_rating(self, drugs_with_details):
        """
        Group drugs by their effectiveness ratings.
        
        Args:
            drugs_with_details: List of drug dictionaries with ratings
            
        Returns:
            dict: Dictionary with rating categories as keys
        """
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
        
        # Return only non-empty categories
        return {
            category: drugs
            for category, drugs in categories.items()
            if drugs
        }
    
    def extract_active_ingredients(self, medicines_info):
        """
        Extract unique active pharmaceutical ingredients.
        
        Args:
            medicines_info: List of medicine dictionaries
            
        Returns:
            list: Sorted list of unique ingredient names
        """
        if not medicines_info:
            return []
        
        ingredients = set()
        
        for medicine in medicines_info:
            generic_name = medicine.get('generic_name', '')
            
            if not generic_name or generic_name == 'N/A':
                continue
            
            # Extract main compounds (up to 3)
            compounds = str(generic_name).split('+')[:3]
            
            for compound in compounds:
                cleaned = compound.strip().split()[0] if compound.strip() else None
                
                if cleaned and len(cleaned) > 3:
                    ingredients.add(cleaned)
        
        return sorted(list(ingredients))[:10]
    
    # ------------------------------------------------------------------------
    # MAIN RECOMMENDATION METHOD
    # ------------------------------------------------------------------------
    
    def get_recommendations(self, disease_name):
        """
        Get comprehensive medicine recommendations for a disease.
        
        Args:
            disease_name: Name of the disease to analyze
            
        Returns:
            tuple: Contains drugs, details, medicines, analyses, etc.
        """
        disease_name = disease_name.strip().lower()
        
        # Try exact match first
        drugs = self.disease_drug_df[
            self.disease_drug_df['disease'] == disease_name
        ]['drug'].unique()
        
        # If no exact match, try fuzzy matching
        if len(drugs) == 0:
            similar = self.find_similar_diseases(disease_name, top_n=1)
            
            if similar[0][1] > 0.3:  # Similarity threshold
                print(
                    f"\n💡 Did you mean '{similar[0][0]}'? "
                    f"(Similarity: {similar[0][1]:.2%})"
                )
                disease_name = similar[0][0]
                drugs = self.disease_drug_df[
                    self.disease_drug_df['disease'] == disease_name
                ]['drug'].unique()
        
        if len(drugs) == 0:
            return (None,) * 9
        
        # Get disease description
        disease_description = self.get_disease_description(disease_name)
        
        # Collect drug details and medicine information
        medicines_info = []
        drugs_with_details = []
        
        for drug in drugs[:25]:  # Limit to 25 drugs
            drug_lower = drug.lower()
            
            # Get drug rating and safety information
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
            
            # Find matching pharmaceutical products
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
        
        # Perform analyses
        price_stats = self.calculate_price_statistics(medicines_info)
        top_manufacturers = self.analyze_manufacturers(medicines_info)
        alternative_drugs = self.get_alternative_drugs(disease_name, drugs[:10])
        categorized_drugs = self.categorize_by_rating(drugs_with_details)
        active_ingredients = self.extract_active_ingredients(medicines_info)
        
        return (
            drugs,
            drugs_with_details,
            medicines_info,
            price_stats,
            top_manufacturers,
            alternative_drugs,
            categorized_drugs,
            disease_description,
            active_ingredients
        )
    
    # ------------------------------------------------------------------------
    # DISPLAY METHODS
    # ------------------------------------------------------------------------
    
    def display_disease_overview(self, disease_name, description):
        """Display disease overview section."""
        if not description:
            return
        
        print("📖 DISEASE OVERVIEW:")
        print("-" * 80)
        print(f"{description}\n")
    
    def display_recommended_drugs(self, drugs):
        """Display list of recommended generic drugs."""
        print(f"📋 RECOMMENDED GENERIC DRUGS ({len(drugs)}):")
        print("-" * 80)
        
        for i, drug in enumerate(drugs[:15], 1):
            print(f"  {i}. {drug.title()}")
    
    def display_categorized_ratings(self, categorized_drugs):
        """Display drugs grouped by rating categories."""
        if not categorized_drugs:
            return
        
        print("\n⭐ DRUGS BY EFFECTIVENESS RATING:")
        print("-" * 80)
        
        for category, drug_list in categorized_drugs.items():
            print(f"\n  {category} ({len(drug_list)} drugs):")
            
            for drug in drug_list[:5]:
                print(
                    f"    • {drug['name'].title()} - "
                    f"Rating: {drug['rating']}/10 "
                    f"({drug['reviews']} reviews)"
                )
    
    def display_safety_information(self, drugs_with_details):
        """Display detailed drug safety and effectiveness."""
        if not drugs_with_details:
            return
        
        print("\n🔬 DETAILED DRUG SAFETY & EFFECTIVENESS:")
        print("-" * 80)
        
        for i, drug_info in enumerate(drugs_with_details[:10], 1):
            print(f"\n  {i}. {drug_info['name'].title()}")
            print(f"     • User Rating: {drug_info['rating']}/10 "
                  f"({drug_info['reviews']} reviews)")
            print(f"     • Activity Level: {drug_info['activity']}%")
            print(f"     • Type: {drug_info['rx_otc']} "
                  f"(Rx=Prescription, OTC=Over-the-counter)")
            
            # Pregnancy safety information
            preg_cat = drug_info['pregnancy_category']
            if preg_cat != 'N/A':
                safety_info = self.PREGNANCY_SAFETY.get(preg_cat, 'N/A')
                print(f"     • Pregnancy Category: {preg_cat} - {safety_info}")
            
            # Alcohol interaction
            if drug_info['alcohol'] != 'N/A':
                interaction = (
                    '⚠️ AVOID - Interacts with alcohol'
                    if drug_info['alcohol'] == 'X'
                    else '✓ No significant interaction'
                )
                print(f"     • Alcohol Interaction: {interaction}")
            
            # Controlled substance warning
            if drug_info['csa'] not in ['N/A', 'N']:
                print(
                    f"     • Controlled Substance: Schedule {drug_info['csa']} "
                    f"(Potential for abuse)"
                )
    
    def display_active_ingredients(self, active_ingredients):
        """Display common active ingredients."""
        if not active_ingredients:
            return
        
        print("\n💊 COMMON ACTIVE INGREDIENTS/COMPOUNDS:")
        print("-" * 80)
        
        for i, ingredient in enumerate(active_ingredients, 1):
            print(f"  {i}. {ingredient}")
    
    def display_price_analysis(self, price_stats):
        """Display comprehensive price analysis."""
        if not price_stats:
            return
        
        print("\n💰 COMPREHENSIVE COST ANALYSIS (Indian Market):")
        print("-" * 80)
        print(f"  • Minimum Price: ₹{price_stats['min_price']:.2f}")
        print(f"  • Maximum Price: ₹{price_stats['max_price']:.2f}")
        print(f"  • Average Price: ₹{price_stats['avg_price']:.2f}")
        print(f"  • Median Price: ₹{price_stats['median_price']:.2f}")
        
        if price_stats['avg_discount'] > 0:
            print(f"  • Average Discount Available: "
                  f"{price_stats['avg_discount']:.1f}%")
        
        print(f"  • Total Products Analyzed: {price_stats['count']}")
        
        price_range = price_stats['max_price'] - price_stats['min_price']
        print(f"  • Price Range: ₹{price_range:.2f}")
    
    def display_manufacturers(self, top_manufacturers):
        """Display top pharmaceutical manufacturers."""
        if not top_manufacturers:
            return
        
        print("\n🏭 TOP PHARMACEUTICAL MANUFACTURERS:")
        print("-" * 80)
        
        for i, (manufacturer, count) in enumerate(top_manufacturers, 1):
            # Clean manufacturer name
            mfr_name = (
                manufacturer.split('*')[-1].strip()
                if '*' in manufacturer
                else manufacturer
            )
            print(f"  {i}. {mfr_name} - {count} products available")
    
    def display_available_products(self, medicines_info):
        """Display available pharmaceutical products."""
        if not medicines_info:
            return
        
        num_products = min(20, len(medicines_info))
        print(f"\n🏥 AVAILABLE PRODUCTS IN INDIA (Top {num_products} products):")
        print("-" * 80)
        
        for i, medicine in enumerate(medicines_info[:20], 1):
            print(f"\n  {i}. {medicine.get('med_name', 'N/A')}")
            print(f"     • Price: "
                  f"{medicine.get('final_price', medicine.get('price', 'N/A'))}")
            print(f"     • Manufacturer: "
                  f"{medicine.get('drug_manufacturer', 'N/A')}")
            print(f"     • Generic Composition: "
                  f"{medicine.get('generic_name', 'N/A')}")
    
    def display_alternatives(self, alternative_drugs):
        """Display alternative drug options."""
        if not alternative_drugs:
            return
        
        print(f"\n🔄 ALTERNATIVE DRUG OPTIONS ({len(alternative_drugs)} available):")
        print("-" * 80)
        print("  Consider these alternatives if primary recommendations "
              "are unavailable:")
        
        for i, alt in enumerate(alternative_drugs[:10], 1):
            print(f"  {i}. {alt.title()}")
    
    def display_prescription_analysis(self, drugs_with_details):
        """Display prescription requirements analysis."""
        if not drugs_with_details:
            return
        
        rx_count = sum(
            1 for d in drugs_with_details 
            if d['rx_otc'] == 'Rx'
        )
        otc_count = sum(
            1 for d in drugs_with_details 
            if d['rx_otc'] == 'OTC'
        )
        
        if rx_count == 0 and otc_count == 0:
            return
        
        print("\n📊 PRESCRIPTION REQUIREMENTS:")
        print("-" * 80)
        print(f"  • Prescription Required (Rx): {rx_count} drugs")
        print(f"  • Over-the-Counter (OTC): {otc_count} drugs")
        
        if rx_count > otc_count:
            print("  ⚠️  Most drugs require doctor's prescription")
        else:
            print("  ✓ Several options available without prescription")
    
    def display_safety_warnings(self):
        """Display comprehensive safety warnings."""
        print("\n⚠️  IMPORTANT SAFETY INFORMATION & PRECAUTIONS:")
        print("-" * 80)
        
        warnings = [
            "ALWAYS consult a qualified healthcare professional before taking any medication",
            "Inform your doctor about ALL current medications and supplements",
            "Check for drug allergies and potential interactions",
            "Pregnant/breastfeeding women must consult doctor before use",
            "Follow prescribed dosage and duration strictly - do NOT self-medicate",
            "Store medicines as per manufacturer instructions",
            "Check expiry dates before consumption",
            "Report any adverse reactions to your healthcare provider immediately",
            "Keep medicines out of reach of children",
            "Do NOT share prescription medications with others"
        ]
        
        for warning in warnings:
            print(f"  • {warning}")
    
    def display_statistics_summary(self, drugs, drugs_with_details, 
                                   medicines_info):
        """Display statistical summary."""
        print("\n📈 STATISTICAL SUMMARY:")
        print("-" * 80)
        print(f"  • Total Generic Drugs Recommended: {len(drugs)}")
        print(f"  • Drugs with User Ratings: {len(drugs_with_details)}")
        print(f"  • Commercial Products Available: {len(medicines_info)}")
        
        unique_mfrs = len(set(
            m.get('drug_manufacturer', '')
            for m in medicines_info
        ))
        print(f"  • Unique Manufacturers: {unique_mfrs}")
        
        # Calculate average rating
        if drugs_with_details:
            rated_drugs = [
                d for d in drugs_with_details 
                if d['rating'] != 'N/A'
            ]
            
            if rated_drugs:
                avg_rating = sum(
                    float(d['rating']) for d in rated_drugs
                ) / len(rated_drugs)
                print(f"  • Average Drug Rating: {avg_rating:.2f}/10")
    
    def show_recommendations(self, disease_name):
        """
        Display comprehensive medicine recommendations for a disease.
        
        This is the main public method that users should call to get
        all recommendations and information about medicines for a disease.
        
        Args:
            disease_name: Name of the disease to analyze
        """
        print(f"\n{'='*80}")
        print(f"COMPREHENSIVE MEDICINE ANALYSIS FOR: {disease_name.upper()}")
        print(f"{'='*80}\n")
        
        # Get all recommendation data
        result = self.get_recommendations(disease_name)
        
        # Handle case where no medicines found
        if result[0] is None:
            print(f"❌ No medicines found for '{disease_name}'")
            print("\n🔍 Showing similar diseases you might be looking for:")
            
            similar = self.find_similar_diseases(disease_name, top_n=5)
            for i, (disease, score) in enumerate(similar, 1):
                if score > 0.1:
                    print(f"  {i}. {disease.title()} (Match: {score:.2%})")
            return
        
        # Unpack results
        (drugs, drugs_with_details, medicines_info, price_stats,
         top_manufacturers, alternative_drugs, categorized_drugs,
         disease_description, active_ingredients) = result
        
        # Display all sections
        self.display_disease_overview(disease_name, disease_description)
        self.display_recommended_drugs(drugs)
        self.display_categorized_ratings(categorized_drugs)
        self.display_safety_information(drugs_with_details)
        self.display_active_ingredients(active_ingredients)
        self.display_price_analysis(price_stats)
        self.display_manufacturers(top_manufacturers)
        self.display_available_products(medicines_info)
        self.display_alternatives(alternative_drugs)
        self.display_prescription_analysis(drugs_with_details)
        self.display_safety_warnings()
        self.display_statistics_summary(drugs, drugs_with_details, medicines_info)
        
        # Footer
        print(f"\n{'-'*80}")
        print("💡 TIP: For best results, consult a healthcare professional "
              "who can provide personalized recommendations")
        print(f"{'-'*80}")


# ============================================================================
# INTERACTIVE INTERFACE
# ============================================================================

def run_interactive_system(recommender):
    """
    Run the interactive medicine recommendation system.
    
    Args:
        recommender: MedicineRecommender instance
    """
    print("\n" + "="*80)
    print("COMPREHENSIVE MEDICINE RECOMMENDATION SYSTEM")
    print("="*80)
    
    # Display feature list
    print("\n🆕 ALL FEATURES INCLUDED:")
    features = [
        "Disease Overview & Description",
        "Drug Ratings & User Reviews (with number of reviews)",
        "Drugs Categorized by Effectiveness Rating",
        "Safety Information (Pregnancy, Alcohol, Controlled Substance)",
        "Comprehensive Cost Analysis (Min/Max/Average/Median/Discount)",
        "Top Pharmaceutical Manufacturers",
        "Common Active Ingredients/Compounds",
        "Alternative Drug Options",
        "Prescription/OTC Classification & Analysis",
        "Activity Level (Drug Popularity)",
        "Detailed Product Listings with Pricing",
        "Statistical Summary",
        "Comprehensive Safety Warnings"
    ]
    
    for feature in features:
        print(f"  ✓ {feature}")
    
    # Show sample diseases
    sample_diseases = recommender.all_diseases[:15]
    sample_text = ', '.join([d.title() for d in sample_diseases])
    print(f"\n📝 Sample diseases available: {sample_text}")
    print(f"💊 Total diseases in database: {len(recommender.all_diseases)}")
    
    # Main interaction loop
    while True:
        print("\n" + "-"*80)
        user_input = input(
            "\n🔍 Enter disease name "
            "(or 'list' to see all diseases, 'quit' to exit): "
        ).strip()
        
        # Handle quit command
        if user_input.lower() in ['quit', 'exit', 'q']:
            print("\n✅ Thank you for using the Comprehensive Medicine "
                  "Recommendation System!")
            print("⚕️  Remember: Always consult healthcare professionals "
                  "for medical advice.")
            break
        
        # Handle list command
        if user_input.lower() == 'list':
            print(f"\n📋 AVAILABLE DISEASES ({len(recommender.all_diseases)}):")
            print("-"*80)
            
            for i, disease in enumerate(sorted(recommender.all_diseases), 1):
                print(f"{i}. {disease.title()}", end="  ")
                if i % 4 == 0:
                    print()
            print("\n")
            continue
        
        # Handle empty input
        if not user_input:
            print("⚠️  Please enter a disease name.")
            continue
        
        # Show recommendations
        recommender.show_recommendations(user_input)
        
        # Ask if user wants to continue
        continue_choice = input(
            "\n\n🔄 Would you like to search for another disease? (yes/no): "
        ).strip().lower()
        
        if continue_choice not in ['yes', 'y']:
            print("\n✅ Thank you for using the Comprehensive Medicine "
                  "Recommendation System!")
            print("⚕️  Remember: Always consult healthcare professionals "
                  "for medical advice.")
            break


# ============================================================================
# MAIN EXECUTION
# ============================================================================

def main():
    """Main execution function."""
    # Load and clean datasets
    disease_drug_df, drug_details_df, pharma_price_df = load_datasets()
    disease_drug_df, drug_details_df, pharma_price_df = clean_datasets(
        disease_drug_df, drug_details_df, pharma_price_df
    )
    
    # Initialize recommender
    recommender = MedicineRecommender(
        disease_drug_df, drug_details_df, pharma_price_df
    )
    
    # Run interactive system
    run_interactive_system(recommender)


# Run the system
if __name__ == "__main__":
    main()
