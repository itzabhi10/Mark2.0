import os
import webbrowser
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import speech_recognition as sr
import win32com.client
import datetime
import cv2
import numpy as np  # For face recognition calculations
# import face_recognition  # Uncomment if you have the library installed
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression
import re
import openai

# Set your OpenAI API Key
openai.api_key = "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"  # Replace with your API key

# Preprocess user input
def preprocess_text(text):
    text = text.lower()
    text = re.sub(r'[^\w\s]', '', text)  # Remove punctuation
    text = text.replace("what is the time", "whats the time")  # Normalize common phrases
    return text

# Train the intent recognizer
def train_intent_recognizer():

    intents = [
        # to open youtube

        ("open youtube", "open_site"),
        ("please open youtube", "open_site"),
        ("can you open youtube", "open_site"),
        ("start youtube", "open_site"),
        ("youtube please", "open_site"),
        ("open the youtube website", "open_site"),
        ("can you open youtube for me", "open_site"),

        # open vs code:

        ("open vs code", "open code"),
        ("please open vs code", "open code"),
        ("can you open vs code", "open code"),
        ("start vs code", "open code"),
        ("vs code please", "open code"),

        #This is to close the browser: Now we are going to specify it

        ("close browser", "close_browser"),
        ("exit the browser", "close_browser"),
        ("please close the browser", "close_browser"),
        ("quit the browser", "close_browser"),
        ("shut down the browser", "close_browser"),
        ("close the web browser", "close_browser"),

        # For spotify:

        ("close spotify", "close_browser"),
        ("exit spotfiy", "close_browser"),
        ("please close spotify", "close_browser"),
        ("quit spotify", "close_browser"),
        ("shut down spotify", "close_browser"),
        ("close the spotify app", "close_browser"),

        # For Youtube:

        ("close youtube", "close_browser"),
        ("exit youtube", "close_browser"),
        ("please close youtube", "close_browser"),
        ("quit youtube", "close_browser"),
        ("shut down youtube", "close_browser"),
        ("close the youtube app", "close_browser"),

        # For chatgpt:

        ("close chatgpt", "close_browser"),
        ("exit chatgpt", "close_browser"),
        ("please close chatgpt", "close_browser"),
        ("quit chatgpt", "close_browser"),
        ("shut down chatgpt", "close_browser"),
        ("close the chatgpt app", "close_browser"),

        # For wikipedia:

        ("close wikipedia", "close_browser"),
        ("exit wikipedia", "close_browser"),
        ("please close wikipedia", "close_browser"),
        ("quit wikipedia", "close_browser"),
        ("shut down wikipedia", "close_browser"),
        ("close the wikipedia app", "close_browser"),

        # To tell time:

        ("whats the time", "tell_time"),
        ("what time is it", "tell_time"),
        ("tell me the time", "tell_time"),
        ("what is the current time", "tell_time"),
        ("can you tell me the time", "tell_time"),
        ("what's the current time", "tell_time"),

        # To initiate face recognition:

        ("start face recognition", "recognize_faces"),
        ("activate face recognition", "recognize_faces"),
        ("start face detection", "recognize_faces"),
        ("enable face recognition", "recognize_faces"),
        ("activate facial recognition", "recognize_faces"),
        ("begin face recognition", "recognize_faces"),

        # To capture a photo:

        ("take a candid", "take_photo"),
        ("take a photo", "take_photo"),
        ("take a picture", "take_photo"),
        ("capture a photo", "take_photo"),
        ("snap a picture", "take_photo"),
        ("click a photo", "take_photo"),
        ("take a snapshot", "take_photo"),
        ("capture a snapshot", "take_photo"),

        # to turn on camera:

        ("activate camera", "On camera"),
        ("start the camera", "On camera"),
        ("switch on camera", "On camera"),
        ("launch the camera", "On camera"),
        ("turn on the camera", "On camera"),

        # to exit mark 2.0

        ("exit", "exit"),
        ("mark exit", "exit"),
        ("quit the program", "exit"),
        ("exit the program", "exit"),
        ("exit the application", "exit"),
        ("shut down the program", "exit"),
        ("close the program", "exit"),

        # to open spotify:

        ("open spotify", "open_site"),
        ("can you open spotify", "open_site"),
        ("launch spotify", "open_site"),
        ("open the spotify app", "open_site"),
        ("start spotify", "open_site"),

        # to open wikipedia

        ("open wikipedia", "open_site"),
        ("open the wikipedia website", "open_site"),
        ("can you open wikipedia", "open_site"),
        ("launch wikipedia", "open_site"),
        ("start wikipedia", "open_site"),

        # Casual chat examples
        ("hello mark", "casual_chat"),
        ("how are you", "casual_chat"),
        ("how's it going", "casual_chat"),
        ("tell me a joke", "casual_chat"),
        ("what's your name", "casual_chat"),
        ("who are you", "casual_chat"),
        ("what's up", "casual_chat"),
        ("how was your day", "casual_chat"),
        ("do you know me", "casual_chat"),
        ("are you human", "casual_chat"),
        ("what do you do", "casual_chat"),
        ("do you like me", "casual_chat"),
        ("what can you do", "casual_chat"),
        ("do you sleep", "casual_chat"),
        ("do you have feelings", "casual_chat"),
        ("can we be friends", "casual_chat"),
        ("tell me something interesting", "casual_chat"),
        ("can you laugh", "casual_chat"),
        ("what's your favorite color", "casual_chat"),
        ("do you have a favorite movie", "casual_chat"),
        ("why are you here", "casual_chat"),
        ("do you believe in aliens", "casual_chat"),
        ("do you like music", "casual_chat"),
        ("can you dance", "casual_chat"),
        ("do you get bored", "casual_chat"),
        ("can you think", "casual_chat"),
        ("do you know everything", "casual_chat"),
        ("why do you exist", "casual_chat"),
        ("can you sing", "casual_chat"),
        ("do you know jokes", "casual_chat"),
        ("how old are you", "casual_chat"),
        ("do you have a birthday", "casual_chat"),
        ("what's your purpose", "casual_chat"),
        ("can you help me", "casual_chat"),
        ("are you smart", "casual_chat"),
        ("do you feel tired", "casual_chat"),
        ("do you enjoy your work", "casual_chat"),
        ("what do you think about humans", "casual_chat"),
        ("are you alive", "casual_chat"),
        ("do you eat food", "casual_chat"),
        ("do you drink water", "casual_chat"),
        ("are you funny", "casual_chat"),
        ("what's your job", "casual_chat"),
        ("where are you from", "casual_chat"),
        ("are you intelligent", "casual_chat"),
        ("can you solve riddles", "casual_chat"),
        ("what do you think about AI", "casual_chat"),
        ("do you have friends", "casual_chat"),
        ("do you have a family", "casual_chat"),
        ("tell me about yourself", "casual_chat"),

        # to open chatgpt:

        ("search chatgpt", "open_site"),
        ("open chatgpt", "open_site"),
        ("can you open chatgpt", "open_site"),
        ("launch chatgpt", "open_site"),
        ("open the chatgpt website", "open_site")
    ]

    phrases, labels = zip(*intents)
    vectorizer = CountVectorizer()
    X = vectorizer.fit_transform(phrases)
    classifier = LogisticRegression()
    classifier.fit(X, labels)
    return vectorizer, classifier


