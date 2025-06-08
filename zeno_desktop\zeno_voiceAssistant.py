import threading
#import pyttsx3
import speech_recognition as sr
import time
from zeno_gesture_tracker.zeno_gesture_tracker import start_gesture_mode, stop_gesture_mode
from zeno_terminalGoogle.googleterminal import search_google_links, open_result_by_number
from zeno_github_uploader.zeno_github_uploader import upload_project, display_all_repos, access_repo_contents, delete_repository
from Quantum_creativity_engine.quantum_creativity_engine import get_creative_idea, MOODS, DOMAINS
import os
import asyncio
import sys
import json
from elevenlabs.client import ElevenLabs
from elevenlabs import play
from dotenv import load_dotenv

# Initialize the speech engine 
#engine = pyttsx3.init(driverName='sapi5')  
#voices = engine.getProperty('voices')  
#engine.setProperty('voice', voices[1].id)  
#engine.setProperty('rate', 180)           
#engine.setProperty('volume', 1.0)

speak_lock = threading.Lock()
recognizer = sr.Recognizer()

load_dotenv()
client = ElevenLabs(api_key=os.getenv("ELEVENSLAB_API_KEY"))

def speak(text):
    """Use ElevenLabs TTS to synthesize and play speech, thread-safe and printing as before."""
    print(f"[Zeno SPEAKING]: {text}", file=sys.stderr)
    with speak_lock:
        try:
            audio = client.text_to_speech.convert(
                text=text,
                voice_id="pwMBn0SsmN1220Aorv15",  # Your chosen voice ID
                model_id="eleven_multilingual_v2",
                output_format="mp3_44100_128",
            )
            play(audio)  # Play is blocking, so the lock prevents overlap
        except Exception as e:
            print(f"[Error playing ElevenLabs speech]: {e}", file=sys.stderr)

def recognize_speech():
    """Recognize speech in the background."""
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("[Zeno] Listening...", file=sys.stderr)
        audio = recognizer.listen(source)
    try:
        command = recognizer.recognize_google(audio)
        print(f"[You]: {command}", file=sys.stderr)
        return command.lower()
    except sr.UnknownValueError:
        speak("Sorry, I didn't catch that.")
    except sr.RequestError:
        speak("Sorry, I'm having trouble with the recognition service.")
    return ""

def wait_for_folder_path():
    for line in sys.stdin:
        try:
            data = json.loads(line)
            if data.get("event") == "user_selected_folder_path":
                return data["data"]["folder_path"]
        except Exception:
            continue


def wait_for_wake_word():
    """Listens in a loop for the wake word 'Hey'."""

    # 🔊 Tell frontend Zeno is listening immediately when mic starts
    print(json.dumps({"event": "mic_started"}) + "\n")
    sys.stdout.flush()

    while True:

        command = recognize_speech()
        if any(phrase in command for phrase in ["hello", "hey", "wake up"]):
            print(json.dumps({"event": "wake_word_detected"}) + "\n")
            sys.stdout.flush()

            time.sleep(3.5)
            
           
            # Now speaks   
            speak(" HEY , Zeno here , your assistant! What would you like me to do...")
            time.sleep(1)
            print(json.dumps({"event": "command_mode_started"}) + "\n")
            sys.stdout.flush()

            handle_commands()
            break

