import random
import time
from datetime import datetime, timedelta
import json
import os

# ============================================================================
# ADVANCED MENTAL HEALTH CHATBOT WITH PREMIUM FEATURES
# ============================================================================

TYPE_SPEED = 0.02
LINE_DELAY = 0.8

class WellnessProfile:
    """Store and manage user's wellness history and patterns"""
    def __init__(self, name):
        self.name = name
        self.sessions = []
        self.total_checkins = 0
        self.streak = 0
        self.favorite_suggestions = {}
        self.mood_patterns = {}

    def add_session(self, data):
        self.sessions.append({
            "timestamp": datetime.now().isoformat(),
            **data
        })
        self.total_checkins += 1

    def get_mood_history(self):
        """Return last 7 check-ins for mood tracking"""
        return self.sessions[-7:] if self.sessions else []

    def identify_patterns(self):
        """Analyze patterns from user's history"""
        if len(self.sessions) < 3:
            return None

        patterns = {
            "most_common_mood": None,
            "most_stressful_day": None,
            "best_coping_strategy": None,
            "improvement_areas": []
        }

        # Most common mood
        moods = [s.get("mental_state") for s in self.sessions[-10:]]
        patterns["most_common_mood"] = max(set(moods), key=moods.count) if moods else None

        # Stress patterns
        stresses = [s.get("job_stress") for s in self.sessions[-10:]]
        patterns["most_stressful_day"] = max(set(stresses), key=stresses.count) if stresses else None

        return patterns

    def to_dict(self):
        return {
            "name": self.name,
            "total_checkins": self.total_checkins,
            "sessions": self.sessions[-30:]  # Keep last 30 sessions
        }


class MindfulBreakRecommender:
    """Intelligent break recommendations based on context"""
    
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
    def recommend(stress_level, available_time=None):
        """Recommend break based on stress and availability"""
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
        "Low Energy": [
            "Rest is not laziness. Rest is medicine. 🌙",
            "I honor my body's signals and give it what it needs.",
            "Small progress is still progress. I celebrate tiny steps. 🎉",
            "I am doing the best I can with what I have. That's beautiful.",
        ],
    }

    @staticmethod
    def get_affirmation(mood):
        if mood in AffirmationLibrary.affirmations:
            return random.choice(AffirmationLibrary.affirmations[mood])
        return random.choice(AffirmationLibrary.affirmations["Stressed"])


class MoodAnalytics:
    """Analyze emotional patterns and provide insights"""

    @staticmethod
    def analyze_session(data):
        """Generate personalized insights from a single session"""
        insights = []

        stress = data.get("job_stress", "")
        activity = data.get("physical_activity", "")
        social = data.get("social_interaction", "")
        mood = data.get("mental_state", "")

        if stress == "High" and activity == "None":
            insights.append(
                "📌 Insight: High stress + no physical activity is a tough combo. "
                "Even a 5-min walk could help reset your nervous system. 🚶"
            )

        if social == "Low" and mood in ["Sad", "Anxious"]:
            insights.append(
                "📌 Insight: You're feeling down and isolating. "
                "Connection is medicine—even a text to a friend can help. 🤝"
            )

        if activity in ["Moderate", "High"] and mood in ["Excited", "Happy"]:
            insights.append(
                "📌 Insight: Movement = mood boost! "
                "Notice how activity lifts your spirit. Keep it up! 💪"
            )

        if data.get("financial_status") == "In debt" and mood == "Stressed":
            insights.append(
                "📌 Insight: Financial stress is real and valid. "
                "Consider one small action: a budget review, or reaching out for help. 💡"
            )

        return insights if insights else [
            "📌 You're doing well navigating your wellness. Keep going! 🌟"
        ]

    @staticmethod
    def generate_weekly_summary(sessions):
        """Generate insights from multiple sessions"""
        if len(sessions) < 3:
            return "Keep checking in! Patterns emerge after a few sessions. 📊"

        moods = [s.get("mental_state") for s in sessions]
        mood_counts = {}
        for mood in moods:
            mood_counts[mood] = mood_counts.get(mood, 0) + 1

        most_frequent = max(mood_counts, key=mood_counts.get)

        summary = f"📊 **Weekly Pattern:**\n"
        summary += f"Most frequent mood: **{most_frequent}** ({mood_counts[most_frequent]} times)\n"

        if most_frequent in ["Stressed", "Anxious", "Sad"]:
            summary += "💙 This week had challenges, and you showed up. That takes courage.\n"
        else:
            summary += "🌟 You're maintaining positive energy this week. Wonderful!\n"

        return summary


def print_with_delay(text, delay=LINE_DELAY, type_speed=TYPE_SPEED):
    for char in text:
        print(char, end="", flush=True)
        time.sleep(type_speed)
    print()
    time.sleep(delay)


def ask_choice(question, options):
    options_display = " / ".join(options)
    while True:
        answer = input(f"\n{question}\n({options_display}): ").strip().title()
        for opt in options:
            if answer.lower() == opt.lower():
                return opt
        print_with_delay("❌ I didn't catch that. Please choose one of the options. 💛")


