import requests

# Switching the model
switch_model_url = 'http://127.0.0.1:8020/switch_model'
model_switch_response = requests.post(switch_model_url, json={"model_name": "femaledarkelf"})
print(model_switch_response.json())

# Sending a TTS request
tts_url = 'http://127.0.0.1:8020/tts_to_audio/'
tts_response = requests.post(tts_url, json={
    "text": " Greetings, traveler. What brings you to Whiterun? I hope you're here for noble reasons, as our Jarl takes great care in ensuring his palace is free from harm. I am Irileth, the Jarl's housecarl, and it is my duty to protect him at all costs. I assure you that I am vigilant and uncompromising in my watchfulness. May I inquire as to why you have come to Whiterun?",
    #"speaker_wav": "D:/Modelisation_IA/xtts-api-server-custom/models/MrHaurrus/test.wav",
    "language": "en",
    "save_path": "D:/Modelisation_IA/xtts-api-server/xtts_api_server/speakers/voicelines.wav"
})
