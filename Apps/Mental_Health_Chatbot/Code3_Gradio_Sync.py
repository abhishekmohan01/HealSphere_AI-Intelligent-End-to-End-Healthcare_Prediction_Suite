import gradio as gr
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import random
import json
import pandas as pd

# ============================================================================
# DATA CLASSES AND LIBRARIES
# ============================================================================

class WellnessProfile:
    """Store and manage user's wellness history"""
    def __init__(self, name="User"):
        self.name = name
        self.sessions = []
        self.total_checkins = 0
    
    def add_session(self, data):
        self.sessions.append({
            "timestamp": datetime.now().isoformat(),
            **data
        })
        self.total_checkins += 1
    
    def get_mood_history(self):
        return self.sessions[-7:] if self.sessions else []
    
    def identify_patterns(self):
        if len(self.sessions) < 3:
            return None
        moods = [s.get("mental_state") for s in self.sessions[-10:]]
        return {
            "most_common_mood": max(set(moods), key=moods.count) if moods else None
        }

# Global profile storage
user_profiles = {}

class AffirmationLibrary:
    """Curated affirmations for different emotional states"""
    affirmations = {
        "Stressed": [
            "This is temporary. I've overcome challenges before. 💪",
            "I am capable of handling what's in front of me, one step at a time.",
            "My worth isn't determined by my productivity. I am enough as I am. 🌟",
            "I choose to focus only on what I can control.",
        ],
        "Anxious": [
            "I am safe in this moment. Right now, I am okay. 🤍",
            "My anxiety is trying to protect me, and I thank it. I am brave.",
            "Worrying won't change the outcome, but my presence of mind will.",
            "I breathe in calm, I breathe out fear. 🫁",
        ],
        "Sad": [
            "It's okay to not be okay. This sadness is valid and temporary. 💙",
            "I deserve kindness, especially from myself.",
            "This pain means I've loved deeply. That's beautiful. 🌸",
            "I'm allowed to rest. Healing happens slowly, and that's okay.",
        ],
        "Overthinking": [
            "My thoughts are not facts. I can observe them without believing them.",
            "I release what I cannot control and trust in the unfolding of life.",
            "Perfectionism is a thief of joy. Good enough is, in fact, enough. ✨",
            "My mind is powerful; today I use it wisely, not against myself.",
        ],
        "Excited": [
            "I embrace this positive energy and let it fuel my day! 🌟",
            "My excitement is valid and beautiful. I celebrate this moment! 🎉",
        ],
        "Happy": [
            "I appreciate this happiness and let it fill my heart. 💛",
            "This joy is a gift. I'm grateful for this feeling. 🌈",
        ],
        "Relaxed": [
            "I embrace this peace and carry it with me. 🕊️",
            "This calm is my natural state. I can return here anytime. 🌊",
        ]
    }
    
    @staticmethod
    def get_affirmation(mood):
        return random.choice(AffirmationLibrary.affirmations.get(mood, AffirmationLibrary.affirmations["Stressed"]))

class MindfulBreakRecommender:
    """Intelligent break recommendations"""
    breaks = {
        "quick": [
            "🫁 Box breathing: Breathe in 4 counts, hold 4, out 4 (1 min)",
            "👁️ 20-20-20 Rule: Every 20 mins, look 20 feet away for 20 secs",
            "🚶 Micro-walk: Just walk around your space for 2 minutes",
            "💧 Hydration pause: Drink water and notice the sensation",
            "🎵 One song break: Play your favorite upbeat song",
        ],
        "medium": [
            "🧘 5-min guided body scan meditation",
            "🌳 Step outside for fresh air, no phone",
            "📝 Brain dump: Write everything on your mind, then discard",
            "🎨 Quick doodle or sketch session",
            "☕ Intentional tea/coffee moment: Savor it fully",
        ],
        "deep": [
            "🕯️ 15-min meditation or breathing practice",
            "🏃 20-min walk or light exercise",
            "📚 Read something inspiring or funny",
            "🎬 Watch a 10-min comedy clip or wholesome video",
            "🤝 Call a friend and genuinely chat",
        ]
    }
    
    @staticmethod
    def recommend(stress_level, available_time="medium"):
        if stress_level == "High":
            category = "deep" if available_time != "quick" else "medium"
        elif stress_level == "Medium":
            category = "medium"
        else:
            category = "quick"
        return random.choice(MindfulBreakRecommender.breaks[category])

