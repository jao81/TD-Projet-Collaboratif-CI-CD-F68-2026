from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from app.persistence import save_prediction
from app.utils import predict, predict_nv_model

app = FastAPI()


class PredictionRequest(BaseModel):
    features: list[float]


@app.post("/predict")
def predict_endpoint(data: PredictionRequest):
    if not data.features: 
        raise HTTPException( status_code=400, detail="features must contain at least one value", ) 
    predictions = predict(data.features)
    save_prediction(data.features, predictions, "v1")
    return {
        "model_version": "v1",
        "predictions": predictions,
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
    save_prediction(data.features, predictions, "v2")
    return {
        "model_version": "v2",
        "predictions": predictions,
    }

@app.post("/predictBoth")
def predict_both(data: PredictionRequest):
    if not data.features: 
        raise HTTPException( status_code=400, detail="features must contain at least one value", )     
    old_predictions = predict(data.features)
    new_predictions = predict_nv_model(data.features)
    save_prediction(data.features, old_predictions, "v1")
    save_prediction(data.features, new_predictions, "v2")
    return {
        "old_model": old_predictions,
        "new_model": new_predictions,
    }   
