from flask import Blueprint, render_template, request, jsonify
import os
import time
import requests
import google.generativeai as genai
from urllib.parse import quote
import random
import datetime
import re

main_routes = Blueprint('main', __name__)

# Configuration
ASSISTANT_NAME = os.environ.get("ASSISTANT_NAME", "Lily")
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
NEWS_API_KEY = os.environ.get("NEWS_API_KEY")

if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)

# Enhanced music library matching your HTML exactly
music_library = {
    "shape of you": {
        "title": "Shape of You",
        "artist": "Ed Sheeran",
        "url": "https://www.youtube.com/watch?v=JGwWNGJdvx8"
    },
    "believer": {
        "title": "Believer",
        "artist": "Imagine Dragons",
        "url": "https://www.youtube.com/watch?v=7wtfhZwyrcc"
    },
    "faded": {
        "title": "Faded",
        "artist": "Alan Walker",
        "url": "https://www.youtube.com/watch?v=60ItHLz5WEA"
    },
    "tum hi ho": {
        "title": "Tum Hi Ho",
        "artist": "Arijit Singh",
        "url": "https://www.youtube.com/shorts/yLzsCp7q9Y8"
    },
    "gerua": {
        "title": "Gerua",
        "artist": "Arijit Singh & Antara Mitra",
        "url": "https://www.youtube.com/watch?v=9D9dY9nYhuw"
    },
    "radha": {
        "title": "Radha",
        "artist": "Shreya Ghoshal",
        "url": "https://www.youtube.com/watch?v=Z_dbZGqe_4I"
    },
    "so high": {
        "title": "So High",
        "artist": "Sidhu Moose Wala",
        "url": "https://www.youtube.com/watch?v=UqUv4VBB-7c"
    },
    "flowers": {
        "title": "Flowers",
        "artist": "Miley Cyrus",
        "url": "https://www.youtube.com/watch?v=G7KNmW9a75Y"
    },
    "as it was": {
        "title": "As It Was",
        "artist": "Harry Styles",
        "url": "https://www.youtube.com/watch?v=H5v3kku4y6Q"
    },
    "stay": {
        "title": "Stay",
        "artist": "The Kid LAROI & Justin Bieber",
        "url": "https://www.youtube.com/watch?v=kTJczUoc26U"
    },
    "levitating": {
        "title": "Levitating",
        "artist": "Dua Lipa",
        "url": "https://www.youtube.com/watch?v=TUVcZfQe-Kw"
    },
    "blinding lights": {
        "title": "Blinding Lights",
        "artist": "The Weeknd",
        "url": "https://www.youtube.com/watch?v=4NRXx6U8ABQ"
    },
    "dance monkey": {
        "title": "Dance Monkey",
        "artist": "Tones and I",
        "url": "https://www.youtube.com/watch?v=q0hyYWKXF0Q"
    },
    "perfect": {
        "title": "Perfect",
        "artist": "Ed Sheeran",
        "url": "https://www.youtube.com/watch?v=2Vv-BfVoq4g"
    },
    "see you again": {
        "title": "See You Again",
        "artist": "Wiz Khalifa ft. Charlie Puth",
        "url": "https://www.youtube.com/watch?v=RgKAFK5djSk"
    },
    "despacito": {
        "title": "Despacito",
        "artist": "Luis Fonsi ft. Daddy Yankee",
        "url": "https://www.youtube.com/watch?v=kJQP7kiw5Fk"
    },
    "uptown funk": {
        "title": "Uptown Funk",
        "artist": "Mark Ronson ft. Bruno Mars",
        "url": "https://www.youtube.com/watch?v=OPf0YbXqDm0"
    },
    "bad guy": {
        "title": "Bad Guy",
        "artist": "Billie Eilish",
        "url": "https://www.youtube.com/watch?v=DyDfgMOUjCI"
    },
    "senorita": {
        "title": "Señorita",
        "artist": "Shawn Mendes & Camila Cabello",
        "url": "https://www.youtube.com/watch?v=Pkh8UtuejGw"
    },
    "old town road": {
        "title": "Old Town Road",
        "artist": "Lil Nas X ft. Billy Ray Cyrus",
        "url": "https://www.youtube.com/watch?v=r7qovpFAGrQ"
    },
    "cheap thrills": {
        "title": "Cheap Thrills",
        "artist": "Sia ft. Sean Paul",
        "url": "https://www.youtube.com/watch?v=nYh-n7EOtMA"
    },
    "happier": {
        "title": "Happier",
        "artist": "Marshmello ft. Bastille",
        "url": "https://www.youtube.com/watch?v=m7Bc3pLyij0"
    },
    "rockstar": {
        "title": "Rockstar",
        "artist": "Post Malone ft. 21 Savage",
        "url": "https://www.youtube.com/watch?v=UceaB4D0jpo"
    },
    "god's plan": {
        "title": "God's Plan",
        "artist": "Drake",
        "url": "https://www.youtube.com/watch?v=xpVfcZ0ZcFM"
    }
}