class GuidedExercises:
    """Library of guided wellness exercises"""
    grounding = {
        "5_4_3_2_1": {
            "name": "5-4-3-2-1 Grounding Technique",
            "description": "Engage all your senses to anchor yourself in the present moment.",
            "steps": [
                "👀 Name 5 things you can SEE around you",
                "👐 Name 4 things you can TOUCH",
                "👂 Name 3 things you can HEAR",
                "👃 Name 2 things you can SMELL",
                "👅 Name 1 thing you can TASTE",
                "Take a deep breath. You're grounded. 🌿"
            ]
        },
        "progressive_relaxation": {
            "name": "Progressive Muscle Relaxation",
            "description": "Release tension by systematically tensing and relaxing muscles.",
            "steps": [
                "Starting with your toes, tense the muscles for 5 seconds",
                "Release and notice the difference (10 seconds)",
                "Move gradually up: feet → calves → thighs → abs → chest → arms",
                "Finally, do your face and head",
                "Notice the calm spreading through your body. 🧘"
            ]
        },
        "box_breathing": {
            "name": "Box Breathing (4-4-4-4)",
            "description": "Calm your nervous system with rhythmic breathing.",
            "steps": [
                "Breathe IN for 4 counts",
                "HOLD for 4 counts",
                "Breathe OUT for 4 counts",
                "HOLD for 4 counts",
                "Repeat 5 times. Feel the calm. ✨"
            ]
        }
    }
    
    journaling = {
        "gratitude": {
            "name": "Gratitude Journaling",
            "prompt": "Write 3 things you're grateful for today, even small ones. Why does each one matter?"
        },
        "worry_release": {
            "name": "Worry Release Journal",
            "prompt": "Write down your top 3 worries. For each, ask: What can I control? What can't I? Focus only on what's in your power."
        },
        "wins": {
            "name": "Daily Wins Journal",
            "prompt": "What's ONE thing you accomplished or handled today, no matter how small? Celebrate it! 🎉"
        },
        "future_self": {
            "name": "Letter to Your Future Self",
            "prompt": "Write a letter to yourself 1 month from now. What advice would you give? What do you want to achieve?"
        }
    }

# ============================================================================
# CALCULATION FUNCTIONS
# ============================================================================

def calculate_wellbeing_score(job_stress, relationship, activity, finances, social, mental):
    score = 50
    
    if job_stress == "Low": score += 10
    elif job_stress == "High": score -= 10
    
    if relationship in ["In a relationship", "Married"]: score += 5
    
    if activity == "High": score += 10
    elif activity == "Moderate": score += 5
    elif activity == "None": score -= 10
    
    if finances == "Stable": score += 8
    elif finances == "In debt": score -= 10
    elif finances == "Struggling": score -= 5
    
    if social == "High": score += 8
    elif social == "Low": score -= 5
    
    if mental in ["Happy", "Excited", "Relaxed"]: score += 10
    elif mental in ["Sad", "Anxious", "Overthinking", "Stressed"]: score -= 10
    
    return max(0, min(100, score))

def interpret_score(score):
    if score >= 80:
        return "🌈", "Thriving", "Your emotional wellness is strong! Keep nurturing what works."
    elif score >= 60:
        return "💛", "Balanced", "You're doing okay. Small consistent steps matter."
    elif score >= 40:
        return "🤍", "Struggling", "You deserve extra care right now. You're not alone."
    else:
        return "💙", "Crisis", "Please reach out. Crisis support is available 24/7."

