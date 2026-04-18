from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

import shutil
import os
from pathlib import Path

from backend.utils.transcribe import transcribe_video
from backend.utils.video import crop_vertical

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

BASE_DIR = Path(__file__).resolve().parent
UPLOAD_DIR = BASE_DIR / "uploads"
OUTPUT_DIR = BASE_DIR / "outputs"

UPLOAD_DIR.mkdir(exist_ok=True)
OUTPUT_DIR.mkdir(exist_ok=True)

app.mount("/outputs", StaticFiles(directory=str(OUTPUT_DIR)), name="outputs")


@app.post("/upload")
async def upload_video(file: UploadFile = File(...)):
    try:
        print(" Upload started")

        file_path = UPLOAD_DIR / file.filename

        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        print(" File saved")

        print("🎙 Transcribing...")
        transcript = transcribe_video(str(file_path))
        print(" Transcription done")

        if not transcript.get("segments"):
            return {"error": "No speech detected"}

        segment = transcript["segments"][0]
        start, end = segment["start"], segment["end"]

        print("Processing video...")

        output_filename = f"clip_{file.filename}"
        output_path = OUTPUT_DIR / output_filename

        crop_vertical(str(file_path), str(output_path), start, end)

        print(" Video ready")

        return {
            "message": "Processed successfully",
            "preview_text": segment["text"],
            "video_url": f"http://127.0.0.1:8001/outputs/{output_filename}"
        }

    except Exception as e:
        print(" ERROR:", str(e))
        return {"error": str(e)}
