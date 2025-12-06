from config import theme_config

def get_custom_css() -> str:
    """Return custom CSS for the application"""
    return f"""
    <style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Poppins:wght@400;500;600;700&display=swap');
    
    /* Global Styles */
    * {{
        font-family: {theme_config.FONT_FAMILY};
    }}
    
    /* Main container */
    .main {{
        background: linear-gradient(135deg, {theme_config.PRIMARY_COLOR} 0%, {theme_config.SECONDARY_COLOR} 100%);
        padding: 0;
    }}
    
    /* Remove default Streamlit padding */
    .block-container {{
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 1200px;
    }}
    
    /* Header styling */
    .app-header {{
        background: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(10px);
        padding: 2rem;
        border-radius: 20px;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
        margin-bottom: 2rem;
        text-align: center;
        animation: fadeInDown 0.6s ease;
    }}
    
    .app-header h1 {{
        font-family: {theme_config.HEADER_FONT};
        color: {theme_config.PRIMARY_COLOR};
        font-size: 3rem;
        font-weight: 700;
        margin: 0;
        background: linear-gradient(135deg, {theme_config.PRIMARY_COLOR}, {theme_config.SECONDARY_COLOR});
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }}
    
    .app-header p {{
        color: {theme_config.TEXT_COLOR};
        font-size: 1.1rem;
        margin-top: 0.5rem;
        opacity: 0.8;
    }}
    
    /* Chat container */
    .chat-container {{
        background: white;
        border-radius: 20px;
        padding: 2rem;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
        margin-bottom: 2rem;
        animation: fadeIn 0.6s ease;
    }}
    
    /* Chat messages */
    .user-message {{
        background: linear-gradient(135deg, {theme_config.USER_MESSAGE_BG}, {theme_config.SECONDARY_COLOR});
        color: {theme_config.USER_MESSAGE_TEXT};
        padding: 1rem 1.5rem;
        border-radius: 20px 20px 5px 20px;
        margin: 1rem 0;
        max-width: 75%;
        margin-left: auto;
        box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
        animation: slideInRight 0.3s ease;
        word-wrap: break-word;
    }}
    
    .ai-message {{
        background: {theme_config.AI_MESSAGE_BG};
        color: {theme_config.AI_MESSAGE_TEXT};
        padding: 1rem 1.5rem;
        border-radius: 20px 20px 20px 5px;
        margin: 1rem 0;
        max-width: 75%;
        margin-right: auto;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
        animation: slideInLeft 0.3s ease;
        word-wrap: break-word;
    }}
    
    .crisis-message {{
        background: linear-gradient(135deg, {theme_config.ERROR_COLOR}, #ff5252);
        color: white;
        padding: 1.5rem;
        border-radius: 15px;
        margin: 1rem 0;
        box-shadow: 0 4px 12px rgba(255, 107, 107, 0.4);
        border-left: 5px solid #c92a2a;
        animation: pulse 1s ease;
    }}
    
    /* Sidebar styling */
    .css-1d391kg {{
        background: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(10px);
    }}
    
    [data-testid="stSidebar"] {{
        background: linear-gradient(180deg, rgba(102, 126, 234, 0.1) 0%, rgba(118, 75, 162, 0.1) 100%);
    }}
    
    /* Cards */
    .info-card {{
        background: white;
        border-radius: 15px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
        border-left: 4px solid {theme_config.PRIMARY_COLOR};
    }}
    
    .info-card:hover {{
        transform: translateY(-5px);
        box-shadow: 0 8px 24px rgba(102, 126, 234, 0.2);
    }}
    
    .resource-card {{
        background: linear-gradient(135deg, rgba(102, 126, 234, 0.1), rgba(118, 75, 162, 0.1));
        border-radius: 15px;
        padding: 1.5rem;
        margin: 1rem 0;
        transition: transform 0.3s ease;
    }}
    
    .resource-card:hover {{
        transform: scale(1.02);
    }}
    
    /* Buttons */
    .stButton > button {{
        background: linear-gradient(135deg, {theme_config.PRIMARY_COLOR}, {theme_config.SECONDARY_COLOR});
        color: white;
        border: none;
        border-radius: 25px;
        padding: 0.75rem 2rem;
        font-weight: 600;
        font-size: 1rem;
        transition: all 0.3s ease;
        box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
    }}
    
    .stButton > button:hover {{
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4);
    }}
    
    .stButton > button:active {{
        transform: translateY(0);
    }}
    
    /* Input fields */
    .stTextInput > div > div > input {{
        border-radius: 15px;
        border: 2px solid #e0e0e0;
        padding: 0.75rem 1rem;
        transition: all 0.3s ease;
    }}
    
    .stTextInput > div > div > input:focus {{
        border-color: {theme_config.PRIMARY_COLOR};
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
    }}
    
    .stTextArea > div > div > textarea {{
        border-radius: 15px;
        border: 2px solid #e0e0e0;
        padding: 1rem;
        transition: all 0.3s ease;
    }}
    
    .stTextArea > div > div > textarea:focus {{
        border-color: {theme_config.PRIMARY_COLOR};
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
    }}
    
    /* Metrics */
    [data-testid="stMetricValue"] {{
        font-size: 2rem;
        font-weight: 700;
        color: {theme_config.PRIMARY_COLOR};
    }}
    
    /* Expander */
    .streamlit-expanderHeader {{
        background: linear-gradient(135deg, rgba(102, 126, 234, 0.1), rgba(118, 75, 162, 0.1));
        border-radius: 10px;
        font-weight: 600;
    }}
    
    /* Success/Error messages */
    .success-message {{
        background: {theme_config.SUCCESS_COLOR};
        color: white;
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
        animation: slideInDown 0.3s ease;
    }}
    
    .error-message {{
        background: {theme_config.ERROR_COLOR};
        color: white;
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
        animation: shake 0.5s ease;
    }}
    
    .warning-message {{
        background: {theme_config.WARNING_COLOR};
        color: {theme_config.TEXT_COLOR};
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
    }}
    
    /* Mood tracker */
    .mood-button {{
        font-size: 3rem;
        padding: 1rem;
        margin: 0.5rem;
        border-radius: 50%;
        transition: transform 0.3s ease;
        cursor: pointer;
        border: 3px solid transparent;
    }}
    
    .mood-button:hover {{
        transform: scale(1.2);
        border-color: {theme_config.PRIMARY_COLOR};
    }}
    
    /* Statistics */
    .stat-card {{
        background: linear-gradient(135deg, {theme_config.PRIMARY_COLOR}, {theme_config.SECONDARY_COLOR});
        color: white;
        padding: 2rem;
        border-radius: 20px;
        text-align: center;
        box-shadow: 0 8px 24px rgba(102, 126, 234, 0.3);
    }}
    
    .stat-number {{
        font-size: 3rem;
        font-weight: 700;
        margin: 0;
    }}
    
    .stat-label {{
        font-size: 1rem;
        opacity: 0.9;
        margin-top: 0.5rem;
    }}
    
    /* Animations */
    @keyframes fadeIn {{
        from {{
            opacity: 0;
        }}
        to {{
            opacity: 1;
        }}
    }}
    
    @keyframes fadeInDown {{
        from {{
            opacity: 0;
            transform: translateY(-20px);
        }}
        to {{
            opacity: 1;
            transform: translateY(0);
        }}
    }}
    
    @keyframes slideInRight {{
        from {{
            opacity: 0;
            transform: translateX(30px);
        }}
        to {{
            opacity: 1;
            transform: translateX(0);
        }}
    }}
    
    @keyframes slideInLeft {{
        from {{
            opacity: 0;
            transform: translateX(-30px);
        }}
        to {{
            opacity: 1;
            transform: translateX(0);
        }}
    }}
    
    @keyframes slideInDown {{
        from {{
            opacity: 0;
            transform: translateY(-20px);
        }}
        to {{
            opacity: 1;
            transform: translateY(0);
        }}
    }}
    
    @keyframes pulse {{
        0%, 100% {{
            transform: scale(1);
        }}
        50% {{
            transform: scale(1.02);
        }}
    }}
    
    @keyframes shake {{
        0%, 100% {{
            transform: translateX(0);
        }}
        25% {{
            transform: translateX(-10px);
        }}
        75% {{
            transform: translateX(10px);
        }}
    }}
    
    /* Hide Streamlit branding */
    #MainMenu {{visibility: hidden;}}
    footer {{visibility: hidden;}}
    header {{visibility: hidden;}}
    
    /* Scrollbar styling */
    ::-webkit-scrollbar {{
        width: 10px;
    }}
    
    ::-webkit-scrollbar-track {{
        background: #f1f1f1;
        border-radius: 10px;
    }}
    
    ::-webkit-scrollbar-thumb {{
        background: linear-gradient(135deg, {theme_config.PRIMARY_COLOR}, {theme_config.SECONDARY_COLOR});
        border-radius: 10px;
    }}
    
    ::-webkit-scrollbar-thumb:hover {{
        background: {theme_config.SECONDARY_COLOR};
    }}
    
    /* Responsive design */
    @media (max-width: 768px) {{
        .app-header h1 {{
            font-size: 2rem;
        }}
        
        .user-message, .ai-message {{
            max-width: 90%;
        }}
        
        .block-container {{
            padding: 1rem;
        }}
    }}
    </style>
    """

