import os
import webbrowser
import instaloader
import wikipedia
import playsound
import cv2
import pywhatkit
import smtplib
from email.message import EmailMessage
from twilio.rest import Client
import openai
from geopy.geocoders import Nominatim
import tweepy
from bs4 import BeautifulSoup
import requests

# Define some constants
NOTEPAD_PATH = "C:\\Windows\\System\\notepad.exe"
CHROME_PATH = "C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe"
AUDIO_PATH = "sample.mp3"
VIDEO_PATH = "sample.mp4"

# Define some functions
def open_notepad():
    os.startfile(NOTEPAD_PATH)

def open_chrome():
    os.startfile(CHROME_PATH)

def send_whatsapp():
    phone = input("Enter the phone number with country code: ")
    message = input("Enter the message: ")
    hour = int(input("Enter the hour (24-hour format): "))
    minute = int(input("Enter the minute: "))
    pywhatkit.sendwhatmsg(phone, message, hour, minute)

def send_email():
    sender = input("Enter your email address: ")
    password = input("Enter your password: ")
    receiver = input("Enter the receiver's email address: ")
    subject = input("Enter the subject: ")
    content = input("Enter the content: ")
    
    msg = EmailMessage()
    msg['From'] = sender
    msg['To'] = receiver
    msg['Subject'] = subject
    msg.set_content(content)

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender, password)
        server.send_message(msg)
        server.quit()
        print("Email sent successfully!")
    except Exception as e:
        print("Email failed to send:", e)

def send_sms():
    account_sid = input("Enter your Twilio account SID: ")
    auth_token = input("Enter your Twilio auth token: ")
    client = Client(account_sid, auth_token)
    sender = input("Enter your Twilio phone number: ")
    receiver = input("Enter the receiver's phone number: ")
    message = input("Enter the message: ")

    try:
        client.messages.create(
            from_=sender,
            to=receiver,
            body=message
        )
        print("SMS sent successfully!")
    except Exception as e:
        print("SMS failed to send:", e)

def chat_with_chatgpt():
    openai.api_key = input("Enter your OpenAI API key: ")
    print("You are now chatting with ChatGPT. Type 'quit' to exit.")
    prompt = "The following is a conversation with ChatGPT, a Python coding mentor. ChatGPT can help you with writing, debugging, and improving your Python code.\n\nHuman: "

    while True:
        query = input("Human: ")
        if query.lower() == 'quit':
            break
        response = openai.Completion.create(
            engine="davinci",
            prompt=prompt + query + "\nChatGPT: ",
            stop=["\nHuman: ", "\nChatGPT: "],
            temperature=0.9,
            top_p=1,
            frequency_penalty=0.5,
            presence_penalty=0.5,
            best_of=1,
            max_tokens=150
        )
        answer = response["choices"][0]["text"]
        print("ChatGPT:", answer)
        prompt += query + "\nChatGPT: " + answer + "\nHuman: "

def get_geolocation():
    geolocator = Nominatim(user_agent="GetLoc")
    address = input("Enter the address: ")
    location = geolocator.geocode(address)
    
    if location:
        print("Address:", location.address)
        print("Latitude:", location.latitude)
        print("Longitude:", location.longitude)
    else:
        print("Address not found")

def get_trending_topics():
    api_key = input("Enter your Twitter API key: ")
    api_secret = input("Enter your Twitter API secret: ")
    access_token = input("Enter your Twitter access token: ")
    access_secret = input("Enter your Twitter access secret: ")

    auth = tweepy.OAuthHandler(api_key, api_secret)
    auth.set_access_token(access_token, access_secret)
    api = tweepy.API(auth)
    
    woeid = int(input("Enter the WOEID of the location: "))
    trends = api.trends_place(woeid)

    print("Top 10 Twitter Trends:")
    for trend in trends[0]["trends"][:10]:
        print(trend["name"])

def get_top_posts():
    loader = instaloader.Instaloader()
    hashtag = input("Enter the hashtag: ")
    posts = loader.get_hashtag_posts(hashtag)
    top_posts = sorted(posts, key=lambda p: p.likes + p.comments, reverse=True)[:10]

    for post in top_posts:
        print(post.url)

def get_page_data():
    url = input("Enter the URL of the Medium or Wikipedia page: ")
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")

        if "medium.com" in url:
            title = soup.find("h1").text
            author = soup.find("a", {"data-action":"show-user-card"}).text
            date = soup.find("time")["datetime"]
            content = soup.find("div", {"class":"section-content"}).text
            print("Title:", title)
            print("Author:", author)
            print("Date:", date)
            print("Content:", content)
        elif "wikipedia.org" in url:
            title = soup.find("h1", {"id":"firstHeading"}).text
            content = soup.find("div", {"id":"bodyContent"}).text
            print("Title:", title)
            print("Content:", content)
        else:
            print("Invalid URL")
    else:
        print("Request failed")

def play_audio():
    playsound.playsound(AUDIO_PATH)

def play_video():
    cap = cv2.VideoCapture(VIDEO_PATH)

    while cap.isOpened():
        ret, frame = cap.read()

        if ret:
            cv2.imshow("Video", frame)

            if cv2.waitKey(25) & 0xFF == ord("q"):
                break
        else:
            break

    cap.release()
    cv2.destroyAllWindows()

def control_speaker():
    engine = pyttsx3.init()
    sessions = AudioUtilities.GetAllSessions()

    for session in sessions:
        volume = session._ctl.QueryInterface(ISimpleAudioVolume)

        if session.Process and session.Process.name() == "python.exe":
            print("Current volume:", volume.GetMasterVolume())
            new_volume = float(input("Enter the new volume (0 to 1): "))
            volume.SetMasterVolume(new_volume, None)
            print("New volume:", volume.GetMasterVolume())
            text = input("Enter the text to speak: ")
            engine.say(text)
            engine.runAndWait()
            break

# Define the menu options
options = {
    "1": ("Open Notepad", open_notepad),
    "2": ("Open Chrome", open_chrome),
    "3": ("Send WhatsApp", send_whatsapp),
    "4": ("Send Email", send_email),
    "5": ("Send SMS", send_sms),
    "6": ("Chat with ChatGPT", chat_with_chatgpt),
    "7": ("Get Geolocation", get_geolocation),
    "8": ("Get Trending Topics on Twitter", get_trending_topics),
    "9": ("Get Top Posts of a Hashtag on Instagram", get_top_posts),
    "10": ("Get Page Data from Medium or Wikipedia", get_page_data),
    "11": ("Play Audio", play_audio),
    "12": ("Play Video", play_video),
    "13": ("Control Speaker", control_speaker),
    "0": ("Exit", exit)
}

# Display the menu and get the user choice
def display_menu():
    print("Menu Driven Program in Python")
    print("Please choose an option:")
    
    for key, value in options.items():
        print(key, "-", value[0])

    choice = input("Enter your choice: ")
    return choice

# Execute the chosen option
def execute_choice(choice):
    if choice in options:
        options[choice][1]()

# Main program loop
while True:
    user_choice = display_menu()

    if user_choice == "0":
        print("Exiting program. Goodbye!")
        break
    else:
        execute_choice(user_choice)
