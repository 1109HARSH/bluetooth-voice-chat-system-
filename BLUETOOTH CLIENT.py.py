# ==========================================
# CLIENT.py
# ==========================================

import socket
import threading
import rsa
import winsound
import keyboard
from datetime import datetime
from vidstream import AudioSender, AudioReceiver

# ==========================================
# SETTINGS
# ==========================================

SERVER_MAC = "E4:1F:D5:ED:1E:16"
PORT = 8

CLIENT_IP = "0.0.0.0"
VOICE_PORT = 9999

# ==========================================
# DATE
# ==========================================

today = datetime.now().strftime("%d %B %Y")

print("\n=================================")
print(f"        {today}")
print("=================================\n")

# ==========================================
# RSA KEYS
# ==========================================

public_key, private_key = rsa.newkeys(1024)

# ==========================================
# BLUETOOTH CLIENT
# ==========================================

client = socket.socket(socket.AF_BLUETOOTH,socket.SOCK_STREAM,socket.BTPROTO_RFCOMM)
print("Connecting To Server...")

client.connect((SERVER_MAC, PORT))
print("Connected Successfully")

# ==========================================
# KEY EXCHANGE
# ==========================================

server_public = rsa.PublicKey.load_pkcs1(client.recv(1024))
client.send(public_key.save_pkcs1())

# ==========================================
# FLAGS
# ==========================================

text_mode = False
voice_mode = False

# ==========================================
# NOTIFICATION SOUND 
# ==========================================

def notify():

    winsound.Beep(1000, 150)

# ==========================================
# SAVE CHAT HISTORY
# ==========================================

def save(msg):

    with open("messages.txt", "a", encoding="utf-8") as f:

        f.write(msg + "\n")

# ==========================================
# RECEIVE TEXT
# ==========================================

def receive_text():

    global text_mode

    while text_mode:

        try:

            data = client.recv(4096)

            if not data:
                break

            msg = rsa.decrypt(data,private_key).decode()
            time = datetime.now().strftime("%I:%M %p")

            chat = f"""
━━━━━━━━━━━━━━━━━━━━━━
Server
{msg}
{time}   👁 Seen
━━━━━━━━━━━━━━━━━━━━━━
"""

            print(chat)

            save(chat)

            notify()

        except:
            break

# ==========================================
# SEND TEXT
# ==========================================

def send_text():

    global text_mode

    text_mode = True

    while text_mode:

        msg = input("YOU: ")

        if msg == "4":

            text_mode = False

            print("\nReturning To Main Menu...\n")

            break

        encrypted = rsa.encrypt(msg.encode(),server_public)
        client.send(encrypted)
        time = datetime.now().strftime("%I:%M %p")

        chat = f"""
━━━━━━━━━━━━━━━━━━━━━━
You
{msg}
{time}   ✓ Sent
━━━━━━━━━━━━━━━━━━━━━━
"""

        print(chat)
        save(chat)

# ==========================================
# VOICE RECEIVER
# ==========================================

def start_voice_receiver():

    receiver = AudioReceiver(CLIENT_IP,VOICE_PORT)
    print("Voice Receiver Started")
    receiver.start_server()

# ==========================================
# PUSH TO RECORD
# ==========================================

def push_to_record(ip):

    global voice_mode

    voice_mode = True

    print("\n HOLD SPACE TO RECORD")
    print("Release SPACE = Send")
    print("Press ESC = Return Menu\n")

    while voice_mode:

        if keyboard.is_pressed("esc"):

            voice_mode = False

            print("\nReturning To Main Menu...\n")

            break

        keyboard.wait("space")

        if not voice_mode:
            break

        print("Recording...")

        sender = AudioSender(ip, VOICE_PORT)

        stream_thread = threading.Thread(target=sender.start_stream,daemon=True)
        stream_thread.start()

        while keyboard.is_pressed("space"):
            pass

        try:

            sender.stop_stream()

        except:
            pass

        print("Voice Message Sent")

# ==========================================
# MAIN MENU
# ==========================================

while True:

    mode = input("""
========================
 CLIENT SYSTEM
========================
1. TEXT CHAT
2. VOICE MESSAGE
3. EXIT
========================

Enter Choice: """)

    # ======================================
    # TEXT CHAT
    # ======================================

    if mode == "1":

        print("\nTEXT CHAT STARTED\n")

        text_mode = True

        receive_thread = threading.Thread(target=receive_text,daemon=True)
        receive_thread.start()
        send_text()

    # ======================================
    # VOICE MESSAGE
    # ======================================

    elif mode == "2":

        ip = input("Enter Server IP: ")

        voice_receiver_thread = threading.Thread(target=start_voice_receiver,daemon=True)
        voice_receiver_thread.start()
        push_to_record(ip)

    # ======================================
    # EXIT
    # ======================================

    elif mode == "3":

        print("Closing Client...")

        try:
            client.close()

        except:
            pass

        break

    else:

        print("Invalid Choice")