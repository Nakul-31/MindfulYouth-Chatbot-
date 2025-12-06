import os
import streamlit as st
from dataclasses import dataclass
from typing import List, Dict

@dataclass
class AppConfig:
    """Application configuration settings"""
    APP_NAME: str = "MindfulYouth"
    APP_VERSION: str = "2.0.0"
    APP_ICON: str = "🧠"
    TAGLINE: str = "Your Companion for Mental Wellness"
    
    # Page settings
    PAGE_TITLE: str = "MindfulYouth - Mental Health Support"
    PAGE_ICON: str = "🧠"
    LAYOUT: str = "wide"
    INITIAL_SIDEBAR_STATE: str = "expanded"
    
    # Chat settings
    MAX_MESSAGE_LENGTH: int = 1000
    MAX_CONVERSATION_HISTORY: int = 20
    TYPING_DELAY: float = 0.02
    
    # AI settings
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    USE_AI: bool = True
    AI_MODEL: str = "gpt-3.5-turbo"
    AI_TEMPERATURE: float = 0.7
    AI_MAX_TOKENS: int = 500

@dataclass
class CrisisConfig:
    """Crisis intervention configuration"""
    CRISIS_KEYWORDS: List[str] = None
    CRISIS_HELPLINES: Dict[str, str] = None

    def __post_init__(self):
        if self.CRISIS_KEYWORDS is None:
            self.CRISIS_KEYWORDS = [
                'suicide', 'kill myself', 'end my life', 'want to die',
                'self harm', 'hurt myself', 'cutting', 'overdose',
                'no reason to live', 'better off dead'
            ]

        if self.CRISIS_HELPLINES is None:
            self.CRISIS_HELPLINES = {
                "🇮🇳 National Mental Health Helpline": "1800-599-0019",
                "🇮🇳 Vandrevala Foundation (24/7)": "1860-2662-345 / 1800-2333-330",
                "🇮🇳 iCall Psychosocial Helpline": "9152987821",
                "🇮🇳 AASRA (24/7)": "91-9820466726",
                "🌍 International Crisis Line": "Text 'HELLO' to 741741"
            }

@dataclass  
class ThemeConfig:
    """UI Theme configuration"""
    PRIMARY_COLOR: str = "#667eea"
    SECONDARY_COLOR: str = "#764ba2"
    BACKGROUND_COLOR: str = "#1a53c6"
    TEXT_COLOR: str = "#262730"
    ACCENT_COLOR: str = "#00c9a7"
    ERROR_COLOR: str = "#ff6b6b"
    SUCCESS_COLOR: str = "#51cf66"
    WARNING_COLOR: str = "#ffd43b"
    
    # Chat bubble colors
    USER_MESSAGE_BG: str = "#667eea"
    USER_MESSAGE_TEXT: str = "#ffffff"
    AI_MESSAGE_BG: str = "#667eea"
    AI_MESSAGE_TEXT: str = "#ffffff"
    
    # Fonts
    FONT_FAMILY: str = "'Inter', 'Segoe UI', sans-serif"
    HEADER_FONT: str = "'Poppins', sans-serif"

# Initialize configurations
app_config = AppConfig()
crisis_config = CrisisConfig()
theme_config = ThemeConfig()

# Mental health resources
MENTAL_HEALTH_RESOURCES = {
    "📞 Helplines": [
        {
            "name": "National Mental Health Helpline",
            "contact": "1800-599-0019",
            "description": "24/7 toll-free mental health support",
            "availability": "24/7"
        },
        {
            "name": "Vandrevala Foundation",
            "contact": "1860-2662-345",
            "description": "Confidential counseling services",
            "availability": "24/7"
        },
        {
            "name": "iCall Psychosocial Helpline",
            "contact": "9152987821",
            "description": "Professional counseling service",
            "availability": "Mon-Sat, 8 AM - 10 PM"
        }
    ],
    "🧘 Self-Help Techniques": [
        {
            "name": "4-7-8 Breathing",
            "description": "Inhale for 4 seconds, hold for 7, exhale for 8",
            "benefit": "Reduces anxiety and promotes calmness"
        },
        {
            "name": "5-4-3-2-1 Grounding",
            "description": "Name 5 things you see, 4 you hear, 3 you touch, 2 you smell, 1 you taste",
            "benefit": "Brings you to the present moment"
        },
        {
            "name": "Progressive Muscle Relaxation",
            "description": "Tense and relax each muscle group",
            "benefit": "Releases physical tension"
        }
    ],
    "📚 Helpful Resources": [
        {
            "name": "Mindfulness Apps",
            "description": "Headspace, Calm, Insight Timer",
            "description": "https://www.headspace.com"
        },
        {
            "name": "UCLA Free Meditations",
            "description": "Guided meditation recordings",
            "description": "https://www.uclahealth.org/marc/mindful-meditations"
        },
        {
            "name": "Mental Health Foundation",
            "description": "Information and support resources",
            "description": "https://www.mentalhealth.org.uk"
        }
    ]
    
}

# Wellness tips
WELLNESS_TIPS = [
    "💙 Practice gratitude - Write down 3 things you're grateful for today",
    "🏃 Move your body - Even 10 minutes of exercise can boost your mood",
    "😴 Prioritize sleep - Aim for 7-9 hours of quality sleep",
    "🥗 Eat mindfully - Nourish your body with healthy foods",
    "👥 Connect with others - Reach out to a friend or family member",
    "📱 Take a digital detox - Unplug from screens for an hour",
    "🌳 Spend time in nature - Go for a walk outside",
    "📝 Journal your thoughts - Write down your feelings",
    "🎨 Express yourself creatively - Draw, paint, or craft",
    "🧘 Practice meditation - Even 5 minutes helps"
]

# Mood tracking emotions
MOOD_OPTIONS = {
    "😊": "Happy",
    "😌": "Calm",
    "😐": "Neutral",
    "😔": "Sad",
    "😰": "Anxious",
    "😤": "Frustrated",
    "😫": "Overwhelmed",
    "😴": "Tired"
}

# Activity suggestions based on mood
MOOD_ACTIVITIES = {
    "Sad": [
        "Listen to uplifting music",
        "Call a friend or family member",
        "Watch a comedy show or funny videos",
        "Do something creative",
        "Get some sunlight or fresh air"
    ],
    "Anxious": [
        "Practice deep breathing exercises",
        "Try progressive muscle relaxation",
        "Go for a walk",
        "Listen to calming music",
        "Use the 5-4-3-2-1 grounding technique"
    ],
    "Overwhelmed": [
        "Break tasks into smaller steps",
        "Take a 10-minute break",
        "Practice saying 'no' to non-essential tasks",
        "Ask for help from someone you trust",
        "Focus on one thing at a time"
    ],
    "Frustrated": [
        "Take deep breaths",
        "Go for a run or workout",
        "Write down your feelings",
        "Talk to someone about what's bothering you",
        "Take a break from the situation"
    ],
    "Tired": [
        "Take a short power nap (20 minutes)",
        "Stay hydrated - drink water",
        "Get some fresh air",
        "Do gentle stretching",
        "Go to bed earlier tonight"
    ]
}