def analyze_session(data):
    """Generate personalized insights"""
    insights = []
    
    stress = data.get("job_stress", "")
    activity = data.get("physical_activity", "")
    social = data.get("social_interaction", "")
    mood = data.get("mental_state", "")
    
    if stress == "High" and activity == "None":
        insights.append("📌 High stress + no physical activity is tough. Even a 5-min walk could help! 🚶")
    
    if social == "Low" and mood in ["Sad", "Anxious"]:
        insights.append("📌 Connection is medicine—even a text to a friend can help. 🤝")
    
    if activity in ["Moderate", "High"] and mood in ["Excited", "Happy"]:
        insights.append("📌 Movement = mood boost! Notice how activity lifts your spirit. 💪")
    
    if data.get("financial_status") == "In debt" and mood == "Stressed":
        insights.append("📌 Financial stress is valid. Consider one small action today. 💡")
    
    return insights if insights else ["📌 You're doing well navigating your wellness. Keep going! 🌟"]

# ============================================================================
# VISUALIZATION FUNCTIONS
# ============================================================================

def create_wellness_gauge(score):
    """Create a gauge chart for wellness score"""
    fig = go.Figure(go.Indicator(
        mode = "gauge+number+delta",
        value = score,
        domain = {'x': [0, 1], 'y': [0, 1]},
        title = {'text': "Wellness Score", 'font': {'size': 24, 'color': '#6366f1'}},
        delta = {'reference': 70, 'increasing': {'color': "#10b981"}},
        gauge = {
            'axis': {'range': [None, 100], 'tickwidth': 1, 'tickcolor': "#94a3b8"},
            'bar': {'color': "#6366f1"},
            'bgcolor': "white",
            'borderwidth': 2,
            'bordercolor': "#e2e8f0",
            'steps': [
                {'range': [0, 40], 'color': '#fee2e2'},
                {'range': [40, 60], 'color': '#fef3c7'},
                {'range': [60, 80], 'color': '#dbeafe'},
                {'range': [80, 100], 'color': '#d1fae5'}
            ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': 90
            }
        }
    ))
    
    fig.update_layout(
        paper_bgcolor="white",
        font={'color': "#1e293b", 'family': "Arial"},
        height=400
    )
    return fig

def create_radar_chart(data):
    """Create radar chart for life areas"""
    categories = ['Work Stress\n(Inverted)', 'Physical\nActivity', 'Financial\nHealth', 
                  'Social\nInteraction', 'Mental\nState']
    
    # Convert to scores
    stress_map = {"Low": 80, "Medium": 50, "High": 20}
    activity_map = {"None": 20, "Low": 40, "Moderate": 70, "High": 90}
    finance_map = {"In debt": 20, "Struggling": 50, "Stable": 90}
    social_map = {"Low": 30, "Moderate": 65, "High": 90}
    mental_map = {"Happy": 90, "Excited": 90, "Relaxed": 85, 
                  "Sad": 30, "Anxious": 35, "Overthinking": 40, "Stressed": 30}
    
    values = [
        stress_map.get(data.get("job_stress", "Medium"), 50),
        activity_map.get(data.get("physical_activity", "Low"), 40),
        finance_map.get(data.get("financial_status", "Stable"), 50),
        social_map.get(data.get("social_interaction", "Moderate"), 50),
        mental_map.get(data.get("mental_state", "Happy"), 50)
    ]
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatterpolar(
        r=values,
        theta=categories,
        fill='toself',
        fillcolor='rgba(99, 102, 241, 0.3)',
        line=dict(color='rgb(99, 102, 241)', width=3),
        name='Your Score'
    ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 100],
                tickfont=dict(size=10),
                gridcolor='#e2e8f0'
            ),
            angularaxis=dict(
                tickfont=dict(size=12, color='#475569')
            ),
            bgcolor='#fafafa'
        ),
        showlegend=False,
        title={
            'text': "Life Areas Balance",
            'y':0.95,
            'x':0.5,
            'xanchor': 'center',
            'yanchor': 'top',
            'font': {'size': 20, 'color': '#6366f1'}
        },
        paper_bgcolor='white',
        height=450
    )
    
    return fig

