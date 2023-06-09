from dataclasses import dataclass
from fastapi import FastAPI, File, Response, UploadFile
from fastapi.middleware.cors import CORSMiddleware

import io
from PIL import Image

from torch_tuned import classify_with_resnet

app = FastAPI(description="Garbage classification API")

origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    # allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


@dataclass
class ApiResult:
    category: str
    confidence: str


@app.post("/classify/")
async def create_file(file: UploadFile = File(...)):
    if not file:
        return {"message": "No file sent"}
    else:
        try:
            request_object_content = await file.read()
            img = Image.open(io.BytesIO(request_object_content))
            result = classify_with_resnet(img)
            return ApiResult(result.category, result.probability)
        except Exception:
            return Response(
                status_code=404,
                content="Wrong file format",
                media_type="application/json",
            )
