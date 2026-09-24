from fastapi import FastAPI
from pydantic import BaseModel
from app.utils import predict
from fastapi import FastAPI, HTTPException

from app.utils import predict, predict_nv_model

app = FastAPI()

class PredictionRequest(BaseModel):
    features: list[float]

@app.post("/predict")
def predict_endpoint(data: PredictionRequest):
    if not data.features: 
        raise HTTPException( status_code=400, detail="features must contain at least one value", ) 
    predictions = predict(data.features)
    return {
        "model_version": "v1",
        "predictions": predictions
    }

@app.get("/")
def read_root():
    return {"message": "API is up and running!"}

@app.get("/favicon.ico")
def favicon():
    return ""

@app.post("/predictNvModel")
def predict_endpoint_v2(data: PredictionRequest):
    if not data.features: 
        raise HTTPException( status_code=400, detail="features must contain at least one value", )     
    predictions = predict_nv_model(data.features)

    return {
        "model_version": "v2",
        "predictions": predictions
    }
