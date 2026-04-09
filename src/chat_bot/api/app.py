from flask import Flask, render_template, request, jsonify, session
import os
from src.chat_bot.config import settings
from src.chat_bot.models.vector_db import VectorDBManager
from src.chat_bot.core.chat_logic import ChatManager
from src.chat_bot.utils.logging import app_logger

def create_app():
    app = Flask(__name__, 
                static_folder='../../../static', 
                template_folder='../../../templates')
    app.secret_key = settings.SECRET_KEY

    # Initialize Managers (Singleton-like behavior for the app)
    # Note: In a production environment with multiple workers, 
    # you'd want to handle this differently (e.g., persistent connections)
    db_manager = VectorDBManager()
    chat_manager = ChatManager()

    @app.route('/')
    def index():
        if 'model_choice' not in session:
            session['model_choice'] = 'groq'
        return render_template('index.html', model_choice=session['model_choice'])

    @app.route('/about')
    def about():
        return render_template('about.html')

    @app.route('/get_chat_history')
    def get_chat_history():
        return jsonify(session.get('chat_history', []))

    @app.route('/save_chat_history', methods=['POST'])
    def save_chat_history():
        data = request.json
        session['chat_history'] = data.get('history', [])
        return jsonify({"status": "success"})

    @app.route('/set_model', methods=['POST'])
    def set_model():
        data = request.json
        model_choice = data.get('model_choice')
        if model_choice in ['groq', 'openrouter']:
            session['model_choice'] = model_choice
            return jsonify({"status": "success", "model": model_choice})
        return jsonify({"status": "error", "message": "Invalid model choice"}), 400

    @app.route('/chat', methods=['POST'])
    def chat():
        data = request.json
        query = data.get('message', '')
        chat_history = data.get('history', [])
        model_choice = session.get('model_choice', 'groq')
        
        app_logger.info(f"User Query: {query}")
        
        # Get context from database
        context = db_manager.search(query)
        
        # Get response from selected model
        messages = chat_history + [{"role": "user", "content": query}]
        response = chat_manager.get_response(messages, context, model_choice)
        
        # Update session history
        new_history = messages + [{"role": "assistant", "content": response}]
        session['chat_history'] = new_history
        
        return jsonify({
            'response': response,
            'context': context
        })

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=5000, debug=True)