# Jokes database matching your HTML
jokes = [
    "Why don't scientists trust atoms? Because they make up everything!",
    "Why did the scarecrow win an award? He was outstanding in his field!",
    "Why don't eggs tell jokes? They'd crack each other up!",
    "What do you call a fake noodle? An impasta!",
    "Why did the math book look so sad? Because it had too many problems!",
    "What do you call a bear with no teeth? A gummy bear!",
    "Why don't skeletons fight each other? They don't have the guts!",
    "What do you call a sleeping bull? A bulldozer!"
]

# Stories database matching your HTML
stories = [
    "**The Mysterious Forest**\n\nOnce upon a time, in a forest where trees whispered secrets, a young explorer discovered a glowing crystal that could understand animal languages. She used it to help forest creatures live in harmony, learning that true magic lies in understanding and kindness.",

    "**The Star Collector**\n\nEvery night, an old astronomer would collect fallen stars in a special net. One evening, a tiny star asked to stay with him, and together they created the most beautiful constellations, teaching everyone that even the smallest light can make a big difference.",

    "**The Time Traveler's Garden**\n\nIn a hidden garden where flowers bloomed in different time periods, a curious gardener discovered she could travel through time by touching specific flowers. She used this gift to fix small mistakes in history, learning that every moment is precious.",

    "**The Whispering Ocean**\n\nA young sailor discovered that the ocean could speak during full moons. The waves shared ancient stories of sunken cities and lost treasures, teaching him that the greatest wealth is knowledge and friendship."
]

# Advice database matching your HTML
advice_list = [
    "💡 **Life Advice:** Take time to appreciate small moments - they often become cherished memories.",
    "💡 **Productivity Tip:** Break big tasks into smaller steps. Progress, no matter how small, is still progress!",
    "💡 **Wellness Tip:** Remember to stay hydrated and take short breaks throughout your day.",
    "💡 **Learning Advice:** The expert in anything was once a beginner. Keep learning and growing!",
    "💡 **Relationship Tip:** Communication is key. Always express your feelings honestly and listen actively.",
    "💡 **Financial Advice:** Save at least 20% of your income and invest in your future self.",
    "💡 **Career Tip:** Network genuinely and always be learning new skills in your field."
]

# Website database matching your HTML
websites = {
    'youtube': {
        'name': 'YouTube',
        'url': 'https://www.youtube.com',
        'icon': 'fab fa-youtube',
        'description': 'Enjoy your favorite videos and music, and upload your own content to share with friends, family, and the world.'
    },
    'google': {
        'name': 'Google',
        'url': 'https://www.google.com',
        'icon': 'fab fa-google',
        'description': 'Search the world\'s information, including webpages, images, videos and more.'
    },
    'github': {
        'name': 'GitHub',
        'url': 'https://www.github.com',
        'icon': 'fab fa-github',
        'description': 'GitHub is where over 100 million developers shape the future of software together.'
    },
    'netflix': {
        'name': 'Netflix',
        'url': 'https://www.netflix.com',
        'icon': 'fab fa-netflix',
        'description': 'Watch TV shows and movies anytime, anywhere.'
    },
    'spotify': {
        'name': 'Spotify',
        'url': 'https://www.spotify.com',
        'icon': 'fab fa-spotify',
        'description': 'Music for everyone. Millions of songs.'
    },
    'amazon': {
        'name': 'Amazon',
        'url': 'https://www.amazon.com',
        'icon': 'fab fa-amazon',
        'description': 'Online shopping for electronics, apparel, and more.'
    }
}

