from fastapi import FastAPI, File, UploadFile
import io
from trash_ai import classify_image
from PIL import Image

app = FastAPI(description="Garbage classification API")


@app.post("/classify/")
async def create_file(file: UploadFile = File(...)):
    if not file:
        return {"message": "No file sent"}
    else:
        request_object_content = await file.read()
        img = Image.open(io.BytesIO(request_object_content))
        return classify_image(img)