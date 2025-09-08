from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import logging

app = Flask(__name__)

# Enable logging
logging.basicConfig(level=logging.INFO)

@app.route("/whatsapp", methods=["POST"])
def whatsapp_reply():
    incoming_msg = request.values.get('Body', '').lower()
    sender = request.values.get('From', '')
    
    logging.info(f"Message from {sender}: {incoming_msg}")
    
    resp = MessagingResponse()
    msg = resp.message()
    
    # Command handling
    if 'hi' in incoming_msg or 'hello' in incoming_msg:
        msg.body("Hello! Welcome to our WhatsApp bot. Type 'Help' to see commands.")
    elif 'help' in incoming_msg:
        msg.body("Commands:\n1. Hi / Hello\n2. Info\n3. Contact")
    elif 'info' in incoming_msg:
        msg.body("This is a WhatsApp bot built with Flask. It runs on the cloud!")
    elif 'contact' in incoming_msg:
        msg.body("You can reach us at: +92-XXXXXXXXXX")
    else:
        msg.body("I received your message: " + incoming_msg + "\nType 'Help' to see commands.")
    
    return str(resp)

if __name__ == "__main__":
    # Bind to 0.0.0.0 for cloud deployment
    app.run(host="0.0.0.0", port=5000)


