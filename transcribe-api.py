from fastapi import FastAPI, UploadFile, Form, HTTPException
import mlx_whisper
import os
import json

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "MLX Transcription API", "version": "1.0.0", "docs": "/docs"}


# Get the list of compatible models
@app.get("/v1/models")
async def list_models():
    try:
        with open("whisper_models.json", "r") as file:
            whisper_models = json.load(file)
        return whisper_models
    except FileNotFoundError:
        raise HTTPException(status_code=500, detail="List of models not found")
    except json.JSONDecodeError:
        raise HTTPException(status_code=500, detail="Invalid json configuration")


@app.post("/v1/audio/transcriptions")
async def transcribe_audio(file: UploadFile, model: str = Form(...)):
    if not file.filename:
        raise HTTPException(status_code=400, detail="No file provided")
    supported_formats = (
        ".mp3",
        ".mp4",
        ".mpeg",
        ".mpga",
        ".m4a",
        ".wav",
        ".webm",
    )
    if not file.filename.lower().endswith(supported_formats):
        raise HTTPException(status_code=400, detail="File must be an audio file")

    temp_file_path = f"/tmp/{file.filename}"
    with open(temp_file_path, "wb") as f:
        f.write(await file.read())

    # Transcribe the audio using mlx_whisper
    try:
        result = mlx_whisper.transcribe(
            audio=temp_file_path, path_or_hf_repo=model, word_timestamps=True
        )
        # return {"text": result["text"]}
        # Return the complete result from the transcription
        return result

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)
