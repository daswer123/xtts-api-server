#  A simple FastAPI Server to run XTTSv2

The project is inspired by [silero-api-server](https://github.com/ouoertheo/silero-api-server)
repo uses [XTTSv2](https://github.com/coqui-ai/TTS)

TODO: This is will be to serve the TTS extension in [SillyTavern](https://github.com/Cohee1207/SillyTavern) soon. The TTS module or server can be used any way you wish.
UPD: There's already a result

## Installation
`pip install xtts-api-server`

I strongly recommend installing pytorch with CUDA so that the entire process is on the video card 

`pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118`

## Starting Server
`python -m xtts-api-server` will run on default ip and port (0.0.0.0:8020)

```
usage: xtts-api-server [-h] [-o HOST] [-p PORT] [-sf SPEAKER_FOLDER] [-o OUTPUT]

Run XTTSv2 within a FastAPI application

options:
  -h, --help            show this help message and exit
  -o HOST, --host HOST
  -p PORT, --port PORT
  -sf SPEAKER_FOLDER, --speaker_folder The folder where you get the samples for tts
  -o OUTPUT, --output Output folder
```

The first time you run or generate, you may need to confirm that you agree to use XTTS.
The model will be loaded into memory after the first generation.

# API Docs
API Docs can be accessed from [http://localhost:8020/docs](http://localhost:8020/docs)

# Voice Samples
You can find the sample in this repository, also by default samples will be saved to `/output/output.wav` or you can change this, more details in the API documentation

# Selecting Folder
You can change the folders for speakers and the folder for output via the API.

# Get Speakers
Once you have at least one file in your speakers folder, you can get its name via API and then you only need to specify the file name.
