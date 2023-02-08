from fastapi import FastAPI, HTTPException, File, UploadFile, Query
from utils.utils import load_image, expand_list
from schemas.image_schema import Img, ImgUrl, ImgBytes
from pred.classifier import predict
from fastapi.middleware.cors import CORSMiddleware
from schemas.labels_schema import Labels


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


@app.post("/classify/", status_code=200)
async def classify(request: ImgUrl, labels: Labels):
    image = load_image(request.img)
    prediction = predict(image, labels)
    if not prediction:
        # the exception is raised, not returned - you will get a validation
        # error otherwise.
        raise HTTPException(status_code=404, detail="Image could not be downloaded")

    return prediction


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


# @app.post("/classify_file")
# def classify_file(labels: Labels, file:  bytes = File(...)):
#     try:
#         contents = file.file.read()
#         with open(file.filename, 'wb') as f:
#             f.write(contents)
#     except Exception:
#         return {"message": "There was an error uploading the file"}
#     finally:
#         file.file.close()

#     return {"message": f"Successfully uploaded {file.filename}"} 


# @app.post("/classify_file/", status_code=200)
# async def classify_file(labels: Labels, file: UploadFile = File(...)):
#     request_object_content = await file.read()
#     image = load_image(request_object_content)
#     prediction = predict(image, labels.labels)
#     if not prediction:
#         # the exception is raised, not returned - you will get a validation
#         # error otherwise.
#         raise HTTPException(status_code=404, detail="Image could not be downloaded")

    # return prediction
