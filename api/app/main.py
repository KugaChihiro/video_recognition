from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi import Body
from fastapi.middleware.cors import CORSMiddleware
import logging
import os
import requests
from dotenv import load_dotenv
from app.transcribe_audio import transcribe_audio
from app.summary import summarize_text
from app.blob_processor import upload_blob, delete_blob
from app.mp4_processor import mp4_processor
from app.send_message import send_message_to_queue
from pydantic import BaseModel

# 環境変数をロード
load_dotenv('.env')

# 環境変数
AZ_SPEECH_KEY = os.getenv("AZ_SPEECH_KEY")
AZ_SPEECH_ENDPOINT = os.getenv("AZ_SPEECH_ENDPOINT")
AZ_BLOB_CONNECTION = os.getenv("AZ_BLOB_CONNECTION")
CONTAINER_NAME = "container-vr-dev"

# ログ設定
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("FastAPIApp")

# FastAPIアプリケーションの初期化
app = FastAPI()

# CORS設定
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class FileData(BaseModel):
    blob_url_mp4: str
    file_name: str

@app.post("/transcribe")
async def main(file: UploadFile = File(...),blob_url_mp4: FileData = Body(...)):
    """
    音声ファイルを文字起こしし、要約を返すエンドポイント。
    """
    try:
        logger.info("Processing request...")

        file_name = file.filename
        file_data = await file.read()

        # Azure Blob Storage にアップロード
        blob_url = await upload_blob(file_name, file_data, CONTAINER_NAME, AZ_BLOB_CONNECTION)
        logger.info(f"Blob uploaded: {blob_url}")

        sanitized_filename = os.path.basename(file.filename)
        file_extension = os.path.splitext(sanitized_filename)[1].lower()

        if file_extension == ".mp4":
            send_message_to_queue(blob_url)
            logger.info(f"Waiting for HTTP request to process MP4 file")     
            transcribed_text = await transcribe_audio(blob_url_mp4.blob_url_mp4, AZ_SPEECH_KEY, AZ_SPEECH_ENDPOINT)
            logger.info(f"Transcribed text: {transcribed_text}")
        else:
            transcribed_text  = await transcribe_audio(blob_url, AZ_SPEECH_KEY, AZ_SPEECH_ENDPOINT)


        # 要約処理
        summarized_text = await summarize_text(transcribed_text)
        logger.info(f"Summarized text: {summarized_text}")

        # 処理後のBlobを削除
        await delete_blob(file_name, CONTAINER_NAME, AZ_BLOB_CONNECTION)
        logger.info(f"Blob deleted: {file_name}")

        # 結果を返却
        return summarized_text

    except Exception as e:
        logger.error(f"Error occurred: {str(e)}")
        raise HTTPException(status_code=500, detail={"error": str(e)})