def calculate_wellbeing_score(job_stress, relationship, activity, finances, social, mental):
    score = 50

    if job_stress == "Low":
        score += 10
    elif job_stress == "High":
        score -= 10

    if relationship in ["In a relationship", "Married"]:
        score += 5

    if activity == "High":
        score += 10
    elif activity == "Moderate":
        score += 5
    elif activity == "None":
        score -= 10

    if finances == "Stable":
        score += 8
    elif finances == "In debt":
        score -= 10
    elif finances == "Struggling":
        score -= 5

    if social == "High":
        score += 8
    elif social == "Low":
        score -= 5

    if mental in ["Happy", "Excited", "Relaxed"]:
        score += 10
    elif mental in ["Sad", "Anxious", "Overthinking", "Stressed"]:
        score -= 10

    return max(0, min(100, score))


def interpret_score(score):
    if score >= 80:
        emoji, status = "🌈", "Thriving"
        msg = "Your emotional wellness is strong! Keep nurturing what works."
    elif score >= 60:
        emoji, status = "💛", "Balanced"
        msg = "You're doing okay. Small consistent steps matter."
    elif score >= 40:
        emoji, status = "🤍", "Struggling"
        msg = "You deserve extra care right now. You're not alone."
    else:
        emoji, status = "💙", "Crisis"
        msg = "Please reach out. Crisis support is available 24/7."

    return emoji, status, msg


def display_main_menu():
    print("\n" + "="*60)
    print_with_delay("🌸 MAIN MENU 🌸", delay=0.3)
    print("="*60)
    print("1️⃣  Daily Check-in")
    print("2️⃣  Guided Exercises")
    print("3️⃣  Affirmations & Motivation")
    print("4️⃣  Mindful Breaks")
    print("5️⃣  Journaling Prompts")
    print("6️⃣  View Your Wellness History")
    print("7️⃣  Emergency Resources")
    print("8️⃣  Exit")
    print("="*60)

    choice = input("\nChoose an option (1-8): ").strip()
    return choice


def run_daily_checkin(profile):
    """Run the daily emotional check-in"""
    print_with_delay("🌸 Let's check in with your wellness today! 🌸")

    options_stress = ["Low", "Medium", "High"]
    options_relationship = ["Single", "In a relationship", "Married"]
    options_activity = ["None", "Low", "Moderate", "High"]
    options_financial = ["Stable", "Struggling", "In debt"]
    options_social = ["Low", "Moderate", "High"]
    options_mental = ["Happy", "Sad", "Anxious", "Overthinking", "Excited", "Stressed", "Relaxed"]

    job_stress = ask_choice("📊 Work stress level?", options_stress)
    relationship = ask_choice("💕 Relationship status?", options_relationship)
    activity = ask_choice("🏃 Physical activity today?", options_activity)
    finances = ask_choice("💰 Financial status?", options_financial)
    social = ask_choice("👥 Social interaction?", options_social)
    mental = ask_choice("🧠 Mental state?", options_mental)

    # Store session
    session_data = {
        "job_stress": job_stress,
        "relationship": relationship,
        "physical_activity": activity,
        "financial_status": finances,
        "social_interaction": social,
        "mental_state": mental
    }
    profile.add_session(session_data)

    score = calculate_wellbeing_score(job_stress, relationship, activity, finances, social, mental)
    emoji, status, msg = interpret_score(score)

    print_with_delay(f"\n{emoji} **Well-being Score: {score}/100 ({status})**")
    print_with_delay(msg)

    # Show insights
    insights = MoodAnalytics.analyze_session(session_data)
    for insight in insights:
        print_with_delay(insight)

    # Show affirmation
    affirmation = AffirmationLibrary.get_affirmation(mental)
    print_with_delay(f"\n💭 **Affirmation for you:**\n{affirmation}")