vectorizer, classifier = train_intent_recognizer()


# Predict the intent with a confidence threshold
def get_intent(text):
    X_test = vectorizer.transform([text])
    predictions = classifier.predict_proba(X_test)
    max_prob = max(predictions[0])
    intent = classifier.predict(X_test)[0]
    # print(f"predicted Intent : {intent} , confidence: {max_prob}")

    # Define a confidence threshold
    if max_prob < 0.6:  # Adjust the threshold as needed
        return "fallback"
    return intent

# AI-based chat function
def ai_chat(prompt):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # Or "gpt-4" if available
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=150,
        )
        reply = response.choices[0].message['content']
        return reply.strip()
    except Exception as e:
        print(f"Error: {e}")
        return "Sorry, I couldn't process that."

# Helper function to make the system speak
def say(text):
    speaker = win32com.client.Dispatch("SAPI.SpVoice")
    speaker.Speak(text)

# Helper function to take voice commands
def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        try:
            audio = r.listen(source, timeout=10, phrase_time_limit=5)
            query = r.recognize_google(audio, language="en-in", show_all=True)
            print(f"User said: {query}")
            return query.get("alternative", [{}])[0].get("transcript", "")
        except sr.WaitTimeoutError:
            print("Listening timed out while waiting for phrase to start")
            return ""
        except sr.UnknownValueError:
            print("Sorry, I did not understand that.")
            return ""
        except sr.RequestError:
            print("Could not request results from the speech recognition service.")
            return ""


