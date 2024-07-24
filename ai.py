import pywhatkit
import time
from pywhatkit.core import core
from pywhatkit.remotekit import start_server
import requests
import json
import os

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
    
    response = requests.post(URL, headers=headers, json=data)
    
    if response.status_code == 200:
        response_json = response.json()
        text = response_json['candidates'][0]['content']['parts'][0]['text']
        return text
    else:
        return f"Error: {response.status_code}, {response.text}"

def reply_to_message(message):
    response = generate_content(message)
    return response

# Inisialisasi WhatsApp
start_server()
print("Scan QR Code to login to WhatsApp Web")
pywhatkit.web.open_web()
time.sleep(30)  # Berikan waktu untuk scan QR code

while True:
    try:
        # Cek pesan baru
        unread = core.check_number()
        if unread:
            for msg in unread:
                sender = msg['sender']
                message = msg['message']
                
                # Generate dan kirim balasan
                reply = reply_to_message(message)
                pywhatkit.sendwhatmsg_instantly(sender, reply, wait_time=10)
                
        time.sleep(10)  # Tunggu 10 detik sebelum cek lagi
    except Exception as e:
        print(f"An error occurred: {e}")
        time.sleep(60)  # Jika terjadi error, tunggu 1 menit sebelum mencoba lagi