@main_routes.route('/')
def home():
    return render_template('index.html')

@main_routes.route('/process_command', methods=['POST'])
def process_command():
    try:
        data = request.json
        command = data.get('command', '').strip()
        
        if not command:
            return jsonify({'response': 'Please type a command!'})
        
        response = process_user_command(command)
        return jsonify({'response': response})
        
    except Exception as e:
        return jsonify({'response': f'Sorry, an error occurred: {str(e)}'})

def process_user_command(command):
    command_lower = command.lower().strip()
    
    # Enhanced greeting with animation-ready response
    if any(word in command_lower for word in ['hello', 'hi', 'hey']):
        return f"👋 **Hello! I'm {ASSISTANT_NAME}!**\n\nI'm your intelligent digital companion, ready to assist you with music, information, entertainment, and much more!\n\nTry saying **'what can you do'** to see all available commands or use the quick commands menu!"
    
    # Help and capabilities
    if command_lower in ['help', 'commands', 'what can you do', 'capabilities']:
        return get_help_commands()
    
    # About creator
    elif any(word in command_lower for word in ["who is your owner", "who made you", "who created you", "about creator"]):
        return get_owner_info()
    
    # Name query
    elif "your name" in command_lower or "what is your name" in command_lower:
        return f"👋 **My name is {ASSISTANT_NAME}!**\n\nI'm your personal AI assistant designed to make your life easier and more enjoyable!"
    
    # Time and date
    elif 'time' in command_lower:
        current_time = time.strftime('%I:%M:%S %p')
        return f"🕒 **Current Time:** {current_time}"
    
    elif 'date' in command_lower:
        current_date = time.strftime('%A, %B %d, %Y')
        return f"📅 **Today is:** {current_date}"
    
    # Music commands - enhanced with your HTML structure
    elif command_lower.startswith('play '):
        return play_song(command_lower[5:])
    
    elif any(word in command_lower for word in ['pause', 'stop music']):
        return "⏸️ **Music paused.** Click play to resume or say 'play music' to continue."
    
    elif any(word in command_lower for word in ['next', 'skip']):
        return "⏭️ **Skipped to next track!**"
    
    elif any(word in command_lower for word in ['previous', 'back']):
        return "⏮️ **Went back to previous track!**"
    
    # Website commands
    elif command_lower.startswith('open '):
        return open_website(command_lower[5:])
    
    # Information commands
    elif 'news' in command_lower:
        return get_news()
    
    elif 'weather' in command_lower:
        return get_weather()
    
    # Entertainment commands
    elif 'joke' in command_lower:
        return f"😄 **{get_joke()}**"
    
    elif 'advice' in command_lower:
        return get_advice()
    
    elif 'story' in command_lower:
        return get_story()
    
    elif 'songs' in command_lower or 'music list' in command_lower or 'available songs' in command_lower:
        return get_songs_list()
    
    # Calculator functionality
    elif any(word in command_lower for word in ['calculate', 'math', 'solve']) or \
         any(op in command_lower for op in ['+', '-', '*', '/']):
        return calculate_math(command_lower)
    
    # Voice commands
    elif 'voice' in command_lower:
        return "🎤 **Voice recognition activated!** Speak your command and I'll respond accordingly."
    
    # Theme commands
    elif 'theme' in command_lower or 'dark mode' in command_lower or 'light mode' in command_lower:
        return "🎨 **Theme switched!** Enjoy the new look and feel of the interface."
    
    # Clear chat
    elif 'clear' in command_lower or 'reset' in command_lower:
        return "🗑️ **Chat cleared!** Starting fresh with a clean conversation."
    
    # Polite responses
    elif any(word in command_lower for word in ["thank you", "thanks"]):
        return "😊 **You're welcome!** I'm always happy to help you with anything you need."
    
    elif any(word in command_lower for word in ["bye", "goodbye", "exit"]):
        return f"👋 **Goodbye!** Thanks for chatting with {ASSISTANT_NAME}. Come back anytime you need assistance!"
    
    # Default AI processing
    else:
        return ai_process(command)

