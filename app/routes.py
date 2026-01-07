# app/routes.py
from flask import Blueprint, render_template, request, jsonify
import re

# Create the blueprint
main_routes = Blueprint('main', __name__)

@main_routes.route('/')
def index():
    return render_template('index.html')

@main_routes.route('/process_command', methods=['POST'])
def process_command():
    try:
        data = request.json
        command = data.get('command', '').lower()
        
        # Process the command
        response_data = process_ai_command(command)
        
        return jsonify({
            'success': True,
            'response': response_data['text'],
            'action': response_data.get('action', 'none'),
            'data': response_data
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

def process_ai_command(command):
    """Process AI commands and return responses"""
    
    command = command.lower().strip()
    
    # Basic identity commands
    if any(word in command for word in ['who are you', 'what is your name', 'your name']):
        return {
            'text': "I'm Lily - Your Advanced AI Assistant! 🤖✨ Created by Faheem Ashraf for the IIT Competition!",
            'action': 'none'
        }
    
    # OPEN WEBSITES
    elif 'open google' in command or 'google' in command:
        return {
            'text': "Opening Google in a new tab...",
            'action': 'open_url',
            'url': 'https://google.com'
        }
    
    elif 'open youtube' in command or 'youtube' in command:
        return {
            'text': "Opening YouTube in a new tab...",
            'action': 'open_url', 
            'url': 'https://youtube.com'
        }
    
    # MUSIC PLAYBACK
    elif 'play music' in command:
        return {
            'text': "🎵 Music Player Activated! I can play Shape of You, Believer, Blinding Lights, Faded, Perfect, Dance Monkey and more!",
            'action': 'music',
            'type': 'list'
        }
    
    elif 'play faded' in command:
        return {
            'text': "🎵 Now playing: Faded by Alan Walker",
            'action': 'music',
            'type': 'play',
            'song': 'faded',
            'url': 'https://www.youtube.com/watch?v=60ItHLz5WEA'
        }
    
    elif 'play shape of you' in command or 'play shape' in command:
        return {
            'text': "🎵 Now playing: Shape of You by Ed Sheeran",
            'action': 'music',
            'type': 'play',
            'song': 'shape of you',
            'url': 'https://www.youtube.com/watch?v=JGwWNGJdvx8'
        }
    
    elif 'play believer' in command:
        return {
            'text': "🎵 Now playing: Believer by Imagine Dragons",
            'action': 'music',
            'type': 'play',
            'song': 'believer',
            'url': 'https://www.youtube.com/watch?v=7wtfhZwyrcc'
        }
    
    # JOKES
    elif any(word in command for word in ['tell me a joke', 'joke']):
        return {
            'text': "Why don't scientists trust atoms? Because they make up everything! 😄",
            'action': 'none'
        }
    
    # GAMES
    elif any(word in command for word in ['play game', 'game']):
        return {
            'text': "🎮 Game Center Activated! Choose from Chess, Trivia, Puzzles, Adventure Games, Tic Tac Toe, or Hangman!",
            'action': 'game',
            'type': 'list'
        }
    
    # MATH
    elif 'calculate' in command or 'math' in command:
        match = re.search(r'(\d+)\s*([+\-*/])\s*(\d+)', command)
        if match:
            num1 = int(match.group(1))
            operator = match.group(2)
            num2 = int(match.group(3))
            
            if operator == '+': result = num1 + num2
            elif operator == '-': result = num1 - num2
            elif operator == '*': result = num1 * num2
            elif operator == '/': result = num1 / num2 if num2 != 0 else 'Error: Division by zero'
            
            return {
                'text': f"🧮 Calculation: {num1} {operator} {num2} = {result}",
                'action': 'none'
            }
        return {
            'text': "🧮 Math Magic Show! Try: 'calculate 15 * 23'",
            'action': 'none'
        }
    
    # Default response
    return {
        'text': f"I understand you're asking about: '{command}'\\n\\nI can help with:\\n• Basic Questions\\n• Music Playback\\n• Games\\n• Cartoon Conversations\\n• Math Calculations\\n• AI Tools\\n\\nTry: 'play music', 'tell me a joke', or 'what can you do'",
        'action': 'none'
    }