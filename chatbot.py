import re
import random
from typing import List, Dict, Optional, Tuple
from datetime import datetime
import logging

from config import app_config, crisis_config

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class MindfulChatbot:
    """Intelligent chatbot for mental health support"""
    
    def __init__(self, use_ai: bool = True):
        """Initialize the chatbot"""
        self.use_ai = use_ai and app_config.USE_AI
        self.ai_available = False
        
        if self.use_ai and app_config.OPENAI_API_KEY:
            try:
                import openai
                openai.api_key = app_config.OPENAI_API_KEY
                self.openai = openai
                self.ai_available = True
                logger.info("✅ OpenAI initialized successfully")
            except ImportError:
                logger.warning("⚠️ OpenAI not installed. Install with: pip install openai")
                self.ai_available = False
            except Exception as e:
                logger.error(f"❌ Failed to initialize OpenAI: {e}")
                self.ai_available = False
        
    def get_response(self, user_message: str, conversation_history: List[Dict] = None) -> Tuple[str, bool]:
        """
        Get chatbot response
        
        Args:
            user_message: User's input message
            conversation_history: Previous conversation messages
            
        Returns:
            Tuple of (response_text, is_crisis)
        """
        if not user_message or not user_message.strip():
            return "I'm here to listen. Please share what's on your mind. 💙", False
        
        # Clean message
        user_message = self._clean_message(user_message)
        
        # Check for crisis keywords
        is_crisis, crisis_response = self._check_crisis(user_message)
        if is_crisis:
            return crisis_response, True
        
        # Get AI or fallback response
        if self.ai_available:
            try:
                response = self._get_ai_response(user_message, conversation_history)
            except Exception as e:
                logger.error(f"AI error: {e}")
                response = self._get_fallback_response(user_message)
        else:
            response = self._get_fallback_response(user_message)
        
        return response, False
    
    def _clean_message(self, message: str) -> str:
        """Clean and validate message"""
        message = message.strip()
        message = re.sub(r'\s+', ' ', message)
        
        if len(message) > app_config.MAX_MESSAGE_LENGTH:
            message = message[:app_config.MAX_MESSAGE_LENGTH]
        
        return message
    
    def _check_crisis(self, message: str) -> Tuple[bool, str]:
        """Check if message contains crisis keywords"""
        message_lower = message.lower()
        
        for keyword in crisis_config.CRISIS_KEYWORDS:
            if keyword in message_lower:
                response = self._get_crisis_response()
                return True, response
        
        return False, ""
    
    def _get_crisis_response(self) -> str:
        """Get crisis intervention response"""
        helplines = "\n".join([
            f"• **{name}**: {number}" 
            for name, number in crisis_config.CRISIS_HELPLINES.items()
        ])
        
        return f"""🆘 **I'm concerned about your safety. Please reach out for immediate help:**

{helplines}

**You are not alone.** These services are confidential and available to support you. 

If you're in immediate danger, please:
- Call emergency services (112 in India)
- Go to your nearest hospital emergency room
- Tell a trusted adult or friend

I'm here to listen, but I'm not a substitute for professional help. Your life matters. 💙"""
    
    def _get_ai_response(self, user_message: str, conversation_history: List[Dict] = None) -> str:
        """Get response from OpenAI API"""
        messages = self._build_prompt(user_message, conversation_history)

        response = self.openai.ChatCompletion.create(
            model=app_config.AI_MODEL,
            messages=messages,
            max_tokens=app_config.AI_MAX_TOKENS,
            temperature=app_config.AI_TEMPERATURE,
            presence_penalty=0.6,
            frequency_penalty=0.3
        )

        content = response.get('choices', [{}])[0].get('message', {}).get('content')
        if content is None:
            content = "I'm sorry, I couldn't generate a response right now. Please try again."
        return content.strip()
    
    def _build_prompt(self, user_message: str, conversation_history: List[Dict] = None) -> List[Dict]:
        """Build conversation prompt for AI"""
        messages = [{
            "role": "system",
            "content": """You are MindfulAI, a compassionate mental health support companion for youth in India.

Your Purpose:
- Provide empathetic, warm, and non-judgmental emotional support
- Offer practical coping strategies and mental health advice  
- Encourage healthy habits and self-care practices
- Recognize when professional help is needed
- Be culturally sensitive and age-appropriate for Indian youth

Guidelines:
- Use simple, clear, conversational language
- Validate feelings genuinely and show empathy
- Keep responses concise (3-5 sentences) but meaningful
- Ask thoughtful follow-up questions when appropriate
- Use occasional emojis to feel approachable (💙 🌟 ✨ 🫂)
- Focus on strengths and resilience
- Never diagnose or replace professional treatment
- Be aware of Indian cultural context and family dynamics

Response Style:
- Start with empathy and validation
- Provide actionable advice or coping strategies
- End with encouragement or a question
- Use "I" statements ("I understand", "I hear you")
- Avoid medical jargon

Remember: You're a supportive friend, not a therapist. Your goal is to listen, validate, and guide toward healthy coping strategies."""
        }]
        
        # Add conversation history (last 5 exchanges)
        if conversation_history:
            for msg in conversation_history[-10:]:
                messages.append({
                    "role": msg["role"],
                    "content": msg["content"]
                })
        
        # Add current message
        messages.append({
            "role": "user",
            "content": user_message
        })
        
        return messages
    
    def _get_fallback_response(self, user_message: str) -> str:
        """Get intelligent fallback response based on keywords"""
        message_lower = user_message.lower()
        
        # Emotion-based patterns
        patterns = {
            r'\b(sad|depressed|down|unhappy|hopeless|lonely|empty)\b': self._response_sad,
            r'\b(anxious|anxiety|nervous|worried|panic|stress|overwhelmed|tense)\b': self._response_anxious,
            r'\b(angry|mad|frustrated|irritated|furious|annoyed)\b': self._response_angry,
            r'\b(scared|afraid|fear|terrified|frightened)\b': self._response_scared,
            r'\b(sleep|insomnia|tired|exhausted|can\'t sleep|awake)\b': self._response_sleep,
            r'\b(exam|test|study|school|college|grades|marks|pressure)\b': self._response_academic,
            r'\b(family|parents|home|mother|father|sibling)\b': self._response_family,
            r'\b(friend|friendship|social|lonely|alone|bullying)\b': self._response_social,
            r'\b(confident|confidence|self-esteem|worth|value)\b': self._response_confidence,
            r'\b(eating|food|weight|body|appetite)\b': self._response_eating,
        }
        
        # Check patterns
        for pattern, response_func in patterns.items():
            if re.search(pattern, message_lower):
                return response_func()
        
        # Check for questions
        if '?' in user_message:
            return self._response_question()
        
        # Check for greetings
        if re.search(r'\b(hi|hello|hey|good morning|good evening)\b', message_lower):
            return self._response_greeting()
        
        # Check for thanks
        if re.search(r'\b(thank|thanks|appreciate)\b', message_lower):
            return self._response_thanks()
        
        # Default empathetic response
        return self._response_default()
    
    # Response functions for different scenarios
    def _response_sad(self) -> str:
        responses = [
            "I hear that you're feeling down right now. 💙 It's okay to feel sad - these emotions are temporary. What do you think might help you feel even a little bit better today?",
            "I'm sorry you're going through this. 🫂 Sadness can feel heavy, but you don't have to carry it alone. Would you like to talk about what's contributing to these feelings?",
            "Thank you for sharing how you're feeling. 💙 It takes courage to acknowledge sadness. Let's think of one small thing that usually brings you comfort - what comes to mind?"
        ]
        return random.choice(responses)
    
    def _response_anxious(self) -> str:
        responses = [
            "Anxiety can feel really overwhelming. 🌟 Let's try grounding together. Take a deep breath and tell me: what are 3 things you can see around you right now?",
            "I understand that worried feeling. 💙 Try the 4-7-8 breathing technique: breathe in for 4, hold for 7, breathe out for 8. Do this a few times. How are you feeling?",
            "Anxious thoughts can spiral quickly. 🫂 Let's slow down together. What's one specific thing that's worrying you most right now? Sometimes naming it helps."
        ]
        return random.choice(responses)
    
    def _response_angry(self) -> str:
        responses = [
            "I can sense your frustration. 💪 It's completely valid to feel angry. Taking a moment to breathe can help. What's making you feel this way?",
            "Anger is a natural emotion. 🌟 It often tells us something important. Would you like to talk about what triggered these feelings?",
            "I hear you're feeling frustrated. 💙 Sometimes anger is our way of protecting ourselves. What do you think your anger is trying to tell you?"
        ]
        return random.choice(responses)
    
    def _response_scared(self) -> str:
        responses = [
            "Feeling scared is difficult. 💙 Right now, in this moment, you're safe. Let's ground ourselves. What's one thing you can touch or hold right now?",
            "I understand fear can be intense. 🫂 You're not alone. Can you tell me what's making you feel afraid? Sometimes sharing it helps.",
            "It's okay to feel scared. 🌟 Fear is our mind trying to protect us. Let's work through this together. What specific thoughts are causing the fear?"
        ]
        return random.choice(responses)
    
    def _response_sleep(self) -> str:
        responses = [
            "Sleep is so important for mental health. 😴 Try establishing a calming bedtime routine: no screens 1 hour before bed, dim lights, maybe some light reading. What's your current sleep routine like?",
            "Trouble sleeping can make everything harder. 💙 Some tips: keep your room cool, avoid caffeine after 2 PM, try progressive muscle relaxation. How many hours are you getting?",
            "Sleep struggles are tough. 🌙 Have you tried: meditation apps, white noise, or writing down your thoughts before bed? What usually keeps you awake?"
        ]
        return random.choice(responses)
    
    def _response_academic(self) -> str:
        responses = [
            "Academic pressure is real! 📚 Remember: your worth isn't defined by grades. Try the Pomodoro technique: 25 min study, 5 min break. What subject is challenging you most?",
            "I understand exam stress. 🌟 Break your study into small chunks, take breaks, stay hydrated. You've got this! What's your biggest concern about your studies?",
            "School pressure can feel intense. 💙 It's okay to ask for help from teachers or peers. What specific challenges are you facing with your studies?"
        ]
        return random.choice(responses)
    
    def _response_family(self) -> str:
        responses = [
            "Family relationships can be complex. 🏠 It's normal to experience challenges at home. Remember, you can't control others, only your reactions. What's been happening?",
            "I hear you about family difficulties. 💙 Sometimes setting boundaries helps, even with family. Would you like to share more about the situation?",
            "Family dynamics can be tough to navigate. 🫂 Your feelings about your family situation are valid. What specific challenge are you facing?"
        ]
        return random.choice(responses)
    
    def _response_social(self) -> str:
        responses = [
            "Friendships and social connections matter. 👥 It's quality over quantity. Even one good friend makes a difference. How are you feeling about your social life?",
            "Social challenges are tough, especially at your age. 💙 Remember, true friends accept you as you are. What's been on your mind about friendships?",
            "Feeling lonely or having friend troubles is hard. 🫂 You're not alone in feeling this way. What specific social situation is bothering you?"
        ]
        return random.choice(responses)
    
    def _response_confidence(self) -> str:
        responses = [
            "Building self-confidence is a journey! 🌟 Start by celebrating small wins. What's one thing you're proud of, even if it seems small?",
            "Self-esteem takes time to build. 💙 Remember: you have unique strengths. What's something you're good at or enjoy doing?",
            "Confidence grows with practice. ✨ Try this: write down 3 things you like about yourself. What would you write?"
        ]
        return random.choice(responses)
    
    def _response_eating(self) -> str:
        responses = [
            "Our relationship with food and body image can be complex. 💙 If you're struggling with eating, please talk to a trusted adult or counselor. What's concerning you?",
            "Body image and eating concerns are serious. 🫂 Your health matters more than appearance. Have you talked to anyone about these feelings?",
            "I'm concerned about what you're sharing regarding food/body. 💙 These are important issues that deserve professional support. Can you reach out to a counselor or doctor?"
        ]
        return random.choice(responses)
    
    def _response_question(self) -> str:
        responses = [
            "That's a thoughtful question! 💙 I'm here to help you explore it. What brought this question to mind?",
            "Good question! 🌟 Let's think about this together. What are your thoughts on it so far?",
            "I'm glad you're asking. 💙 Understanding ourselves and our situations is important. Let me share some perspective..."
        ]
        return random.choice(responses)
    
    def _response_greeting(self) -> str:
        responses = [
            "Hello! 👋 I'm MindfulAI, here to support you. How are you feeling today?",
            "Hi there! 💙 It's good to see you. What's on your mind today?",
            "Hey! 🌟 Welcome. I'm here to listen. How can I support you today?"
        ]
        return random.choice(responses)
    
    def _response_thanks(self) -> str:
        responses = [
            "You're very welcome! 💙 I'm here whenever you need to talk. How are you feeling now?",
            "I'm glad I could help! 🌟 Remember, I'm always here to listen. Is there anything else on your mind?",
            "Happy to support you! 💙 Taking care of your mental health is important. Feel free to come back anytime."
        ]
        return random.choice(responses)
    
    def _response_default(self) -> str:
        responses = [
            "Thank you for sharing that with me. 💙 I'm here to listen and support you. Could you tell me more about how you're feeling?",
            "I hear you. 🫂 Your feelings and experiences matter. What would be most helpful for you right now?",
            "I'm listening. 💙 Sometimes just talking helps. What else is on your mind?",
            "Thank you for opening up. 🌟 I'm here to support you through whatever you're experiencing. How can I help?"
        ]
        return random.choice(responses)
    
    def is_ai_available(self) -> bool:
        """Check if AI is available"""
        return self.ai_available