def create_mood_timeline(profile):
    """Create mood history timeline"""
    if not profile.sessions:
        fig = go.Figure()
        fig.add_annotation(
            text="No check-ins yet! Complete your first assessment.",
            xref="paper", yref="paper",
            x=0.5, y=0.5, showarrow=False,
            font=dict(size=16, color="#94a3b8")
        )
        fig.update_layout(height=300, paper_bgcolor='white')
        return fig
    
    sessions = profile.sessions[-10:]
    dates = [datetime.fromisoformat(s['timestamp']).strftime('%m/%d') for s in sessions]
    moods = [s.get('mental_state', 'Unknown') for s in sessions]
    
    # Mood to score mapping
    mood_scores = {
        "Happy": 90, "Excited": 85, "Relaxed": 80,
        "Stressed": 40, "Anxious": 35, "Sad": 30, "Overthinking": 45
    }
    scores = [mood_scores.get(m, 50) for m in moods]
    
    # Mood to color mapping
    mood_colors = {
        "Happy": "#10b981", "Excited": "#f59e0b", "Relaxed": "#3b82f6",
        "Stressed": "#ef4444", "Anxious": "#f97316", "Sad": "#6366f1", "Overthinking": "#8b5cf6"
    }
    colors = [mood_colors.get(m, "#94a3b8") for m in moods]
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=dates,
        y=scores,
        mode='lines+markers',
        line=dict(color='#6366f1', width=3),
        marker=dict(size=12, color=colors, line=dict(width=2, color='white')),
        text=moods,
        hovertemplate='<b>%{text}</b><br>Date: %{x}<br>Score: %{y}<extra></extra>'
    ))
    
    fig.update_layout(
        title={
            'text': "Your Mood Journey",
            'font': {'size': 20, 'color': '#6366f1'}
        },
        xaxis_title="Date",
        yaxis_title="Wellness Score",
        yaxis=dict(range=[0, 100], gridcolor='#e2e8f0'),
        xaxis=dict(gridcolor='#e2e8f0'),
        paper_bgcolor='white',
        plot_bgcolor='#fafafa',
        height=350,
        hovermode='x unified'
    )
    
    return fig

def create_category_bars(data):
    """Create horizontal bar chart for categories"""
    categories = ['Work Stress', 'Physical Activity', 'Financial Health', 'Social Life', 'Mental State']
    
    stress_map = {"Low": 80, "Medium": 50, "High": 20}
    activity_map = {"None": 20, "Low": 40, "Moderate": 70, "High": 90}
    finance_map = {"In debt": 20, "Struggling": 50, "Stable": 90}
    social_map = {"Low": 30, "Moderate": 65, "High": 90}
    mental_map = {"Happy": 90, "Excited": 90, "Relaxed": 85, 
                  "Sad": 30, "Anxious": 35, "Overthinking": 40, "Stressed": 30}
    
    values = [
        stress_map.get(data.get("job_stress", "Medium"), 50),
        activity_map.get(data.get("physical_activity", "Low"), 40),
        finance_map.get(data.get("financial_status", "Stable"), 50),
        social_map.get(data.get("social_interaction", "Moderate"), 50),
        mental_map.get(data.get("mental_state", "Happy"), 50)
    ]
    
    colors = ['#ef4444', '#10b981', '#f59e0b', '#3b82f6', '#8b5cf6']
    
    fig = go.Figure(go.Bar(
        x=values,
        y=categories,
        orientation='h',
        marker=dict(
            color=colors,
            line=dict(color='white', width=2)
        ),
        text=[f"{v}%" for v in values],
        textposition='outside',
        hovertemplate='<b>%{y}</b><br>Score: %{x}%<extra></extra>'
    ))
    
    fig.update_layout(
        title={
            'text': "Category Breakdown",
            'font': {'size': 20, 'color': '#6366f1'}
        },
        xaxis=dict(range=[0, 100], title="Score (%)", gridcolor='#e2e8f0'),
        yaxis=dict(title=""),
        paper_bgcolor='white',
        plot_bgcolor='#fafafa',
        height=400,
        showlegend=False
    )
    
    return fig

