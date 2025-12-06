import streamlit as st
from datetime import datetime
import time

# Import custom modules
from config import app_config, MENTAL_HEALTH_RESOURCES, MOOD_OPTIONS
from styles import get_custom_css, get_message_html, get_crisis_html, get_info_card_html, get_resource_card_html
from chatbot import MindfulChatbot
from utils import (
    get_daily_tip, get_mood_suggestions, analyze_mood_trends,
    calculate_wellbeing_score, get_wellbeing_message, get_greeting_message,
    calculate_usage_stats, validate_message, sanitize_input
)

# Page configuration
st.set_page_config(
    page_title=app_config.PAGE_TITLE,
    page_icon=app_config.PAGE_ICON,
    layout=app_config.LAYOUT,
    initial_sidebar_state=app_config.INITIAL_SIDEBAR_STATE
)

# Apply custom CSS
st.markdown(get_custom_css(), unsafe_allow_html=True)

# Initialize session state
if 'messages' not in st.session_state:
    st.session_state.messages = []

if 'mood_data' not in st.session_state:
    st.session_state.mood_data = []

if 'chatbot' not in st.session_state:
    st.session_state.chatbot = MindfulChatbot(use_ai=True)

if 'current_page' not in st.session_state:
    st.session_state.current_page = 'Chat'

if 'show_welcome' not in st.session_state:
    st.session_state.show_welcome = True


def render_header():
    """Render application header"""
    st.markdown(f"""
    <div class="app-header">
        <h1>{app_config.APP_ICON} {app_config.APP_NAME}</h1>
        <p>{app_config.TAGLINE}</p>
    </div>
    """, unsafe_allow_html=True)


def render_chat_page():
    """Render main chat interface"""
    st.markdown('<div class="chat-container">', unsafe_allow_html=True)
    
    # Welcome message
    if st.session_state.show_welcome and len(st.session_state.messages) == 0:
        greeting = get_greeting_message()
        st.markdown(get_info_card_html(
    f"{greeting}",
    f"""
    <span style="color:#667EEA;">
    Welcome to {app_config.APP_NAME}! I'm MindfulAI, your companion for mental wellness.
    I'm here to listen, support, and help you navigate your thoughts and feelings.
    Feel free to share whatever is on your mind. 💙
    </span>
    """,
    "🧠"
), unsafe_allow_html=True)
    
    # Display chat messages
    chat_container = st.container()
    with chat_container:
        for message in st.session_state.messages:
            is_user = message['role'] == 'user'
            st.markdown(
                get_message_html(message['content'], is_user),
                unsafe_allow_html=True
            )
    
    # Chat input
    st.markdown("---")
    col1, col2 = st.columns([6, 1])
    
    with col1:
        user_input = st.text_input(
            "Your message",
            key="chat_input",
            placeholder="Type your message here...",
            label_visibility="collapsed"
        )
    
    with col2:
        send_button = st.button("Send 📤", use_container_width=True)
    
    # Handle message sending
    if send_button and user_input:
        handle_user_message(user_input)
        st.rerun()
    
    # Quick action buttons
    st.markdown("### Quick Actions")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("😰 Feeling Anxious", use_container_width=True):
            handle_user_message("I'm feeling anxious")
            st.rerun()
    
    with col2:
        if st.button("😔 Feeling Sad", use_container_width=True):
            handle_user_message("I'm feeling sad")
            st.rerun()
    
    with col3:
        if st.button("💪 Need Motivation", use_container_width=True):
            handle_user_message("I need motivation")
            st.rerun()
    
    # Clear chat button
    st.markdown("---")
    if st.button("🗑️ Clear Chat History", use_container_width=True):
        st.session_state.messages = []
        st.session_state.show_welcome = True
        st.success("Chat history cleared!")
        st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)


def handle_user_message(user_input: str):
    """Process and respond to user message"""
    st.session_state.show_welcome = False
    
    # Validate input
    is_valid, error_msg = validate_message(user_input)
    if not is_valid:
        st.error(error_msg)
        return
    
    # Sanitize input
    user_input = sanitize_input(user_input)
    
    # Add user message
    st.session_state.messages.append({
        'role': 'user',
        'content': user_input,
        'timestamp': datetime.now()
    })
    
    # Get bot response
    with st.spinner("MindfulAI is typing..."):
        response, is_crisis = st.session_state.chatbot.get_response(
            user_input,
            st.session_state.messages
        )
    
    # Add bot response
    st.session_state.messages.append({
        'role': 'assistant',
        'content': response,
        'timestamp': datetime.now(),
        'is_crisis': is_crisis
    })


