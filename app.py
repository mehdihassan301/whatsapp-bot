from flask import Flask, request
import requests
import os

app = Flask(__name__)

# ==============================
# 🔑 WhatsApp Cloud API Settings
# ==============================
VERIFY_TOKEN = "probsolv_2025_secret"  # You choose this (must match Meta portal)
WHATSAPP_ACCESS_TOKEN = "EAAKxZAvmtQpsBPfDKQl7lFeIKHy4XEZCQhiEXoXRbZAZCgTTYhe3ZBjEe3kUFEsZBoKoRZCRffFZBhvUOKW9rTaHahKGIwjf30ijBZA5ipnnFMSaLXb1VfmeR1nOa9zLxpKwspVU3nBeyr9bHZBrgrloCAk6ZARDYEggEUZCoFwfqj1by68znIaehQb3TSZAHZCNTLa5NRD7PzReERvpErEXlOBopjdnpjTLFkxupEvVQKXzKLH7W6HQZDZD"
PHONE_NUMBER_ID = "768273019710136"
RECIPIENT_WA_NUMBER = "923272583013"  # Your WhatsApp number
# ==============================

@app.route("/webhook", methods=["GET", "POST"])
def webhook():
    if request.method == "GET":
        # Meta webhook verification
        mode = request.args.get("hub.mode")
        token = request.args.get("hub.verify_token")
        challenge = request.args.get("hub.challenge")

        if mode == "subscribe" and token == VERIFY_TOKEN:
            return challenge, 200
        else:
            return "Verification failed", 403

    if request.method == "POST":
        data = request.get_json()
        print("📩 Incoming:", data)

        # Extract message text (if exists)
        try:
            message = data["entry"][0]["changes"][0]["value"]["messages"][0]
            from_number = message["from"]
            msg_body = message["text"]["body"]

            print(f"Message from {from_number}: {msg_body}")

            # Send reply
            send_whatsapp_message(from_number, f"✅ I received your message: {msg_body}")
        except Exception as e:
            print("❌ Error handling message:", e)

        return "EVENT_RECEIVED", 200


def send_whatsapp_message(to, message):
    """Send WhatsApp message via Cloud API"""
    url = f"https://graph.facebook.com/v17.0/{PHONE_NUMBER_ID}/messages"
    headers = {
        "Authorization": f"Bearer {WHATSAPP_ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }
    payload = {
        "messaging_product": "whatsapp",
        "to": to,
        "text": {"body": message}
    }

    r = requests.post(url, headers=headers, json=payload)
    print("📤 Sent reply:", r.status_code, r.text)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)