def create_mood_distribution(profile):
    """Create pie chart of mood distribution"""
    if not profile.sessions:
        fig = go.Figure()
        fig.add_annotation(
            text="Complete more check-ins to see patterns!",
            xref="paper", yref="paper",
            x=0.5, y=0.5, showarrow=False,
            font=dict(size=14, color="#94a3b8")
        )
        fig.update_layout(height=300, paper_bgcolor='white')
        return fig
    
    moods = [s.get('mental_state', 'Unknown') for s in profile.sessions[-10:]]
    mood_counts = {}
    for mood in moods:
        mood_counts[mood] = mood_counts.get(mood, 0) + 1
    
    colors_map = {
        "Happy": "#10b981", "Excited": "#f59e0b", "Relaxed": "#3b82f6",
        "Stressed": "#ef4444", "Anxious": "#f97316", "Sad": "#6366f1", "Overthinking": "#8b5cf6"
    }
    
    labels = list(mood_counts.keys())
    values = list(mood_counts.values())
    colors = [colors_map.get(m, "#94a3b8") for m in labels]
    
    fig = go.Figure(data=[go.Pie(
        labels=labels,
        values=values,
        hole=.4,
        marker=dict(colors=colors, line=dict(color='white', width=2)),
        textinfo='label+percent',
        textfont=dict(size=12)
    )])
    
    fig.update_layout(
        title={
            'text': "Mood Distribution",
            'font': {'size': 20, 'color': '#6366f1'}
        },
        paper_bgcolor='white',
        height=400,
        showlegend=True,
        legend=dict(orientation="v", yanchor="middle", y=0.5, xanchor="left", x=1.1)
    )
    
    return fig

# ============================================================================
# GRADIO INTERFACE FUNCTIONS
# ============================================================================

def daily_checkin(name, job_stress, relationship, activity, finances, social, mental):
    """Process daily check-in and return results"""
    if not name:
        return "⚠️ Please enter your name!", None, None, None, None, "", ""
    
    # Get or create profile
    if name not in user_profiles:
        user_profiles[name] = WellnessProfile(name)
    
    profile = user_profiles[name]
    
    # Create session data
    session_data = {
        "job_stress": job_stress,
        "relationship": relationship,
        "physical_activity": activity,
        "financial_status": finances,
        "social_interaction": social,
        "mental_state": mental
    }
    
    # Add to profile
    profile.add_session(session_data)
    
    # Calculate score
    score = calculate_wellbeing_score(job_stress, relationship, activity, finances, social, mental)
    emoji, status, msg = interpret_score(score)
    
    # Generate insights
    insights = analyze_session(session_data)
    insights_text = "\n\n".join(insights)
    
    # Get affirmation
    affirmation = AffirmationLibrary.get_affirmation(mental)
    
    # Create result message
    result = f"""
# {emoji} Wellness Report for {name}

## Overall Score: {score}/100 - {status}

{msg}

## 💭 Your Affirmation
{affirmation}

## 🔍 Insights
{insights_text}

---
*Total check-ins: {profile.total_checkins}*
"""
    
    # Create visualizations
    gauge = create_wellness_gauge(score)
    radar = create_radar_chart(session_data)
    bars = create_category_bars(session_data)
    timeline = create_mood_timeline(profile)
    
    return result, gauge, radar, bars, timeline, "", ""

def get_mindful_break(stress_level, time_available):
    """Get mindful break recommendation"""
    suggestion = MindfulBreakRecommender.recommend(stress_level, time_available.lower())
    
    return f"""
## ⏸️ Your Personalized Break

**Current Stress:** {stress_level}  
**Time Available:** {time_available}

### ✨ Recommended Activity:
{suggestion}

---
⏰ **Set a timer and give yourself this gift. You deserve it!** 🎁

Remember: Taking breaks isn't lazy—it's essential self-care that makes you more productive and healthier.
"""

