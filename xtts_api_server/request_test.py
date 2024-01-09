import requests

# Switching the model
switch_model_url = 'http://127.0.0.1:8020/switch_model'
model_switch_response = requests.post(switch_model_url, json={"model_name": "FemaleDarkElfEng"})
print(model_switch_response.json())

# Sending a TTS request
tts_url = 'http://127.0.0.1:8020/tts_to_audio/'
tts_response = requests.post(tts_url, json={
    "text": "Greetings, traveler. You stand in the presence of Jarl Balgruuf the Greater, a leader both wise and brave in these troubled times. His wisdom guides Whiterun, as the city stands like a beacon of hope amidst the chaos of Skyrim. May your deeds earn his favor, and your sword defend our lands.",
    #"speaker_wav": "D:/Modelisation_IA/xtts-api-server-custom/models/MrHaurrus/test.wav",
    "language": "en"
})
