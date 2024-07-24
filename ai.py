import os
import time
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

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

# Inisialisasi browser
driver = webdriver.Chrome()  # Pastikan ChromeDriver sudah diinstal dan ada di PATH
driver.get("https://web.whatsapp.com")
print("Silakan scan QR code untuk login ke WhatsApp Web")

input("Tekan Enter setelah berhasil login...")

while True:
    try:
        # Cek pesan baru
        unread = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'span[aria-label="Belum dibaca"][data-icon="unread-count"]'))
        )
        
        for chat in unread:
            chat.click()
            
            message_element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'div.selectable-text.copyable-text'))
            )
            message = message_element.text
            
            # Generate balasan
            reply = generate_content(message)
            
            # Kirim balasan
            input_box = driver.find_element(By.CSS_SELECTOR, 'div[contenteditable="true"]')
            input_box.send_keys(reply)
            driver.find_element(By.CSS_SELECTOR, 'button[aria-label="Kirim"]').click()
        
        time.sleep(10)  # Tunggu 10 detik sebelum cek lagi
        
    except Exception as e:
        print(f"An error occurred: {e}")
        time.sleep(60)  # Jika terjadi error, tunggu 1 menit sebelum mencoba lagi

driver.quit()