def get_guided_exercise(exercise_type, sub_type):
    """Get guided exercise instructions"""
    if exercise_type == "Grounding Techniques":
        exercises = GuidedExercises.grounding
        if sub_type == "5-4-3-2-1 Technique":
            ex = exercises["5_4_3_2_1"]
        elif sub_type == "Progressive Muscle Relaxation":
            ex = exercises["progressive_relaxation"]
        else:
            ex = exercises["box_breathing"]
        
        steps = "\n\n".join([f"**{i+1}.** {step}" for i, step in enumerate(ex['steps'])])
        
        return f"""
# 🧘 {ex['name']}

{ex['description']}

---

{steps}

---

🌟 **Wonderful! Take your time with this exercise. You're doing great!**
"""
    
    else:  # Journaling
        journals = GuidedExercises.journaling
        if sub_type == "Gratitude Journal":
            jrnl = journals["gratitude"]
        elif sub_type == "Worry Release Journal":
            jrnl = journals["worry_release"]
        elif sub_type == "Daily Wins Journal":
            jrnl = journals["wins"]
        else:
            jrnl = journals["future_self"]
        
        return f"""
# 📝 {jrnl['name']}

## Prompt:
{jrnl['prompt']}

---

💡 **Take your time. Write as much or as little as you'd like in the text box above.**

Remember: There's no right or wrong way to journal. This is your safe space.
"""

def view_history(name):
    """View user's wellness history"""
    if not name or name not in user_profiles:
        return "Please complete a check-in first!", None, None
    
    profile = user_profiles[name]
    
    if not profile.sessions:
        return "No check-ins yet! Start your wellness journey with a daily check-in. 🌱", None, None
    
    # Create summary
    patterns = profile.identify_patterns()
    most_common = patterns["most_common_mood"] if patterns else "N/A"
    
    recent = profile.get_mood_history()
    recent_text = "\n".join([
        f"- **{datetime.fromisoformat(s['timestamp']).strftime('%Y-%m-%d')}**: {s.get('mental_state', 'N/A')}"
        for s in recent[-5:]
    ])
    
    summary = f"""
# 📊 Wellness History for {name}

## Statistics
- **Total Check-ins:** {profile.total_checkins}
- **Most Common Mood:** {most_common}

## Recent Check-ins
{recent_text}

---

Keep checking in regularly to track your patterns and progress! 🌱
"""
    
    timeline = create_mood_timeline(profile)
    distribution = create_mood_distribution(profile)
    
    return summary, timeline, distribution

def get_resources():
    """Get mental health resources"""
    return """
# 🆘 Mental Health Resources

## If you're in crisis, please reach out immediately:

### 🇮🇳 INDIA
- **Call Us:** 8004638881
- **Whatsapp Call:** 9118849274
- **Helpline:** 8090561508
- **Hotline:** 1800-89-14416

### 🌍 INTERNATIONAL
- **Crisis Text Line:** Text HOME to 741741
- **International Hotline:** [https://www.helpguide.org/find-help](https://www.helpguide.org/find-help)

---

## 💙 Remember:
- Your life matters
- This pain is temporary
- You deserve support
- Asking for help is strength, not weakness

---

## 📚 Additional Resources
- **NIMHANS (India):** 080-46110007
- **Mental Health Foundation:** [mentalhealth.org.uk](https://www.mentalhealth.org.uk/)
- **Mind:** [mind.org.uk](https://www.mind.org.uk/)

---

🤍 **You're not alone in this. Professional help is available and effective.** 🤍
"""

# ============================================================================
# GRADIO INTERFACE
# ============================================================================

