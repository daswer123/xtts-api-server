# A simple FastAPI Server to run XTTSv2

This project is inspired by [silero-api-server](https://github.com/ouoertheo/silero-api-server) and utilizes [XTTSv2](https://github.com/coqui-ai/TTS).

I created a Pull Request that has been merged into the dev branch of SillyTavern: [here](https://github.com/SillyTavern/SillyTavern/pull/1383).

The TTS module or server can be used in any way you prefer.

## Installation

To begin, install the `xtts-api-server` package using pip:

```bash
pip install xtts-api-server
```

I strongly recommend installing PyTorch with CUDA support to leverage the processing power of your video card, which will enhance the speed of the entire process:

```bash
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
```

## Starting Server

`python -m xtts_api_server` will run on default ip and port (localhost:8020)

```
usage: xtts_api_server [-h] [-hs HOST] [-p PORT] [-sf SPEAKER_FOLDER] [-o OUTPUT]

Run XTTSv2 within a FastAPI application

options:
  -h, --help show this help message and exit
  -hs HOST, --host HOST
  -p PORT, --port PORT
  -sf SPEAKER_FOLDER, --speaker_folder The folder where you get the samples for tts
  -o OUTPUT, --output Output folder
```

The first time you run or generate, you may need to confirm that you agree to use XTTS.

# API Docs

API Docs can be accessed from [http://localhost:8020/docs](http://localhost:8020/docs)

# Voice Samples

You can find the sample in this repository, also by default samples will be saved to `/output/output.wav` or you can change this, more details in the API documentation

# Selecting Folder

You can change the folders for speakers and the folder for output via the API.

# Get Speakers

Once you have at least one file in your speakers folder, you can get its name via API and then you only need to specify the file name.
