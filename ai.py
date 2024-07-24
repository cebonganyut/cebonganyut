Berikut adalah versi Python dari program tersebut yang memungkinkan Anda untuk memasukkan teks secara bebas:

```python
import requests
import json

API_KEY = "AIzaSyCN94L68GCs9s9hVOTNysDJHNT3m5YOEFw"
URL = f"https://generativelanguage.googleapis.com/v1/models/gemini-pro:generateContent?key={API_KEY}"

def generate_content(user_input):
    headers = {
        'Content-Type': 'application/json'
    }
    
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
        return response.json()
    else:
        return f"Error: {response.status_code}, {response.text}"

# Meminta input dari pengguna
user_input = input("Masukkan pertanyaan atau pernyataan Anda: ")

# Memanggil fungsi dan mencetak hasilnya
result = generate_content(user_input)
print(json.dumps(result, indent=2))
```

Apakah Anda ingin saya menjelaskan atau menguraikan kode ini?
