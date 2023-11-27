# A simple FastAPI Server to run XTTSv2

There's a [google collab version](https://colab.research.google.com/drive/1b-X3q5miwYLVMuiH_T73odMO8cbtICEY?usp=sharing) you can use it if your computer is weak.
You can check out the [guide](https://rentry.org/xtts-api-server-colab-guide)

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
pip install torch==2.1.0 torchaudio==2.1.0 --index-url https://download.pytorch.org/whl/cu118
```

## Starting Server

`python -m xtts_api_server` will run on default ip and port (localhost:8020)

```
usage: xtts_api_server [-h] [-hs HOST] [-p PORT] [-sf SPEAKER_FOLDER] [-o OUTPUT] [-t TUNNEL_URL] [-ms MODEL_SOURCE] [--lowvram]

Run XTTSv2 within a FastAPI application

options:
  -h, --help show this help message and exit
  -hs HOST, --host HOST
  -p PORT, --port PORT
  -sf SPEAKER_FOLDER, --speaker_folder The folder where you get the samples for tts
  -o OUTPUT, --output Output folder
  -t TUNNEL_URL, --tunnel URL of tunnel used (e.g: ngrok, localtunnel)
  -ms MODEL_SOURCE, --model-source ["api","apiManual","local"]
  --lowvram The mode in which the model will be stored in RAM and when the processing will move to VRAM, the difference in speed is small
```

If you want your host to listen, use -hs 0.0.0.0

The -t or --tunnel flag is needed so that when you get speakers via get you get the correct link to hear the preview. More info [here](https://imgur.com/a/MvpFT59)

Model-source defines in which format you want to use xtts:

1. `local` - loads a version 2.0.2 model into the models folder and uses `XttsConfig` and `inference`.
2. `apiManual` - loads a version 2.0.2 model into the models folder and uses the `tts_to_file` function from the TTS api
3. `api` - will load the latest version of the model..

The first time you run or generate, you may need to confirm that you agree to use XTTS.

# API Docs

API Docs can be accessed from [http://localhost:8020/docs](http://localhost:8020/docs)

# Voice Samples

You can find the sample in this repository, also by default samples will be saved to `/output/output.wav` or you can change this, more details in the API documentation

# Selecting Folder

You can change the folders for speakers and the folder for output via the API.

# Get Speakers

Once you have at least one file in your speakers folder, you can get its name via API and then you only need to specify the file name.

# Note on creating samples for quality voice cloning

The following post is a quote by user [Material1276 from reddit](https://www.reddit.com/r/Oobabooga/comments/1807tsl/comment/ka5l8w9/?share_id=_5hh4KJTXrEOSP0hR0hCK&utm_content=2&utm_medium=android_app&utm_name=androidcss&utm_source=share&utm_term=1)

> Some suggestions on making good samples
>
> Keep them about 7-9 seconds long. Longer isn't necessarily better.
>
> Make sure the audio is down sampled to a Mono, 22050Hz 16 Bit wav file. You will slow down processing by a large % and it seems cause poor quality results otherwise (based on a few tests). 24000Hz is the quality it outputs at anyway!
>
> Using the latest version of Audacity, select your clip and Tracks > Resample to 22050Hz, then Tracks > Mix > Stereo to Mono. and then File > Export Audio, saving it as a WAV of 22050Hz
>
> If you need to do any audio cleaning, do it before you compress it down to the above settings (Mono, 22050Hz, 16 Bit).
>
> Ensure the clip you use doesn't have background noises or music on e.g. lots of movies have quiet music when many of the actors are talking. Bad quality audio will have hiss that needs clearing up. The AI will pick this up, even if we don't, and to some degree, use it in the simulated voice to some extent, so clean audio is key!
>
> Try make your clip one of nice flowing speech, like the included example files. No big pauses, gaps or other sounds. Preferably one that the person you are trying to copy will show a little vocal range. Example files are in [here](https://github.com/oobabooga/text-generation-webui/tree/main/extensions/coqui_tts/voices)
>
> Make sure the clip doesn't start or end with breathy sounds (breathing in/out etc).
>
> Using AI generated audio clips may introduce unwanted sounds as its already a copy/simulation of a voice, though, this would need testing.
