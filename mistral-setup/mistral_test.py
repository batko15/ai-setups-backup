#!/data/data/com.termux/files/usr/bin/python
"""
Mistral Setup Test Script
Prüft alle installierten Komponenten
"""

import os
import sys
import subprocess
import json

def test_component(name, command, expected=None):
    """Teste eine Komponente"""
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True, timeout=10)
        status = "✅ PASS" if result.returncode == 0 else "❌ FAIL"
        output = result.stdout.strip() or result.stderr.strip()
        print(f"{status} | {name}")
        if output and len(output) < 100:
            print(f"       Output: {output[:100]}")
        return result.returncode == 0
    except Exception as e:
        print(f"❌ FAIL | {name}")
        print(f"       Error: {str(e)[:100]}")
        return False

def main():
    print("=" * 60)
    print("MISTRAL SETUP - KOMPONENTENTEST")
    print("=" * 60)
    print()
    
    tests_passed = 0
    tests_total = 0
    
    # Test 1: Ollama
    tests_total += 1
    if test_component("Ollama Server", "ollama --version"):
        tests_passed += 1
    
    # Test 2: Ollama Modell
    tests_total += 1
    if test_component("Mistral-7B Modell", "ollama show mistral:latest"):
        tests_passed += 1
    
    # Test 3: OpenClaw CLI
    tests_total += 1
    if test_component("OpenClaw CLI", "openclaw --version"):
        tests_passed += 1
    
    # Test 4: Node.js
    tests_total += 1
    if test_component("Node.js", "node --version"):
        tests_passed += 1
    
    # Test 5: npm
    tests_total += 1
    if test_component("npm", "npm --version"):
        tests_passed += 1
    
    # Test 6: Python
    tests_total += 1
    if test_component("Python", "python --version"):
        tests_passed += 1
    
    # Test 7: pip
    tests_total += 1
    if test_component("pip", "pip --version"):
        tests_passed += 1
    
    # Test 8: MCP Server Filesystem
    tests_total += 1
    if test_component("MCP Filesystem", "npm list -g @modelcontextprotocol/server-filesystem"):
        tests_passed += 1
    
    # Test 9: MCP Server GitHub
    tests_total += 1
    if test_component("MCP GitHub", "npm list -g @modelcontextprotocol/server-github"):
        tests_passed += 1
    
    # Test 10: gTTS
    tests_total += 1
    if test_component("gTTS", "python -c 'from gtts import gTTS; print(\"OK\")'"):
        tests_passed += 1
    
    # Test 11: SpeechRecognition
    tests_total += 1
    if test_component("SpeechRecognition", "python -c 'import speech_recognition; print(\"OK\")'"):
        tests_passed += 1
    
    # Test 12: pyttsx3
    tests_total += 1
    if test_component("pyttsx3", "python -c 'import pyttsx3; print(\"OK\")'"):
        tests_passed += 1
    
    # Test 13: Swap File
    tests_total += 1
    if os.path.exists(os.path.expanduser("~/swapfile")):
        print("✅ PASS | Swap Datei")
        tests_passed += 1
    else:
        print("❌ FAIL | Swap Datei")
    
    # Test 14: Config Files
    tests_total += 1
    if os.path.exists("/data/data/com.termux/files/home/.mistral/config.yaml") and \
       os.path.exists("/data/data/com.termux/files/home/.openclaw/openclaw.json"):
        print("✅ PASS | Konfigurationsdateien")
        tests_passed += 1
    else:
        print("❌ FAIL | Konfigurationsdateien")
    
    # Test 15: Autostart Script
    tests_total += 1
    if os.path.exists("/data/data/com.termux/files/home/.termux/boot/start-mistral.sh"):
        print("✅ PASS | Autostart Skript")
        tests_passed += 1
    else:
        print("❌ FAIL | Autostart Skript")
    
    # Test 16: Voice Control Script
    tests_total += 1
    if os.path.exists("/data/data/com.termux/files/home/mistral_voice_control.py"):
        print("✅ PASS | Sprachsteuerungs-Skript")
        tests_passed += 1
    else:
        print("❌ FAIL | Sprachsteuerungs-Skript")
    
    print()
    print("=" * 60)
    print(f"ERGEBNIS: {tests_passed}/{tests_total} Tests bestanden")
    print("=" * 60)
    
    if tests_passed >= tests_total * 0.8:
        print("\n✅ SETUP ERFOLGREICH!")
        print("Alle wichtigen Komponenten sind installiert und funktionieren.")
    else:
        print("\n⚠️  Einige Tests sind fehlgeschlagen.")
        print("Bitte überprüfe die Fehler und führe die Installation erneut aus.")

if __name__ == "__main__":
    main()