def play_song(song_name):
    song_name = song_name.strip()
    if not song_name:
        return "🎵 **Please tell me which song to play!**\n\nTry: 'play shape of you' or 'play music' for a random song"
    
    # Check exact match
    if song_name in music_library:
        song = music_library[song_name]
        return f"🎵 **Playing:** {song['title']} by {song['artist']}\n\n• Song opened in YouTube\n• Use music player controls for navigation\n• Say 'next' or 'previous' to change songs"
    
    # Check partial matches
    for key, song_data in music_library.items():
        if song_name in key:
            return f"🎵 **Playing:** {song_data['title']} by {song_data['artist']}\n\n• Song opened in YouTube\n• Use music player controls for navigation\n• Say 'songs' to see all available tracks"
    
    # If not found, provide helpful response
    available_songs = list(music_library.keys())[:8]
    return f"🎵 **Song Not Found**\n\nI couldn't find '{song_name}' in my library of {len(music_library)}+ songs.\n\n**Available songs include:** {', '.join(available_songs)}\n\nTry: 'play [song name]' or 'songs' to see all available tracks"

def open_website(site_name):
    site_name = site_name.strip()
    if not site_name:
        return "🌐 **Please specify which website to open!**\n\nAvailable: YouTube, Google, GitHub, Netflix, Spotify, Amazon"
    
    if site_name in websites:
        site = websites[site_name]
        return f"🌐 **Opening {site['name']}**\n\n{site['description']}\n\n• Website opening in new tab\n• Full browsing experience available\n• Say 'open [site]' for other websites"
    
    return f"❌ **Website Not Supported**\n\nI can open: {', '.join(websites.keys())}\n\nTry: 'open youtube' or 'open google'"

def get_news():
    # Enhanced news response matching your HTML
    return """📰 **Latest News Headlines:**

• **AI Technology** Reaches New Milestones in Healthcare
• **Space Exploration:** Mars Mission Updates Revealed  
• **Climate Change** Solutions Making Significant Progress
• **Tech Giants** Announce Groundbreaking Innovations
• **Global Economy** Shows Positive Growth Trends

For specific news categories, try: 'tech news', 'sports news', or 'business updates'"""

def get_weather():
    return """🌤️ **Weather Information:**

**Currently:** Partly Cloudy, 72°F (22°C)
**Today:** High 75°F (24°C), Low 65°F (18°C)
**Humidity:** 65%, **Wind:** 8 mph NE
**Condition:** Perfect day to go outside!

For location-specific forecasts, try: 'weather in [city name]'"""

def get_joke():
    return random.choice(jokes)

def get_advice():
    return random.choice(advice_list)

def get_story():
    return f"📖 {random.choice(stories)}"

def get_songs_list():
    song_list = "\n".join([f"🎵 **{song_data['title']}** - {song_data['artist']}" for song_data in music_library.values()])
    return f"🎵 **Available Songs ({len(music_library)}+ popular tracks):**\n\n{song_list}\n\n**Say 'play [song name]'** to play any of these songs directly from YouTube!"

