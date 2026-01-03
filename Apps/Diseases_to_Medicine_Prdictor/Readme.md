# 💊 Comprehensive Medicine Recommendation System

<div align="center">

![Python](https://github.com/abhishekmohan01/HealSphere_AI-Intelligent-End-to-End-Healthcare_Prediction_Suite/blob/main/Apps/Diseases_to_Medicine_Prdictor/Screenshot%202026-01-03%20085131.png)
![Gradio](https://img.shields.io/badge/Gradio-4.0+-orange.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)
![Status](https://img.shields.io/badge/Status-Active-success.svg)

**A powerful medical recommendation system with an interactive web interface that provides detailed drug information, safety data, pricing analysis, and alternative treatment options.**

[Features](#-features) • [Demo](#-demo) • [Installation](#-installation) • [Usage](#-usage) • [Documentation](#-documentation)

</div>

---

## 📋 Table of Contents

- [Overview](#-overview)
- [Features](#-features)
- [Demo](#-demo)
- [Installation](#-installation)
- [Usage](#-usage)
- [Data Requirements](#-data-requirements)
- [System Architecture](#-system-architecture)
- [API Reference](#-api-reference)
- [Screenshots](#-screenshots)
- [Contributing](#-contributing)
- [License](#-license)
- [Disclaimer](#-disclaimer)

---

## 🎯 Overview

The Comprehensive Medicine Recommendation System is an AI-powered healthcare tool designed to help users find relevant medications for various medical conditions. Built with Python and powered by Gradio, it provides:

- 🔍 Intelligent disease matching using NLP
- 💊 Comprehensive drug information and ratings
- 🔬 Detailed safety profiles (pregnancy categories, drug interactions)
- 💰 Real-time pricing analysis from Indian pharmaceutical markets
- 📊 Statistical insights and comparative analysis
- 🌐 Beautiful, responsive web interface

---

## ✨ Features

### 🎨 **User Interface**
- **Beautiful Gradio Web Interface** - Modern, responsive design with gradient themes
- **Real-time Search** - Instant results as you type
- **Disease Browser** - Dropdown with 100+ available diseases
- **Interactive Cards** - Color-coded safety ratings and organized information
- **Public Shareable Link** - Share the application with anyone

### 📊 **Core Functionality**

#### 1. Disease Analysis
- Fuzzy matching for disease names
- Comprehensive disease descriptions
- Similar disease suggestions

#### 2. Drug Information
- **Rating System**: Drugs categorized by effectiveness (8-10, 6-7.9, 4-5.9, <4)
- **User Reviews**: Number of reviews and average ratings
- **Activity Levels**: Drug popularity metrics
- **Prescription Status**: Rx (Prescription) vs OTC (Over-the-counter)

#### 3. Safety Information
- **Pregnancy Categories**: 
  - ✅ Category A/B (Safe/Probably Safe)
  - ⚠️ Category C/D (Caution/Risk)
  - ❌ Category X (Contraindicated)
- **Alcohol Interactions**: Warning for drugs that interact with alcohol
- **Controlled Substances**: DEA schedule classifications
- **Side Effects & Precautions**: Comprehensive safety warnings

#### 4. Pricing Analysis
- Minimum, Maximum, Average, and Median prices
- Discount percentages
- Price range calculations
- Multi-product comparisons

#### 5. Pharmaceutical Intelligence
- **Top Manufacturers**: Leading pharmaceutical companies
- **Active Ingredients**: Chemical compounds and generic names
- **Alternative Options**: 10+ alternative medications
- **Product Availability**: Real products from Indian market

#### 6. Statistical Insights
- Total drugs available
- Rated vs unrated medications
- Commercial products count
- Manufacturer diversity
- Average ratings

---

## 🎬 Demo

### Quick Start
```python
# Run the application
python medicine_recommender_gradio.py
```

### Sample Queries
```
✅ diabetes
✅ hypertension
✅ asthma
✅ depression
✅ migraine
✅ arthritis
```

### Expected Output
The system provides a comprehensive HTML report including:
- Disease overview with medical description
- Categorized drug recommendations
- Safety profiles for each medication
- Pricing analysis with statistics
- Top manufacturers
- Alternative treatment options

---

## 🚀 Installation

### Prerequisites
- Python 3.8 or higher
- pip package manager
- Internet connection (for Gradio sharing)

### Step 1: Clone the Repository
```bash
git clone https://github.com/yourusername/medicine-recommender.git
cd medicine-recommender
```

### Step 2: Install Dependencies
```bash
pip install -r requirements.txt
```

Or install manually:
```bash
pip install pandas numpy scikit-learn gradio
```

### Step 3: Prepare Data Files
Place your CSV files in the project directory:
- `1.csv` - Disease-Drug mapping
- `2.csv` - Drug details & ratings
- `3.csv` - Pharmaceutical prices

---

## 📖 Usage

### For Google Colab

```python
# Upload the script to Colab
# Run the notebook - it will prompt for CSV uploads
# Click the generated public link

!python medicine_recommender_gradio.py
```

### For Local Development

```python
# Ensure CSV files are in the same directory
python medicine_recommender_gradio.py

# Access the interface at:
# Local: http://127.0.0.1:7860
# Public: https://xxxxx.gradio.live (generated automatically)
```

### Using the Interface

1. **Enter Disease Name**: Type in the search box (e.g., "diabetes")
2. **Click Search**: Press Enter or click the "Search Medicines" button
3. **Browse Results**: Scroll through the comprehensive analysis
4. **Try Alternatives**: Use the disease dropdown for other conditions

### Alternative: Browse Mode

1. Click **"📋 Browse All Available Diseases"** accordion
2. Select a disease from the dropdown (100+ options)
3. Click **"Load Selected Disease"**
4. Results appear automatically

---

## 📁 Data Requirements

### File 1: Disease-Drug Mapping (`1.csv`)

| Column | Description | Example |
|--------|-------------|---------|
| disease | Medical condition name | diabetes |
| drug | Generic drug name | metformin |

### File 2: Drug Details (`2.csv`)

| Column | Description | Example |
|--------|-------------|---------|
| drug_name | Drug name | Metformin |
| rating | User rating (0-10) | 8.5 |
| no_of_reviews | Review count | 1250 |
| medical_condition | Condition treated | Diabetes |
| activity | Popularity % | 85 |
| rx_otc | Prescription status | Rx |
| pregnancy_category | Safety category | B |
| alcohol | Alcohol interaction | X |
| csa | Controlled substance | N |
| medical_condition_description | Disease info | Type 2 diabetes is... |

### File 3: Pharmaceutical Products (`3.csv`)

| Column | Description | Example |
|--------|-------------|---------|
| med_name | Product name | Glycomet 500mg |
| disease_name | Condition | Diabetes |
| generic_name | Active ingredients | Metformin |
| drug_manufacturer | Company name | USV Ltd |
| price | List price | ₹25.00 |
| final_price | Sale price | ₹20.00 Save 20% |

---

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Gradio Web Interface                      │
│  ┌───────────┐  ┌───────────┐  ┌────────────────────────┐  │
│  │  Search   │  │  Disease  │  │   Results Display      │  │
│  │   Input   │  │  Browser  │  │   (HTML Formatted)     │  │
│  └───────────┘  └───────────┘  └────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│              MedicineRecommender Class                       │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  Disease Matching (TF-IDF + Cosine Similarity)      │   │
│  │  Drug Information Retrieval                         │   │
│  │  Safety Analysis Engine                             │   │
│  │  Pricing Statistics Calculator                      │   │
│  │  Manufacturer Analysis                              │   │
│  │  HTML Report Generator                              │   │
│  └─────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                    Data Layer (Pandas)                       │
│  ┌──────────────┐  ┌─────────────┐  ┌──────────────────┐  │
│  │   Disease    │  │    Drug     │  │  Pharmaceutical  │  │
│  │   Mapping    │  │   Details   │  │     Products     │  │
│  └──────────────┘  └─────────────┘  └──────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

### Key Components

1. **Frontend Layer**: Gradio interface with custom CSS
2. **Business Logic**: MedicineRecommender class with 20+ methods
3. **Data Processing**: Pandas dataframes with optimized queries
4. **ML Component**: Scikit-learn for text similarity matching

---

## 🔧 API Reference

### MedicineRecommender Class

```python
class MedicineRecommender:
    """Main recommendation engine"""
    
    def __init__(self, disease_drug_df, drug_details_df, pharma_price_df):
        """Initialize with three dataframes"""
        pass
    
    def find_similar_diseases(self, user_input, top_n=5):
        """Find similar diseases using fuzzy matching
        
        Args:
            user_input (str): Disease name to search
            top_n (int): Number of results
            
        Returns:
            list: [(disease_name, similarity_score), ...]
        """
        pass
    
    def get_recommendations(self, disease_name):
        """Get comprehensive recommendations
        
        Args:
            disease_name (str): Disease to analyze
            
        Returns:
            tuple: (drugs, details, medicines, stats, ...)
        """
        pass
    
    def format_html_output(self, disease_name):
        """Generate formatted HTML report
        
        Args:
            disease_name (str): Disease name
            
        Returns:
            str: HTML formatted report
        """
        pass
```

### Helper Functions

```python
def clean_datasets(disease_drug_df, drug_details_df, pharma_price_df):
    """Clean and standardize all datasets"""
    pass

def calculate_price_statistics(medicines_info):
    """Analyze pricing data"""
    pass

def categorize_by_rating(drugs_with_details):
    """Group drugs by effectiveness ratings"""
    pass
```

---

## 📸 Screenshots

### 1. Main Interface
```
╔═══════════════════════════════════════════════════════════╗
║     💊 Comprehensive Medicine Recommendation System       ║
║   Get detailed drug information, safety data, pricing     ║
╚═══════════════════════════════════════════════════════════╝

[🔍 Enter Disease Name: _________________________] [Search]

💡 Tip: Try diseases like 'diabetes', 'hypertension', 'asthma'
```

### 2. Results Display
```
╔═══════════════════════════════════════════════════════════╗
║                    💊 DIABETES                            ║
║          Comprehensive Medicine Analysis Report           ║
╚═══════════════════════════════════════════════════════════╝

📖 Disease Overview
─────────────────────────────────────────────────────────────
Type 2 diabetes is a chronic condition that affects...

📊 Quick Statistics
┌────────────┐  ┌────────────┐  ┌────────────┐
│     45     │  │     38     │  │    156     │
│Generic Drug│  │With Ratings│  │  Products  │
└────────────┘  └────────────┘  └────────────┘
```

---

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

### Reporting Bugs
- Open an issue with detailed description
- Include screenshots if applicable
- Provide steps to reproduce

### Feature Requests
- Explain the feature and its benefits
- Provide use cases
- Consider implementation complexity

### Pull Requests
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### Development Guidelines
- Follow PEP 8 style guide
- Add docstrings to all functions
- Write unit tests for new features
- Update README.md if needed

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

```
MIT License

Copyright (c) 2026 Medicine Recommendation System

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction...
```

---

## ⚠️ Disclaimer

### Important Medical Information

**THIS SOFTWARE IS FOR INFORMATIONAL PURPOSES ONLY**

- ❌ **NOT a substitute** for professional medical advice
- ❌ **NOT for self-diagnosis** or self-medication
- ❌ **NOT validated** by medical regulatory authorities
- ✅ **Always consult** qualified healthcare professionals
- ✅ **Verify information** with licensed pharmacists
- ✅ **Follow prescription** guidelines strictly

### Legal Disclaimer

The creators and contributors of this software:
- Make **NO WARRANTIES** about accuracy or completeness
- Are **NOT LIABLE** for any damages or adverse effects
- **DO NOT ENDORSE** any specific medications or treatments
- **RECOMMEND** consulting licensed medical professionals

### Data Accuracy

- Drug information may be outdated
- Prices are indicative and may vary
- Safety data should be verified with current medical literature
- Always check with local regulatory authorities

---

## 📞 Support

### Get Help

- 📧 **Email**: abhishek5489@outlook.com
- 💬 **Issues**: [GitHub Issues](https://github.com/abhishekmohan01)
- 📖 **Documentation**: [Wiki](https://github.com/abhishekmohan01)
- 🌐 **Website**: [medicinerecommender.com](https://github.com/abhishekmohan01)

### FAQ

**Q: Can I use this for medical diagnosis?**  
A: No, this tool is for informational purposes only. Always consult a doctor.

**Q: How accurate is the pricing data?**  
A: Prices are indicative from the Indian market and may vary by location and time.

**Q: Can I add my own drug database?**  
A: Yes, simply format your data to match the required CSV structure.

**Q: Is internet required?**  
A: Only for sharing the Gradio link. Local use works offline.

**Q: Can I deploy this commercially?**  
A: Check the MIT License terms and ensure compliance with medical regulations.

---

## 🌟 Acknowledgments

- **Scikit-learn** - For TF-IDF and similarity algorithms
- **Gradio** - For the amazing web interface framework
- **Pandas** - For powerful data manipulation
- **Python Community** - For excellent documentation and support
- Made by - ** Abhishek Mohan , vansh Yadav , Vivek Kumar and Team **
---

## 📈 Roadmap

### Version 2.0 (Planned)
- [ ] Multi-language support (Hindi, Tamil, Telugu)
- [ ] Voice search capability
- [ ] Drug interaction checker
- [ ] Dosage calculator
- [ ] Symptom checker integration
- [ ] Export reports as PDF
- [ ] Mobile app version
- [ ] Integration with pharmacy APIs
- [ ] AI chatbot for queries
- [ ] User accounts and history

### Version 3.0 (Future)
- [ ] Blockchain for prescription verification
- [ ] Telemedicine integration
- [ ] Insurance coverage checker
- [ ] Clinical trial information
- [ ] Drug recall alerts
- [ ] Personalized recommendations using ML

---

## 📊 Project Statistics

- **Languages**: Python 100%
- **Lines of Code**: 1,500+
- **Functions**: 25+
- **Data Sources**: 3 CSV files
- **Diseases Covered**: 100+
- **Drugs Analyzed**: 1,000+
- **Products Available**: 5,000+

---

<div align="center">

### ⭐ Star this repository if you found it helpful!

**Made with ❤️ for better healthcare access BY Abhishek Mohan , Vansh Yadav , Vivek Kumar and Team..**

[⬆ Back to Top](#-comprehensive-medicine-recommendation-system)

</div>

---

## 🔐 Security

### Reporting Vulnerabilities
If you discover a security vulnerability, please email mohan.abhishek2001@gmail.com

### Best Practices
- Keep dependencies updated
- Don't expose sensitive patient data
- Use HTTPS in production
- Implement rate limiting
- Regular security audits

---

## 📝 Changelog

### v1.0.0 (January 2026)
- ✨ Initial release
- 🎨 Beautiful Gradio interface
- 🔍 Fuzzy disease matching
- 💊 Comprehensive drug database
- 💰 Pricing analysis
- 🔬 Safety information
- 📊 Statistical insights

---

**Last Updated**: January 2026  
**Maintained By**: Abhishek Mohan , Vansh and Team
**Status**: Active Development
