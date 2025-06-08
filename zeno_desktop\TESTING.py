from dotenv import load_dotenv
import os
from elevenlabs.client import ElevenLabs
from elevenlabs import play
import threading
import speech_recognition as sr
import time
from zeno_gesture_tracker.zeno_gesture_tracker import start_gesture_mode, stop_gesture_mode
from zeno_terminalGoogle.googleterminal import search_google_links, open_result_by_number
from zeno_github_uploader.zeno_github_uploader import upload_project, display_all_repos, access_repo_contents, delete_repository
from Quantum_creativity_engine.quantum_creativity_engine import get_creative_idea
import os
import asyncio


load_dotenv()
client = ElevenLabs(api_key=os.getenv("ELEVENSLAB_API_KEY"))


speak_lock = threading.Lock()
recognizer = sr.Recognizer()

def speak(text):
    """Use ElevenLabs TTS to synthesize and play speech."""
    print(f"[Zeno SPEAKING]: {text}")
    with speak_lock:
        try:
            audio = client.text_to_speech.convert(
                text=text,
                voice_id="pwMBn0SsmN1220Aorv15",  
                model_id="eleven_multilingual_v2",
                output_format="mp3_44100_128",
            )
            play(audio)
        except Exception as e:
            print(f"[Error playing ElevenLabs speech]: {e}")

def recognize_speech():
    """Recognize speech in the background."""
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("[Zeno] Listening...")
        audio = recognizer.listen(source)
    try:
        command = recognizer.recognize_google(audio)
        print(f"[You]: {command}")
        return command.lower()
    except sr.UnknownValueError:
        speak("Sorry, I didn't catch that.")
    except sr.RequestError:
        speak("Sorry, I'm having trouble with the recognition service.")
    return ""

def wait_for_wake_word():
    """Listens in a loop for the wake word 'Hey'."""
    while True:
        command = recognize_speech()
        if "hello" or "hey" or "Zeno" in command:
            speak("Hey Zeno here,your sneaky assistant!You are back already!, UMM actually i was in the middle of a sweet dream, anyways ,Say your command!")
            handle_commands()



def handle_commands():
    """Function that handles the voice commands, with speech recognition."""
    while True:
        command = recognize_speech()
        if not command:  # Skip empty commands
            continue

        if "goodbye" in command:
            speak("Goodbye to you, actually going back to my sweet dream that you interrupted.")
            os._exit(0)

        if "gesture tracker" in command:
            if "activate" in command:
                speak("Activating gesture tracker mode.")
                start_gesture_mode()
            elif "stop" in command:
                speak("Turning off gesture tracker.")
                stop_gesture_mode()

        elif  "wild idea" in command:
            speak("Welcome to your creativity engine")
            speak("What is your current mood? Please choose from moods displayed on the screen")
            mood = recognize_speech().strip()

            speak("What tech domain are you curious about? Choose from domains displayed on the screen")
            domain = recognize_speech().strip()

            speak("Do you have any specific thoughts or interests? (Optional)")
            thought = recognize_speech().strip()

            speak("⚛️ Firing quantum seed and entangling creative fields... Please wait.")

            # Use the get_creative_idea function from the creativity engine
            result = asyncio.run(get_creative_idea(user_mood=mood, tech_domain=domain, custom_thought=thought))

            if "idea" in result:
                speak("✨ Quantum Idea Generated ✨")
                speak(f"🌀 Mood: {result['mood']}")
                speak(f"💡 Domain: {result['domain']}")
                speak(f"🌱 Quantum Seed: {result['seed']}\n")
                speak(result["idea"])
            else:
                speak("❌ Error: " + result["error"])
     

        elif "github" in command:
            speak("What would you like to do with GitHub?")
            github_command = recognize_speech()

            if not github_command:  # If no command, continue listening
                continue


            if "create" in github_command or "upload" in github_command:
                speak("What should the repository be called?")
                repo_name = recognize_speech()

                speak("Please say a short description.")
                description = recognize_speech()

                speak("Please enter the folder path on your computer.")
                folder_path = input("Enter folder path: ")

                upload_project(repo_name, description, folder_path)
                speak(f"Project '{repo_name}' upload completed.")

            elif "list" in github_command or "display" in github_command:
                speak("Fetching your repositories.")
                display_all_repos()

            elif "access" in github_command:
                speak("Say the repository name.")
                repo_name = recognize_speech()
                access_repo_contents(repo_name)

            elif "delete" in github_command:
                speak("Which repository would you like to delete?")
                repo_name = recognize_speech()
                delete_repository(repo_name)
                speak(f"Deleted repository '{repo_name}'")

        elif "google" in command:
            speak("What would you like to search for?")
            query = recognize_speech()
            if not query:
                continue

            speak(f"Searching Google for {query}")
            results = search_google_links(query)

            if not results:
                speak("Sorry, I couldn't find any results.")
                continue

            for i, url in enumerate(results, 1):
                speak(f"Result {i}")
                print(f"{i}. {url}")

            speak("Which result number should I open? (say 'first result', 'second result', etc.)")
            selection = recognize_speech()
            
            # Define the mapping for spoken words to result numbers
            result_mapping = {
                'first': 1,
                'second': 2,
                'third': 3,
                'fourth': 4,
                'fifth': 5,
                'sixth': 6,
                'seventh': 7,
                'eighth': 8,
                'ninth': 9,
                'tenth': 10,
            }

            # Check if the selection is one of the mapped results
            if any(word in selection for word in result_mapping):
                # Extract the word (like 'first', 'second', etc.)
                for word, number in result_mapping.items():
                    if word in selection:
                        selected_number = number
                        if open_result_by_number(selected_number):
                            speak(f"Opening {word} result")
                        else:
                            speak("That result number doesn't exist.")
                        break
            else:
                speak("I didn't hear a valid result number.")
            




if __name__=="__main__":
    wait_for_wake_word()


