from flask import Flask, request, jsonify
from flask_cors import CORS
import logging
from agent import WebSearchAssistant, chat as agent_chat

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s: %(message)s')
app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

CONTEXT_SIZE = 65536


@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.json
    if not data or 'message' not in data:
        return jsonify({"error": "Missing required fields: message"}), 400

    message = data['message']

    try:
        response = agent_chat(assistant_client, assistant, thread, message)

        return jsonify({
            "role": "assistant",
            "content": str(response)
        })
    except Exception as e:
        logging.error(f"Chat error: {e}")
        return jsonify({"error": str(e)}), 500


@app.route('/api/clear_chat', methods=['POST'])
def clear_chat():
    try:

        return jsonify({"message": "Chat history cleared"})
    except Exception as e:
        logging.error(f"Clear chat error: {e}")
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    assistant_client = WebSearchAssistant()
    # Create an assistant and a new thread.
    assistant = assistant_client.create_assistant()
    thread = assistant_client.create_thread()
    app.run(host='0.0.0.0', port=5555)
