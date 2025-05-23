from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pathlib import Path
import shutil
import os

app = FastAPI()

# CORS 허용 (React 클라이언트에서 접근 가능하게)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 실제 서비스 시에는 출처 제한하세요
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# video 저장 폴더
VIDEO_DIR = Path(__file__).parent / "video"
VIDEO_DIR.mkdir(exist_ok=True)

@app.post("/upload")
async def upload_video(video: UploadFile = File(...)):
    if not video.filename.endswith(".mp4"):
        return JSONResponse(status_code=400, content={"error": "Only .mp4 files are allowed"})

    file_path = VIDEO_DIR / f"{int(Path().stat().st_mtime)}_{video.filename}"
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(video.file, buffer)

    return {
        "success": True,
        "filename": file_path.name,
        "url": f"/video/{file_path.name}"
    }
