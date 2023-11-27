from TTS.api import TTS
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse

from pydantic import BaseModel
import uvicorn

import os
import shutil
from loguru import logger
from argparse import ArgumentParser

from xtts_api_server.tts_funcs import TTSWrapper,supported_languages

# Default Folders , you can change them via API
OUTPUT_FOLDER = os.getenv('OUTPUT', 'output')
SPEAKER_FOLDER = os.getenv('SPEAKER', 'speakers')
BASE_URL = os.getenv('BASE_URL', '127.0.0.1:8020')

# Create an instance of the TTSWrapper class and server
app = FastAPI()
XTTS = TTSWrapper(OUTPUT_FOLDER,SPEAKER_FOLDER)

# Load model
logger.info("The model starts to load,wait until it loads")
XTTS.load_model() 

# Add CORS middleware 
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class OutputFolderRequest(BaseModel):
    output_folder: str

class SpeakerFolderRequest(BaseModel):
    speaker_folder: str

class SynthesisRequest(BaseModel):
    text: str
    speaker_wav: str 
    language: str

class SynthesisFileRequest(BaseModel):
    text: str
    speaker_wav: str 
    language: str
    file_name_or_path: str  

@app.get("/speakers_default")
def get_speakers():
    speakers = XTTS.get_speakers()
    return speakers

@app.get("/speakers")
def get_speakers():
    speakers = XTTS.get_speakers_special()
    return speakers

@app.get("/languages")
def get_languages():
    languages = XTTS.list_languages()
    return {"languages": languages}

@app.get("/get_folders")
def get_folders():
    speaker_folder = XTTS.speaker_folder
    output_folder = XTTS.output_folder
    return {"speaker_folder": speaker_folder, "output_folder": output_folder}

@app.get("/sample/{file_name}")
def get_sample(file_name: str):
    file_path = os.path.join(XTTS.speaker_folder, file_name)
    if os.path.isfile(file_path):
        return FileResponse(file_path, media_type="audio/wav")
    else:
        logger.error("File not found")
        raise HTTPException(status_code=404, detail="File not found")

@app.post("/set_output")
def set_output(output_req: OutputFolderRequest):
    try:
        XTTS.set_out_folder(output_req.output_folder)
        return {"message": f"Output folder set to {output_req.output_folder}"}
    except ValueError as e:
        logger.error(e)
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/set_speaker_folder")
def set_speaker_folder(speaker_req: SpeakerFolderRequest):
    try:
        XTTS.set_speaker_folder(speaker_req.speaker_folder)
        return {"message": f"Speaker folder set to {speaker_req.speaker_folder}"}
    except ValueError as e:
        logger.error(e)
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/tts_to_audio/")
async def tts_to_audio(request: SynthesisRequest):
    try:
        # Validate language code against supported languages.
        if request.language.lower() not in supported_languages:
            raise HTTPException(status_code=400,
                                detail="Language code sent is either unsupported or misspelled.")

        # Generate an audio file using process_tts_to_file.
        output_file_path = XTTS.process_tts_to_file(
            text=request.text,
            speaker_name_or_path=request.speaker_wav,
            language=request.language.lower()
        )

        # Return the file in the response
        return FileResponse(
            path=output_file_path,
            media_type='audio/wav',
            filename="output.wav",
            )

    except Exception as e:
        logger.error(e)
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")


@app.post("/tts_to_file")
async def tts_to_file(request: SynthesisFileRequest):
    try:
        logger.info(f"Processing TTS to file with request: {request}")

        # Validate language code against supported languages.
        if request.language.lower() not in supported_languages:
             raise HTTPException(status_code=400,
                                 detail="Language code sent is either unsupported or misspelled.")

        # Now use process_tts_to_file for saving the file.
        output_file = XTTS.process_tts_to_file(
            text=request.text,
            speaker_name_or_path=request.speaker_wav,
            language=request.language.lower(),
            file_name_or_path=request.file_name_or_path  # The user-provided path to save the file is used here.
        )
        return {"message": "The audio was successfully made and stored.", "output_path": output_file}

    except Exception as e:
        logger.error(e)
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")

if __name__ == "__main__":
    uvicorn.run(app,host="0.0.0.0",port=8002)