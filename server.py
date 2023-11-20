import torch
from TTS.api import TTS
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.responses import FileResponse

app = FastAPI()

# Load model once at server startup
device = "cuda" if torch.cuda.is_available() else "cpu"
tts_model = TTS("tts_models/multilingual/multi-dataset/xtts_v2").to(device)

# List of supported language codes
supported_languages = {
    "ar":"Arabic",
    "pt":"Brazilian Portuguese",
    "zh-cn":"Chinese",
    "cs":"Czech",
    "nl":"Dutch",
    "en":"English",
    "fr":"French",
    "de":"German",
    "it":"Italian",
    "pl":"Polish",
    "ru":"Russian",
    "es":"Spanish",
    "tr":"Turkish",
    "ja":"Japanese",
    "ko":"Korean",
    "hu":"Hungarian"
}

@app.get("/languages/")
def get_languages():
    return supported_languages

class SynthesisRequest(BaseModel):
    text: str
    speaker_wav: str #
    language: str

class SynthesisFileRequest(BaseModel):
    text: str
    speaker_wav: str
    language: str
    file_path: str # The user specifies the path to save the file

@app.post("/synthesize_to_audio/")
def synthesize_to_audio(request: SynthesisRequest):
    try:
        # Generating a temporary file to be transferred to the user.
        temporary_file_path = "temp_output.wav"
        tts_model.tts_to_file(
            text=request.text,
            speaker_wav=request.speaker_wav,
            language=request.language,
            file_path=temporary_file_path
        )
        return FileResponse(path=temporary_file_path, media_type='audio/wav', filename="output.wav")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/synthesize_to_file/")
def synthesize_to_file(request: SynthesisFileRequest):
    try:
        tts_model.tts_to_file(
            text=request.text,
            speaker_wav=request.speaker_wav,
            language=request.language,
            output_path=request.file_path  # The user-provided path to save the file is used here.
        )
        return {"message": "The file was successfully saved", "output_path": request.file_path}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)