# Bluetooth Chat and Voice Messaging System

This is a project I developed for my Computer Security and Networking coursework. It is a Bluetooth-based communication system that supports encrypted text messaging, voice messaging, and chat history management.

## What's the Project About?

The project allows two devices connected through Bluetooth RFCOMM to communicate securely. Text messages are protected using RSA encryption, while voice messages can be recorded and sent using a push-to-record mechanism.

The system also includes a chat history feature that allows users to search previous conversations by keyword or date.

## Features

* RSA encrypted text messaging
* Bluetooth RFCOMM communication
* Voice message support
* Push-to-record functionality
* Chat history storage
* Search messages by keyword
* Search messages by date
* Message notifications
* Client-Server architecture

## Files

* `SERVER.py` – Server-side application
* `CLIENT.py` – Client-side application
* `messages.txt` – Stores chat history
* `requirements.txt` – Required Python libraries

## Technologies Used

* Python
* Bluetooth RFCOMM Sockets
* RSA Encryption
* Threading
* VidStream Audio Library
* Winsound
* Keyboard Module

## How to Run

### Install Dependencies

```bash
pip install -r requirements.txt 
```

### Start the Server

```bash
python SERVER.py
```

### Start the Client

```bash
python CLIENT.py
```

Connect both devices using Bluetooth and follow the on-screen menu.

## Main Menu Options

### 1. Text Chat

Allows users to exchange RSA-encrypted text messages over Bluetooth.

### 2. Voice Message

Allows users to record and send voice messages using push-to-record functionality.

### 3. Search History

Search previously stored conversations using:

* Keywords
* Dates
* Both keyword and date

### 4. Exit

Closes the connection and terminates the application.

## Security Features

The system uses RSA public-key cryptography to encrypt text messages before transmission. This helps protect messages from unauthorized access during communication.

## Learning Outcomes

This project demonstrates:

* Bluetooth socket programming
* Client-server communication
* RSA encryption and key exchange
* Multi-threading in Python
* Voice streaming concepts
* Secure messaging principles
* Chat history management

## Conclusion

This project combines networking, cryptography, and multimedia communication into a single application. It provides a practical demonstration of secure Bluetooth-based messaging and voice communication using Python.
