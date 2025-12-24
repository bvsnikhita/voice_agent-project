# speech.py - WORKING VERSION WITH GOOGLE TTS
import speech_recognition as sr
import requests
import io
import pygame
import tempfile
import os


class TeluguVoice:
    def __init__(self):
        """Initialize Telugu voice system with Google TTS"""
        self.recognizer = sr.Recognizer()
        self.use_google_tts = True
        print("🔊 తెలుగు వాయిస్ సిస్టమ్ (గూగుల్ TTS) సిద్ధంగా ఉంది")

    def speak(self, text):
        """Speak Telugu text using Google TTS"""
        print(f"\n🤖 అసిస్టెంట్: {text}")

        try:
            # Use Google Translate TTS API
            tts_url = f"https://translate.google.com/translate_tts"

            params = {
                'ie': 'UTF-8',
                'tl': 'te',  # Telugu language
                'client': 'tw-ob',
                'q': text
            }

            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }

            response = requests.get(tts_url, params=params, headers=headers)

            if response.status_code == 200:
                # Save to temp file
                with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as f:
                    temp_path = f.name
                    f.write(response.content)

                # Play with pygame
                pygame.mixer.init()
                pygame.mixer.music.load(temp_path)
                pygame.mixer.music.play()

                # Wait for playback to finish
                while pygame.mixer.music.get_busy():
                    pygame.time.Clock().tick(10)

                # Cleanup
                pygame.mixer.quit()
                os.unlink(temp_path)
            else:
                print("⚠️ TTS failed, showing text only")

        except Exception as e:
            print(f"❌ TTS error: {e}")
            print(f"[Voice would say: {text}]")

    def listen(self):
        """Listen to Telugu speech"""
        try:
            with sr.Microphone() as source:
                print("🎤 వినడం... 5 సెకన్లలో మాట్లాడండి")
                self.recognizer.adjust_for_ambient_noise(source, duration=1)
                audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=10)

            text = self.recognizer.recognize_google(audio, language="te-IN")
            print(f"👤 మీరు చెప్పారు: {text}")
            return text

        except sr.WaitTimeoutError:
            print("⏰ మాట్లాడలేదు. టెక్స్ట్‌లో టైప్ చేయండి:")
            return input("టెక్స్ట్: ")
        except Exception as e:
            print(f"❌ దోషం: {e}")
            return ""


# Install required library first
def check_dependencies():
    """Check and install required packages"""
    try:
        import pygame
        import requests
    except ImportError:
        print("Installing required packages...")
        import subprocess
        subprocess.check_call(["pip", "install", "pygame", "requests"])
        print("Packages installed successfully!")


# Test function
if __name__ == "__main__":
    # Check dependencies
    check_dependencies()

    # Test the voice system
    voice = TeluguVoice()
    voice.speak("నమస్కారం, నేను తెలుగు ప్రభుత్వ పథకాల సహాయకుడిని")

    # Test listening
    print("\nNow testing listening... Speak something in Telugu in 5 seconds:")
    text = voice.listen()
    if text:
        voice.speak(f"మీరు చెప్పారు: {text}")