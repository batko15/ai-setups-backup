#!/data/data/com.termux/files/usr/bin/python
"""
Mistral Voice Control System
- Weckwort: "Mistral"
- STT: Google Speech Recognition (online)
- TTS: gTTS (online) oder pyttsx3 (offline)
"""

import os
import sys
import time
import speech_recognition as sr
import pyttsx3
from gtts import gTTS
import pyaudio
import tempfile

# Konfiguration
WAKE_WORD = "Mistral"
LANGUAGE = "de-DE"
STT_ENGINE = "google"
TTS_ENGINE = "gTTS"  # oder "pyttsx3"

# Mikrofon-Einstellungen
recognizer = sr.Recognizer()
microphone = sr.Microphone()

# TTS Engine initialisieren (für Offline-Nutzung)
tts_engine = None
if TTS_ENGINE == "pyttsx3":
    tts_engine = pyttsx3.init()
    tts_engine.setProperty('rate', 150)
    # Versuche deutsche Stimme
    voices = tts_engine.getProperty('voices')
    for voice in voices:
        if 'de' in voice.id.lower() or 'german' in voice.id.lower():
            tts_engine.setProperty('voice', voice.id)
            break

def speak(text, language=LANGUAGE):
    """Text zu Sprache"""
    print(f"Mistral: {text}")
    
    if TTS_ENGINE == "gTTS":
        try:
            tts = gTTS(text=text, lang=language[:2], slow=False)
            with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as fp:
                tts.save(fp.name)
                # Versuche mit afplay (Termux hat normalerweise kein afplay)
                # Versuche mit mpv oder ffplay
                os.system(f"termux-media-player play {fp.name} >/dev/null 2>&1 &")
                time.sleep(1)
                os.unlink(fp.name)
        except Exception as e:
            print(f"gTTS Fehler: {e}")
            # Fallback zu pyttsx3
            if tts_engine:
                tts_engine.say(text)
                tts_engine.runAndWait()
    elif TTS_ENGINE == "pyttsx3" and tts_engine:
        tts_engine.say(text)
        tts_engine.runAndWait()
    else:
        # Fallback: Termux-Toast
        os.system(f'termux-toast "Mistral: {text}"')

def listen_for_wake_word(timeout=5):
    """Hore auf Weckwort"""
    print(f"Warte auf Weckwort: '{WAKE_WORD}'...")
    
    try:
        with microphone as source:
            recognizer.adjust_for_ambient_noise(source, duration=1)
            audio = recognizer.listen(source, timeout=timeout, phrase_time_limit=3)
        
        try:
            text = recognizer.recognize_google(audio, language=LANGUAGE)
            print(f"Erkannt: {text}")
            
            if WAKE_WORD.lower() in text.lower():
                speak(f"Ja, ich höre. Wie kann ich helfen?")
                return True
                
        except sr.UnknownValueError:
            print("Nicht verstanden")
        except sr.RequestError as e:
            print(f"Spracherkennungs-Fehler: {e}")
            
    except Exception as e:
        print(f"Fehler: {e}")
    
    return False

def listen_for_command():
    """Hore auf Sprachbefehl"""
    print("Warte auf Befehl...")
    
    try:
        with microphone as source:
            audio = recognizer.listen(source, timeout=10, phrase_time_limit=8)
        
        try:
            text = recognizer.recognize_google(audio, language=LANGUAGE)
            print(f"Befehl erkannt: {text}")
            return text.lower()
        except sr.UnknownValueError:
            speak("Entschuldigung, ich habe das nicht verstanden.")
            return None
        except sr.RequestError as e:
            speak(f"Es gab ein Problem mit der Spracherkennung.")
            return None
    except Exception as e:
        print(f"Fehler: {e}")
        speak("Es gab einen Fehler beim Zuhören.")
        return None

def process_command(command):
    """Verarbeite Sprachbefehl"""
    if not command:
        return True
    
    command = command.lower()
    
    if any(greeting in command for greeting in ["hallo", "hi", "hey", "servus", "moin"]):
        speak(f"Hallo! Ich bin Mistral, dein persönlicher Assistent. Wie kann ich helfen?")
    
    elif any(farewell in command for farewell in ["tschüss", "bye", "auf wiedersehen", "bis dann", "ciao"]):
        speak("Auf Wiedersehen! Wenn du mich brauchst, sage einfach Mistral.")
        return False
    
    elif any(thanks in command for thanks in ["danke", "vielen dank", "thank you", "thanks"]):
        speak("Gern geschehen!")
    
    elif "wetter" in command:
        speak("Leider habe ich noch keine Wetterfunktion. Ich kann aber viele andere Dinge tun.")
    
    elif any(time_cmd in command for time_cmd in ["zeit", "uhrzeit", "wie spät", "wie spät"]):
        from datetime import datetime
        now = datetime.now().strftime("%H:%M:%S")
        speak(f"Die aktuelle Uhrzeit ist {now}.")
    
    elif any(date_cmd in command for date_cmd in ["datum", "tag", "heute"]):
        from datetime import datetime
        today = datetime.now().strftime("%A, den %d. %B %Y")
        speak(f"Heute ist {today}.")
    
    elif any(end_cmd in command for end_cmd in ["beende", "stop", "schluss", "aus", "ende"]):
        speak("Ich beende jetzt.")
        return False
    
    elif "name" in command or "wie heißt" in command:
        speak("Ich bin Mistral, dein KI-Assistent.")
    
    elif "hilfe" in command or "was kann" in command:
        speak("Ich kann auf deine Stimme reagieren. Sage zum Beispiel: Wie spät ist es? Welches Datum ist heute? Oder einfach Hallo!")
    
    else:
        speak(f"Ich verstehe '{command}' noch nicht. Versuche etwas Einfaches wie 'Hallo' oder 'Wie spät ist es?'")
    
    return True

def main():
    """Hauptschleife"""
    print(f"Mistral Voice Control - Weckwort: '{WAKE_WORD}'")
    print("Drücke Ctrl+C zum Beenden")
    
    speak(f"Hallo! Ich bin Mistral, dein persönlicher Assistent. Sage '{WAKE_WORD}' um mich aufzuwecken.")
    
    try:
        while True:
            # Warte auf Weckwort
            if not listen_for_wake_word():
                continue
            
            # Konversationsmodus
            while True:
                command = listen_for_command()
                if command is None:
                    continue
                
                if not process_command(command):
                    break
                    
    except KeyboardInterrupt:
        speak("Auf Wiedersehen!")
        print("\nSprachsteuerung beendet.")

if __name__ == "__main__":
    main()