def calculate_math(command):
    try:
        # Extract math expression
        math_text = command.replace('calculate', '').replace('math', '').replace('solve', '').strip()
        
        # Simple calculation handling
        if '+' in math_text:
            parts = math_text.split('+')
            if len(parts) == 2:
                num1 = float(parts[0].strip())
                num2 = float(parts[1].strip())
                result = num1 + num2
                return f"🔢 **Calculation:** {num1} + {num2} = **{result}**"
        
        elif '-' in math_text:
            parts = math_text.split('-')
            if len(parts) == 2:
                num1 = float(parts[0].strip())
                num2 = float(parts[1].strip())
                result = num1 - num2
                return f"🔢 **Calculation:** {num1} - {num2} = **{result}**"
        
        elif '*' in math_text:
            parts = math_text.split('*')
            if len(parts) == 2:
                num1 = float(parts[0].strip())
                num2 = float(parts[1].strip())
                result = num1 * num2
                return f"🔢 **Calculation:** {num1} × {num2} = **{result}**"
        
        elif '/' in math_text:
            parts = math_text.split('/')
            if len(parts) == 2:
                num1 = float(parts[0].strip())
                num2 = float(parts[1].strip())
                if num2 != 0:
                    result = num1 / num2
                    return f"🔢 **Calculation:** {num1} ÷ {num2} = **{result}**"
                else:
                    return "❌ **Error:** Division by zero is not allowed"
        
        return """🔢 **Calculator Help:**

**Try these examples:**
• "calculate 15 + 23"
• "calculate 100 / 5" 
• "calculate 8 * 7"
• "calculate 50 - 15"

I can handle basic arithmetic operations with ease!"""
        
    except Exception as e:
        return f"❌ **Calculation Error**\n\nI couldn't process that calculation. Please try a simpler format like: 'calculate 15 + 23'"

def get_owner_info():
    return """About My Creator

I was created by Faheem Ashraf, a passionate developer from Kashmir who believes in making technology accessible and helpful for everyone!

He is studying Computer Science Engineering at Mewar University and designed me to be your reliable digital companion for everyday tasks, entertainment, and assistance. My mission is to make your life easier and more enjoyable!

Connect with him on LinkedIn: www.linkedin.com/in/faheem-ul-islam-rather-08b009348"""



def get_help_commands():
    return f"""🌟 **{ASSISTANT_NAME} AI - Your Complete Assistant**

🎵 **Music & Entertainment**
• Play 25+ popular songs directly from YouTube
• Music player with full controls (play, pause, next, previous)
• YouTube integration with real music playback

🌐 **Web Navigation** 
• Direct access to YouTube, Google, GitHub, Netflix, Spotify, Amazon
• Quick website opening with preview
• Seamless browsing experience

📰 **Live Information**
• Latest news headlines and updates
• Current time and calendar information  
• Weather forecasts and conditions

🔢 **Tools & Utilities**
• Mathematical calculations and problem solving
• Smart command recognition
• Voice command support

💡 **Life Assistance**
• Helpful advice for daily life and decisions
• Learning support and motivation
• Entertainment and creative interactions

😊 **Entertainment Features**
• Interactive stories and narratives
• Fun jokes and humor
• Interesting facts and trivia

🎯 **Quick Commands:**
• "play [song name]" - Play specific song
• "open [website]" - Open any supported website
• "news" - Latest headlines
• "time/date" - Current time/date
• "weather" - Weather information  
• "joke" - Tell a joke
• "story" - Short story
• "calculate" - Math operations
• "advice" - Life advice
• "songs" - Show available songs
• "voice" - Activate voice commands

💬 **Just ask anything else** - I'm here to help with whatever you need!"""

def ai_process(command):
    if not GEMINI_API_KEY:
        # Enhanced default response matching your HTML
        return f"""🤖 **I understand you're looking for:** "{command}"

**I can help you with:**
• **Playing music** (25+ songs available)
• **Opening websites** directly  
• **Getting news**, time, weather updates
• **Telling jokes** & entertaining stories
• **Mathematical calculations** & problem solving
• **Life advice** & helpful suggestions

**Try these commands:**
• "play shape of you"
• "open youtube"
• "what can you do" 
• "what songs are available"
• "tell me a joke"

Or ask me anything else - I'll do my best to assist you!"""
    
    try:
        model = genai.GenerativeModel('gemini-pro')
        response = model.generate_content(command)
        return f"🤖 {response.text}"
    except Exception as e:
        return f"🤖 **I understand:** '{command}'\n\nHow can I assist you with that? If you need specific features, try the commands above!"

@main_routes.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'assistant': ASSISTANT_NAME,
        'features': {
            'music_library': len(music_library),
            'websites': len(websites),
            'ai_enabled': bool(GEMINI_API_KEY),
            'news_enabled': bool(NEWS_API_KEY)
        },
        'timestamp': datetime.datetime.now().isoformat(),
        'version': '3.0'
    })