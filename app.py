from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from twilio.rest import Clients
import flask

app = Flask(app.py)

# ==============================
# 🔑 Twilio Config
# ==============================
# 👉 Get these from https://console.twilio.com/
TWILIO_ACCOUNT_SID = "ACbb808dd2c5127739aef94eed7647cecf"  # your Account SID
TWILIO_AUTH_TOKEN = "ce9a4ac094b68f5fb560e39884750239"             # your Auth Token
TWILIO_WHATSAPP_NUMBER = "+14155238886"       # Twilio Sandbox or your purchased WhatsApp number

client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

# ==============================
# Simple User State
# ==============================
user_sessions = {}  

# ==============================
# Routes
# ==============================

@app.route("/")
def home():
    return "🚀 Twilio DocFiler Bot is running!"


@app.route("/webhook", methods=["GET"])
def webhook():
    """Handle incoming WhatsApp messages from Twilio"""
    from_number = request.form.get("From", "")
    incoming_msg = request.form.get("Body", "").strip()
    response = MessagingResponse()
    msg = response.message()

    # Initialize session if new user
    if from_number not in user_sessions:
        user_sessions[from_number] = {"step": "name", "data": {}}
        msg.body("👋 Welcome to *DocFiler*!\nLet’s auto-fill your document.\n\n👉 What’s your *full name*?")
        return str(response)

    session = user_sessions[from_number]

    # Handle steps
    if session["step"] == "name":
        session["data"]["name"] = incoming_msg
        session["step"] = "age"
        msg.body("✅ Got it!\nNow, please enter your *age*.")

    elif session["step"] == "age":
        session["data"]["age"] = incoming_msg
        session["step"] = "address"
        msg.body("✅ Thanks!\nPlease share your *address*.")

    elif session["step"] == "address":
        session["data"]["address"] = incoming_msg
        session["step"] = "done"

        # Example auto-filled document text
        doc_text = (
            "📄 *Auto-filled Document*\n\n"
            f"👤 Name: {session['data']['name']}\n"
            f"🎂 Age: {session['data']['age']}\n"
            f"🏠 Address: {session['data']['address']}\n\n"
            "✅ This info has been recorded by DocFiler."
        )

        msg.body(doc_text)

        # Reset session
        del user_sessions[from_number]

    else:
        msg.body("🤖 Something went wrong. Type *start* to begin again.")
        user_sessions.pop(from_number, None)

    return str(response)


# ==============================
# Run app
# ==============================
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)