def get_message_html(content: str, is_user: bool = False) -> str:
    """Generate HTML for chat message"""
    message_class = "user-message" if is_user else "ai-message"
    prefix = "You" if is_user else "MindfulAI"
    emoji = "👤" if is_user else "🧠"
    
    return f"""
    <div class="{message_class}">
        <strong>{emoji} {prefix}:</strong><br>
        {content}
    </div>
    """

def get_crisis_html(message: str) -> str:
    """Generate HTML for crisis message"""
    return f"""
    <div class="crisis-message">
        <h3 style="margin-top: 0;">🆘 IMMEDIATE HELP AVAILABLE</h3>
        {message}
    </div>
    """

def get_info_card_html(title: str, content: str, icon: str = "ℹ️") -> str:
    """Generate HTML for info card"""
    return f"""
    <div class="info-card">
        <h3 style="margin-top: 0;">{icon} {title}</h3>
        <p style="margin-bottom: 0;">{content}</p>
    </div>
    """

def get_resource_card_html(title: str, description: str, contact: str = None, link: str = None) -> str:
    """Generate HTML for resource card"""
    contact_html = f"<p><strong>📞 Contact:</strong> {contact}</p>" if contact else ""
    link_html = f'<p><a href="{link}" target="_blank" style="color: {theme_config.PRIMARY_COLOR}; text-decoration: none; font-weight: 600;">Learn More →</a></p>' if link else ""
    
    return f"""
    <div class="resource-card">
        <h4 style="margin-top: 0; color: {theme_config.PRIMARY_COLOR};">{title}</h4>
        <p>{description}</p>
        {contact_html}
        {link_html}
    </div>
    """