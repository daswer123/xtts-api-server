from TTS.api import TTS
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.responses import StreamingResponse

from pydantic import BaseModel
import uvicorn

import shutil
from loguru import logger
from argparse import ArgumentParser

from tts_funcs import TTSWrapper

# Default Folders , you can change them via API
OUTPUT_FOLDER = "output"
SPEAKER_FOLDER = "speakers"

# Create an instance of the TTSWrapper class and server
app = FastAPI()
XTTS = TTSWrapper()

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
    output_path: str  

@app.get("/speakers/")
def get_speakers():
    speakers = XTTS.get_speakers()
    return {"speakers": speakers}

@app.get("/languages/")
def get_languages():
    languages = XTTS.list_languages()
    return {"languages": languages}

@app.get("/get_folders/")
def get_folders():
    speaker_folder = XTTS.speaker_folder
    output_folder = XTTS.output_folder
    return {"speaker_folder": speaker_folder, "output_folder": output_folder}

@app.post("/set_output/")
def set_output(output_req: OutputFolderRequest):
    try:
        XTTS.set_out_folder(output_req.output_folder)
        return {"message": f"Output folder set to {output_req.output_folder}"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/set_speaker_folder/")
def set_speaker_folder(speaker_req: SpeakerFolderRequest):
    try:
        XTTS.set_speaker_folder(speaker_req.speaker_folder)
        return {"message": f"Speaker folder set to {speaker_req.speaker_folder}"}
    except ValueError as e:
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
            language=request.language.lower(),
            file_name_or_path=None  # Generate a unique temp filename within the method.
        )

        def iterfile():
            with open(output_file_path, mode="rb") as file_like:  # read the file as stream
                yield from file_like

        response = StreamingResponse(iterfile(), media_type='audio/wav')

        # Set content disposition header to prompt download with proper filename
        response.headers["Content-Disposition"] = "attachment; filename=output.wav"

        return response

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An eldritch error has occurred: {str(e)}")


@app.post("/tts_to_file/")
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
            file_name_or_path=request.file_path  # The user-provided path to save the file is used here.
        )
        return {"message": "The scroll of sound has been sealed and saved.", "output_path": output_file}

    except Exception as e:
         raise HTTPException(status_code=500, detail=f"A sinister fault has slipped through: {str(e)}")

if __name__ == "__main__":
    parser = ArgumentParser(description="Run the Uvicorn server.")
    parser.add_argument("-hs", "--host", default="0.0.0.0", help="Host to bind")
    parser.add_argument("-p", "--port", default=8020, type=int, help="Port to bind")

    args = parser.parse_args()
    logger.info("Starting server...")

    uvicorn.run(app, host=args.host, port=args.port)