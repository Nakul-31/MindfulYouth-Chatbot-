import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import List, Dict, Tuple
import random

from config import WELLNESS_TIPS, MOOD_ACTIVITIES


def get_daily_tip() -> str:
    """Get a random wellness tip"""
    return random.choice(WELLNESS_TIPS)


def get_mood_suggestions(mood: str) -> List[str]:
    """Get activity suggestions based on mood"""
    return MOOD_ACTIVITIES.get(mood, [
        "Take a moment to breathe deeply",
        "Go for a short walk",
        "Listen to calming music",
        "Talk to someone you trust",
        "Practice mindfulness"
    ])


def create_mood_dataframe(mood_data: List[Dict]) -> pd.DataFrame:
    """Create DataFrame from mood tracking data"""
    if not mood_data:
        return pd.DataFrame(columns=['Date', 'Mood', 'Notes'])
    
    df = pd.DataFrame(mood_data)
    df['Date'] = pd.to_datetime(df['Date'])
    return df


def analyze_mood_trends(mood_data: List[Dict]) -> Dict:
    """Analyze mood trends from tracking data"""
    if not mood_data or len(mood_data) < 2:
        return {
            'total_entries': len(mood_data),
            'most_common_mood': 'Not enough data',
            'trend': 'Not enough data',
            'streak': 0
        }
    
    df = create_mood_dataframe(mood_data)
    
    # Count moods
    mood_counts = df['Mood'].value_counts()
    most_common = mood_counts.index[0] if not mood_counts.empty else 'Unknown'
    
    # Calculate trend (simple positive/negative ratio)
    positive_moods = ['Happy', 'Calm', 'Neutral']
    negative_moods = ['Sad', 'Anxious', 'Frustrated', 'Overwhelmed', 'Tired']
    
    positive_count = df[df['Mood'].isin(positive_moods)].shape[0]
    negative_count = df[df['Mood'].isin(negative_moods)].shape[0]
    
    if positive_count > negative_count:
        trend = "Mostly Positive 📈"
    elif negative_count > positive_count:
        trend = "Needs Attention 📉"
    else:
        trend = "Balanced ⚖️"
    
    # Calculate logging streak
    df_sorted = df.sort_values('Date', ascending=False)
    streak = 1
    current_date = df_sorted.iloc[0]['Date'].date()
    
    for i in range(1, len(df_sorted)):
        prev_date = df_sorted.iloc[i]['Date'].date()
        if (current_date - prev_date).days == 1:
            streak += 1
            current_date = prev_date
        else:
            break
    
    return {
        'total_entries': len(mood_data),
        'most_common_mood': most_common,
        'trend': trend,
        'streak': streak,
        'positive_count': positive_count,
        'negative_count': negative_count
    }


def create_chat_summary(messages: List[Dict]) -> str:
    """Create a summary of the chat session"""
    if not messages:
        return "No messages yet."
    
    user_messages = [m for m in messages if m['role'] == 'user']
    ai_messages = [m for m in messages if m['role'] == 'assistant']
    
    summary = f"""
    **Chat Session Summary**
    - Total messages: {len(messages)}
    - Your messages: {len(user_messages)}
    - MindfulAI responses: {len(ai_messages)}
    - Session duration: Active
    """
    return summary


def format_timestamp(dt: datetime = None) -> str:
    """Format timestamp for display"""
    if dt is None:
        dt = datetime.now()
    return dt.strftime("%I:%M %p")