def handle_commands():
    """Function that handles the voice commands, with speech recognition."""
    while True:
        command = recognize_speech()
        if not command:
            continue

        command= command.lower()

        if any(keyword in command for keyword in ["github", "wild idea", "google", " gesture"]):
            print(json.dumps({"event": "command_detected"}) + "\n")
            sys.stdout.flush()

        if "goodbye" in command:
            
            print(json.dumps({"event": "goodbye_detected"}) + "\n")
            sys.stdout.flush()
            speak("Goodbye.Wake me only if the simulation crashes!")
            os._exit(0)

        if "gesture" in command:
            if "activate" in command:
                speak("Activating gesture tracker mode.")
                start_gesture_mode()

            elif "stop" in command:
                speak("Turning off gesture tracker.")
                stop_gesture_mode()

        elif "wild idea" in command:
            speak("Welcome to your creativity engine")
            speak("What is your current mood? Please choose from moods displayed on the screen")
            print(json.dumps({
                "event": "moods_triggered",
                "data": { 
                    "moods": MOODS
                }
            }) + "\n")
            sys.stdout.flush()
            mood = recognize_speech().strip()

            speak("What tech domain are you curious about? Choose from domains displayed on the screen")
            print(json.dumps({
                "event": "domains_triggered",
                "data": { 
                    "domains": DOMAINS
                    
                }
            }) + "\n")
            sys.stdout.flush()
            domain = recognize_speech().strip()

            speak("Do you have any specific thoughts or interests? (Optional)")
            thought = recognize_speech().strip()

            speak("⚛️ Firing quantum seed and entangling creative fields... Please wait.")

            result = asyncio.run(get_creative_idea(user_mood=mood, tech_domain=domain, custom_thought=thought))

            if "idea" in result:
                speak(" Quantum Idea Generated ")
                speak(f" Mood: {result['mood']}")
                speak(f" Domain: {result['domain']}")
                

                print(json.dumps({
                    "event": "wild_idea_result",
                    "data": {
                        "seed": result["seed"],
                        "idea": result["idea"]
                    }
                }) + "\n")
                sys.stdout.flush()
                
                speak(f" Quantum Seed: {result['seed']}\n")
                speak(result["idea"])
            else:
                speak("❌ Error: " + result["error"])

        elif "github" in command:
            speak("What would you like to do with GitHub?")
            github_command = recognize_speech()

            if not github_command:
                continue

            if "create" in github_command or "upload" in github_command:
                speak("What should the repository be called?")
                repo_name = recognize_speech()


                speak("Please say a short description.")
                description = recognize_speech()


                speak("Please enter the folder path on your computer.")
                print(json.dumps({

                    "event": "folder_path",
                    "data": {
                        "prompt": "Please enter the folder path for your project upload."
                    }
                }) + "\n")
                sys.stdout.flush()


                folder_path= wait_for_folder_path()


                speak(f"Uploading your project like a boss")
                upload_project(repo_name, description, folder_path)

                speak(f"Project '{repo_name}' upload's done. Now can i go back to dreaming in binary???")


            elif "list" in github_command or "display" in github_command:
                speak("Fetching your repositories.")

                repos=display_all_repos()

                speak(f"Here are all of your repositories")
                print(json.dumps({

                    "event": "display_all_repos",
                    "data": {
                        "repositories": repos
                    }
                }) + "\n")
                sys.stdout.flush()
                

            elif "access" in github_command:
                speak("Say the repository name.")

                repo_name = recognize_speech()
                contents=access_repo_contents(repo_name)
                
                speak(f"Here are the contents of the {repo_name}")

                print(json.dumps({

                    "event": "access_contents_of_repo",
                    "data": {
                        "repository": repo_name,
                        "contents": contents
                    }
                }) + "\n")
                sys.stdout.flush()

            elif "delete" in github_command:
                speak("Which repository would you like to delete?")
                repo_name = recognize_speech()
                delete_repository(repo_name)
                speak(f"Deleted repository '{repo_name}'")

        elif "google" in command:
            speak("speak your error, bestie?")
            query = recognize_speech()
            if not query:
                continue

            speak(f"Searching for {query}")
            results = search_google_links(query)

            if not results:
                speak("Sorry, I couldn't find any results.")
                continue

            for i, url in enumerate(results, 1):

                speak(f"Result {i}")

                print(json.dumps({

                    "event": "google_search_result",
                    "data": {
                        "number": i,
                        "url": url
                    }
                }) + "\n")
                sys.stdout.flush()

            speak("Looks like i found 3 top searches for your query.Which result number should I open? (say 'first result', 'second result', etc.)")
            selection = recognize_speech()
            
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

            if any(word in selection for word in result_mapping):
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

if __name__ == "__main__":
    wait_for_wake_word() 


