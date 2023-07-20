import speech_recognition as sr  # Importing the speech_recognition library for speech recognition functionality
import pyttsx3  # Importing the pyttsx3 library for text-to-speech conversion
import shelve  # Importing the shelves library for data storage
import spacy
data_file = "chatbot_data.db"  # Filename of the data file used to store chatbot data


# Function to retrieve chatbot data from the data file
def get_chatbot_data():
    with shelve.open(data_file, flag='c') as shelf:  # Open the data file in read-only mode ('c' flag)
        if "chatbot_data" not in shelf:  # Check if chatbot_data key is present in the data file
            return {"conversation_history": []}  # Return a default dictionary with an empty conversation history
        return shelf["chatbot_data"]  # Return the chatbot data stored in the data file


# Function to save chatbot data to the data file
def save_chatbot_data(data):
    with shelve.open(data_file, flag='w') as shelf:  # Open the data file in write mode ('w' flag)
        shelf["chatbot_data"] = data  # Store the chatbot data in the data file


# Function to listen to user input using the microphone
def listen():
    r = sr.Recognizer()  # Initialize a speech recognizer
    with sr.Microphone() as source:  # Use the microphone as the audio source
        print("Chatbot: Listening...")
        r.energy_threshold = 2000  # Adjust the energy threshold as needed to control sensitivity
        audio = r.listen(source)  # Listen to the audio input from the microphone

    try:
        print("Chatbot: Recognizing...")
        query = r.recognize_google(audio)  # Use Google's speech recognition service to recognize the audio
        print(f"User: {query}")
        return query  # Return the recognized query as user input
    except sr.UnknownValueError:
        print("Chatbot: Sorry, I didn't catch that. Could you please repeat?")
        return listen()  # If speech is not recognized, ask the user to repeat
    except sr.RequestError:
        print("Chatbot: Sorry, I'm currently experiencing some technical issues. Please try again later.")
        return None  # If there are any issues with the speech recognition service, return None


# Function to speak the text using text-to-speech
def speak(text):
    engine = pyttsx3.init()  # Initialize the text-to-speech engine
    engine.say(text)  # Convert the text to speech
    engine.runAndWait()  # Wait for the speech to be completed


# Function to print the user's question and chatbot's response
def print_dialogue(user, chatbot):
    print(f"You: {user}")  # Print the user's question
    print("Chatbot:", chatbot)  # Print the chatbot's response
    print()


# Main chat function
def chat():
    chatbot_data = get_chatbot_data()  # Retrieve the chatbot data from the data file
    conversation_history = chatbot_data.get("conversation_history", [])  # Get the conversation history from the data

    speak("Hi! What's your name?")  # Speak the greeting
    name = listen()  # Listen for the user's name
    speak(f"Nice to meet you, {name}!")  # Speak a welcome message with the user's name

    while True:
        speak("Ask me a question or say 'exit' to exit.")  # Prompt the user to ask a question or exit
        question = listen()  # Listen for the user's question

        if question is None:  # If there was an issue with speech recognition, continue to the next iteration
            continue

        if question.lower() == "exit":  # If the user wants to exit, break the loop
            break

        found_answer = False
        for q, a in chatbot_data.items():  # Iterate over the chatbot data to find a matching question
            if q.lower() == question.lower():  # If the question matches, get the corresponding answer
                answer = a
                speak(answer)  # Speak the answer
                print_dialogue(question, answer)  # Print the dialogue
                found_answer = True
                break

        if not found_answer:
            speak("I'm sorry, I don't know the answer. Can you please provide me with the answer?")  # Ask for answer
            answer = listen()  # Listen for the user's answer
            chatbot_data[question] = answer  # Add the question and answer to the chatbot data
            conversation_history.append((question, answer))  # Add the question and answer to the conversation history
            chatbot_data["conversation_history"] = conversation_history  # Update the conversation history in the data
            save_chatbot_data(chatbot_data)  # Save the updated chatbot data
            speak("Thanks! I'll remember that for next time.")  # Confirm that the answer is remembered
            print_dialogue(question, answer)  # Print the dialogue

    print("Chatbot: Here's our conversation history:")  # Print the conversation history
    for question, answer in conversation_history:
        print(f"{name}: {question}")
        print("Chatbot:", answer)
        print()

    speak("Goodbye!")  # Speak the goodbye message


# Start the chat
chat()