def create_app():
    with gr.Blocks(theme=gr.themes.Soft(primary_hue="indigo", secondary_hue="pink")) as app:
        
        gr.Markdown("""
        # 🌸 MindfulMe - Your Personal Wellness Companion
        
        Welcome to your emotional wellness journey! Track your mental health, get personalized insights, 
        and access guided exercises and affirmations. 💜
        
        ⚠️ **Important:** This is a wellness companion, not a replacement for professional therapy.
        """)
        
        with gr.Tabs():
            
            # ============================================================================
            # TAB 1: DAILY CHECK-IN
            # ============================================================================
            with gr.Tab("📝 Daily Check-In"):
                gr.Markdown("## Complete your daily wellness check-in")
                
                with gr.Row():
                    with gr.Column(scale=1):
                        name_input = gr.Textbox(label="Your Name", placeholder="Enter your name...")
                        
                        job_stress = gr.Radio(
                            ["Low", "Medium", "High"],
                            label="📊 Work Stress Level",
                            value="Medium"
                        )
                        
                        relationship = gr.Radio(
                            ["Single", "In a relationship", "Married"],
                            label="💕 Relationship Status",
                            value="Single"
                        )
                        
                        activity = gr.Radio(
                            ["None", "Low", "Moderate", "High"],
                            label="🏃 Physical Activity",
                            value="Low"
                        )
                        
                        finances = gr.Radio(
                            ["Stable", "Struggling", "In debt"],
                            label="💰 Financial Status",
                            value="Stable"
                        )
                        
                        social = gr.Radio(
                            ["Low", "Moderate", "High"],
                            label="👥 Social Interaction",
                            value="Moderate"
                        )
                        
                        mental = gr.Radio(
                            ["Happy", "Sad", "Anxious", "Overthinking", "Excited", "Stressed", "Relaxed"],
                            label="🧠 Mental State",
                            value="Happy"
                        )
                        
                        submit_btn = gr.Button("Submit Check-In", variant="primary", size="lg")
                    
                    with gr.Column(scale=2):
                        result_text = gr.Markdown()
                        
                        with gr.Row():
                            gauge_plot = gr.Plot(label="Wellness Score")
                            radar_plot = gr.Plot(label="Life Balance")
                        
                        with gr.Row():
                            bars_plot = gr.Plot(label="Category Breakdown")
                            timeline_plot = gr.Plot(label="Mood Timeline")
                
                submit_btn.click(
                    fn=daily_checkin,
                    inputs=[name_input, job_stress, relationship, activity, finances, social, mental],
                    outputs=[result_text, gauge_plot, radar_plot, bars_plot, timeline_plot, name_input, gr.Textbox(visible=False)]
                )
            
            # ============================================================================
            # TAB 2: GUIDED EXERCISES
            # ============================================================================
            with gr.Tab("🧘 Guided Exercises"):
                gr.Markdown("## Practice mindfulness and grounding techniques")
                
                with gr.Row():
                    with gr.Column():
                        exercise_type = gr.Radio(
                            ["Grounding Techniques", "Journaling"],
                            label="Choose Exercise Type",
                            value="Grounding Techniques"
                        )
                        
                        grounding_choice = gr.Radio(
                            ["5-4-3-2-1 Technique", "Progressive Muscle Relaxation", "Box Breathing"],
                            label="Grounding Techniques",
                            value="5-4-3-2-1 Technique",
                            visible=True
                        )
                        
                        journaling_choice = gr.Radio(
                            ["Gratitude Journal", "Worry Release Journal", "Daily Wins Journal", "Letter to Future Self"],
                            label="Journaling Prompts",
                            value="Gratitude Journal",
                            visible=False
                        )
                        
                        journal_input = gr.Textbox(
                            label="Your Journal Entry",
                            placeholder="Write your thoughts here...",
                            lines=8,
                            visible=False
                        )
                        
                        exercise_btn = gr.Button("Get Exercise", variant="primary")
                        
                        def update_exercise_visibility(exercise_type):
                            if exercise_type == "Grounding Techniques":
                                return gr.update(visible=True), gr.update(visible=False), gr.update(visible=False)
                            else:
                                return gr.update(visible=False), gr.update(visible=True), gr.update(visible=True)
                        
                        exercise_type.change(
                            fn=update_exercise_visibility,
                            inputs=[exercise_type],
                            outputs=[grounding_choice, journaling_choice, journal_input]
                        )
                    
                    with gr.Column():
                        exercise_output = gr.Markdown()
                
                def get_exercise_wrapper(ex_type, ground_choice, journal_choice):
                    sub_choice = ground_choice if ex_type == "Grounding Techniques" else journal_choice
                    return get_guided_exercise(ex_type, sub_choice)
                
                exercise_btn.click(
                    fn=get_exercise_wrapper,
                    inputs=[exercise_type, grounding_choice, journaling_choice],
                    outputs=[exercise_output]
                )
            
            # ============================================================================
            # TAB 3: MINDFUL BREAKS
            # ============================================================================
            with gr.Tab("⏸️ Mindful Breaks"):
                gr.Markdown("## Get personalized break recommendations")
                
                with gr.Row():
                    with gr.Column():
                        stress_level = gr.Radio(
                            ["Low", "Medium", "High"],
                            label="Current Stress Level",
                            value="Medium"
                        )
                        
                        time_available = gr.Radio(
                            ["Quick", "Medium", "Deep"],
                            label="Time Available",
                            value="Medium"
                        )
                        
                        break_btn = gr.Button("Get Break Recommendation", variant="primary")
                    
                    with gr.Column():
                        break_output = gr.Markdown()
                
                break_btn.click(
                    fn=get_mindful_break,
                    inputs=[stress_level, time_available],
                    outputs=[break_output]
                )
            
            # ============================================================================
            # TAB 4: AFFIRMATIONS
            # ============================================================================
            with gr.Tab("💭 Affirmations"):
                gr.Markdown("## Get personalized affirmations for your mood")
                
                with gr.Row():
                    with gr.Column():
                        affirmation_mood = gr.Radio(
                            ["Happy", "Sad", "Anxious", "Overthinking", "Excited", "Stressed", "Relaxed"],
                            label="Current Mood",
                            value="Happy"
                        )
                        
                        affirmation_btn = gr.Button("Get Affirmation", variant="primary")
                    
                    with gr.Column():
                        affirmation_output = gr.Markdown()
                
                def get_affirmation_wrapper(mood):
                    affirmation = AffirmationLibrary.get_affirmation(mood)
                    return f"""
# 💭 Your Affirmation

## For when you're feeling {mood}:

### {affirmation}

---

💡 **Pro tip:** Read this aloud to yourself. Say it with conviction. You deserve to believe it.

Take a deep breath and let these words sink in. 🌟
"""
                
                affirmation_btn.click(
                    fn=get_affirmation_wrapper,
                    inputs=[affirmation_mood],
                    outputs=[affirmation_output]
                )
            
            # ============================================================================
            # TAB 5: WELLNESS HISTORY
            # ============================================================================
            with gr.Tab("📊 Wellness History"):
                gr.Markdown("## Track your progress over time")
                
                with gr.Row():
                    with gr.Column():
                        history_name = gr.Textbox(label="Your Name", placeholder="Enter your name...")
                        history_btn = gr.Button("View History", variant="primary")
                    
                    with gr.Column():
                        history_output = gr.Markdown()
                
                with gr.Row():
                    history_timeline = gr.Plot(label="Mood Timeline")
                    history_distribution = gr.Plot(label="Mood Distribution")
                
                history_btn.click(
                    fn=view_history,
                    inputs=[history_name],
                    outputs=[history_output, history_timeline, history_distribution]
                )
            
            # ============================================================================
            # TAB 6: EMERGENCY RESOURCES
            # ============================================================================
            with gr.Tab("🆘 Resources"):
                gr.Markdown(get_resources())
        
        gr.Markdown("""
        ---
        
        ### 💙 About MindfulMe
        
        MindfulMe is your personal wellness companion designed to help you:
        - Track your emotional patterns
        - Access guided mindfulness exercises
        - Get personalized affirmations
        - Learn healthy coping strategies
        - Monitor your mental health journey
        
        **Remember:** This tool is for wellness support, not a replacement for professional mental health care.
        If you're in crisis, please reach out to the resources in the Resources tab immediately.
        
        ---
        
        *Made with 💜 for your wellbeing*
        """)
    
    return app

# ============================================================================
# LAUNCH APP
# ============================================================================

if __name__ == "__main__":
    app = create_app()
    app.launch(share=True)  # share=True generates a public Gradio link
