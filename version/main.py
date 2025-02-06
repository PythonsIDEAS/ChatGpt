from flask import Flask, request, jsonify
from flask_cors import CORS
from gptclient import GPTClient  # Import the updated GPTClient class

app = Flask(__name__)
CORS(app)

# Initialize GPT client
gpt_client = GPTClient()

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_message = data.get("message", "")

    if not user_message:
        return jsonify({"error": "Empty message"}), 400

    # Get the AI response
    ai_response = gpt_client.get_response(user_message)

    return jsonify({"response": ai_response})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)