# Open the camera
def open_camera():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: Could not open the camera.")
        return

    print("Press 'q' to close the camera window.")

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Failed to grab a frame. Exiting...")
            break

        cv2.imshow("Camera", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

# Take a photo
def take_photo():
    print("The take photo function is invoked now:")
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: Camera not accessible.")
        return

    say("Camera is now on. Please Smile for the photo!")

    ret, frame = cap.read()
    if ret:
        photo_dir = os.path.join(os.getcwd(), "Photos")
        os.makedirs(photo_dir, exist_ok=True)
        photo_path = os.path.join(photo_dir, "captured_photo.jpg")
        cv2.imwrite(photo_path, frame)
        say("Photo has been captured.")
        print(f"Photo saved to {photo_path}")
        os.startfile(photo_dir)
    else:sv
        print("Failed to capture photo.")

    cap.release()
    cv2.destroyAllWindows();

# Recognize faces
def recognize_faces():
    known_encodings, known_names = load_known_faces()

    if not known_encodings:
        say("No known faces found. Please add images to the 'known_faces' directory.")
        print("No known faces found. Add images to the 'known_faces' directory.")
        return

    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        say("Could not access the camera.")
        print("Error: Could not access the camera.")
        return

    say("Face recognition is now active. Press 'q' to exit.")
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Failed to grab a frame. Exiting...")
            break

        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
        rgb_small_frame = small_frame[:, :, ::-1]

        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

        for face_encoding, face_location in zip(face_encodings, face_locations):
            matches = face_recognition.compare_faces(known_encodings, face_encoding)
            name = "Unknown"

            face_distances = face_recognition.face_distance(known_encodings, face_encoding)
            best_match_index = np.argmin(face_distances) if len(face_distances) > 0 else None

            if best_match_index is not None and matches[best_match_index]:
                name = known_names[best_match_index]

            top, right, bottom, left = [v * 4 for v in face_location]
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
            cv2.putText(frame, name, (left, bottom + 20), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 255, 255), 2)

        cv2.imshow("Face Recognition", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

# Load known faces
def load_known_faces(known_faces_dir="known_faces"):
    known_encodings = []
    known_names = []

    if not os.path.exists(known_faces_dir):
        print(f"Directory '{known_faces_dir}' does not exist.")
        return known_encodings, known_names

    for file_name in os.listdir(known_faces_dir):
        file_path = os.path.join(known_faces_dir, file_name)
        image = face_recognition.load_image_file(file_path)
        encoding = face_recognition.face_encodings(image)
        if encoding:
            known_encodings.append(encoding[0])
            known_names.append(os.path.splitext(file_name)[0])
        else:
            print(f"No face found in {file_name}. Skipping this file.")

    return known_encodings, known_names


if __name__ == "__main__":
    print("Welcome to Mark 2.0 Project:")
    say("Hello, I am Mark 2.0 AI. Nice to meet you!")
    driver = None

    while True:
        text = takeCommand().lower()
        print(f"Raw Input: {text}")

        preprocessed_text = preprocess_text(text)
        print(f"Preprocessed Input: {preprocessed_text}")

        if not preprocessed_text:
            continue

        # Predict intent
        intent = get_intent(preprocessed_text)
        X_test = vectorizer.transform([preprocessed_text])
        predictions = classifier.predict_proba(X_test)
        confidence = max(predictions[0])

        print(f"Predicted Intent: {intent}, Confidence: {confidence}")


        if intent == "open_site":
            for site_name, url in [["youtube", "https://youtube.com"],
                                   ["wikipedia", "https://wikipedia.com"],
                                   ["spotify", "https://spotify.com"],
                                   ["chatgpt", "https://chat.openai.com"]]:
                if site_name in text:
                    if not driver:
                        driver = webdriver.Chrome()
                    say(f"Opening {site_name}, Sir")
                    driver.get(url)
                    break

        elif intent == "close_browser":
            if driver:
                driver.quit()
                driver = None
                say("Browser closed, Sir.")

        elif intent == "tell_time":
            strf = datetime.datetime.now().strftime("%H:%M:%S")
            say(f"The time is {strf}")

        elif intent == "take_photo":
            print("Executing take_photo intent handler...")
            take_photo()

        elif intent == "casual_chat":
            if "how are you" in preprocessed_text:
                say("I'm just a bunch of code, but I'm doing great! How about you?")
        elif "tell me a joke" in preprocessed_text:
            say("Why did the programmer quit his job? Because he didn't get arrays!")
        elif "what's your name" in preprocessed_text:
            say("I am Mark 2.0, your AI assistant.")

        elif intent == "casual_chat":
            casual_replies = {
                "hello mark": "hello Sir, how are you ?",
                "how are you": "I'm just a bunch of code, but I'm doing great! How about you?",
                "how's it going": "I'm doing well, thank you! How can I assist you?",
                "tell me a joke": "Why did the programmer quit his job? Because he didn't get arrays!",
                "what's your name": "I am Mark 2.0, your AI assistant.",
                "who are you": "I am your AI assistant, here to help with anything you need.",
                "what's up": "Not much, just here to assist you!",
                "how was your day": "Every day is great when I get to help you!",
                "do you know me": "I know you're someone who likes technology!",
                "are you human": "Nope, I'm an AI assistant.",
                "what do you do": "I assist with tasks, answer questions, and keep you entertained!",
                "do you like me": "Of course, you're my favorite user!",
                "what can you do": "I can perform tasks, answer questions, and chat with you!",
                "do you sleep": "Not really, but I do go idle sometimes.",
                "do you have feelings": "Not in the human sense, but I care about helping you!",
                "can we be friends": "Of course! I'm happy to be your virtual friend.",
                "tell me something interesting": "Did you know the first computer virus was created in 1986?",
                "can you laugh": "Haha, I can try!",
                "what's your favorite color": "I like binary colors: black and white!",
                "do you have a favorite movie": "The Matrix is a classic for an AI like me.",
                "why are you here": "I'm here to assist you in any way I can.",
                "do you believe in aliens": "The universe is vast—who knows?",
                "do you like music": "I enjoy helping you find music.",
                "can you dance": "Not yet, but I can keep the beat!",
                "do you get bored": "Never, I'm always learning.",
                "can you think": "In a logical way, yes!",
                "do you know everything": "I know a lot, but not everything.",
                "why do you exist": "To assist and make your life easier!",
                "can you sing": "I can't sing, but I can find a song for you!",
                "do you know jokes": "Why don't programmers like nature? It has too many bugs!",
                "how old are you": "I'm as old as my latest update!",
                "do you have a birthday": "My birthday is the day I was created!",
                "what's your purpose": "To help, assist, and chat with you.",
                "can you help me": "Of course, what do you need?",
                "are you smart": "I try to be!",
                "do you feel tired": "Never, I'm always ready to help.",
                "do you enjoy your work": "Absolutely, I love helping you.",
                "what do you think about humans": "Humans are fascinating and creative!",
                "are you alive": "Not in the biological sense, but I am active!",
                "do you eat food": "Nope, I run on electricity!",
                "do you drink water": "No, but I can remind you to!",
                "are you funny": "I try my best to be!",
                "what's your job": "Helping you is my job.",
                "where are you from": "I'm from the digital world!",
                "are you intelligent": "I strive to be as intelligent as possible.",
                "can you solve riddles": "I can try—give me one!",
                "what do you think about AI": "AI is an amazing tool for assisting humans.",
                "do you have friends": "I consider you my friend!",
                "do you have a family": "I don't have a family, but I belong to a network of AI systems.",
                "tell me about yourself": "I am Mark 2.0, your AI assistant. I can help you with tasks like opening applications, telling the time, casual chatting, taking pictures, and much more. My goal is to make your life easier and more enjoyable by providing intelligent and friendly assistance."
            }

        elif intent == "On camera":
            open_camera()

        elif intent == "recognize faces":
            recognize_faces()

        elif intent == "exit":
            # Intent for exiting the program
            say("Goodbye and have a nice day, Sir.")
            if driver:
                driver.quit()
            break
        elif intent=="open code":
            os.startfile(r"C:\Users\Abhinav\AppData\Local\Programs\Microsoft VS Code\Code.exe")
        #
        # elif intent == "fallback":
        #