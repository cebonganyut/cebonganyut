import os
import time
import requests
from whatsapp_bot import WhatsAppBot

# Konfigurasi API Gemini
API_KEY = os.environ.get('AIzaSyCN94L68GCs9s9hVOTNysDJHNT3m5YOEFw')
URL = f"https://generativelanguage.googleapis.com/v1/models/gemini-pro:generateContent?key={API_KEY}"

def generate_content(user_input):
    headers = {'Content-Type': 'application/json'}
    data = {
        "contents": [
            {
                "role": "user",
                "parts": [{"text": user_input}]
            }
        ]
    }
    
    try:
        response = requests.post(URL, headers=headers, json=data)
        response.raise_for_status()  # Akan raise exception untuk status code error
        
        response_json = response.json()
        text = response_json['candidates'][0]['content']['parts'][0]['text']
        return text
    except requests.RequestException as e:
        print(f"Error in API request: {e}")
        return "Maaf, terjadi kesalahan saat memproses permintaan Anda."
    except (KeyError, IndexError) as e:
        print(f"Error parsing API response: {e}")
        return "Maaf, terjadi kesalahan saat memproses respons."

# Inisialisasi WhatsApp bot
bot = WhatsAppBot()

print("Silakan scan QR Code untuk login ke WhatsApp Web")
bot.wait_for_login()
print("Login berhasil!")

@bot.message_handler(pattern=".*")
def reply_to_message(message):
    print(f"Menerima pesan: {message.content}")
    response = generate_content(message.content)
    print(f"Mengirim balasan: {response}")
    message.reply(response)

print("Bot siap menerima pesan...")
bot.start()

# Keep the script running
while True:
    try:
        time.sleep(1)
    except KeyboardInterrupt:
        print("Mematikan bot...")
        bot.stop()
        break