def calculate_wellbeing_score(mood_data: List[Dict]) -> int:
    """Calculate a wellbeing score (0-100) based on recent moods"""
    if not mood_data:
        return 50  # Neutral baseline
    
    # Weight recent entries more heavily
    mood_scores = {
        'Happy': 100,
        'Calm': 85,
        'Neutral': 60,
        'Tired': 45,
        'Frustrated': 35,
        'Sad': 25,
        'Anxious': 20,
        'Overwhelmed': 15
    }
    
    # Take last 7 entries
    recent_moods = mood_data[-7:] if len(mood_data) > 7 else mood_data
    
    total_score = 0
    weights_sum = 0
    
    for i, entry in enumerate(reversed(recent_moods)):
        weight = len(recent_moods) - i  # More recent = higher weight
        mood = entry.get('Mood', 'Neutral')
        score = mood_scores.get(mood, 50)
        total_score += score * weight
        weights_sum += weight
    
    final_score = int(total_score / weights_sum) if weights_sum > 0 else 50
    return max(0, min(100, final_score))  # Clamp between 0-100


def get_wellbeing_message(score: int) -> Tuple[str, str]:
    """Get message and emoji based on wellbeing score"""
    if score >= 80:
        return "Excellent! 🌟", "#51cf66"
    elif score >= 60:
        return "Good 😊", "#00c9a7"
    elif score >= 40:
        return "Fair 😐", "#ffd43b"
    else:
        return "Needs Care 💙", "#667eea"


def export_mood_data(mood_data: List[Dict]) -> str:
    """Export mood data as CSV string"""
    if not mood_data:
        return "No data to export"
    
    df = create_mood_dataframe(mood_data)
    return df.to_csv(index=False)


def create_sample_mood_data(days: int = 14) -> List[Dict]:
    """Create sample mood data for demo purposes"""
    moods = ['Happy', 'Calm', 'Neutral', 'Sad', 'Anxious', 'Frustrated', 'Overwhelmed', 'Tired']
    sample_data = []
    
    for i in range(days):
        date = datetime.now() - timedelta(days=days-i-1)
        sample_data.append({
            'Date': date.strftime("%Y-%m-%d"),
            'Mood': random.choice(moods),
            'Notes': f"Sample entry {i+1}"
        })
    
    return sample_data


def validate_message(message: str, max_length: int = 1000) -> Tuple[bool, str]:
    """Validate user message"""
    if not message or not message.strip():
        return False, "Message cannot be empty"
    
    if len(message) > max_length:
        return False, f"Message too long (max {max_length} characters)"
    
    return True, "Valid"


def sanitize_input(text: str) -> str:
    """Sanitize user input"""
    # Remove any potential harmful characters
    text = text.strip()
    # Remove excessive whitespace
    text = ' '.join(text.split())
    return text


def get_greeting_message() -> str:
    """Get time-appropriate greeting"""
    hour = datetime.now().hour
    
    if 5 <= hour < 12:
        greeting = "Good morning"
        emoji = "🌅"
    elif 12 <= hour < 17:
        greeting = "Good afternoon"
        emoji = "☀️"
    elif 17 <= hour < 21:
        greeting = "Good evening"
        emoji = "🌆"
    else:
        greeting = "Good night"
        emoji = "🌙"
    
    # Add color using HTML <span>
    colored_greeting = f"<span style='color:#667EEA;'>{greeting}!</span> {emoji}"
    
    return colored_greeting



def calculate_usage_stats(messages: List[Dict], mood_data: List[Dict]) -> Dict:
    """Calculate usage statistics"""
    return {
        'total_messages': len(messages),
        'user_messages': len([m for m in messages if m['role'] == 'user']),
        'ai_responses': len([m for m in messages if m['role'] == 'assistant']),
        'mood_entries': len(mood_data),
        'avg_message_length': np.mean([len(m['content']) for m in messages]) if messages else 0,
        'session_active': len(messages) > 0
    }


def format_resource_link(title: str, url: str) -> str:
    """Format resource link for display"""
    return f"[{title}]({url})"


def create_progress_bar(value: int, max_value: int = 100) -> str:
    """Create ASCII progress bar"""
    filled = int((value / max_value) * 20)
    bar = "█" * filled + "░" * (20 - filled)
    return f"{bar} {value}/{max_value}"