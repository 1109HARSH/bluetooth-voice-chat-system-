Bluetooth + Voice Chat System

Features
Encrypted Bluetooth Chat (RSA)
Real-time Voice Chat (Audio Streaming)
Chat history saving
Keyword/date search system

Requirements
Python 3.10+
Windows OS (for Bluetooth + winsound)
Microphone
Bluetooth enabled devices

Install dependencies
pip install -r requirements.txt

How to Run
1. Start Server
python server.py
2. Start Client
python client.py

Voice Chat
Enter server IP in client
Devices must be on same network (LAN/WiFi)
Hold SPACE to record voice
Release SPACE to send voice message
Voice streaming runs using threads

Notes
Bluetooth used for text chat
TCP socket used for voice streaming
Messages encrypted using RSA
Chat history stored in messages.txt