def render_mood_tracker():
    """Render mood tracking interface"""
    st.markdown('<div class="chat-container">', unsafe_allow_html=True)
    
    st.header("🎭 Mood Tracker")
    st.write("Track your daily moods to understand your emotional patterns better.")
    
    # Mood selection
    st.subheader("How are you feeling today?")
    
    cols = st.columns(4)
    selected_mood = None
    
    for idx, (emoji, mood) in enumerate(MOOD_OPTIONS.items()):
        col = cols[idx % 4]
        with col:
            if st.button(f"{emoji}\n{mood}", key=f"mood_{mood}", use_container_width=True):
                selected_mood = mood
    
    # Add mood entry
    if selected_mood:
        notes = st.text_area(
            "Add notes (optional)",
            placeholder="What's on your mind?",
            max_chars=500
        )
        
        if st.button("Save Mood Entry", type="primary", use_container_width=True):
            st.session_state.mood_data.append({
                'Date': datetime.now().strftime("%Y-%m-%d %H:%M"),
                'Mood': selected_mood,
                'Notes': notes
            })
            st.success(f"Mood logged: {selected_mood}! 🎉")
            
            # Show suggestions
            suggestions = get_mood_suggestions(selected_mood)
            if suggestions:
                st.info("**Suggested activities:**\n" + "\n".join([f"• {s}" for s in suggestions]))
            
            time.sleep(1)
            st.rerun()
    
    # Display mood history
    if st.session_state.mood_data:
        st.markdown("---")
        st.subheader("📊 Your Mood History")
        
        # Analytics
        analysis = analyze_mood_trends(st.session_state.mood_data)
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total Entries", analysis['total_entries'])
        
        with col2:
            st.metric("Most Common", analysis['most_common_mood'])
        
        with col3:
            st.metric("Current Trend", analysis['trend'])
        
        with col4:
            st.metric("Logging Streak", f"{analysis['streak']} days")
        
        # Wellbeing score
        wellbeing_score = calculate_wellbeing_score(st.session_state.mood_data)
        wellbeing_msg, wellbeing_color = get_wellbeing_message(wellbeing_score)
        
        st.markdown(f"""
        <div style="background: {wellbeing_color}; color: white; padding: 1.5rem; 
                    border-radius: 15px; text-align: center; margin: 1rem 0;">
            <h3 style="margin: 0;">Wellbeing Score</h3>
            <h1 style="margin: 0.5rem 0; font-size: 3rem;">{wellbeing_score}/100</h1>
            <p style="margin: 0;">{wellbeing_msg}</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Recent entries
        st.subheader("Recent Entries")
        for entry in reversed(st.session_state.mood_data[-5:]):
            emoji = [e for e, m in MOOD_OPTIONS.items() if m == entry['Mood']][0]
            st.markdown(f"""
            <div class="info-card">
                <strong>{emoji} {entry['Mood']}</strong> - {entry['Date']}<br>
                <small>{entry.get('Notes', 'No notes')}</small>
            </div>
            """, unsafe_allow_html=True)
        
        # Clear mood data
        if st.button("🗑️ Clear Mood History", use_container_width=True):
            st.session_state.mood_data = []
            st.success("Mood history cleared!")
            st.rerun()
    else:
        st.info("No mood entries yet. Start tracking your mood to see your patterns!")
    
    st.markdown('</div>', unsafe_allow_html=True)


def render_resources():
    """Render mental health resources"""
    st.markdown('<div class="chat-container">', unsafe_allow_html=True)
    
    st.header("📚 Mental Health Resources")
    st.write("Access helpful resources, helplines, and self-help techniques.")
    
    # Display resources by category
    for category, items in MENTAL_HEALTH_RESOURCES.items():
        st.subheader(category)
        
        for item in items:
            title = item['name']
            description = item['description']
            contact = item.get('contact')
            link = item.get('link')
            availability = item.get('availability')
            benefit = item.get('benefit')
            
            # Build content
            content_parts = [description]
            if availability:
                content_parts.append(f"**Available:** {availability}")
            if benefit:
                content_parts.append(f"**Benefit:** {benefit}")
            
            content = "<br>".join(content_parts)
            
            st.markdown(
                get_resource_card_html(title, content, contact, link),
                unsafe_allow_html=True
            )
    
    st.markdown('</div>', unsafe_allow_html=True)


def render_wellness_tips():
    """Render wellness tips section"""
    st.markdown('<div class="chat-container">', unsafe_allow_html=True)
    
    st.header("✨ Wellness Tips")
    
    # Daily tip
    daily_tip = get_daily_tip()
    st.markdown(f"""
    <div style="background: linear-gradient(135deg, #667eea, #764ba2); 
                color: white; padding: 2rem; border-radius: 20px; 
                text-align: center; margin: 1rem 0;">
        <h3 style="margin: 0;">💡 Today's Wellness Tip</h3>
        <p style="font-size: 1.2rem; margin: 1rem 0 0 0;">{daily_tip}</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Self-care categories
    st.subheader("Self-Care Categories")
    
    categories = {
        "🧘 Mindfulness": [
            "Practice 5 minutes of meditation daily",
            "Try mindful breathing when stressed",
            "Use grounding techniques (5-4-3-2-1)",
            "Practice gratitude journaling"
        ],
        "💪 Physical Health": [
            "Get 7-9 hours of sleep",
            "Exercise for 30 minutes daily",
            "Stay hydrated (8 glasses of water)",
            "Eat balanced, nutritious meals"
        ],
        "🧠 Mental Health": [
            "Take breaks during study/work",
            "Set healthy boundaries",
            "Practice positive self-talk",
            "Seek help when needed"
        ],
        "👥 Social Wellness": [
            "Connect with loved ones regularly",
            "Join clubs or groups you enjoy",
            "Practice active listening",
            "Volunteer in your community"
        ]
    }
    
    for category, tips in categories.items():
        with st.expander(category):
            for tip in tips:
                st.write(f"• {tip}")
    
    st.markdown('</div>', unsafe_allow_html=True)


def render_sidebar():
    """Render sidebar navigation"""
    with st.sidebar:
        st.markdown(f"### {app_config.APP_ICON} {app_config.APP_NAME}")
        st.markdown(f"*Version {app_config.APP_VERSION}*")
        st.markdown("---")
        
        # Navigation
        st.markdown("### 🧭 Navigation")
        
        pages = {
            "💬 Chat": "Chat",
            "🎭 Mood Tracker": "Mood Tracker",
            "📚 Resources": "Resources",
            "✨ Wellness Tips": "Wellness"
        }
        
        for label, page in pages.items():
            if st.button(label, use_container_width=True, key=f"nav_{page}"):
                st.session_state.current_page = page
                st.rerun()
        
        st.markdown("---")
        
        # Quick stats
        stats = calculate_usage_stats(st.session_state.messages, st.session_state.mood_data)
        
        st.markdown("### 📊 Your Stats")
        st.metric("Chat Messages", stats['total_messages'])
        st.metric("Mood Entries", stats['mood_entries'])
        
        if st.session_state.mood_data:
            wellbeing = calculate_wellbeing_score(st.session_state.mood_data)
            st.metric("Wellbeing", f"{wellbeing}/100")
        
        st.markdown("---")
        
        # AI Status
        ai_status = "🟢 Active" if st.session_state.chatbot.is_ai_available() else "🟡 Fallback Mode"
        st.markdown(f"**AI Status:** {ai_status}")
        
        st.markdown("---")
        
        # Emergency contact
        st.markdown("### 🆘 Crisis Support")
        st.error("""
        **In immediate danger?**
        
        🇮🇳 Emergency: **112**
        
        Mental Health Helpline:
        **1800-599-0019**
        """)


def main():
    """Main application function"""
    # Render header
    render_header()
    
    # Render sidebar
    render_sidebar()
    
    # Render current page
    if st.session_state.current_page == 'Chat':
        render_chat_page()
    elif st.session_state.current_page == 'Mood Tracker':
        render_mood_tracker()
    elif st.session_state.current_page == 'Resources':
        render_resources()
    elif st.session_state.current_page == 'Wellness':
        render_wellness_tips()


if __name__ == "__main__":
    main()