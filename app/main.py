from fastapi import FastAPI, File, UploadFile
from fastapi.responses import FileResponse
import csv
import os
import shutil
import zipfile
from add_text_to_pic import generate_images
import time

app = FastAPI()

UPLOAD_DIR = "./upload_files"
OUTPUT_DIR = "./generated_images"


@app.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
    os.makedirs(UPLOAD_DIR, exist_ok=True)
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    temp_file_path = os.path.join(UPLOAD_DIR, file.filename)

    with open(temp_file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    with open(temp_file_path, "r", encoding="utf-8") as csvfile:
        reader = csv.reader(csvfile)
        next(reader)  # Skip header
        for row in reader:
            username, club_info, division_info, option_info, remark, option = row
            generate_images(username, club_info, division_info, option_info, remark, option, OUTPUT_DIR)
    # For checking the upload file content, save the file temporarily
    # os.remove(temp_file_path)

    return {"detail": "Badges generated successfully"}


@app.get("/download/")
async def download_image():

    timestamp = int(time.time())
    formatted_time = time.strftime("%Y-%m-%d_%H-%M-%S", time.localtime(timestamp))
    zip_file_name = f"generated_images_{formatted_time}.zip"

    zip_file_path = f"./{zip_file_name}"
    with zipfile.ZipFile(zip_file_path, "w") as zipf:
        for root, dirs, files in os.walk(OUTPUT_DIR):
            for file in files:
                file_path = os.path.join(root, file)
                zipf.write(file_path, os.path.relpath(file_path, OUTPUT_DIR))

    return FileResponse(zip_file_path, media_type="application/zip", filename=zip_file_name)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
