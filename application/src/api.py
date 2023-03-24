from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware

import io
from classifiers.clip import classify_with_clip
from PIL import Image

app = FastAPI(description="Garbage classification API")

origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/classify/")
async def create_file(file: UploadFile = File(...)):
    if not file:
        return {"message": "No file sent"}
    else:
        request_object_content = await file.read()
        img = Image.open(io.BytesIO(request_object_content))
        return classify_with_clip(img)