def run_guided_exercises():
    """Show guided exercises menu"""
    print_with_delay("\n🧘 GUIDED EXERCISES 🧘")
    print("\n1️⃣  Grounding Techniques")
    print("2️⃣  Journaling")
    print("3️⃣  Back to Main Menu")

    choice = input("\nChoose (1-3): ").strip()

    if choice == "1":
        print("\n🌿 GROUNDING TECHNIQUES 🌿")
        print("1️⃣  5-4-3-2-1 Technique (Presence)")
        print("2️⃣  Progressive Muscle Relaxation (Tension Relief)")
        print("3️⃣  Box Breathing (Calm)")

        sub_choice = input("\nChoose (1-3): ").strip()

        exercises = {
            "1": GuidedExercises.grounding["5_4_3_2_1"],
            "2": GuidedExercises.grounding["progressive_relaxation"],
            "3": GuidedExercises.grounding["box_breathing"],
        }

        if sub_choice in exercises:
            ex = exercises[sub_choice]
            print_with_delay(f"\n✨ {ex['name'].upper()}")
            print_with_delay(ex['description'])
            print("\n" + "—" * 40)
            for step in ex['steps']:
                print_with_delay(step)
            print_with_delay("\n🌟 Wonderful! You completed this exercise. Proud of you!")

    elif choice == "2":
        print("\n📔 JOURNALING 📔")
        print("1️⃣  Gratitude Journal")
        print("2️⃣  Worry Release Journal")
        print("3️⃣  Celebrate Your Wins")
        print("4️⃣  Letter to Your Future Self")

        sub_choice = input("\nChoose (1-4): ").strip()

        journals = {
            "1": GuidedExercises.journaling["gratitude"],
            "2": GuidedExercises.journaling["worry_release"],
            "3": GuidedExercises.journaling["wins"],
            "4": GuidedExercises.journaling["future_self"],
        }

        if sub_choice in journals:
            jrnl = journals[sub_choice]
            print_with_delay(f"\n📝 {jrnl['name'].upper()}")
            print_with_delay(jrnl['prompt'])
            print_with_delay("\n(Take your time. Write as much or as little as you'd like.)")
            journal_entry = input("\n> ")
            print_with_delay("\n💙 Thank you for sharing. Your words matter. 💙")


def run_mindful_breaks():
    """Suggest mindful breaks based on stress"""
    print_with_delay("\n⏸️ MINDFUL BREAK RECOMMENDER ⏸️")

    stress = ask_choice("Current stress level?", ["Low", "Medium", "High"])
    time_available = ask_choice("How much time do you have?", ["quick", "medium", "deep"])

    break_suggestion = MindfulBreakRecommender.recommend(stress, time_available)

    print_with_delay(f"\n✨ Here's a perfect break for you:\n{break_suggestion}")
    print_with_delay("\n⏰ Set a timer and give yourself this gift. You deserve it! 🎁")


def view_wellness_history(profile):
    """Display user's wellness history and patterns"""
    if not profile.sessions:
        print_with_delay("\n📊 No check-ins yet! Start your wellness journey with a daily check-in. 🌱")
        return

    print_with_delay("\n📊 YOUR WELLNESS HISTORY 📊")
    print_with_delay(f"Total check-ins: {profile.total_checkins}")

    history = profile.get_mood_history()
    print("\nLast check-ins:")
    for i, session in enumerate(history[-5:], 1):
        mood = session.get("mental_state", "N/A")
        date = session.get("timestamp", "N/A")[:10]
        print(f"{i}. {date} - {mood}")

    patterns = profile.identify_patterns()
    if patterns and patterns["most_common_mood"]:
        print_with_delay(f"\n🧠 Your Pattern: You're often feeling **{patterns['most_common_mood']}**")

    if len(history) >= 3:
        summary = MoodAnalytics.generate_weekly_summary(history)
        print_with_delay(f"\n{summary}")


def show_resources():
    """Show mental health resources and crisis support"""
    print_with_delay("\n🆘 MENTAL HEALTH RESOURCES 🆘")
    print("""
    If you're in crisis, please reach out immediately:

    🇮🇳 INDIA:
    • AASRA: 9820466726
    • iCall: 9152987821
    • Vandrevala Foundation: 9999 666 555
    • COOJ: 0422-4640050

    🌍 INTERNATIONAL:
    • Crisis Text Line: Text HOME to 741741
    • International Suicide Hotline: findahelpline.com

    💙 Remember:
    - Your life matters
    - This pain is temporary
    - You deserve support
    - Asking for help is strength
    """)
    print_with_delay("\n🤍 Please reach out. You're not alone. 🤍")


def main():
    """Main chatbot loop"""
    print_with_delay("🌸 Welcome to MindfulMe - Your Personal Wellness Companion 🌸")
    
    name = input("\n👋 What's your name? ").strip().title() or "Friend"
    profile = WellnessProfile(name)

    print_with_delay(f"\n💛 Hi {name}! I'm so glad you're here.")
    print_with_delay("I'm here to support your emotional wellness journey with exercises, affirmations, and insights. 🌟")
    print_with_delay("Remember: I'm a companion, not a therapist. For serious concerns, please seek professional help. 💙")

    while True:
        choice = display_main_menu()

        if choice == "1":
            run_daily_checkin(profile)
        elif choice == "2":
            run_guided_exercises()
        elif choice == "3":
            affirmation = AffirmationLibrary.get_affirmation("Stressed")
            print_with_delay(f"\n💭 Here's your affirmation:\n\n{affirmation}")
        elif choice == "4":
            run_mindful_breaks()
        elif choice == "5":
            run_guided_exercises()
        elif choice == "6":
            view_wellness_history(profile)
        elif choice == "7":
            show_resources()
        elif choice == "8":
            print_with_delay(f"\n👋 Goodbye, {name}! Remember, you're doing great. Take care of yourself! 💖")
            break
        else:
            print_with_delay("❌ Invalid choice. Please try again. 💛")


if __name__ == "__main__":
    main()
