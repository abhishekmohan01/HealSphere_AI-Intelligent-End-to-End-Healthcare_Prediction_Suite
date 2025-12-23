# 🌸 MindfulMe - Your Personal Wellness Companion

A comprehensive mental wellness tracking application built with Gradio and Plotly that helps you monitor your emotional health, practice mindfulness, and track your wellness journey over time.

![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![Gradio](https://img.shields.io/badge/gradio-latest-orange.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

## ✨ Features

### 📝 Daily Check-In
- Track multiple wellness dimensions: work stress, relationships, physical activity, finances, social interaction, and mental state
- Get a personalized wellness score (0-100) with visual gauge representation
- Receive AI-generated insights based on your inputs
- View interactive visualizations including:
  - Wellness gauge chart
  - Radar chart for life balance
  - Category breakdown bars
  - Mood timeline tracking

### 🧘 Guided Exercises
**Grounding Techniques:**
- 5-4-3-2-1 Sensory Grounding
- Progressive Muscle Relaxation
- Box Breathing (4-4-4-4)

**Journaling Prompts:**
- Gratitude Journal
- Worry Release Journal
- Daily Wins Journal
- Letter to Future Self

### ⏸️ Mindful Breaks
- Personalized break recommendations based on:
  - Current stress level (Low/Medium/High)
  - Available time (Quick/Medium/Deep)
- Activities range from 1-minute breathing exercises to 20-minute walks

### 💭 Affirmations
- Mood-specific affirmations for 7 emotional states:
  - Happy, Excited, Relaxed
  - Stressed, Anxious, Sad, Overthinking
- Curated messages designed to provide comfort and encouragement

### 📊 Wellness History
- Track your progress over time
- Visualize mood patterns and distributions
- Identify your most common emotional states
- View historical trends with interactive charts

### 🆘 Emergency Resources
- Crisis hotlines for India and international locations
- Mental health support resources
- Clear guidance for crisis situations

## 🚀 Installation

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Setup

1. Clone the repository:
```bash
git clone https://github.com/yourusername/mindfulme.git
cd mindfulme
```

2. Install required dependencies:
```bash
pip install gradio plotly pandas
```

3. Run the application:
```bash
python app.py
```

4. Open your browser and navigate to the local URL provided (typically `http://127.0.0.1:7860`)

## 📦 Dependencies

```
gradio>=4.0.0
plotly>=5.0.0
pandas>=1.3.0
```

## 🎯 Usage

### Starting Your Wellness Journey

1. **Complete Your First Check-In:**
   - Navigate to the "Daily Check-In" tab
   - Enter your name
   - Select options for each wellness dimension
   - Click "Submit Check-In" to receive your personalized report

2. **Practice Mindfulness:**
   - Visit the "Guided Exercises" tab
   - Choose between grounding techniques or journaling
   - Follow the step-by-step instructions

3. **Take a Break:**
   - Go to the "Mindful Breaks" tab
   - Select your stress level and available time
   - Get a personalized break recommendation

4. **Track Your Progress:**
   - Use the "Wellness History" tab to view your journey
   - See patterns in your mood over time
   - Identify trends and improvements

## 📊 Data & Privacy

- **Local Storage:** All data is stored in-memory during your session
- **No External Servers:** Your wellness data never leaves your local machine
- **Session-Based:** Data resets when you close the application
- **Privacy First:** No data collection, tracking, or third-party sharing

## 🎨 Visualizations

MindfulMe uses Plotly to create interactive visualizations:
- **Gauge Charts:** Visual representation of overall wellness score
- **Radar Charts:** Multi-dimensional view of life areas
- **Line Graphs:** Mood tracking over time
- **Pie Charts:** Distribution of emotional states
- **Bar Charts:** Category-wise breakdown

## ⚠️ Important Disclaimer

**MindfulMe is a wellness companion tool and NOT a replacement for professional mental health care.** 

- This application is designed for self-reflection and wellness tracking
- It does not provide medical advice, diagnosis, or treatment
- If you're experiencing a mental health crisis, please contact emergency services or the crisis resources listed in the app
- For ongoing mental health concerns, please consult with a licensed mental health professional

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### Ideas for Contributions
- Additional guided exercises
- More affirmations for different moods
- New visualization types
- Export functionality for wellness data
- Mobile-responsive improvements
- Internationalization/localization

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Built with [Gradio](https://gradio.app/) for the interactive interface
- Visualizations powered by [Plotly](https://plotly.com/)
- Crisis resources compiled from verified mental health organizations

## 📧 Support

If you encounter any issues or have suggestions:
- Open an issue on GitHub
- Provide detailed information about the problem
- Include steps to reproduce any bugs

## 🌟 Roadmap

Future enhancements planned:
- [ ] Data export functionality (JSON/CSV)
- [ ] Persistent storage option
- [ ] Multi-language support
- [ ] Mobile app version
- [ ] Integration with wearable devices
- [ ] Customizable affirmations
- [ ] Group/family wellness tracking
- [ ] Professional dashboard for therapists

## 💜 Made with Care by Abhishek Mohan 

MindfulMe was created with the belief that mental wellness should be accessible to everyone. We hope this tool supports you on your journey to better emotional health.

---

**Remember:** Taking care of your mental health is not selfish it's essential. You deserve support, care, and compassion, especially from yourself. 🌸
