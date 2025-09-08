from flask import Flask, request, jsonify
from twilio.twiml.messaging_response import MessagingResponse
from twilio.rest import Client
import os

app = Flask(__name__)

# ---------------------------
# Twilio Config
# ---------------------------
TWILIO_ACCOUNT_SID = os.environ.get("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.environ.get("TWILIO_AUTH_TOKEN")
TWILIO_WHATSAPP_NUMBER = os.environ.get("TWILIO_WHATSAPP_NUMBER")
client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

# ---------------------------
# Meta (Cloud API) Config
# ---------------------------
VERIFY_TOKEN = os.environ.get("VERIFY_TOKEN", "my_verify_token")  
# 👆 You can set this in Railway → Variables (make it match the token you set in Meta Developer Portal)

# ---------------------------
# Routes
# ---------------------------

@app.route("/")
def home():
    return "🚀 WhatsApp Bot is running!"

# ---- Meta Cloud API Webhook Verification ----
@app.route("/webhook", methods=["GET", "POST"])
def webhook():
    if request.method == "GET":  # Verification (Meta)
        mode = request.args.get("hub.mode")
        token = request.args.get("hub.verify_token")
        challenge = request.args.get("hub.challenge")

        if mode == "subscribe" and token == VERIFY_TOKEN:
            return challenge, 200
        else:
            return "❌ Verification failed", 403

    elif request.method == "POST":  # Handle incoming messages (Twilio or Meta)
        data = request.get_json(silent=True)

        # ---------------------------
        # Case 1: Twilio Incoming Message
        # ---------------------------
        if request.form:  
            incoming_msg = request.form.get("Body", "").lower()
            response = MessagingResponse()
            msg = response.message()

            if "hello" in incoming_msg:
                msg.body("👋 Hello! How can I help you today?")
            else:
                msg.body("🤖 I'm a bot powered by Twilio + Flask!")

            return str(response)

        # ---------------------------
        # Case 2: Meta Cloud API Incoming Message
        # ---------------------------
        if data and "entry" in data:
            for entry in data["entry"]:
                for change in entry.get("changes", []):
                    value = change.get("value", {})
                    messages = value.get("messages", [])
                    for message in messages:
                        from_number = message["from"]
                        text = message.get("text", {}).get("body", "")

                        # Example: reply using Twilio
                        client.messages.create(
                            from_=f"whatsapp:{TWILIO_WHATSAPP_NUMBER}",
                            body=f"You said: {text}",
                            to=f"whatsapp:{from_number}"
                        )
            return jsonify({"status": "received"}), 200

        return "ok", 200

# ---------------------------
# Run app
# ---------------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

if __name__ == "__main__":
    # Bind to 0.0.0.0 for cloud deployment
    app.run(host="0.0.0.0", port=5000)


