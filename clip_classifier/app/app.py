from fastapi import FastAPI, HTTPException, File, UploadFile
from utils.utils import load_image, expand_list
from pred.classifier import predict
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI(title="Image Classifier API")

origins = [
    "http://localhost:3000",
    "localhost:3000",
    "*",
    "http://127.0.0.1:8089/",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def read_main():
    return {"msg": "Hello World !!!!"}


@app.post("/classify_file")
async def classify_file(labels: list[str], image: UploadFile = File(...)):
    image = load_image(await image.read())
    labels = expand_list(labels)

    prediction = predict(image, labels)
    if not prediction:
        # the exception is raised, not returned - you will get a validation
        # error otherwise.
        raise HTTPException(status_code=404, detail="Image could not be downloaded")

    return prediction

    return {"file_size": image.file_size}
