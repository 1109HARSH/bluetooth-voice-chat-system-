# ==========================================
# SERVER.py
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

MAC_ADDRESS = "E4:1F:D5:ED:1E:16"
PORT = 9

SERVER_IP = "0.0.0.0"
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
# BLUETOOTH SERVER
# ==========================================

Server_Handler = socket.socket(socket.AF_BLUETOOTH,socket.SOCK_STREAM,socket.BTPROTO_RFCOMM)
Server_Handler.bind((MAC_ADDRESS, PORT))
Server_Handler.listen(1)
print("Waiting for connection...")

Client_Conn, Client_Addr = Server_Handler.accept()
print(f"Connected To: {Client_Addr}")

# ==========================================
# KEY EXCHANGE
# ==========================================

Client_Conn.send(public_key.save_pkcs1())
Client_Public = rsa.PublicKey.load_pkcs1(Client_Conn.recv(1024))

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
# SEARCH CHAT HISTORY
# ==========================================

def search_chat(keyword=None, date=None):

    try:

        with open("messages.txt", "r", encoding="utf-8") as f:

            lines = f.readlines()

        print("\nSEARCH RESULTS:\n")

        found = False

        for line in lines:

            if keyword and keyword.lower() not in line.lower():
                continue

            if date and date not in line:
                continue

            print("✔", line.strip())

            found = True

        if not found:
            print("No messages found")

    except FileNotFoundError:

        print("No chat history found")

# ==========================================
# RECEIVE TEXT
# ==========================================

def receive_text():

    global text_mode

    while text_mode:

        try:

            data = Client_Conn.recv(4096)

            if not data:
                break

            msg = rsa.decrypt(data,private_key).decode()
            time = datetime.now().strftime("%I:%M %p")

            chat = f"""
━━━━━━━━━━━━━━━━━━━━━━
Client
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

        # RETURN TO MENU
        if msg == "4":

            text_mode = False

            print("\nReturning To Main Menu...\n")

            break

        encrypted = rsa.encrypt(msg.encode(),Client_Public)
        Client_Conn.send(encrypted)
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

    receiver = AudioReceiver(SERVER_IP,VOICE_PORT)
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

        # EXIT
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

        # RECORD WHILE SPACE HELD
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
 SERVER SYSTEM
========================
1. TEXT CHAT
2. VOICE MESSAGE
3. SEARCH HISTORY
4. EXIT
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

        ip = input("Enter Client IP: ")

        voice_receiver_thread = threading.Thread(target=start_voice_receiver,daemon=True)
        voice_receiver_thread.start()
        push_to_record(ip)

    # ======================================
    # SEARCH HISTORY
    # ======================================

    elif mode == "3":

        choice = input("""
1. Keyword
2. Date
3. Both

Choice: """)

        if choice == "1":

            search_chat(keyword=input("Keyword: "))

        elif choice == "2":

            search_chat(date=input("Date: "))

        elif choice == "3":

            search_chat(keyword=input("Keyword: "),
                        date=input("Date: "))

    # ======================================
    # EXIT
    # ======================================

    elif mode == "4":

        print("Closing Server...")

        try:
            Client_Conn.close()
            Server_Handler.close()

        except:
            pass

        break

    else:

        print("Invalid Choice")