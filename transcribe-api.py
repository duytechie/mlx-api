from fastapi import FastAPI, UploadFile, Form, HTTPException
import mlx_whisper

app = FastAPI()


@app.post("/v1/audio/transcriptions")
async def transcribe_audio(file: UploadFile = Form(...), model: str = Form(...)):
    if not file.filename.lower().endswith((".mp3", ".wav", ".ogg")):
        raise HTTPException(status_code=400, detail="File must be an audio file")

    temp_file_path = f"/tmp/{file.filename}"
    with open(temp_file_path, "wb") as f:
        f.write(await file.read())

    # Transcrbie the audio using mlx_whisper
    try:
        result = mlx_whisper.transcribe(
            audio=temp_file_path, path_or_hf_repo=model, word_timestamps=True
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    return {"text": result["text"]}


# Implementation
"""
curl -X POST http://localhost:8000/v1/audio/transcriptions \
  -H "Content-Type: multipart/form-data; boundary=----boundary" \
  -F "file=@/path/to/audio.mp3" \
  -F "model= "
"""
